// Parameters with conditional defaults
svg_file = is_undef(svg_file) ? "C:/Users/oran/github/voidtray/output/test5_vector.svg" : svg_file;
extrude_height = is_undef(extrude_height) ? 5 : extrude_height;
svg_width = is_undef(svg_width) ? 100 : svg_width;
svg_height = is_undef(svg_height) ? 80 : svg_height;

linear_extrude(height = extrude_height)
    translate([-svg_width/2, -svg_height/2, 0])
       // scale([0.264583, 0.264583])
            import(file = svg_file);