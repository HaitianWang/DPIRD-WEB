import os
import numpy as np
import pandas as pd
import rasterio
import tensorflow as tf
import sys
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.applications.inception_v3 import InceptionV3
from tensorflow.keras.layers import Conv2D, UpSampling2D, concatenate, Input, BatchNormalization, Layer
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
import matplotlib.pyplot as plt
import zipfile

# Define spectrum names at the module level
SPECTRUM_NAMES = ['ExG', 'ExR', 'PRI', 'MGRVI', 'SAVI', 'MSAVI', 'EVI', 'REIP', 'CI', 'OSAVI', 'TVI', 'MCARI', 'TCARI']

# GPU configuration
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
    return image

def create_dataset(base_path):
    images = []
    print(f"Traversing base directory: {base_path}")
    for root, dirs, files in os.walk(base_path):
        for dir_name in dirs:
            if dir_name.startswith('smalldata_'):
                dir_path = os.path.join(root, dir_name)
                print(f"Processing folder: {dir_path}")
                for file_name in os.listdir(dir_path):
                    if file_name.endswith('.tif'):
                        print(f"Processing file: {file_name}")
                        channels = []
                        for index in SPECTRUM_NAMES:
                            index_path = os.path.join(dir_path, f"{index}_{file_name.split('_')[1]}_{file_name.split('_')[2].split('.')[0]}.tif")
                            if os.path.exists(index_path):
                                channels.append(load_tif(index_path))
                            else:
                                print(f"File {index_path} does not exist, adding zero array")
                                channels.append(np.zeros((512, 512)))  
                       
                        multi_channel_image = np.stack(channels, axis=-1)
                        images.append(multi_channel_image)
                       
    print(f"Finished creating dataset. Number of images: {len(images)}")
    return np.array(images)

def pre_process(data_path):
    # Extracting the ZIP file
    unzip_path = data_path.replace('.zip', '')
    if not os.path.exists(unzip_path):
        with zipfile.ZipFile(data_path, 'r') as zip_ref:
            zip_ref.extractall(unzip_path)
            print(f"Extracted zip file to {unzip_path}")
    
    X = create_dataset(unzip_path)
    return X, SPECTRUM_NAMES