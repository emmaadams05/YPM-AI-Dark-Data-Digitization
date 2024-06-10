# Marsh Papers &rarr; Google Vision AI &rarr; Entity Recognition 

**Project Goal:** Find named entities in the O.C. Marsh Papers and be able to link the references in the letter to the actual entities.
* Uses the [*Google Cloud Vision API*](https://cloud.google.com/vision/docs) for OCR to extract text on PDF/TIFF files.
* Uses the [*Google Cloud Storage API*](https://console.cloud.google.com/storage/) to store PDF/TIFF files for text extraction
* Uses [*spaCy*](https://spacy.io/api/entityrecognizer) for Named Entity Recognition

---
## Project Requirements
* Python 3.11 & pip3
    * *Note*: Python 3.12 and above **will not work** with our usage of spaCy.
* Google Cloud Project & Account
    * Storage API enabled with desired bucket of PDFs to extract entities from
    * Billing API enabled
    * [Service account](https://cloud.google.com/iam/docs/service-account-overview) and key (named *credentials.json*) downloaded into designatied project folder
* **Required Libraries & APIs:**
    * Google Cloud Vision
        * *pip install —upgrade google-cloud-vision*
    * [spaCy](https://spacy.io/usage)
    * pandas, os, ReGex (re), json, typing
---
## Project Set Up
1. Create a Google Cloud account and create a project
2. Enable Google Cloud Storage and Cloud Vision APIs
3. Create a bucket in Google Cloud storage and add the desired PDF/TIFF files to the bucket
4. Create a virtual environment using Python OR create a new local folder to store project files
5. Download the required libraries for Python usage
6. Create a service account for Google Cloud (with Storage and Vision APIs enabled)
    * Download the service accoung key, rename it to "credentials.json", and store it in the local folder (or folder for the virtual environment).
7. Download [*main.py*](https://github.com/emmaadams05/YPM-Dark-Data/blob/marsh_papers/main.py) from this GitHub repository and store it in the project folder (or folder for the virtual environment).
8. Open the [*main.py*](https://github.com/emmaadams05/YPM-Dark-Data/blob/marsh_papers/main.py) file and run the desired functions.
---

## Function Usage
* *list_blobs(bucket_name):* Finds all file names from a specific bucket in Google Cloud Storage (GCS)
    * **Parameters**: 
        * bucket_name (string): the specific bucket name in GCS
    * **Returns:**
        * Dictionary of all file names in GCS bucket and their respective URIs
            &nbsp;&nbsp; *Dict Keys:*  file names
            &nbsp;&nbsp; *Dict Values:* spcecific URI for files

* *async_detect_document(gcs_source_uri, gcs_destination_uri, max_pdf_pages):* Runs OCR with PDF/TIFF as source files on GCS
    * **Parameters**: 
        * gcs_source_uri: the URI from GCS in a specific bucket
        * gcs_destination_uri: the desired URI output to be stored in GCS
        * max_pdf_size: the maximum number of pages in any pdf (default is 100)
    * **Returns:**
        * A string of the name of the outputted json file for this specific pdf.

* *extract_full_text_json(json_file_name):* Utilizes JSON parsing to extract the text page-by-page from a json file.
    * **Parameters**: 
        * json_file_name (string): name of the json file to be parsed
    * **Returns:**
        * Dictionary of lists of all relevant data.
            &nbsp;&nbsp; *Dict Keys:* the respective column name (ex. Page Number, URI, etc.)
            &nbsp;&nbsp; *Dict Values:* the data for that column for the respective URI and page number.

* *ner(sample_texts):* runs the full text list through a Name Entity Recognition tool to idetify key entities from the text.
    * **Parameters**: 
        * sample_texts: list, full list of all strings outputted by the JSON parser.

    * **Returns:**
        * A list of all entities for each page of full text.


* *run_full_ocr_extraction(bucket_name, max_pdf_pages):* Use to run the GC Vision on all files in a GCS bucket.
    * **Parameters**: 
        * bucket_name: (str) the name of the bucket to run the function on
        * max_pdf_pages: (int) the maximum number of pages per pdf, defaults to 100

    * **Returns:**
        * List of all output files names; also adds new JSON files to the GCS bucket.

* *extract_and_process_text_to_csv(project_id, bucket_name, csv_result_path, max_pdf_pages):* Extracts all fullTextAnnotations from JSON file and creates a CSV of all relevant data.
    * **Parameters**: 
        * project_id: ID of the specific project in Google Cloud
        * bucket_name: name of Google Cloud Storage bucket
        * csv_result_path: the directory to the result_path, include  file name and .csv (ex. "results/asaph_results.csv")
        * max_pdf_pages: (int) the maximum number of pages per pdf

    * **Returns:**
        * A pandas dataframe of all relevant data; also produces a CSV from that data.
