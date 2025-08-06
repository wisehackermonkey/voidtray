
# Complete Image to Vector Workflow
# Background removal
from rembg import remove

# 3d cad with python for stl generation
import ezdxf
from svgpathtools import svg2paths
import os
import cadquery as cq
import math
from cqgridfinity import *

# Image handling
from PIL import Image
# Bitmask and image processing (create_bitmask_and_contours)
import numpy as np
from skimage import measure,morphology, filters
from skimage.io import imread, imsave
from scipy import ndimage 
# Visualization
import matplotlib.pyplot as plt
# File handling
import io
import os
import tempfile
# Vectorization
import vtracer
from svgpathtools import svg2paths
from scipy.interpolate import splprep, splev
import svgwrite
# ==== CONFIGURATION ====
# svg_path = r"C:\Users\oran\github\voidtray\output\test4_vector.svg"
# dxf_path = r"C:\Users\oran\github\voidtray\output\shape.dxf"
# stl_output_path = r"C:\Users\oran\github\voidtray\output\shape.stl"

unit_size = 45  # mm grid cell size


# Assuming 96 DPI for your SVG
svg_to_mm_scale = 25.4 / 96  # ~0.264583

# flask server
import os
from flask import Flask, render_template, request, redirect, send_from_directory, url_for
from PIL import Image
from werkzeug.utils import secure_filename
import base64
 
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
STATIC_FOLDER = 'static'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['STATIC_FOLDER'] = STATIC_FOLDER
MEGABYTE = (2 ** 10) ** 2
app.config['MAX_CONTENT_LENGTH'] = None
app.config['MAX_FORM_MEMORY_SIZE'] = 100 * MEGABYTE


os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


# Complete workflow example
input_path = 'static/test4.jpg' 
base_name = os.path.splitext(os.path.basename(input_path))[0]

dxf_path = os.path.join("output", f"{base_name}.dxf")
stl_output_path = os.path.join("static", f"{base_name}.stl")

base_name = os.path.splitext(os.path.basename(input_path))[0]
output_svg = os.path.join("output", f"{base_name}")
 
# image processing
# ---------------------------------------

def remove_background(input_path):
    """
    Remove background from an image using rembg
    
    Args:
        input_path (str): Path to input image
        
    Returns:
        tuple: (original_img, no_bg_img) - Original and background-removed PIL Images
    """
    # Load input image and convert to RGBA
    img = Image.open(input_path).convert('RGBA')
    
    # Convert to bytes for rembg processing
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes = img_bytes.getvalue()
    
    # Remove background
    output_bytes = remove(img_bytes)
    output_img = Image.open(io.BytesIO(output_bytes)).convert('RGBA')
    
    return img, output_img
 

def create_bitmask_and_contours(rgba_image):
    """
    Create smoothed binary mask from RGBA image and extract contours
    
    Args:
        rgba_image (PIL.Image): RGBA image with transparent background
        
    Returns:
        tuple: (binary_mask, contours)
            - binary_mask (numpy.ndarray): Boolean array where True = foreground
            - contours (list): List of smoothed contour arrays
    """
    # Extract alpha channel
    alpha = np.array(rgba_image.split()[-1])
    
    # Apply Gaussian blur for smooth edges
    alpha_smoothed = filters.gaussian(alpha, sigma=1.5)
    
    # Create binary mask with adaptive thresholding
    threshold = filters.threshold_otsu(alpha_smoothed)
    binary_mask = alpha_smoothed > threshold
    
    # Apply morphological operations for smooth, clean edges
    binary_mask = morphology.binary_closing(binary_mask, morphology.disk(2))
    binary_mask = morphology.binary_opening(binary_mask, morphology.disk(2))
    
    # Additional smoothing pass
    binary_mask = morphology.binary_erosion(binary_mask, morphology.disk(1))
    binary_mask = morphology.binary_dilation(binary_mask, morphology.disk(3))
    
    # Extract smooth contours
    contours = measure.find_contours(binary_mask.astype(float), level=0.5)
    
    # Apply contour smoothing
    smoothed_contours = []
    for contour in contours:
        if len(contour) > 10:
            smooth_contour = np.column_stack([
                ndimage.gaussian_filter1d(contour[:, 0], sigma=1.0),
                ndimage.gaussian_filter1d(contour[:, 1], sigma=1.0)
            ])
            smoothed_contours.append(smooth_contour)
        else:
            smoothed_contours.append(contour)
    
    return binary_mask, smoothed_contours

