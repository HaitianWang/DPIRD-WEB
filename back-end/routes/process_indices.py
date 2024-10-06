# This script is designed to process a zip file containing multispectral images and calculate various vegetation indices from those images.
# It includes the following main steps:
# 1. Extract the uploaded zip file to a specified folder.
# 2. Identify and load specific image bands such as Blue, Green, Red, Near-Infrared (NIR), and Red-Edge.
# 3. Calculate a set of vegetation indices (e.g., NDVI, GNDVI, SAVI, etc.) based on the loaded image bands.
# 4. Save the calculated indices as .tif files in the output folder for further analysis or use.


import os
import zipfile
import numpy as np
import rasterio

# Extract and process the uploaded zip file, calculating vegetation indices from the extracted images.
def process_zip_and_calculate_indices(zip_file_path, output_folder):
    """
    Processes a zip file containing multispectral images, extracts it, and calculates vegetation indices.

    Parameters:
    zip_file_path (str): Path to the zip file containing the images.
    output_folder (str): Path to the folder where extracted images and processed indices will be stored.

    Returns:
    None
    """
    print("zip_file_path, output_folder", zip_file_path, output_folder)
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Define variables for image bands
    blue, green, red, nir, re = None, None, None, None, None

    # Traverse extracted files and read images based on band type
    for root, dirs, files in os.walk(output_folder):
        for file in files:
            file_path = os.path.join(root, file)
            if "Blue" in file:
                blue = rasterio.open(file_path).read(1)
            elif "Green" in file:
                green = rasterio.open(file_path).read(1)
            elif "Red_" in file and "RedEdge" not in file:
                red = rasterio.open(file_path).read(1)
            elif "NIR" in file:
                nir = rasterio.open(file_path).read(1)
            elif "RedEdge" in file:
                re = rasterio.open(file_path).read(1)
            elif "RGB" in file:
                print(f"RGB image found: {file_path}, no processing required.")
                continue

    # Ensure all required image bands are loaded
    if any([blue is None, green is None, red is None, nir is None, re is None]):
        raise ValueError("One or more required images (blue, green, red, nir, re) are missing!")

    # Calculate vegetation indices
    indices = calculate_indices(blue, green, red, nir, re)

    # Assume a profile to save .tif files
    profile = {
        'crs': rasterio.crs.CRS.from_epsg(4326),  # Example CRS, adjust as needed
        'transform': rasterio.transform.from_origin(0, 0, 1, 1),  # Example transform, adjust as needed
    }

    # Save calculated indices as .tif files
    hor, cor = 1, 1  # Example values, replace with actual values if available
    save_indices_as_tif(indices, output_folder, hor, cor, profile)

# Calculate various vegetation indices from the multispectral bands
def calculate_indices(blue, green, red, nir, re):
    """
    Calculates multiple vegetation indices from the given image bands.

    Parameters:
    blue (numpy array): The blue band image.
    green (numpy array): The green band image.
    red (numpy array): The red band image.
    nir (numpy array): The near-infrared (NIR) band image.
    re (numpy array): The red-edge band image.

    Returns:
    dict: A dictionary of calculated vegetation indices.
    """
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

# Save the calculated indices as .tif files
def save_indices_as_tif(indices, folder_path, hor, cor, profile):
    """
    Saves the calculated vegetation indices as .tif files.

    Parameters:
    indices (dict): Dictionary of vegetation indices to save.
    folder_path (str): Path to the folder where the files will be saved.
    hor (int): Horizontal coordinate or identifier.
    cor (int): Vertical coordinate or identifier.
    profile (dict): Profile for the output .tif files including CRS and transform.

    Returns:
    None
    """
    for index_name, index_data in indices.items():
        tif_path = os.path.join(folder_path, f'{index_name}_{hor}_{cor}.tif')
        with rasterio.open(
                tif_path, 'w', driver='GTiff', height=index_data.shape[0], width=index_data.shape[1],
                count=1, dtype=index_data.dtype, crs=profile['crs'], transform=profile['transform']
        ) as dst:
            dst.write(index_data, 1)
        print(f'Saved {tif_path}')
