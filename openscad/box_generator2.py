
import ezdxf
from svgpathtools import svg2paths
import os
import cadquery as cq
import math

# ==== CONFIGURATION ====
svg_path = r"C:\Users\oran\github\voidtray\output\test4_vector.svg"
dxf_path = r"C:\Users\oran\github\voidtray\output\shape.dxf"
stl_output_path = r"C:\Users\oran\github\voidtray\output\shape.stl"

unit_size = 45  # mm grid cell size
box_height = 90  # mm box height (30cm)
extrude_height = box_height+5  # mm extrusion height upward
extrude_start_z = 30  # mm extrusion start height
bottom_layer_offset= 5

# Assuming 96 DPI for your SVG
svg_to_mm_scale = 25.4 / 96  # ~0.264583

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

columns, rows, min_x, min_y, max_x, max_y = count_grid_cells_for_dxf(dxf_path, cell_size=unit_size)
print(f"Grid size: {columns} columns x {rows} rows")

# ==== Step 3: Create grid box solid ====
grid_width = columns * unit_size
grid_height = rows * unit_size

box = cq.Workplane("XY")

for col in range(columns):
    for row in range(rows):
        box = box.union(
            cq.Workplane("XY")
            .box(unit_size, unit_size, box_height)
            .translate((
                col * unit_size + unit_size / 2,
                row * unit_size + unit_size / 2,
                box_height / 2
            ))
        )

# Center the box grid on XY=0
box = box.translate((-grid_width/2, -grid_height/2, 0))

# ==== Step 4: Import DXF, extrude upward, translate to center, offset Z by 5mm ====
dxf_shape = (
    cq.importers.importDXF(dxf_path)
    .wires()
    .toPending()
    .extrude(extrude_height)
)


center_x = (min_x + max_x) / 2
center_y = (min_y + max_y) / 2

dxf_shape = dxf_shape.translate((-center_x, -center_y, bottom_layer_offset))

# ==== Step 5: Intersect box and extruded DXF shape ====
result = box.cut(dxf_shape)

# ==== Step 6: Export STL ====
cq.exporters.export(result, stl_output_path)
print(f"STL exported to: {stl_output_path}")
