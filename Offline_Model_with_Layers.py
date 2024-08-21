import os
import numpy as np
import matplotlib.pyplot as plt
import rasterio
import tensorflow as tf
from tensorflow.keras.layers import Input, Conv2D, Lambda, Conv3D
from tensorflow.keras.models import Model
from sklearn.model_selection import train_test_split

# GPU configuration (keeping this part as is)
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

def load_raster(file_path):
    with rasterio.open(file_path) as src:
        data = src.read(1).astype(np.float32)
    
    # Check for NaN values
    if np.isnan(data).any():
        nan_value = np.nan
        print(f"NaN detected in file {file_path}")
        return None
    
    # Check if scaling is necessary
    min_val = np.min(data)
    max_val = np.max(data)
    
    if min_val < 0 or max_val > 1:
        print(f"Scaling applied to {file_path}")
        
        # Apply min-max scaling
        data = (data - min_val) / (max_val - min_val)
    else:
        print(f"No scaling needed for {file_path}")
        print(f"Data range: [{min_val}, {max_val}]")
    
    return data


spectral_indices = ['CI', 'EVI', 'ExG', 'ExR', 'GNDVI', 'MCARI', 'MGRVI', 'MSAVI', 'NDVI', 'OSAVI', 'PRI', 'SAVI', 'TVI']

def create_dataset(base_path):
    inputs = []
    targets = []
   
    spectral_indices = ['CI', 'EVI', 'ExG', 'ExR', 'GNDVI', 'MCARI', 'MGRVI', 'MSAVI', 'NDVI', 'OSAVI', 'PRI', 'SAVI', 'TVI']
    
    print("Processing spectral index images:")
    for root, _, files in os.walk(base_path):
        dataset_images = {}
        missing_indices = []
        nan_detected = False
        for index in spectral_indices:
            matching_files = [f for f in files if f.startswith(f'{index}_') and f.endswith('.tif')]
            if matching_files:
                file_path = os.path.join(root, matching_files[0])
                print(f"\nProcessing {index}: {file_path}")
                data = load_raster(file_path)
               
                if data is None:
                    nan_detected = True
                    break
               
                dataset_images[index] = data
            else:
                missing_indices.append(index)
       
        if len(missing_indices) == 0 and not nan_detected:
            # Stack all indices as input
            input_stack = np.stack([dataset_images[index] for index in spectral_indices], axis=-1)
            inputs.append(input_stack)
           
            # Create multi-channel target
            ndvi_target = dataset_images['NDVI']
            exr_target = dataset_images['ExR']
            
            target = np.stack([ndvi_target, exr_target], axis=-1)
            
            targets.append(target)
        else:
            if nan_detected:
                print(f"Skipping folder {root} due to NaN values in one of the files.")
            else:
                print(f"Skipping folder {root} due to missing indices: {missing_indices}")
   
    return np.array(inputs), np.array(targets)

# Load the dataset
base_path = './2021Test'
X, y = create_dataset(base_path)

# Print shapes for debugging
print("X shape:", X.shape)
print("y shape:", y.shape)

# Split the data
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

from tensorflow.keras.regularizers import l1

def build_cnn_model_with_l1(input_shape, l1_reg=0.001):
    inputs = Input(shape=input_shape)
   
    # First Convolutional Block with L1 regularization
    x = Conv2D(32, (3, 3), padding='same', activation='relu', kernel_regularizer=l1(l1_reg))(inputs)
    x = Conv2D(32, (3, 3), padding='same', activation='relu', kernel_regularizer=l1(l1_reg))(x)
   
    # Output layer (2 channels: NDVI and ExR)
    outputs = Conv2D(2, (1, 1), activation='linear')(x)
   
    model = Model(inputs, outputs)
    return model

input_shape = X_train.shape[1:]  # For example, (256, 256, 13)

# Build the model with L1 regularization
model = build_cnn_model_with_l1(input_shape=input_shape, l1_reg=0.001)
model.compile(optimizer='adam', loss='mse', metrics=['mae'])
model.summary()

# Train the model
history = model.fit(
    X_train, y_train,
    validation_data=(X_val, y_val),
    epochs=300,
    batch_size=12,
    verbose=1
)

# Save the model to an H5 file
model.save('cnn_model_with_l1.h5')

# Plot the training history
plt.plot(history.history['loss'], label='train_loss')
plt.plot(history.history['val_loss'], label='val_loss')
plt.legend()
plt.show()

import matplotlib.colors as mcolors

def plot_multiple_examples(X_val, y_val, y_pred, num_examples=5):
    ndvi_layer = X_val[..., spectral_indices.index('NDVI')]  # Extract the NDVI layer
    exr_layer = X_val[..., spectral_indices.index('ExR')]  # Extract the ExR layer
   
    # Create a custom colormap
    cmap = mcolors.LinearSegmentedColormap.from_list("custom_cmap", [(1, 0, 0), (1, 1, 1), (0, 1, 0)], N=256)
    
    def create_visualization(ndvi, exr):
        vis = np.where(exr > 0.5, -1,  # Red when ExR is high
                np.where((ndvi <= 0.54) & (exr <= 0.5), 1,  # White when both are low
                ndvi))  # NDVI value when NDVI is high and ExR is low
        return vis
    
    for i in range(num_examples):
        plt.figure(figsize=(20, 15))
       
        # Plot RGB Image (assuming it's the first 3 channels)
        plt.subplot(2, 3, 1)
        plt.imshow(X_val[i][:, :, :3])
        plt.title(f"Input RGB - Example {i+1}")
       
        # Plot NDVI Image
        plt.subplot(2, 3, 2)
        plt.imshow(ndvi_layer[i], cmap='viridis')
        plt.title(f"Input NDVI - Example {i+1}")
        
        # Plot ExR Image
        plt.subplot(2, 3, 3)
        plt.imshow(exr_layer[i], cmap='viridis')
        plt.title(f"Input ExR - Example {i+1}")
       
        # Plot True y with custom colormap
        true_vis = create_visualization(y_val[i][..., 0], y_val[i][..., 1])
        plt.subplot(2, 3, 4)
        plt.imshow(true_vis, cmap=cmap, vmin=-1, vmax=1)
        plt.title(f"True y - Example {i+1}")
       
        # Plot Predicted y with custom colormap
        pred_vis = create_visualization(y_pred[i][..., 0], y_pred[i][..., 1])
        plt.subplot(2, 3, 5)
        plt.imshow(pred_vis, cmap=cmap, vmin=-1, vmax=1)
        plt.title(f"Predicted y - Example {i+1}")
       
        plt.tight_layout()
        plt.show()

# Example usage after prediction
y_pred = model.predict(X_val)
# Plot examples from the validation set
plot_multiple_examples(X_val, y_val, y_pred, num_examples=3)
