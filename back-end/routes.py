from flask import Blueprint, jsonify, request, current_app
from werkzeug.utils import secure_filename
import os
import shutil
from core import main as core_main

upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        src_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(src_path)
        shutil.copy(src_path, './tmp/ct')
        image_path = os.path.join('./tmp/ct', filename)
        
        pid, input_image, predicted_mask, image_info = core_main.c_main(
            image_path, current_app.model)
        
        # Create directories if they don't exist
        os.makedirs('./tmp/input', exist_ok=True)
        os.makedirs('./tmp/draw', exist_ok=True)
        
        # Save the input and predicted images
        input_image_path = f'./tmp/input/{pid}.png'
        predicted_mask_path = f'./tmp/draw/{pid}.png'
        input_image.save(input_image_path)
        predicted_mask.save(predicted_mask_path)
        
        return jsonify({
            'status': 1,
            'input_image_url': f'{request.host_url}tmp/input/{pid}.png',
            'predicted_mask_url': f'{request.host_url}tmp/draw/{pid}.png',
            'image_info': image_info
        })
    return jsonify({'status': 0})

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']