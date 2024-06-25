# YPM Dark Data Internship

**Goal:** The main purpose of this internship was to explore the possible implications of Artificial Intelligence (OCR, HTR image-classification, etc.) in the Museum/Gallery world.
* Over the course of 8 weeks, I investigated Optical Character Recogition, Multi-Modal AI, and Image-Classification with respect to their possible uses in the Yale Peabody Museum.

## Marsh Papers → Google Vision AI → Entity Recognition
One of the uses of AI we found employable for the museum is the application of Optical Character Recognition using Google's Cloud Vision API (GCV) and spaCy's Named-Entity Recognition (NER).Using these tools, we were able to extract the text from various correspondance addressed to O.C. Marsh (Yale Professor and former president of the National Academy of Sciences) and then note specific entities from the transcribed text.

#### Notes & Findings:
* GCV works decently well for transcribing old-handwritten texts but often makes mistakes as expected.
* Medium runtime per PDF file, but inexpensive.
* Easier to work with image files (JPG/PNG) rather than PDFs/TIFFs; if you use image files you are able to suggest a target language (ie. English, French, etc.)
* GCV exports its findings in the form of a JSON file, so you must retreive the transcribed text from parsing the JSON file.
* spaCy's NER works very well and quickly for extracting important names and important entities.
* There are many other HTR/OCR platforms and tools that can be explored other than GCV.

#### Future Usage:
This project can be used for the museum to transcribe and process old documents and dark data. It is designed to take in mutliple PDF files simultaneously and produce transcribed text and import entities from the text.

## Copesbrain Label Recogntion
Another application of AI we found interesting for the Museum is the use of Google's Vertex AI platform, a mutli-modal AI that can take in mutliple input forms (text, images, etc) and output different forms. Using this tool, we were able to extract the text on labels on some of Copes specimen.

#### Notes & Findings:
* Google's Vertex AI is very good at taking in inputs and answering a specific prompt about the input.
* By inputting an image of a specimen with a certain label on it, we are able to specifically query the Vertex AI to extract *only* the label and its text on the specimen.
    * For example, this can be done by specifying to the AI to "ignore the ruler at the bottom of the image" and "identify the label on the main specimen in the image and output its text and a description of the label itself.
 * We found that it is able to do this and format the results as you please, making it very easy to work with with large quantities of data.
 * The Vertex AI can be on the more expensive side of Google's Cloud services.

#### Future Usage:
This project can be used for the museum to help researchers label and digitize specimen that have accumulated over time. Since drawer image-capturing technology, it can be combined with this to separate images and then identify the labels in a simple, turn-key process.

## YPM Image Classification
The last idea for implementing AI into the museum was to train a machine learning model to identify and classify images of the YPM into categories such as exhibit, pre/post-renovation, etc. To implement this we originally used Google Cloud's AutoML feature to create a multi-label classification model. Then we used Google's Teachable Machine platform to create a single-label classification model for each respective category.

#### Notes & Findings:
* Google's AutoML model is very nice and easy to use, but it was expensive and consumed the free-trial money quickly when it was deployed to an endpoint that was not actively being used.
* Using multiple models for each label category was easier than nusing multi-label classification, this way it ensures that exhibits are mutually exclusive and only pulls one label form each individual category.
* Using Google's Teachable Machine was very easy, trained very quickly, and customizeable.
  * It is completely free and able to be exported to an endpoint model with Python and Tensorflow and Keras.

#### Future Usage:
This project is one that will improve the effienciency of digitizing and uploading images taken in the museum. It can possibly be implemented into some of the photography pipelines used to mass assign labels (exhibit, pre/post-renovation) to image sets.
