# import the appropriate libraries and APIs
import os
import base64
import vertexai
import pandas as pd
from vertexai.generative_models import GenerativeModel, Part, FinishReason
import vertexai.preview.generative_models as generative_models

# specify the  Google Cloud Service Account key
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(os.path.dirname(__file__), "credentials.json")

def list_blobs(bucket_name:str) -> dict[str, str]:
    """
    Use: find all file names from a specific bucket in Google Cloud Storage (GCS)

    Parameter:
            bucket_name (string): the specific bucket name in GCS
    
    Returns: dictionary of all file names in GCS bucket and their respective URIs.
            Dict Keys: pdf file names.
            Dict Values: GCS spcecific URI for files.
    """

    #initialize GCS client
    storage_client = storage.Client()

    # Note: Client.list_blobs requires at least package version 1.17.0.
    blobs = storage_client.list_blobs(bucket_name)

    uri_dict = dict()

    #loop through all blobs
    for blob in blobs:
        #create a new dictionary entry to have the file name and respective URI
        uri_dict[blob.name] = ("gs://" + blob.id[:-(len(str(blob.generation)) + 1)])

    return uri_dict


def generate_text(image_uri):
    """
    Use: Utilizes Google Cloud's Vetex AI to extract the label text and description from a JPEG image file stored in a Google Cloud Storage Bucket
    
    Parameters:
            image_uri: (str), the string of a GCS URI

    Returns: the response of GC Vertex AI scan on the image

    """
    print(f"Generating label text & description for blob {image_uri}.")
    
    #include the URI from Google Cloud Storage for the image.
    image1 = Part.from_uri(
        mime_type="image/jpeg",
        uri=image_uri)
    
    #intialize the configuration settings
    generation_config = {
        "max_output_tokens": 8192,
        "temperature": 1,
        "top_p": 0.95,
    }

    #settings to prevent explicit images from being examined
    safety_settings = {
        generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    }

    responses = model.generate_content(
        #insert your prompt here; be as specific as possible
        ["""Identify the written text and numbers on the label on the main subject of the image, if there is no text or numbers, identify this as "no text". Ignore the ruler on the bottom. Then describe the label (include color, shape, material like paint or paper or sticker, etc.). Be Concise but accurate and clear in the description. Return your response in the form: label_text; label_description""", image1],
        generation_config=generation_config,
        safety_settings=safety_settings,
        stream=True,
    )

    for response in responses:
        print(image_uri, "text:", response.text, end="")
        return response.text


def generate_bucket_text(project_id:str, bucket_name:str, csv_directory:str):
    """
    Use: Generates a Vertex AI label text response for all JPEG files in a GCS Bucket. Exports the relevant data as CSV.

    Parameters:
            project_id: the GC project ID
            bucket_name: the name of the bucket in GCS
            csv_directory: the path directory and file name you want for the CSV of the results. Must include the .csv extension (example "folder/results.csv")

    Returns:
            the resulting pandas dataframe of the respective results
    """
    #set the project to be copesbrain
    os.environ["GCLOUD_PROJECT"] = project_id

    #make sure to include the correct project ID under project, and location
    vertexai.init(project=project_id, location="us-central1")

    model = GenerativeModel(
        "gemini-1.5-flash-001",
    )

    #get the URIs and blob names from google cloud storage
    blobs_dict = list_blobs(bucket_name)
    #create lists to store the image file names, responses, and label/despcription texts
    image_files = [blob for blob in blobs_dict]
    full_responses = []
    label_text = []
    label_descriptions = []

    # get the Vertex AI responses for all images in the GCS bucket
    for blob in blobs_dict:
        current_response = generate_text(blobs_dict[blob])
        full_responses.append(current_response)

    # the repsonses *should* be split based on a semicolon, with the label text being the former and the label description being the latter
    for response in full_responses:
        #split each individual response and append the split text into their respective lists
        split_response = response.split(";")
        label_text.append(split_response[0])
        label_descriptions.append(split_response[1])

    # store the results in a dictionary and then export as a CSV
    csv_dict = {"Pic Number": image_files, "Original Label":label_text, "Description of Label":label_descriptions}
    df = pd.DataFrame.from_dict(csv_dict)
    df.to_csv(csv_directory)

    #return the dataframe
    return df
