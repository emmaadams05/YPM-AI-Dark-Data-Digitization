import json
import re
import os
import spacy
import pandas as pd
from typing import Dict, List
from google.cloud import vision
from google.cloud import storage
nlp = spacy.load("en_core_web_sm")

#identify user-specific credentials files
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(os.path.dirname(__file__), "credentials.json")


def list_blobs(bucket_name:str) -> Dict[str, str]:
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


def async_detect_document(gcs_source_uri:str, gcs_destination_uri:str, max_pdf_pages:int=100) -> str:
    """
    Use: Runs OCR with PDF/TIFF as source files on GCS
    
    Parameters:
            gcs_source_uri: the URI from GCS in a specific bucket
            gcs_destination_uri: the desired URI output to be stored in GCS
            max_pdf_size: the maximum number of pages in any pdf

    Returns: a string of the name of the outputted json file for this specific pdf
    """

    # Supported mime_types are: 'application/pdf' and 'image/tiff'
    mime_type = "application/pdf"

    # How many pages should be grouped into each json output file.
        #doesnt affect number of node in JSON file, so 100 is large enough to fit all pages for marsh_project
    batch_size = max_pdf_pages

    client = vision.ImageAnnotatorClient()

    feature = vision.Feature(type_=vision.Feature.Type.DOCUMENT_TEXT_DETECTION)


    gcs_source = vision.GcsSource(uri=gcs_source_uri)
    input_config = vision.InputConfig(gcs_source=gcs_source, mime_type=mime_type)

    gcs_destination = vision.GcsDestination(uri=gcs_destination_uri)
    output_config = vision.OutputConfig(
        gcs_destination=gcs_destination, batch_size=batch_size
    )

    async_request = vision.AsyncAnnotateFileRequest(
        features=[feature], input_config=input_config, output_config=output_config
    )

    operation = client.async_batch_annotate_files(requests=[async_request])

    print(f"Waiting for the operation to finish for blob {gcs_source_uri[25:33]}.")
    operation.result(timeout=420)

    # Once the request has completed and the output has been
    # written to GCS, we can list all the output files.
    storage_client = storage.Client()

    match = re.match(r"gs://([^/]+)/(.+)", gcs_destination_uri)
    bucket_name = match.group(1)
    prefix = match.group(2)

    bucket = storage_client.get_bucket(bucket_name)

    # List objects with the given prefix, filtering out folders.
    blob_list = [
        blob
        for blob in list(bucket.list_blobs(prefix=prefix))
        if not blob.name.endswith("/")
    ]

    #store the name of the outputted json file to be used for parsing purposes
    for blob in blob_list:
        output_file_name = blob.name

    # Process the first output file from GCS.
    # Since we specified batch_size=2, the first response contains
    # the first two pages of the input file.
    output = blob_list[0]

    json_string = output.download_as_bytes().decode("utf-8")
    response = json.loads(json_string)

    # The actual response for the first page of the input file.
    first_page_response = response["responses"][0]
    annotation = first_page_response["fullTextAnnotation"]

    return output_file_name


def extract_full_text_json(json_file_name:str):
    """
    Use: Utilizes JSON parsing to extract the text page-by-page from a json file.

    Parameters:
            json_file_name (string): name of the json file to be parsed

    Returns: Dictionary of lists of all relevant data.
            keys: the respective column name (ex. Page Number, URI, etc.)
            values: the data for that column for the respective URI and page number.
    """

    #open json files from google cloud storage and extract the JSON data
    storage_client = storage.Client()
    bucket = storage_client.bucket("sample_marsh_papers")
    blob = bucket.blob(json_file_name)
    str_json = blob.download_as_text()
    json_data = json.loads(str_json)

    #initialize empty lists to store the subsequent text or page numbers
    texts_list = []
    page_number_list = []
    uri_list = []
    file_name_list = []

    #parse through every page in the pdf
    for i in range(len(json_data["responses"])):
        #add the full text from each page along w/ the page number to their respective lists
        try:
            texts_list.append(json_data["responses"][i]["fullTextAnnotation"]["text"])
        #sometimes there is no fullTextAnnotation if no text is found on a page, so this is the exception
        except:
            #add a empty string to the full textlist to perserve the same indices across all lists
            texts_list.append("")
        page_number_list.append(json_data["responses"][i]["context"]["pageNumber"])
        uri_list.append(json_data["responses"][i]["context"]["uri"])
        file_name_list.append(json_data["responses"][i]["context"]["uri"][25:33])


    # create a dictionary to temporarily store the data
    data = {"Page Number": page_number_list, "Full Text": texts_list, "URI":uri_list, "File Name": file_name_list}

    #return the dictionary of relevant data
    return data


