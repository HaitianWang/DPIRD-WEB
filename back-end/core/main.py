from core import process
import os
import numpy as np
import matplotlib.pyplot as plt
import rasterio
import tensorflow as tf
import matplotlib.colors as mcolors
import io
from PIL import Image
import uuid
import matplotlib
from sklearn.model_selection import train_test_split
from tensorflow.keras.layers import Conv2D, Input
from tensorflow.keras.models import Model

# Assuming process is an external module that you import
# from core import process

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

from PIL import Image
import numpy as np
import io
#import matplotlib.pyplot as plt

#import rasterio
import numpy as np

def convert_array_to_rgb(image_array):
    """
    Convert a numpy array from a normalized RGB image to an 8-bit RGB image.
   
    Parameters:
    image_array (numpy.ndarray): The input image array (normalized to [0, 1]).
   
    Returns:
    numpy.ndarray: The image converted to RGB with values in the range [0, 255].
    """
    # Ensure the array is 3D
    if image_array.ndim == 2:
        # If it's a 2D array, replicate it to 3 channels
        image_array = np.stack((image_array,) * 3, axis=-1)
    elif image_array.ndim > 3:
        # If it has more than 3 dimensions, take the first 3 channels
        image_array = image_array[:, :, :3]
   
    # Convert to 8-bit (0-255 range)
    rgb_array = (image_array * 255).astype(np.uint8)
   
    return rgb_array

import matplotlib.pyplot as plt
import io
from PIL import Image

def save_image(img_array, title, cmap=None):
    plt.figure(figsize=(5, 5))
   
    if cmap is None:
        rgb_img = convert_array_to_rgb(img_array)
        plt.imshow(rgb_img)
    else:
        plt.imshow(img_array, cmap=cmap)
   
    plt.title(title)
    plt.axis('off')
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return Image.open(buf)

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
    
    print(f"Original RGB image shape: {original_rgb_images[0].shape}, dtype: {original_rgb_images[0].dtype}")

    return pid, input_images, predicted_mask, image_info, ['RGB']