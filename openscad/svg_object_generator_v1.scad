// Parameters
svg_file = "C:/Users/oran/github/voidtray/test/images/smoothed_output.svg";
extrude_height = 5;

// Known SVG dimensions in mm (after scaling from px to mm)
svg_width = 100;  
svg_height = 80;

linear_extrude(height = extrude_height)
    translate([-svg_width/2, -svg_height/2, 0])
        scale([0.264583, 0.264583])
            import(file = svg_file);
