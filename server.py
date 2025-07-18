# from flask import Flask, request, render_template, jsonify, send_from_directory
# import os
# import base64
# from datetime import datetime
# from werkzeug.utils import secure_filename

# app = Flask(__name__)
# UPLOAD_FOLDER = 'uploads'
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/upload', methods=['POST'])
# def upload_cropped():
#     data = request.json.get('image')
#     if not data:
#         return jsonify({'error': 'No image data received'}), 400

#     img_data = data.split(',')[1]
#     img_bytes = base64.b64decode(img_data)
#     filename = f"{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}.png"
#     filepath = os.path.join(UPLOAD_FOLDER, filename)

#     with open(filepath, 'wb') as f:
#         f.write(img_bytes)

#     return jsonify({'filename': filename})

# @app.route('/upload-image', methods=['POST'])
# def upload_image():
#     file = request.files.get('file')
#     if not file:
#         return 'No file uploaded', 400
#     filename = secure_filename(file.filename)
#     filepath = os.path.join(UPLOAD_FOLDER, filename)
#     file.save(filepath)
#     return jsonify({'filename': filename})

# @app.route('/uploads/<filename>')
# def serve_uploaded_file(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, request, render_template, jsonify, send_from_directory
import os
import base64
from datetime import datetime

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload-image', methods=['POST'])
def upload_image():
    image_data = request.json.get('image')
    if not image_data:
        return jsonify({'error': 'No image data received'}), 400

    header, encoded = image_data.split(',', 1)
    img_bytes = base64.b64decode(encoded)
    filename = f"original_{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}.png"
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    with open(filepath, 'wb') as f:
        f.write(img_bytes)

    return jsonify({'filename': filename})

@app.route('/crop-image', methods=['POST'])
def crop_image():
    image_data = request.json.get('image')
    if not image_data:
        return jsonify({'error': 'No image data received'}), 400

    header, encoded = image_data.split(',', 1)
    img_bytes = base64.b64decode(encoded)
    filename = f"cropped_{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}.png"
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    with open(filepath, 'wb') as f:
        f.write(img_bytes)

    return jsonify({'filename': filename})

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)
if __name__ == '__main__':
    app.run(debug=True)