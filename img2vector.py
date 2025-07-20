# input_png = "test/images/output_example_1.png"  # Change this to your PNG file path
# output_svg = "test/images/inverted_output.svg" 

# # open image 
# # invert the colors uisng numpy or scikit image
# # save in temp file
# # send temp file to convert_image_to_svg_py
# import vtracer
# vtracer.convert_image_to_svg_py(input_png, output_svg, colormode='binary')

# take in vector bitmask and smooth the edge and make the line super clean
# open image
# 
# input_png = "test/images/output_example_1.png"  # Change this to your PNG file path
# output_svg = "test/images/inverted_output.svg" 

# 

import numpy as np
from PIL import Image
import tempfile
import os
import vtracer

def convert_to_vector(input_image,output_svg):
    # open image 
    img = Image.open(input_png)

    # convert to numpy array for inversion
    img_array = np.array(img)

    # invert colors using numpy - subtract from max value (255 for 8-bit)
    if img_array.dtype == np.uint8:
        inverted_array = 255 - img_array
    else:
        inverted_array = np.iinfo(img_array.dtype).max - img_array

    # convert back to PIL Image
    inverted_img = Image.fromarray(inverted_array)

    # save in temp file
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
        temp_png_path = temp_file.name
        inverted_img.save(temp_png_path)

    # send temp file to convert_image_to_svg_py
    vtracer.convert_image_to_svg_py(temp_png_path, output_svg, colormode='binary')

    # cleanup temp file
    os.unlink(temp_png_path)

input_png = "test/images/output_example_2.png"  # Change this to your PNG file path
output_svg = "test/images/inverted_output.svg" 


convert_to_vector(input_png,output_svg)

# using scikit image add the Savitzky–Golay Filter 
# save the output as inverted_output_savitzky_golay.svg