# Example usage:
# rgba_image = Image.open("output/no_background.png")
# binary_mask, contours = create_bitmask_and_contours(rgba_image)
def convert_to_smoothed_vector(input_image, output_svg, canvas_size=(None, None), 
                             num_sampled_points=100, output_points=50, smoothing=1):
    """
    Convert an image to a smoothed vector SVG.
    
    Args:
        input_image (str or PIL.Image): Path to input image file or PIL Image object
        output_svg (str): Path for output SVG file
        canvas_size (tuple): Canvas size in pixels (width, height)
        num_sampled_points (int): Number of points to sample from original path
        output_points (int): Number of points in smoothed output
        smoothing (float): Smoothing parameter for spline (lower = tighter fit)
    """
    
    # Step 1: Handle input - either path or PIL Image
    if isinstance(input_image, str):
        img = Image.open(input_image)
    else:
        img = input_image
    
    img_array = np.array(img)
    
    # Invert colors
    if img_array.dtype == np.uint8:
        inverted_array = 255 - img_array
    else:
        inverted_array = np.iinfo(img_array.dtype).max - img_array
    
    inverted_img = Image.fromarray(inverted_array)
    
    # Save inverted image to temp file
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_png:
        temp_png_path = temp_png.name
        inverted_img.save(temp_png_path)
    
    # Create intermediate SVG
    with tempfile.NamedTemporaryFile(suffix='.svg', delete=False) as temp_svg:
        temp_svg_path = temp_svg.name
    
    try:
        # Convert to SVG
        vtracer.convert_image_to_svg_py(temp_png_path, temp_svg_path, colormode='binary')
        
        # Step 2: Smooth the vector
        # Load SVG paths
        paths, *_ = svg2paths(temp_svg_path)
        
        if not paths:
            raise ValueError("No paths found in the generated SVG")
        
        # Use the first path
        path = paths[0]
        
        # Sample points from the path
        points = np.array([path.point(t) for t in np.linspace(0, 1, num_sampled_points)])
        x = points.real
        y = points.imag
        
        # Smooth with spline
        tck, _ = splprep([x, y], s=smoothing)
        u_new = np.linspace(0, 1, output_points)
        x_smooth, y_smooth = splev(u_new, tck)
        smooth_points = np.column_stack((x_smooth, y_smooth))
        
        # Compute bounding box and center on canvas
        min_x, min_y = np.min(smooth_points, axis=0)
        max_x, max_y = np.max(smooth_points, axis=0)
        path_width = max_x - min_x
        path_height = max_y - min_y
        
        canvas_width, canvas_height = canvas_size
        translate_x = (canvas_width - path_width) / 2 - min_x
        translate_y = (canvas_height - path_height) / 2 - min_y
        
        smooth_points_centered = [(x + translate_x, y + translate_y) for x, y in smooth_points]
        
        # Construct path string with closed path
        d_str = f"M {smooth_points_centered[0][0]},{smooth_points_centered[0][1]} " + \
                " ".join(f"L {x},{y}" for x, y in smooth_points_centered[1:]) + " Z"
        
        # Create final SVG
        dwg = svgwrite.Drawing(output_svg, size=canvas_size)
        dwg.add(dwg.path(d=d_str, fill="black", stroke="none"))
        dwg.save()
        
        print(f"Smoothed vector saved to: {output_svg}")
        
    finally:
        # Cleanup temp files
        os.unlink(temp_png_path)
        if os.path.exists(temp_svg_path):
            os.unlink(temp_svg_path)

def visualize_results(original_img, binary_mask, contours, no_bg_img=None):
    """
    Visualize the processing results
    
    Args:
        original_img (PIL.Image): Original image
        binary_mask (numpy.ndarray): Binary mask
        contours (list): List of contours
        no_bg_img (PIL.Image, optional): Background-removed image
    """
    # Determine number of subplots
    num_plots = 4 if no_bg_img is not None else 3
    
    fig, axes = plt.subplots(1, num_plots, figsize=(15, 5))
    
    # Original image
    axes[0].imshow(original_img)
    axes[0].set_title('Original Image')
    axes[0].axis('off')
    
    plot_idx = 1
    
    # Background removed image (if provided)
    if no_bg_img is not None:
        axes[plot_idx].imshow(no_bg_img)
        axes[plot_idx].set_title('Background Removed')
        axes[plot_idx].axis('off')
        plot_idx += 1
    
    # Binary mask
    axes[plot_idx].imshow(binary_mask, cmap='gray')
    axes[plot_idx].set_title('Binary Mask')
    axes[plot_idx].axis('off')
    plot_idx += 1
    
    # Contours
    axes[plot_idx].imshow(binary_mask, cmap='gray', alpha=0.3)
    for contour in contours:
        axes[plot_idx].plot(contour[:, 1], contour[:, 0], 'r-', linewidth=2)
    axes[plot_idx].set_title(f'Contours ({len(contours)} found)')
    axes[plot_idx].axis('off')
    
    plt.tight_layout()
    plt.show()

