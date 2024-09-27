import os
import zipfile
import numpy as np
import rasterio

# 提取并处理上传的 zip 文件
def process_zip_and_calculate_indices(zip_file_path, output_folder):
    print("zip_file_path, output_folder", zip_file_path, output_folder)
    # 创建输出文件夹
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 定义初始变量
    blue, green, red, nir, re = None, None, None, None, None

    # 遍历解压文件，查找并读取图像
    for root, dirs, files in os.walk(output_folder):
        for file in files:
            file_path = os.path.join(root, file)
            if "Blue" in file:  # 使用“Blue”来匹配
                blue = rasterio.open(file_path).read(1)
            elif "Green" in file:  # 使用“Green”来匹配
                green = rasterio.open(file_path).read(1)
            elif "Red_" in file and "RedEdge" not in file:  # 使用“Red”来匹配红光波段
                red = rasterio.open(file_path).read(1)
            elif "NIR" in file:  # 使用“NIR”来匹配
                nir = rasterio.open(file_path).read(1)
            elif "RedEdge" in file:  # 使用“RedEdge”来匹配
                re = rasterio.open(file_path).read(1)
            elif "RGB" in file:  # 如果找到 RGB tif 图像，不做任何处理，直接跳过
                print(f"RGB image found: {file_path}, no processing required.")
                continue

    # 确保所有必需的波段图像都存在
    if any([blue is None, green is None, red is None, nir is None, re is None]):
        raise ValueError("One or more required images (blue, green, red, nir, re) are missing!")

    # 计算指数
    indices = calculate_indices(blue, green, red, nir, re)

    # 假设你有一个 profile，用于保存 .tif 文件
    profile = {
        'crs': rasterio.crs.CRS.from_epsg(4326),  # 示例 CRS，你需要根据实际情况调整
        'transform': rasterio.transform.from_origin(0, 0, 1, 1),  # 示例 transform，根据实际情况调整
    }

    # 保存计算的指数为 .tif 文件
    hor, cor = 1, 1  # 示例值，你可以根据实际情况替换
    save_indices_as_tif(indices, output_folder, hor, cor, profile)

# 计算指数的函数保持不变
def calculate_indices(blue, green, red, nir, re):
    indices = {}

    # Green Normalized Difference Vegetation Index (GNDVI)
    GNDVI = (nir - green) / (nir + green)
    indices['GNDVI'] = GNDVI

    # Soil Adjusted Vegetation Index (SAVI)
    L = 0.5  # The L value is a constant
    SAVI = (nir - red) * (1 + L) / (nir + red + L)
    indices['SAVI'] = SAVI

    # Modified Soil Adjusted Vegetation Index (MSAVI)
    MSAVI = 0.5 * (2 * nir + 1 - np.sqrt((2 * nir + 1) ** 2 - 8 * (nir - red)))
    indices['MSAVI'] = MSAVI

    # Excess Green (ExG)
    ExG = 2 * green - red - blue
    indices['ExG'] = ExG

    # Excess Red (ExR)
    ExR = 1.3 * red - green
    indices['ExR'] = ExR

    # Photochemical Reflectance Index (PRI)
    PRI = (green - blue) / (green + blue)
    indices['PRI'] = PRI

    # Modified Green Red Vegetation Index (MGRVI)
    MGRVI = (green ** 2 - red ** 2) / (green ** 2 + red ** 2)
    indices['MGRVI'] = MGRVI

    # Normalized Difference Vegetation Index (NDVI)
    NDVI = (nir - red) / (nir + red)
    indices['NDVI'] = NDVI

    # Enhanced Vegetation Index (EVI)
    EVI = 2.5 * (nir - red) / (nir + 6 * red - 7.5 * blue + 1)
    indices['EVI'] = EVI

    # Red Edge Inflection Point Index (REIP)
    REIP = 700 + 40 * (((red + re) / 2 - green) / (re - green))
    indices['REIP'] = REIP

    # Chlorophyll Index (CI)
    CI = (nir / red) - 1
    indices['CI'] = CI

    # Optimized Soil Adjusted Vegetation Index (OSAVI)
    OSAVI = (nir - red) / (nir + red + 0.16)
    indices['OSAVI'] = OSAVI

    # Transformed Vegetation Index (TVI)
    TVI = np.sqrt(NDVI + 0.5)
    indices['TVI'] = TVI

    # Modified Chlorophyll Absorption in Reflectance Index (MCARI)
    MCARI = (re - red) - 0.2 * (re - green) * (re / red)
    indices['MCARI'] = MCARI

    # Transformed Chlorophyll Absorption in Reflectance Index (TCARI)
    TCARI = 3 * ((re - red) - 0.2 * (re - green) * (re / red))
    indices['TCARI'] = TCARI

    return indices

# 保存计算出来的指数为 .tif 文件
def save_indices_as_tif(indices, folder_path, hor, cor, profile):
    for index_name, index_data in indices.items():
        tif_path = os.path.join(folder_path, f'{index_name}_{hor}_{cor}.tif')
        with rasterio.open(
                tif_path, 'w', driver='GTiff', height=index_data.shape[0], width=index_data.shape[1],
                count=1, dtype=index_data.dtype, crs=profile['crs'], transform=profile['transform']
        ) as dst:
            dst.write(index_data, 1)
        print(f'Saved {tif_path}')