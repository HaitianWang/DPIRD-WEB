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

openai.api_key = "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"  # This is api-key for OpenAI and it should be replaced by your own

file_ops_bp = Blueprint('file_ops', __name__)

@file_ops_bp.route('/upload', methods=['POST', 'OPTIONS'])
@cross_origin(origins="*", methods=['POST', 'OPTIONS'], allow_headers=['Content-Type'])
def upload_file():
    if request.method == 'OPTIONS':
        return '', 204

    file = request.files['file']
    print(datetime.datetime.now(), file.filename)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        zip_name = filename.rsplit('.', 1)[0]  # 获取文件名，不包括扩展名
        output_folder = os.path.join('./tmp/ct', zip_name)  # 文件夹位置
        src_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(src_path)

        # 创建文件夹
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        print("src_path, output_folder",src_path, output_folder)
        # 调用 process_indices.py 中的函数，处理图像并计算指数，并保存到 output_folder
        process_zip_and_calculate_indices(src_path, output_folder)

        # 调用其他处理逻辑
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
    return send_from_directory('data', 'testfile.zip', as_attachment=True)

@file_ops_bp.route('/tmp/<path:file>', methods=['GET'])
def show_photo(file):
    if request.method == 'GET' and file is not None:
        image_data = open(f'tmp/{file}', "rb").read()
        response = make_response(image_data)
        response.headers['Content-Type'] = 'image/png'
        return response

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def analyze_text(text):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # 使用聊天模型
            messages=[
                {"role": "system", "content": "You're a helpful agricultural expert."},  # 给定一个系统角色
                {"role": "user", "content": text}  # 用户输入为传入的文本
            ],
            max_tokens=500,
            n=1,
            stop=None,
            temperature=0.7
        )
        gpt_reply = response.choices[0].message['content'].strip()  # 获取聊天模型的回复
        return gpt_reply

    except Exception as e:
        return f"Error: {str(e)}"
