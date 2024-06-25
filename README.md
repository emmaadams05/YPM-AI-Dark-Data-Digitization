# YPM Dark Data Internship

**Goal:** The main purpose of this internship was to explore the possible implications of Artificial Intelligence (OCR, HTR image-classification, etc.) in the Museum/Gallery world.
* Over the course of 8 weeks, I investigated Optical Character Recogition, Multi-Modal AI, and Image-Classification with respect to their possible uses in the Yale Peabody Museum.

## Marsh Papers → Google Vision AI → Entity Recognition
One of the uses of AI we found employable for the museum is the application of Optical Character Recognition using Google's Cloud Vision API (GCV) and spaCy's Named-Entity Recognition (NER).
Using these tools, we were able to extract the text from various correspondance addressed to O.C. Marsh (Yale Professor and former president of the National Academy of Sciences) and then note specific entities from the transcribed text.
#### Notes & Findings:
* GCV works decently well for transcribing old-handwritten texts but often makes mistakes as expected.
* Medium runtime per PDF file, but inexpensive.
* Easier to work with image files (JPG/PNG) rather than PDFs/TIFFs; if you use image files you are able to suggest a target language (ie. English, French, etc.)
* GCV exports its findings in the form of a JSON file, so you must retreive the transcribed text from parsing the JSON file.
* spaCy's NER works very well and quickly for extracting important names and important entities.



