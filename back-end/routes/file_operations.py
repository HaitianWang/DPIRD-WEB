# This script is responsible for handling file uploads and processing in the DPIRD Intellicrop project.
# The main features include:
# 1. Handling file uploads, specifically .zip files, and extracting them.
# 2. Processing the extracted files to calculate spectral indices and generate predictions using a machine learning model.
# 3. Saving the results (input images, predicted mask) and providing URLs for accessing these files.
# 4. Using OpenAI's GPT model to analyze weed data and provide agricultural suggestions based on the results.
# 5. Supporting file downloads and displaying images from temporary directories.

import zipfile
import shutil
from flask import Blueprint, jsonify, request, make_response, send_from_directory, current_app
from flask_cors import cross_origin
from werkzeug.utils import secure_filename
import os
import datetime
import core.main
import openai
from .process_indices import process_zip_and_calculate_indices

openai.api_key = ""  # This is api-key for OpenAI and it should be replaced by your own

file_ops_bp = Blueprint('file_ops', __name__)

@file_ops_bp.route('/upload', methods=['POST', 'OPTIONS'])
@cross_origin(origins="*", methods=['POST', 'OPTIONS'], allow_headers=['Content-Type'])
def upload_file():
    """
    Handles file uploads, specifically .zip files, for processing.
    The function saves the uploaded file, extracts its contents, processes the images,
    and generates weed identification predictions using a machine learning model.

    Returns a JSON response with URLs to the processed images and analysis results, including weed removal suggestions.
    """
    if request.method == 'OPTIONS':
        return '', 204

    file = request.files['file']
    print(datetime.datetime.now(), file.filename)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        print("filename", filename)
        zip_name = filename.rsplit('.', 1)[0]  # Get the file name without the extension
        print("zip_name", zip_name)
        src_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(src_path)

        # Extract ZIP file
        with zipfile.ZipFile(src_path, 'r') as zip_ref:
            zip_ref.extractall('./tmp/ct')

        folder_name = get_single_folder_name_from_zip(src_path)
        print("folder_name", folder_name)
        output_folder = os.path.join('./tmp/ct', folder_name)

        print("src_path, output_folder", src_path, output_folder)

        # Process images and calculate indices
        process_zip_and_calculate_indices(src_path, output_folder)

        # Call other processing logic
        pid, input_images, predicted_mask, image_info, spectrum_names = core.main.c_main(
            output_folder, current_app.model)

        print("openai-version", openai.__version__)

        # Analyze image_info using GPT to get weed removal suggestions
        analysis_prompt = f"""
        The DPIRD AgriVision platform is an expert platform developed by the Department of Agriculture of Western Australia, designed for further analysis of
        weed identification results and providing AI-driven professional advice. You are now serving as a professional agricultural consultant on this
        platform. Based on the weed information from the test field we provide, combined with your professional agricultural knowledge and the remote
        sensing knowledge base, please provide detailed explanations and analysis. Additionally, give guidance tailored to the specific conditions of
        Western Australia (such as environment, climate, soil, rainfall, etc.). If there is a high weed density, provide a clear warning based on the
        national context of Australia, and offer advanced analysis.
        The image shows {image_info['Vegetation']} vegetation, {image_info['Weed']} weed, and {image_info['Misc/Other']} miscellaneous or other elements. 
        Attention: Don't have markdown formatting. Do not bold text. No "*" in output. Different points suggest subparagraphs.
        """
        weed_removal_suggestions = analyze_text(analysis_prompt)
        print("suggestions", weed_removal_suggestions)

        # Create directories if they don't exist
        os.makedirs('./tmp/input', exist_ok=True)
        os.makedirs('./tmp/draw', exist_ok=True)

        # Save all input images and the predicted mask
        input_image_urls = []
        for img, name in zip(input_images, spectrum_names):
            input_image_path = f'./tmp/input/{pid}_{name}.png'
            img.save(input_image_path)
            input_image_urls.append(f'{request.host_url}tmp/input/{pid}_{name}.png')

        predicted_mask_path = f'./tmp/draw/{pid}_predicted.png'
        predicted_mask.save(predicted_mask_path)

        return jsonify({
            'status': 1,
            'input_image_urls': input_image_urls,
            'spectrum_names': spectrum_names,
            'predicted_mask_url': f'{request.host_url}tmp/draw/{pid}_predicted.png',
            'image_info': image_info,
            'weed_removal_suggestions': weed_removal_suggestions
        })

    return jsonify({'status': 0})

@file_ops_bp.route("/download", methods=['GET'])
def download_file():
    """
    Handles file downloads by sending the requested file to the client.
    """
    return send_from_directory('data', 'testfile.zip', as_attachment=True)

@file_ops_bp.route('/tmp/<path:file>', methods=['GET'])
def show_photo(file):
    """
    Serves images from the 'tmp' directory. The images are typically those processed or saved during file uploads.

    Parameters:
    file (str): The path to the image file in the 'tmp' directory.

    Returns:
    Flask response: The requested image with the appropriate content-type header.
    """
    if request.method == 'GET' and file is not None:
        image_data = open(f'tmp/{file}', "rb").read()
        response = make_response(image_data)
        response.headers['Content-Type'] = 'image/png'
        return response

def allowed_file(filename):
    """
    Check if the uploaded file is allowed by verifying its extension.

    Parameters:
    filename (str): The name of the file being uploaded.

    Returns:
    bool: True if the file is allowed, False otherwise.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def analyze_text(text):
    """
    Analyze the given text using the OpenAI GPT-3.5-turbo model to provide expert analysis on weed management.

    Parameters:
    text (str): The text input that needs to be analyzed by GPT.

    Returns:
    str: The response generated by GPT based on the input text.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use the chat model
            messages=[
                {"role": "system", "content": "You're a helpful agricultural expert."},  # Set a system role
                {"role": "user", "content": text}  # User input as text
            ],
            max_tokens=500,
            n=1,
            stop=None,
            temperature=0.7
        )
        gpt_reply = response.choices[0].message['content'].strip()  # Get response from the model
        return gpt_reply

    except Exception as e:
        return f"Error: {str(e)}"

def get_single_folder_name_from_zip(zip_file_path):
    """
    Extract the name of the first folder from a ZIP file.

    Parameters:
    zip_file_path (str): The path to the ZIP file.

    Returns:
    str: The name of the first folder in the ZIP file.
    """
    # Stores the folder name
    folder_name = None

    # Open the ZIP file
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        # Iterate over all entries in the ZIP file
        for file_info in zip_ref.infolist():
            # If it's a directory and folder_name is not set, record its name
            if file_info.is_dir():
                folder_name = os.path.basename(os.path.normpath(file_info.filename))
                break  # Only process the first directory, assuming there's only one

    return folder_name
