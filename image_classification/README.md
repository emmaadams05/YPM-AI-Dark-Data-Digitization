# YPM Image Classification with Google's Teachable Machine

**Project Goal:** Use a machine learning model to classify images of the Yale Peabody Museum into various categories based on exhibit, date, etc. 

## System & Project Requirements
* Python
* Numpy
* Tensorflow
* Keras

## Project Set Up
1. Set up coding environment and install required packages.
2. Create an image project on [Teachable Machine](https://teachablemachine.withgoogle.com/) (saving the project to drive is **highly reccommended**).
3. Create labels and upload sample images to their respective labels.
4. Adjust the training settings and train the model
5. Export the model using the *Tensorflow* option and download the model.
6. Add the model to the same directory as a new python file.
7. Use Teachable Machine's provided code to assign labels to images.

## Function Usage:
* *predict_exhibit_class(image_path:str):* Predicts the exhibit of a given image from a specified path.
  * **Parameters:**
    * image_path (string): Path to the image to be predicted.

  * **Returns:**
    * A tuple containing the predicted exhibit (index 0) and the confidence score (index 1).
 
* *predict_pre_post_renovation(image_path:str):* Predicts if a given image from a specified path was taken before or after the 2020-2024 renovation.
  * **Parameters:**
    * image_path (string): Path to the image to be predicted.

  * **Returns:**
    * A tuple containing the predicted pre/post-renovation (index 0) and the confidence score (index 1).

* *predict_all(image_path:str):* Predicts the exhibit and relative time of a given image from a specified path.
  * **Parameters:**
    * image_path (string): Path to the image to be predicted.

  * **Returns:**
    * A dictionary where the keys are the specific categories, and the key values are a tuple of the predicted class (index 0) and the confidence of that class (index 1).
 
