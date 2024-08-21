
# Pharmaceutical-Capsule-Sorting-and-Defect-Detection-System

This project aims to automate the sorting of medicine capsules based on their color and detect defects such as cracks or irregular shapes using machine learning techniques. Two methods are explored to achieve this: utilizing pre-trained machine learning models and training a Convolutional Neural Network (CNN) for custom capsule recognition.

## Project Overview

The system uses a Raspberry Pi equipped with a camera module and servo motors for physical sorting based on color detection. Image processing techniques are employed to detect colors (Red, Green, Blue, Yellow, Purple) using HSV values and contour detection. Additionally, the system is designed to identify defects in capsules, such as cracks or irregular shapes, enhancing pharmaceutical quality control processes.


## Methodologies

### Method 1: Using Pre-trained ML Models

- **Color Detection**:
  - Convert camera input to HSV color space.
  - Define color ranges for capsules (Red, Green, Blue, Yellow, Purple).
  - Utilize OpenCV to threshold images and detect contours for each color.
  
- **Defect Detection**:
  - Implement pre-trained models from scikit-learn for defect classification based on color attributes (e.g., cracked or broken capsules).

### Method 2: Training a CNN for Custom Recognition

- **Dataset Preparation**:
  - Gather a dataset of labeled images depicting capsules of various colors and defects (cracked, broken, etc.).

- **Model Training**:
  - Implement a CNN architecture using frameworks like TensorFlow or PyTorch.
  - Train the model on the dataset to recognize both colors and defects.

- **Integration**:
  - Integrate the trained CNN model with the Raspberry Pi system for real-time sorting and defect detection.