def save_intermediate_results(no_bg_img, binary_mask, output_dir='output'):
    """
    Save intermediate processing results
    
    Args:
        no_bg_img (PIL.Image): Background-removed image
        binary_mask (numpy.ndarray): Binary mask
        output_dir (str): Directory to save results
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Save background-removed image
    no_bg_path = os.path.join(output_dir, 'no_background.png')
    no_bg_img.save(no_bg_path)
    print(f"Background-removed image saved to: {no_bg_path}")
    
    # Save binary mask
    mask_path = os.path.join(output_dir, 'binary_mask.png')
    mask_img = Image.fromarray((binary_mask * 255).astype(np.uint8))
    mask_img.save(mask_path)
    print(f"Binary mask saved to: {mask_path}")
    
    return no_bg_path, mask_path

def complete_image_to_vector_workflow(input_path, output_svg=None, output_dir='output',
                                    canvas_size=(None, None), num_sampled_points=50, 
                                    output_points=40, smoothing=1, visualize=True,
                                    save_intermediates=True):
    """
    Complete workflow: image -> background removal -> vectorization -> smoothing
    
    Args:
        input_path (str): Path to input image
        output_svg (str, optional): Path for output SVG. If None, uses input filename
        output_dir (str): Directory for output files
        canvas_size (tuple): Canvas size for final SVG
        num_sampled_points (int): Points to sample from vector path
        output_points (int): Points in smoothed output
        smoothing (float): Smoothing parameter
        visualize (bool): Whether to show visualization
        save_intermediates (bool): Whether to save intermediate results
        
    Returns:
        dict: Dictionary containing all results
    """
    
    print("🔄 Starting complete image-to-vector workflow...")
    
    # Step 1: Remove background
    print("📷 Step 1: Removing background...")
    original_img, no_bg_img = remove_background(input_path)
    print("✅ Background removal complete")
    
    # Step 2: Create bitmask and extract contours
    print("🎭 Step 2: Creating binary mask and extracting contours...")
    binary_mask, contours = create_bitmask_and_contours(no_bg_img)
    print(f"✅ Found {len(contours)} contours")
    
    # Step 3: Save intermediate results (optional)
    no_bg_path, mask_path = None, None
    if save_intermediates:
        print("💾 Step 3: Saving intermediate results...")
        no_bg_path, mask_path = save_intermediate_results(no_bg_img, binary_mask, output_dir)
    
    # Step 4: Convert to smoothed vector
    print("🎨 Step 4: Converting to smoothed vector...")
    if output_svg is None:
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        output_svg = os.path.join(output_dir, f"{base_name}_vector.svg")
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_svg), exist_ok=True)
    
    convert_to_smoothed_vector(
        mask_path, output_svg, canvas_size, 
        num_sampled_points, output_points, smoothing
    )
    print("✅ Vector conversion complete")
    
    # Step 5: Visualize results (optional)
    if visualize:
        print("📊 Step 5: Visualizing results...")
        visualize_results(original_img, binary_mask, contours, no_bg_img)
    
    print("🎉 Workflow complete!")
    
    # Return all results
    return {
        'original_img': original_img,
        'no_bg_img': no_bg_img,
        'binary_mask': binary_mask,
        'contours': contours,
        'output_svg': output_svg,
        'no_bg_path': no_bg_path,
        'mask_path': mask_path
    }


# 3d model generation
#----------------------------



# ==== Step 2: Count grid size based on DXF bounding box ====
def count_grid_cells_for_dxf(dxf_path, cell_size=45):
    doc = ezdxf.readfile(dxf_path)
    msp = doc.modelspace()
    units = doc.header.get('$INSUNITS', 0)
    print(f"INSUNITS value: {units}")
    points = []
    for entity in msp:
        if entity.dxftype() == 'LWPOLYLINE':
            points.extend([(point[0], point[1]) for point in entity.get_points()])
        elif entity.dxftype() == 'LINE':
            points.append((entity.dxf.start.x, entity.dxf.start.y))
            points.append((entity.dxf.end.x, entity.dxf.end.y))

    if not points:
        raise ValueError("No path points found in the DXF file.")

    xs, ys = zip(*points)
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    width = max_x - min_x
    height = max_y - min_y

    # INSUNITS=6 means mm, no conversion needed
    print(f"Bounding box (mm): width={width:.2f}, height={height:.2f}")

    columns = math.ceil(width / cell_size)
    rows = math.ceil(height / cell_size)

    return columns, rows, min_x, min_y, max_x, max_y

# TODO add extrude hight, extrude start, extruded offset
def stl_file_generator(svg_path,mm_to_px_scale_ratio=0.0,box_height=0.0):
   
    unit_size = 45  # mm grid cell size
    units = 6 # 
    box_height = 7*units  # 7mm per box units height source https://gridfinity.xyz/specification/
    bottom_layer_offset= 4.5+5 #4.5 is the base of the gridfinity, 5 is the bottom wall


    paths, _ = svg2paths(svg_path)
    doc = ezdxf.new(dxfversion='R2010')
    msp = doc.modelspace()

    for path in paths:
        for segment in path:
            start = segment.start
            end = segment.end
            # Scale SVG coords to mm here:
            start_point = (start.real * mm_to_px_scale_ratio, start.imag * mm_to_px_scale_ratio)
            end_point = (end.real * mm_to_px_scale_ratio, end.imag * mm_to_px_scale_ratio)
            msp.add_line(start_point, end_point)

    os.makedirs(os.path.dirname(dxf_path), exist_ok=True)
    doc.saveas(dxf_path)

    columns, rows, min_x, min_y, max_x, max_y = count_grid_cells_for_dxf(dxf_path, cell_size=unit_size)
    print(f"Grid size: {columns} columns x {rows} rows")

    
    
    

    # ==== Step 4: Import DXF, extrude upward, translate to center, offset Z by 5mm ====
    dxf_shape = (
        cq.importers.importDXF(dxf_path)
        .wires()
        .toPending()
        .extrude(box_height)
    )


    center_x = (min_x + max_x) / 2
    center_y = (min_y + max_y) / 2

    dxf_shape = dxf_shape.translate((-center_x, -center_y, bottom_layer_offset))
    # Center the box grid on XY=0
    # ==== Step 5: Intersect box and extruded DXF shape ====
    box = GridfinityBox(columns, rows, 5, solid=True, solid_ratio=0.8, verbose=True)
    r = box.render()
    result = r.cut(dxf_shape)

    # ==== Step 6: Export STL ====
    cq.exporters.export(result, stl_output_path)
    print(f"STL exported to: {stl_output_path}")


@app.errorhandler(413)
def request_entity_too_large(error):
    return 'Image you uploaded is to Large, try again with a file less than 50 mb, we recommend https://imageresizer.com', 413

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', download_url=None)

@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if croppedImage (base64) is provided
    data_url = request.form.get('croppedImage')
    mm_to_px_scale_ratio = request.form.get("mm_per_pixel")
    mm_to_px_scale_ratio = float(mm_to_px_scale_ratio)
    box_height = float(request.form.get("box_height"))
    if data_url:
        header, encoded = data_url.split(",", 1)
        image_data = base64.b64decode(encoded)
        image = Image.open(io.BytesIO(image_data))
        
        filename = "cropped_upload.png"
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(input_path)
    else:
        # Fallback to standard file upload
        file = request.files.get('file')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(input_path)
        else:
            return redirect('/')

    # === Run STL generation workflow ===
    base_name = os.path.splitext(os.path.basename(input_path))[0]
    dxf_path = os.path.join(OUTPUT_FOLDER, f"test4.dxf")
    stl_output_path = os.path.join(OUTPUT_FOLDER, f"test4.stl")

    with Image.open(input_path) as img:
        canvas_size = img.size

    results = complete_image_to_vector_workflow(
        input_path=input_path,
        output_dir=OUTPUT_FOLDER,
        canvas_size=canvas_size,
        num_sampled_points=100,
        output_points=50,
        smoothing=1,
        visualize=False,
        save_intermediates=True
    )

    output_svg = os.path.join(OUTPUT_FOLDER, f"{base_name}")
    stl_file_generator(f"{output_svg}_vector.svg",mm_to_px_scale_ratio,box_height)

    return render_template('index.html', download_url=url_for('static', filename="test4.stl"))
if __name__ == '__main__':
    app.run(debug=True)
