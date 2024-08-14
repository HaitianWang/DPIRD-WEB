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

def c_main(path, model):
    X, spectrum_names = process.pre_process(path)
    print(f'Number of images: {X.shape[0]}')
    if X.size == 0:
        raise ValueError("The dataset is empty. Please check the data directory and file paths.")
   
    print("Normalizing input images")
    X = X / np.max(X)
    matplotlib.use('Agg')

    def save_image(img, title):
        plt.figure(figsize=(5, 5))
        plt.imshow(img, cmap='gray')
        plt.title(title)
        plt.axis('off')
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)
        return Image.open(buf)

    print("Predicting on validation set")
    y_pred = model.predict(X)
   
    # Save all input images
    input_images = [save_image(X[0, :, :, i], name) for i, name in enumerate(spectrum_names)]
    predicted_mask = save_image(np.argmax(y_pred[0], axis=-1), 'Predicted Mask')
   
    # Unique ID for this prediction
    pid = str(uuid.uuid4())

    sum_of_channels = np.sum(y_pred, axis=-1)

    # Verify if all values are close to 1
    are_all_close_to_one = np.allclose(sum_of_channels, 1)
    print(f"Are all sums of the four channels equal to 1? {are_all_close_to_one}")
   
    # Image info
    image_info = {
        'input_shape': X.shape,
        'prediction_shape': y_pred.shape,
        'sum_of_channels': sum_of_channels.tolist(),
    }
   
    return pid, input_images, predicted_mask, image_info, spectrum_names