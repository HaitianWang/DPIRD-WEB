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

def load_tif(file_path, is_rgb=False):
    print(f"Loading TIF file from {file_path}")
    with rasterio.open(file_path) as src:
        if is_rgb:
            # Read all three channels for an RGB image
            image = np.dstack([src.read(i) for i in range(1, 4)]).astype(np.float32)
        else:
            # Read only the first channel for other types of images
            image = src.read(1).astype(np.float32)
    
    # Check for NaN values
    if np.isnan(image).any():
        print(f"NaN detected in file {file_path}")
        return None
    
    # Check if scaling is necessary
    min_val = np.min(image)
    max_val = np.max(image)
    
    if is_rgb:
        print(f"Loading RGB image from {file_path}")
        # Normalize RGB to [0, 1] range
        image = (image - min_val) / (max_val - min_val)
        return image
    
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

    # 获取 base_path 中的所有文件
    files = os.listdir(base_path)
    print(f"Files in base path: {files}")
    dataset_images = {}
    missing_indices = []

    # 遍历 SPECTRAL_INDICES 来匹配文件
    for index in SPECTRAL_INDICES:
        # 找到包含光谱索引（如 'CI', 'EVI', 'ExG' 等）的文件
        matching_files = [f for f in files if f.startswith(f'{index}_') and f.endswith('.tif')]
        if matching_files:
            file_path = os.path.join(base_path, matching_files[0])
            print(f"Found file for {index}: {file_path}")
            # 如果是 RGB 图像，设置 is_rgb=True
            data = load_tif(file_path, is_rgb=(index == 'RGB'))

            # 如果是 RGB 图像，使用第一个通道
            if index == 'RGB':
                dataset_images[index] = data[:, :, 0]  # 仅使用 RGB 图像的第一个通道
                original_rgb_images.append(data)  # 存储完整的 RGB 图像
            else:
                dataset_images[index] = data
        else:
            print(f"Missing file for index {index} in directory {base_path}")
            missing_indices.append(index)
            break  # 如果缺少索引文件，停止处理该目录

    if len(missing_indices) == 0:
        # 按 SPECTRAL_INDICES 的顺序堆叠图像
        input_stack = np.stack([dataset_images[index] for index in SPECTRAL_INDICES], axis=-1)
        if input_stack.shape[-1] == len(SPECTRAL_INDICES):  # 确保通道数量正确
            inputs.append(input_stack)
        else:
            print(f"Warning: Unexpected number of channels: {input_stack.shape[-1]}. Expected {len(SPECTRAL_INDICES)}.")
    else:
        print(f"Skipping due to missing indices: {missing_indices}")

    # 验证是否加载了任何图像
    if inputs:
        num_channels = inputs[0].shape[-1]
        print(f"Finished creating dataset. Number of images: {len(inputs)}. Each image has {num_channels} channels.")
    else:
        print(f"Finished creating dataset. No images loaded.")

    return np.array(inputs), np.array(original_rgb_images)


def pre_process(data_path):
    print("data_path",data_path)
    X, original_rgb_images = create_dataset(data_path)
    return X, original_rgb_images, SPECTRAL_INDICES
