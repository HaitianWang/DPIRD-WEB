# This script is part of the DPIRD Intellicrop project, designed to process satellite or aerial imagery data.
# It primarily focuses on loading and processing multi-spectral images stored in .tif format.
# The main steps include:
# 1. Configuring GPU settings for TensorFlow to handle large datasets efficiently.
# 2. Loading and pre-processing image files, with support for both RGB and single-channel spectral images.
# 3. Stacking the spectral indices in the correct order and scaling the pixel values as needed.
# 4. Handling missing data by skipping directories that do not contain all the required spectral indices.
# The processed data is prepared for further analysis or model training in the context of agricultural monitoring.

import os
import numpy as np
import rasterio
import tensorflow as tf
import zipfile

# Define the spectral indices that the model expects
SPECTRAL_INDICES = ['RGB', 'CI', 'EVI', 'ExG', 'ExR', 'GNDVI', 'MCARI', 'MGRVI', 'MSAVI', 'NDVI', 'OSAVI', 'PRI', 'SAVI', 'TVI']

# GPU configuration (unchanged)
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    try:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)  # Enable dynamic memory allocation for GPUs
        print(f"Available GPUs: {gpus}")
    except RuntimeError as e:
        print(e)
else:
    print("No GPUs available. Check your CUDA and cuDNN installation.")  # Display if no GPUs are detected

def load_tif(file_path, is_rgb=False):
    """
    Load a .tif file and return the image data.

    Parameters:
    file_path (str): The path to the .tif file.
    is_rgb (bool): If True, load the image as an RGB image with three channels. Default is False.

    Returns:
    numpy.ndarray: The loaded image as a numpy array, with scaling if necessary.
    """
    print(f"Loading TIF file from {file_path}")
    with rasterio.open(file_path) as src:
        if is_rgb:
            # Load all three channels for an RGB image
            image = np.dstack([src.read(i) for i in range(1, 4)]).astype(np.float32)
        else:
            # Load only the first channel for non-RGB images
            image = src.read(1).astype(np.float32)

    # Check for NaN values in the image data
    if np.isnan(image).any():
        print(f"NaN detected in file {file_path}")
        return None

    # Check if scaling is necessary for the image values
    min_val = np.min(image)
    max_val = np.max(image)

    if is_rgb:
        print(f"Loading RGB image from {file_path}")
        # Normalize RGB to [0, 1] range
        image = (image - min_val) / (max_val - min_val)
        return image

    if min_val < 0 or max_val > 1:
        print(f"Scaling applied to {file_path}")
        # Apply min-max scaling for non-RGB images
        image = (image - min_val) / (max_val - min_val)
    else:
        print(f"No scaling needed for {file_path}")
        print(f"Data range: [{min_val}, {max_val}]")

    return image

def create_dataset(base_path):
    """
    Create a dataset by loading and stacking images from the given directory.

    Parameters:
    base_path (str): The path to the directory containing the .tif files.

    Returns:
    numpy.ndarray: A stacked numpy array of image data.
    numpy.ndarray: The original RGB images.
    """
    inputs = []
    original_rgb_images = []  # To store the original RGB images
    print(f"Traversing base directory: {base_path}")

    # Retrieve all files from the base directory
    files = os.listdir(base_path)
    print(f"Files in base path: {files}")
    dataset_images = {}
    missing_indices = []

    # Loop through the SPECTRAL_INDICES to match the files
    for index in SPECTRAL_INDICES:
        # Find files that contain the spectral index (e.g., 'CI', 'EVI', 'ExG', etc.)
        matching_files = [f for f in files if f.startswith(f'{index}_') and f.endswith('.tif')]
        if matching_files:
            file_path = os.path.join(base_path, matching_files[0])
            print(f"Found file for {index}: {file_path}")
            # Set is_rgb=True for RGB images
            data = load_tif(file_path, is_rgb=(index == 'RGB'))

            # For RGB images, use the first channel only
            if index == 'RGB':
                dataset_images[index] = data[:, :, 0]  # Only use the first channel of the RGB image
                original_rgb_images.append(data)  # Store the full RGB image
            else:
                dataset_images[index] = data
        else:
            print(f"Missing file for index {index} in directory {base_path}")
            missing_indices.append(index)
            break  # Stop processing if any index file is missing

    if len(missing_indices) == 0:
        # Stack the images according to the order of SPECTRAL_INDICES
        input_stack = np.stack([dataset_images[index] for index in SPECTRAL_INDICES], axis=-1)
        if input_stack.shape[-1] == len(SPECTRAL_INDICES):  # Ensure the correct number of channels
            inputs.append(input_stack)
        else:
            print(f"Warning: Unexpected number of channels: {input_stack.shape[-1]}. Expected {len(SPECTRAL_INDICES)}.")
    else:
        print(f"Skipping due to missing indices: {missing_indices}")

    # Verify that any images were loaded
    if inputs:
        num_channels = inputs[0].shape[-1]
        print(f"Finished creating dataset. Number of images: {len(inputs)}. Each image has {num_channels} channels.")
    else:
        print(f"Finished creating dataset. No images loaded.")

    return np.array(inputs), np.array(original_rgb_images)

def pre_process(data_path):
    """
    Pre-process the images by loading them from the given data path.

    Parameters:
    data_path (str): The path to the directory containing the .tif files.

    Returns:
    numpy.ndarray: The pre-processed image data.
    numpy.ndarray: The original RGB images.
    list: The list of spectral indices.
    """
    print("data_path", data_path)
    X, original_rgb_images = create_dataset(data_path)
    return X, original_rgb_images, SPECTRAL_INDICES
