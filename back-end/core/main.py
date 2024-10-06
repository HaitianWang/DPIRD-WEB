# This script processes multi-spectral data for DPIRD Intellicrop, specifically focused on generating predictions and visualizing results.
# The steps include:
# 1. Reducing the number of channels in the input data as needed.
# 2. Converting image arrays to RGB format for easier visualization.
# 3. Applying a custom colormap to display predictions, where red represents weeds, green represents vegetation, and white represents neutral areas.
# 4. Calculating the distribution of these colors in the predicted mask.
# 5. Saving the original and predicted images for analysis.
# The code also handles model predictions and generates a unique identifier for each prediction.

from core import process
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
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

def save_image(mask, title):
    """
    Save an image where the colormap reflects the true range of -1 to 1.

    Parameters:
    mask (numpy.ndarray): The predicted mask array.
    title (str): Title of the image.

    Returns:
    PIL.Image.Image, numpy.ndarray: The saved image in both PIL and numpy formats.
    """
    # Normalize the colormap to reflect the range of -1 to 1
    norm = mcolors.Normalize(vmin=-1, vmax=1)

    # Define a custom colormap: Red for weed, white for neutral, green for vegetation
    colors = [(1, 0, 0), (1, 1, 1), (0, 1, 0)]
    cmap = mcolors.LinearSegmentedColormap.from_list('custom_cmap', colors, N=256)

    # Apply the colormap with normalization
    plt.figure(figsize=(5, 5))
    plt.imshow(mask, cmap=cmap, norm=norm)
    plt.title(title)
    plt.axis('off')

    # Save the image
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=100)
    plt.close()
    buf.seek(0)
    pil_img = Image.open(buf)
    np_img = np.array(pil_img)

    return pil_img, np_img

def color_distribution(mask):
    """
    Calculate the distribution of colors in the predicted mask.

    Parameters:
    mask (numpy.ndarray): The predicted mask array.

    Returns:
    dict: A dictionary containing the percentage of each color.
    """
    total_pixels = mask.size

    # Adjust these thresholds based on your specific range
    red_pixels = np.sum(mask < -0.1)  # Red for negative values
    green_pixels = np.sum(mask > 0.1)  # Green for positive values
    white_pixels = np.sum((mask >= -0.1) & (mask <= 0.1))  # White for values close to 0

    return {
        'red': (red_pixels / total_pixels) * 100,
        'green': (green_pixels / total_pixels) * 100,
        'white': (white_pixels / total_pixels) * 100
    }

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

    # Save the original RGB image
    original_rgb_image = original_rgb_images[0]
    input_images = [save_image(original_rgb_image, 'Original RGB')[0]]

    # Get the predicted mask
    predicted_mask = y_pred[0, :, :, 0]  # Take the first channel

    # Calculate color distribution using the original predicted mask
    color_stats = color_distribution(predicted_mask)

    # Save the predicted mask with the true range of -1 to 1 reflected in the colormap
    predicted_mask_pil, predicted_mask_np = save_image(predicted_mask, 'Predicted Mask')

    # Save the original mask and colorized mask for visual inspection
    plt.imsave('predicted_mask_with_true_range.png', predicted_mask_np)

    print(f"Predicted mask shape: {predicted_mask.shape}")
    print(f"Predicted mask min: {predicted_mask.min()}, max: {predicted_mask.max()}")
    print(f"Color distribution: {color_stats}")

    # Unique ID for this prediction
    pid = str(uuid.uuid4())

    # Image info
    image_info = {
        'Vegetation': f"{color_stats['green']:.2f}%",
        'Weed': f"{color_stats['red']:.2f}%",
        'Misc/Other': f"{color_stats['white']:.2f}%"
    }

    print(f"Original RGB image shape: {original_rgb_images[0].shape}, dtype: {original_rgb_images[0].dtype}")

    return pid, input_images, predicted_mask_pil, image_info, ['RGB']
