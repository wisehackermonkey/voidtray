# how to image pipeline works.

#  look at pipe.ipynb
todo 
⦁	contour edge offset 3mm
⦁	find a tool for uploading images to your desktop from phone, with browser
- make pipeline
- how to run openscad CLI, or server

# flow of data
- adjust contrast (add instructions for user, dont put hands)
- remove background
- create bit mask
- vectorize (bit mask to svg)
- smooth and simplify the vector path (svg)
- save image with UUID name



options for image process:
- temp file
- in memory file
- actual file with UUID


# how to remove the image's shadows
- my first attempt
i liked the gamma correction the best
![1753294433074](image/README_IMAGE_PIPELINE/1753294433074.png)
# tried another method, also didnt work
![1753294716583](image/README_IMAGE_PIPELINE/1753294716583.png)
# all those were automated versions

![1753294858709](image/README_IMAGE_PIPELINE/1753294858709.png)
# kinda worked. but i want to adjust the bit mask

# after breaking out into affinty photo , looks like adjusting exposure does the biggest bang for buck at removing shadows
![1753296059914](image/README_IMAGE_PIPELINE/1753296059914.png)
# adjusting the exposer in python works great!
![1753296677486](image/README_IMAGE_PIPELINE/1753296677486.png)
# becomes much better mat, when the gamma is adjusted
![1753296708430](image/README_IMAGE_PIPELINE/1753296708430.png)


# heres the final output with the better mat
![1753296645312](image/README_IMAGE_PIPELINE/1753296645312.png)


# final inteface
- Remove shadows (gamma)
- Image Exposure (good for removing shadows)
- contrast (sometimes helpful)
- reset to original
- "Process image", "Save locally"