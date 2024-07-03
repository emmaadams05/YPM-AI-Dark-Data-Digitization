# Copesbrain Vertex AI Label Descriptions

**Project Goal:** Utilize AI to identify the label text and description on various specimen.
* Uses the *Google Vertex AI* API to generate responses based on images.
* Used *Google Cloud Storage* API to store JPEG files.

## Project & System Requirements
* Python3.11 (or later) & pip3
* Google Cloud Project & Account
    * Storage API enabled with desired bucket of images to extract text from.
    * Billing API enabled
    * Vertex AI API enabled
    * [Service account](https://cloud.google.com/iam/docs/service-account-overview) and key (named *credentials.json*) downloaded into designatied project folder
* **Required Libraries & APIs**
    * [Google Cloud CLI](https://cloud.google.com/sdk/docs/install?_gl=1*1ff8ux8*_ga*NzQ4NDE0NDQuMTcxNjIzMDQwMw..*_ga_WH2QY8WWF5*MTcxNjkxNTU2My4xNC4xLjE3MTY5MTU5MjYuMC4wLjA.&_ga=2.41872420.-74841444.1716230403&_gac=1.195626590.1716910793.CjwKCAjwgdayBhBQEiwAXhMxtrfmcEdVJMyuSMQoN7SUSBs5O_wTNO1Q1W5PnTayCLBrCcbLhPnWSRoCOfgQAvD_BwE) (You must authorize the Service Account)
    * [Vertex AI SDK](https://cloud.google.com/python/docs/reference/aiplatform/latest/index.html)
    * os, base64, pandas
 
## Project Setup
1. Set up coding environment and install required packages.
2. Install Google Cloud CLI and Google Cloud AI Platform package. 
3. Create a Google Cloud project and store image files in a bucket in Google Cloud Storage.
4. Enable Google Cloud Storage API, Billing API, Vertex API in the Google Cloud online console and download and store the API key from service account.
5. Download *sample_vertex.py* and run the functions as described below. Change the prompt in the generate_text function surrounded by 3 double quotation marks to fit your project's needs.
   
**Note:** To get the raw code directly from Google, go to *Google Cloud Console &rarr; Vertex AI Studio &rarr; Multimodal*, then create a single turn prompt and add an image. The hit *get code* and install the packages and change the image directory to match any image files. 

## Fucntion Usage
* *list_blobs(bucket_name):* Finds all file names from a specific bucket in Google Cloud Storage (GCS).
    * **Parameters:** 
        * bucket_name (string): the specific bucket name in GCS.
    * **Returns:**
        * Dictionary of all file names in GCS bucket and their respective URIs.
            &nbsp;&nbsp; *Dict Keys:*  file names
            &nbsp;&nbsp; *Dict Values:* spcecific URI for files

* *generate_text(image_uri):* Utilizes Google Cloud's Vetex AI to extract the label text and description from a JPEG image file stored in a Google Cloud Storage Bucket.
    * **Parameters:** 
        * image_uri (string): the string of a GCS URI.
    * **Returns:**
        * The response of GC Vertex AI scan on the image.

* *generate_bucket_text(project_id, bucket_name, csv_directory):* Generates a Vertex AI label text response for all JPEG files in a GCS Bucket. Exports the relevant data as CSV.
    * **Parameters:**
        * project_id (string): the GC project ID.
        * bucket_name (string): the name of the bucket in GCS.
        * csv_directory (string): the path directory and file name you want for the CSV of the results. Must include the .csv extension (example "folder/results.csv").
    * **Returns:**
        * The resulting pandas dataframe of the respective results.
