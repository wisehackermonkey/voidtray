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

# found out that i wasnt smoothing the binary mask enought, and caused shitty edges
![1753903283617](image/README_IMAGE_PIPELINE/1753903283617.png)

# output looks great
from
![1753903345365](image/README_IMAGE_PIPELINE/1753903345365.png)
to
![1753903322126](image/README_IMAGE_PIPELINE/1753903322126.png)

# getting the smoothing for the bitmask working

![1753904083515](image/README_IMAGE_PIPELINE/1753904083515.png)

# the binary mask looks great now!
![1753904287777](image/README_IMAGE_PIPELINE/1753904287777.png)
![1753904391458](image/README_IMAGE_PIPELINE/1753904391458.png)
# but the vector output is shit
![1753904595096](image/README_IMAGE_PIPELINE/1753904595096.png)
# turns out it was a simple path not being passed issue! omg whyhahah
![1753904823336](image/README_IMAGE_PIPELINE/1753904823336.png)
### seems to work with my two example images
# works faily good with openscad!
![1753905004016](image/README_IMAGE_PIPELINE/1753905004016.png)

# got the open scad to work from CLI
![1753905649412](image/README_IMAGE_PIPELINE/1753905649412.png)


# trying out cadquery for python as a alternative or openscad

![1753907880905](image/README_IMAGE_PIPELINE/1753907880905.png)
`conda install -c conda-forge cadquery`
# got it working in cad  query,
![1753909689507](image/README_IMAGE_PIPELINE/1753909689507.png)

# wow that did 80% of what i wanted! cool. i like that fact that its all python and not mixing
![1753911650200](image/README_IMAGE_PIPELINE/1753911650200.png)
# first 3d model cut from a svg!
![1753912112847](image/README_IMAGE_PIPELINE/1753912112847.png)
# works with the spoon
but having issues with scaling
![1753912906582](image/README_IMAGE_PIPELINE/1753912906582.png)

still issues with scale but bettter
![1753914654287](image/README_IMAGE_PIPELINE/1753914654287.png)

# turns out it was the svg import god that was way harder than expected
![1753915967298](image/README_IMAGE_PIPELINE/1753915967298.png)

# thats looking pretty good!
![1753916702470](image/README_IMAGE_PIPELINE/1753916702470.png)
# got the full chain working!
![1753918910871](image/README_IMAGE_PIPELINE/1753918910871.png)
![1753918886650](image/README_IMAGE_PIPELINE/1753918886650.png)

# web ui
![1753919507683](image/README_IMAGE_PIPELINE/1753919507683.png)

![1753919508253](image/README_IMAGE_PIPELINE/1753919508253.png)

# added a kickass crop interface
![1753922470533](image/README_IMAGE_PIPELINE/1753922470533.png)

# working on the ui for pixel to mm ratio

# here's the v1
![1754012580991](image/README_IMAGE_PIPELINE/1754012580991.png)

# first try dimentional accuracy

![1754013054858](image/README_IMAGE_PIPELINE/1754013054858.png)
# suppried it wasnt crazy off!
### 91.24mm vs the actual 85.6 mm!

# final inteface
- Remove shadows (gamma)
- Image Exposure (good for removing shadows)
- contrast (sometimes helpful)
- reset to original
- "Process image", "Save locally"