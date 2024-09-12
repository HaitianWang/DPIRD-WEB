from flask import Blueprint, jsonify, request, current_app
from werkzeug.utils import secure_filename
import os
import shutil
import openai
from core import main as core_main

upload_bp = Blueprint('upload', __name__)

openai.api_key = ""  # This is api-key for OpenAI and it should be replaced by your own

@upload_bp.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        src_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(src_path)
        shutil.copy(src_path, './tmp/ct')
        image_path = os.path.join('./tmp/ct', filename)

        # Call core_main.c_main to get the necessary information
        pid, input_image, predicted_mask, image_info = core_main.c_main(
            image_path, current_app.model)

        # Analyze image_info using GPT to get weed removal suggestions
        analysis_prompt = f"""
        The image shows {image_info['Vegetation']} vegetation, {image_info['Weed']} weed, and {image_info['Misc/Other']} miscellaneous or other elements.
        Please provide suggestions for how to effectively remove the weeds while minimizing harm to the crops.
        """
        weed_removal_suggestions = analyze_text(analysis_prompt)
        print("suggestions", weed_removal_suggestions)

        # Create directories if they don't exist
        os.makedirs('./tmp/input', exist_ok=True)
        os.makedirs('./tmp/draw', exist_ok=True)

        # Save the input and predicted images
        input_image_path = f'./tmp/input/{pid}.png'
        predicted_mask_path = f'./tmp/draw/{pid}.png'
        input_image.save(input_image_path)
        predicted_mask.save(predicted_mask_path)

        # Return the JSON response with image info and weed removal suggestions
        return jsonify({
            'status': 1,
            'input_image_url': f'{request.host_url}tmp/input/{pid}.png',
            'predicted_mask_url': f'{request.host_url}tmp/draw/{pid}.png',
            'image_info': image_info,
            'weed_removal_suggestions': weed_removal_suggestions
        })
    return jsonify({'status': 0})

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


def analyze_text(text):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=text,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.7
        )
        gpt_reply = response.choices[0].text.strip()
        return gpt_reply

    except Exception as e:
        return f"Error: {str(e)}"
