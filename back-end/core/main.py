from core import process
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.applications.inception_v3 import InceptionV3
from tensorflow.keras.layers import Conv2D, UpSampling2D, concatenate, Input, BatchNormalization, Layer
from tensorflow.keras.models import Model
import numpy as np
import pandas as pd
import rasterio
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
import io
from PIL import Image
import uuid
import matplotlib

def reduce_channels(X, channels_to_keep=13):
    """
    Reduce the number of channels in the input data to the specified number.
    This function assumes that the channels you want to keep are the first `channels_to_keep` channels.
    
    Parameters:
    X (numpy array): The input data with shape (num_samples, height, width, num_channels).
    channels_to_keep (int): The number of channels to keep.
    
    Returns:
    numpy array: The input data with reduced channels.
    """
    return X[:, :, :, 1:]

def convert_tif_to_rgb(image):
    """
    Convert TIF image color values to the range [0, 255] for RGB display.
    
    Parameters:
    image (numpy array): The input TIF image with shape (height, width, 3).
    
    Returns:
    numpy array: The image converted to uint8 with values in the range [0, 255].
    """
    if image.shape[-1] != 3:
        raise ValueError("Input image must have 3 channels for RGB conversion.")

    scaled_image = np.zeros_like(image, dtype=np.uint8)
    
    for i in range(3):  # Assuming the channels are ordered as Red, Green, Blue
        channel = image[:, :, i]
        min_val = np.min(channel)
        max_val = np.max(channel)

        if max_val > min_val:
            scaled_image[:, :, i] = ((channel - min_val) / (max_val - min_val) * 255).astype(np.uint8)
        else:
            scaled_image[:, :, i] = np.zeros_like(channel, dtype=np.uint8)  # Handle edge case where the channel is uniform

    return scaled_image


def c_main(path, model):
    # Preprocess the data and get the input images and original RGB images
    X, original_rgb_images, spectrum_names = process.pre_process(path)
    print(f'Number of images: {X.shape[0]}')
    
    if X.size == 0:
        raise ValueError("The dataset is empty. Please check the data directory and file paths.")
   
    # Reduce the channels to 13 if necessary
    if X.shape[-1] == 14:
        X = reduce_channels(X, channels_to_keep=13)
        spectrum_names = spectrum_names[:13]  # Adjust the spectrum names if necessary

    matplotlib.use('Agg')
    
    # Function to save images
    def save_image(img, title, cmap=None):
        """
        Save the image with the appropriate colormap. 
        If cmap is None and the image has 3 channels, it assumes the image is RGB and uses the default colors.
        """
        plt.figure(figsize=(5, 5))
        
        if cmap is None and img.shape[-1] == 3:
            # For RGB images, convert TIF color values to the range [0, 255]
            img = convert_tif_to_rgb(img)
            plt.imshow(img)
        else:
            plt.imshow(img, cmap=cmap)
        
        plt.title(title)
        plt.axis('off')
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)
        return Image.open(buf)

    print("Predicting on validation set")
    y_pred = model.predict(X)

    # Custom color map: -1 to red, 0 to white, 1 to green
    def custom_cmap():
        colors = [(1, 0, 0), (1, 1, 1), (0, 1, 0)]  # Red, White, Green
        cmap_name = 'custom_cmap'
        return matplotlib.colors.LinearSegmentedColormap.from_list(cmap_name, colors, N=256)

    # Save the original RGB image
    original_rgb_image = original_rgb_images[0]  # Assuming we're working with the first image
    input_images = [save_image(original_rgb_image, 'Original RGB')]

    # Apply the custom colormap to the predicted mask
    y_pred_rescaled = np.clip(y_pred[0, :, :, 0], -1, 1)  # Assuming the output is in the range [-1, 1]
    predicted_mask = save_image(y_pred_rescaled, 'Predicted Mask', cmap=custom_cmap())

    # Unique ID for this prediction
    pid = str(uuid.uuid4())

    # Image info
    image_info = {
        'input_shape': X.shape,
        'prediction_shape': y_pred.shape,
    }

    return pid, input_images, predicted_mask, image_info, ['RGB']
