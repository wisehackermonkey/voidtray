
import ezdxf
from svgpathtools import svg2paths
import os
import cadquery as cq
import math
import cadquery as cq
from cqgridfinity import *

# ==== CONFIGURATION ====

svg_path = r"C:\Users\oran\github\voidtray\output\cropped_upload_vector.svg"
dxf_path = r"C:\Users\oran\github\voidtray\output\shape.dxf"
stl_output_path = r"C:\Users\oran\github\voidtray\output\shape.stl"

unit_size = 45  # mm grid cell size
units = 6 # 
box_height = 7*units  # 7mm per box units height source https://gridfinity.xyz/specification/
bottom_layer_offset= 4.5+5 #4.5 is the base of the gridfinity, 5 is the bottom wall

# Assuming 96 DPI for your SVG
svg_to_mm_scale = 0.169802  # ~0.264583


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


# def stl_file_generator(svg_path):

paths, _ = svg2paths(svg_path)
doc = ezdxf.new(dxfversion='R2010')
msp = doc.modelspace()

for path in paths:
    for segment in path:
        start = segment.start
        end = segment.end
        # Scale SVG coords to mm here:
        start_point = (start.real * svg_to_mm_scale, start.imag * svg_to_mm_scale)
        end_point = (end.real * svg_to_mm_scale, end.imag * svg_to_mm_scale)
        msp.add_line(start_point, end_point)

os.makedirs(os.path.dirname(dxf_path), exist_ok=True)
doc.saveas(dxf_path)

columns, rows, min_x, min_y, max_x, max_y = count_grid_cells_for_dxf(dxf_path, cell_size=unit_size)
print(f"Grid size: {columns} columns x {rows} rows")

# ==== Step 3: Create grid box solid ====


 
# ==== Step 4: Import DXF, extrude upward, translate to center, offset Z by 5mm ====
dxf_shape = (
    cq.importers.importDXF(dxf_path)
    .wires()
    .toPending()
    .extrude(box_height)
)


center_x = (min_x + max_x) / 2
center_y = (min_y + max_y) / 2
# ==== Step 5: Intersect box and extruded DXF shape ====

dxf_shape = dxf_shape.translate((-center_x, -center_y, bottom_layer_offset))

box = GridfinityBox(columns, rows, 5, solid=True, solid_ratio=0.8, verbose=True)
r = box.render()
result = r.cut(dxf_shape)
cq.exporters.export(result, stl_output_path)

 
# ==== Step 6: Export STL ====
 print(f"STL exported to: {stl_output_path}")
# stl_file_generator(svg_path)