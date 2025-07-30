# import cadquery as cq
# import ezdxf
# import os
# import math
# from svgpathtools import svg2paths

# # ==== CONFIGURATION ====
# svg_path = r"C:\Users\oran\github\voidtray\output\test5_vector.svg"
# dxf_path = r"C:\Users\oran\github\voidtray\output\shape.dxf"
# stl_output_path = r"C:\Users\oran\github\voidtray\output\shape.stl"

# unit_size = 45  # mm (grid cell width and length)
# box_height = 30  # mm (30 cm box height)
# extrude_height = 30  # mm extrusion height upward
# extrude_start_z = 5  # mm starting 5mm above zero
# # === Function to count grid cells to fit DXF bounding box ===
# def count_grid_cells_for_dxf(dxf_path, cell_size=45):
#     doc = ezdxf.readfile(dxf_path)
#     msp = doc.modelspace()

#     points = []

#     for entity in msp:
#         if entity.dxftype() == 'LWPOLYLINE':
#             points.extend([(point[0], point[1]) for point in entity.get_points()])
#         elif entity.dxftype() == 'LINE':
#             points.append((entity.dxf.start.x, entity.dxf.start.y))
#             points.append((entity.dxf.end.x, entity.dxf.end.y))

#     if not points:
#         raise ValueError("No path points found in the DXF file.")

#     xs, ys = zip(*points)
#     min_x, max_x = min(xs), max(xs)
#     min_y, max_y = min(ys), max(ys)

#     width = max_x - min_x
#     height = max_y - min_y

#     columns = math.ceil(width / cell_size)
#     rows = math.ceil(height / cell_size)

#     return columns, rows, min_x, min_y, max_x, max_y

# # ==== STEP 1: SVG to DXF ====
# paths, _ = svg2paths(svg_path)
# doc = ezdxf.new(dxfversion='R2010')
# msp = doc.modelspace()

# for path in paths:
#     for segment in path:
#         start = segment.start
#         end = segment.end
#         msp.add_line((start.real, start.imag), (end.real, end.imag))

# os.makedirs(os.path.dirname(dxf_path), exist_ok=True)
# doc.saveas(dxf_path)

# # ==== STEP 2: Count columns and rows ====
# columns, rows, min_x, min_y, max_x, max_y = count_grid_cells_for_dxf(dxf_path, cell_size=unit_size)
# print(f"Grid size: {columns} columns x {rows} rows")

# # ==== STEP 3: Create grid box solid ====
# grid_width = columns * unit_size
# grid_height = rows * unit_size

# box = cq.Workplane("XY")

# for col in range(columns):
#     for row in range(rows):
#         box = box.union(
#             cq.Workplane("XY")
#             .box(unit_size, unit_size, box_height)
#             .translate((
#                 col * unit_size + unit_size / 2,
#                 row * unit_size + unit_size / 2,
#                 box_height / 2  # center the box height-wise starting from 0
#             ))
#         )

# # Center the grid box on XY=0, Z base at 0
# box = box.translate((-grid_width/2, -grid_height/2, 0))

# # ==== STEP 4: Import DXF, extrude upward starting at Z=5mm ====
# dxf_shape = (
#     cq.importers.importDXF(dxf_path)
#     .wires()
#     .toPending()
#     .extrude(extrude_height)  # extrude UP by 300 mm
# )

# # Translate DXF path so base is at Z=5mm, and centered in XY
# center_x = (min_x + max_x) / 2
# center_y = (min_y + max_y) / 2

# dxf_shape = dxf_shape.translate((-center_x, -center_y, extrude_start_z))

# # ==== STEP 5: Intersect extruded DXF with box grid ====
# result = box.cut(dxf_shape)


# # ==== STEP 6: Export result to STL ====
# # cq.exporters.export(result, stl_output_path)
# # print(f"STL exported to: {stl_output_path}")

import cadquery as cq
import ezdxf
import os
import math
from svgpathtools import svg2paths

# ==== CONFIGURATION ====
svg_path = r"C:\Users\oran\github\voidtray\output\test5_vector.svg"
dxf_path = r"C:\Users\oran\github\voidtray\output\shape.dxf"
stl_output_path = r"C:\Users\oran\github\voidtray\output\shape.stl"

unit_size = 45    # mm (grid cell width and length)
box_height = 300  # mm (30 cm box height)
extrude_height = 300  # mm extrusion height upward
extrude_start_z = 5   # mm starting 5mm above zero

# === Map DXF INSUNITS to mm scale factor ===
units_to_mm = {
    0: 1,       # unitless - assume mm
    1: 25.4,    # inches to mm
    2: 304.8,   # feet to mm
    3: 1609344, # miles to mm (unlikely)
    4: 1000,    # meters to mm
    5: 1,       # millimeters to mm
    6: 10,      # centimeters to mm
}

# === Function to count grid cells to fit DXF bounding box ===
def count_grid_cells_for_dxf(dxf_path, cell_size=45):
    doc = ezdxf.readfile(dxf_path)
    doc.header['$INSUNITS'] = 6
    units = doc.header.get('$INSUNITS', 0)
    scale_factor = units_to_mm.get(units, 6)

    msp = doc.modelspace()
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

    width = (max_x - min_x) / scale_factor
    height = (max_y - min_y) / scale_factor

    columns = math.ceil(width / cell_size)
    rows = math.ceil(height / cell_size)

    print(f"DXF units (INSUNITS): {units}, scaling by {scale_factor} to mm")
    print(f"Bounding box width (mm): {width}, height (mm): {height}")
    print(f"Grid size: {columns} columns x {rows} rows")

    return columns, rows, min_x, min_y, max_x, max_y, scale_factor

# ==== STEP 1: SVG to DXF ====
paths, _ = svg2paths(svg_path)
doc = ezdxf.new(dxfversion='R2010')
msp = doc.modelspace()

for path in paths:
    for segment in path:
        start = segment.start
        end = segment.end
        msp.add_line((start.real, start.imag), (end.real, end.imag))

os.makedirs(os.path.dirname(dxf_path), exist_ok=True)
doc.saveas(dxf_path)

# ==== STEP 2: Count columns and rows, get scale factor ====
columns, rows, min_x, min_y, max_x, max_y, scale_factor = count_grid_cells_for_dxf(dxf_path, cell_size=unit_size)

# ==== STEP 3: Create grid box solid ====
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
                box_height / 2  # center box height starting at 0
            ))
        )

# Center grid box on XY=0, base Z=0
box = box.translate((-grid_width / 2, -grid_height / 2, 0))

# ==== STEP 4: Import DXF, scale and extrude upward starting at Z=5mm ====
dxf_shape = (
    cq.importers.importDXF(dxf_path)
    .wires()
    .toPending()
    .extrude(extrude_height)  # extrude UP by 300 mm
)
   

# Translate DXF shape to center on XY=0 and start at Z=5
center_x = ((min_x + max_x) / 2) / scale_factor
center_y = ((min_y + max_y) / 2) / scale_factor
dxf_shape = dxf_shape.translate((-center_x, -center_y, extrude_start_z))

# ==== STEP 5: Cut extruded DXF shape out of grid box ====
result = box.cut(dxf_shape)

# ==== STEP 6: Export to STL ====
cq.exporters.export(result, stl_output_path)
print(f"STL exported to: {stl_output_path}")
