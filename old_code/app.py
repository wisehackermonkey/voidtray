from flask import Flask, request, send_file, render_template_string
from rembg import remove
from PIL import Image
import io

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
  <title>Polygon Crop + Background Removal</title>
<script type="module">
  import PolygonCropTool from "https://cdn.skypack.dev/polygon-crop-tool";
  window.PolygonCropTool = PolygonCropTool;
</script>
  <script async src="https://docs.opencv.org/4.x/opencv.js" type="text/javascript"></script>
  <style>
    canvas { border: 1px solid #ccc; margin-top: 10px; display: block; }
    #controls { margin-top: 10px; }
  </style>
</head>
<body>
  <h2>Polygon Crop Tool + Background Removal</h2>
  <input type="file" id="upload" accept="image/*" />
  <div id="controls">
    <button id="crop">Crop Polygon</button>
    <button id="remove-bg">Remove Background</button>
  </div>
  <canvas id="canvas"></canvas>

  <script>
    const upload = document.getElementById('upload');
    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d');
    let image = new Image();
    let polygonCrop;

    upload.onchange = function () {
      const file = upload.files[0];
      if (!file) return;

      image.src = URL.createObjectURL(file);
      image.onload = () => {
        canvas.width = image.width;
        canvas.height = image.height;
        ctx.drawImage(image, 0, 0);

        if (polygonCrop) polygonCrop.destroy();
        polygonCrop = new PolygonCropTool(canvas, { showCropButton: false });
      };
    };

    document.getElementById('crop').onclick = () => {
      if (!polygonCrop) return;
      const cropped = polygonCrop.crop();
      canvas.width = cropped.width;
      canvas.height = cropped.height;
      ctx.putImageData(cropped, 0, 0);
      polygonCrop.destroy();
    };

    document.getElementById('remove-bg').onclick = async () => {
      canvas.toBlob(async (blob) => {
        const formData = new FormData();
        formData.append('image', blob, 'cropped.png');

        const res = await fetch('/remove-bg', {
          method: 'POST',
          body: formData
        });

        const resultBlob = await res.blob();
        const img = new Image();
        img.src = URL.createObjectURL(resultBlob);
        img.onload = () => {
          canvas.width = img.width;
          canvas.height = img.height;
          ctx.clearRect(0, 0, canvas.width, canvas.height);
          ctx.drawImage(img, 0, 0);
        };
      }, 'image/png');
    };
  </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_PAGE)

@app.route('/remove-bg', methods=['POST'])
def remove_bg():
    if 'image' not in request.files:
        return 'No image provided', 400

    img_file = request.files['image']
    img = Image.open(img_file.stream).convert("RGBA")

    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes = img_bytes.getvalue()

    output = remove(img_bytes)

    return send_file(
        io.BytesIO(output),
        mimetype='image/png',
        as_attachment=False,
        download_name='removed.png'
    )

if __name__ == '__main__':
    app.run(debug=True)
