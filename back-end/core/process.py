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
            tf.config.experimental.set_memory_growth(gpu, True)
        print(f"Available GPUs: {gpus}")
    except RuntimeError as e:
        print(e)
else:
    print("No GPUs available. Check your CUDA and cuDNN installation.")

def load_tif(file_path):
    print(f"Loading TIF file from {file_path}")
    with rasterio.open(file_path) as src:
        image = src.read(1).astype(np.float32)
    
    # Check for NaN values
    if np.isnan(image).any():
        print(f"NaN detected in file {file_path}")
        return None
    
    # Check if scaling is necessary
    min_val = np.min(image)
    max_val = np.max(image)
    
    if min_val < 0 or max_val > 1:
        print(f"Scaling applied to {file_path}")
        
        # Apply min-max scaling
        image = (image - min_val) / (max_val - min_val)
    else:
        print(f"No scaling needed for {file_path}")
        print(f"Data range: [{min_val}, {max_val}]")
    
    return image


def create_dataset(base_path):
    inputs = []
    original_rgb_images = []  # To store the original RGB images
    print(f"Traversing base directory: {base_path}")
    
    for root, dirs, files in os.walk(base_path):
        for dir_name in dirs:
            if dir_name.startswith('smalldata_'):
                dir_path = os.path.join(root, dir_name)
                print(f"Processing folder: {dir_path}")
                dataset_images = {}
                missing_indices = []

                for index in SPECTRAL_INDICES:
                    matching_files = [f for f in os.listdir(dir_path) if f.startswith(f'{index}_') and f.endswith('.tif')]
                    if matching_files:
                        file_path = os.path.join(dir_path, matching_files[0])
                        print(f"Found file for {index}: {file_path}")
                        data = load_tif(file_path)
                        dataset_images[index] = data

                        # If this is the RGB image, store the original data
                        if index == 'RGB':
                            original_rgb_images.append(data)
                    else:
                        print(f"Missing file for index {index} in directory {dir_path}")
                        missing_indices.append(index)
                        break  # Stop processing this directory if any index is missing

                if len(missing_indices) == 0:
                    # Stack the images in the correct order as per SPECTRAL_INDICES
                    input_stack = np.stack([dataset_images[index] for index in SPECTRAL_INDICES], axis=-1)
                    if input_stack.shape[-1] == 14:  # Ensure correct number of channels (14 expected)
                        inputs.append(input_stack)
                    else:
                        print(f"Warning: Unexpected number of channels: {input_stack.shape[-1]}. Expected 14.")
                else:
                    print(f"Skipping folder {dir_path} due to missing indices: {missing_indices}")
    
    # Verification step
    if inputs:
        num_channels = inputs[0].shape[-1]
        print(f"Finished creating dataset. Number of images: {len(inputs)}. Each image has {num_channels} channels.")
    else:
        print(f"Finished creating dataset. No images loaded.")

    return np.array(inputs), np.array(original_rgb_images)


def pre_process(data_path):
    # Extracting the ZIP file
    unzip_path = data_path.replace('.zip', '')
    if not os.path.exists(unzip_path):
        with zipfile.ZipFile(data_path, 'r') as zip_ref:
            zip_ref.extractall(unzip_path)
            print(f"Extracted zip file to {unzip_path}")
    
    X, original_rgb_images = create_dataset(unzip_path)
    return X, original_rgb_images, SPECTRAL_INDICES