def ner(sample_texts:List[str]) -> List[str]:
    """
    Use: Run the full text list through a Name Entity Recognition tool to idetify key entities from the text.

    Parameters:
            sample_texts: List, full list of all strings outputted by the JSON parser.

    Output: A list of all entities for each page of full text.
    """

    full_entity_list = []

    #loop through list of texts
    for text in sample_texts:
        #initialize an empty string to store the entities found in each text
        entities_found = ""

        # identify the entities in the text for each item in the full texts list
        doc = nlp(text)
        for ent in doc.ents:
            # correct spelling and add to entity string
            entities_found += f"{ent.text},"

        #add the entity string to the full list of entities in each letter page
        full_entity_list.append(entities_found)

    return full_entity_list


def run_full_ocr_extraction(bucket_name:str, max_pdf_pages:int=100) -> List[Dict[str, List[str]]]:
    """
    Use: Use to run the GC Vision on all files in a GCS bucket.
    
    Parameters:
            bucket_name: (str) the name of the bucket to run the function on
            max_pdf_pages: (int) the maximum number of pages per pdf, defaults to 100

    Returns: List of all output files names; also adds new JSON files to the GCS bucket.
    """
    #get a dictionary of all blobs, where the key is the file name and the value is the file's GCS URI
    blobs_dict = list_blobs(bucket_name)
    output_blob_names = []

    # for each blob in the bucket
    for blob in blobs_dict:
        #run the Google Cloud Vision OCR/HTR asynchronous function
        #outputs json files in "sample_marsh_papers_json" bucket in GCS
        output_file_name = async_detect_document(blobs_dict[blob], f"gs://{bucket_name}/{blob[0:8]}_text_", max_pdf_pages)
        output_blob_names.append(output_file_name)
        print(f"Finished running {blob[0:]} through OCR Scan")
    
    return output_blob_names


def extract_process_text_to_csv(project_id:str, bucket_name:str, csv_result_path:str, max_pdf_pages:int):
    """
    Use: Extracts all fullTextAnnotations from JSON file and creates a CSV of all relevant data

    Parameters:
            project_id: ID of the specific project in Google Cloud
            bucket_name: name of Google Cloud Storage bucket
            csv_result_path: the directory to the result_path, include  file name and .csv (ex. "results/asaph_results.csv")
            max_pdf_pages: (int) the maximum number of pages per pdf
            
    Returns: A pandas dataframe of all relevant data; also produces a CSV from that data.
    """
    #identify user-specific credentials files
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(os.path.dirname(__file__), "credentials.json")

    #set the project to be designated project
    os.environ["GCLOUD_PROJECT"] = project_id

    #runs the OCR scan and adds the JSON files to google cloud storage for extraction; returns the resulting JSON blob names
    output_blobs_list = run_full_ocr_extraction(bucket_name, max_pdf_pages)

    #initialize empty list to store the data for all json files
    full_json_results = []

    #get the json data for each individual json file and store the resulting dictionaries in a list
    for blob in output_blobs_list:
        print(f"Extracting Full Text from JSON File for {blob[0:8]}.pdf")
        data = extract_full_text_json(blob)
        full_json_results.append(data)

    #initialize empty lists to store all relevant data for future CSV purposes
    full_text_total_list = []
    full_page_number_list = []
    full_URI_list = []
    full_file_name_list = []

    #add all data for each file to one large list for each category
    for data in full_json_results:
        full_text_total_list += data["Full Text"]
        full_file_name_list += data["File Name"]
        full_page_number_list += data["Page Number"]
        full_URI_list += data["URI"]
    
    #check each full text in the list for animal/taxonomic names
    print("Scanning all text annotations through NER.")
    full_entity_list = ner(full_text_total_list)

    #create dictionary of all relevant data
    final_dict = {"File Name": full_file_name_list, "Page Number": full_page_number_list, "Full Text": full_text_total_list, "Identified Entities (Spell Checked)": full_entity_list}

    #create dataframe and export as CSV file
    df = pd.DataFrame.from_dict(final_dict)
    df.to_csv(csv_result_path)
    print("Process is finished.")

    return df

#sample extraction for the pdf files in the sample_marsh_papers bucket in GCS    
extract_process_text_to_csv(project_id="marsh-papers", bucket_name="sample_marsh_papers", csv_result_path="results/asaph_results.csv", max_pdf_pages=51)
