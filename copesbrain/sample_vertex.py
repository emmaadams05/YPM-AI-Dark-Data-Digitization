# import the appropriate libraries and APIs
import os
import base64
import vertexai
from vertexai.generative_models import GenerativeModel, Part, FinishReason
import vertexai.preview.generative_models as generative_models

#set the project to be copesbrain
os.environ["GCLOUD_PROJECT"] = "copesbrain"

#make sure to include the correct project ID under project, and location
vertexai.init(project="copesbrain", location="us-central1")
model = GenerativeModel(
    "gemini-1.5-flash-001",
)

def generate_text(image_uri):
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
        ["""Identify the written text on the label on the main subject of the image. Ignore the ruler on the bottom. Only output the text, no other words.""", image1],
        generation_config=generation_config,
        safety_settings=safety_settings,
        stream=True,
    )

    for response in responses:
        print(response.text, end="")


test = {'ID0006.jpg': 'gs://copesbrain_samplebucket1/ID0006.jpg', 'ID0027.jpg': 'gs://copesbrain_samplebucket1/ID0027.jpg', 'ID0031.jpg': 'gs://copesbrain_samplebucket1/ID0031.jpg', 'ID0069.jpg': 'gs://copesbrain_samplebucket1/ID0069.jpg', 'ID0084.jpg': 'gs://copesbrain_samplebucket1/ID0084.jpg'}


generate_text('gs://copesbrain_samplebucket1/ID0006.jpg')
