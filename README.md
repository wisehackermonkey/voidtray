# voidtray
----
[![Open Source Love svg2](https://badges.frapsoft.com/os/v2/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


<!-- <img src="NNNNNN" width="400"> -->


<h2 align="center">____________________</h2>

<h4 align="center">________________________</h4>

---


# Installation
### 
```bash
cd ~
git clone https://github.com/wisehackermonkey/voidtray.git
cd voidtray
conda init powershell

conda create -n voidtray 
conda activate voidtray

conda install -c conda-forge scikit-image -y
python -c "import skimage; print(skimage.__version__)"

conda install -c conda-forge matplotlib -y


conda install -c conda-forge jupyterlab -y
# test jupyter
jupyter lab
```
# visit 
http://localhost:8888/lab
![alt text](image.png)
![alt text](image-1.png)

# enter the password on click the link
![alt text](image-2.png)



![alt text](image-3.png)

![alt text](image-4.png)

#sucess!
![alt text](image-5.png)



conda install -c conda-forge ipywidgets -y
partial success
![alt text](image-6.png)

![alt text](image-7.png)

# getting something. but i need a way to denoise

![alt text](image-8.png)

# different
![alt text](image-9.png)

# i think using a background removal tool will get my a huge way farther
conda install -c conda-forge rembg -y
![alt text](image-10.png)
# see how the tape that is white does a great job!


had to change from python 3.13 to 3.11 because rembg doesnt work on latest

conda install -c conda-forge jupyterlab ipywidgets matplotlib -y
 
pip install pillow "rembg[cpu,cli]" # for library + cli


rembg looks promising
![alt text](image-11.png)

# sucess!
![alt text](image-12.png)

# looks great!

![alt text](image-13.png)
# now on a spoon
![alt text](image-14.png)

# got a convex hull working!
![alt text](image-15.png)

# my mouse
![alt text](image-16.png)
# for two objects they are treated as one. need to fix
![alt text](image-17.png)
# works but has some weirness
![alt text](image-18.png)
# need to convert to vector

# kinda working but has edge width problems
![](image-19.png)
# got the line width down
![alt text](image-20.png)

# figured out how to fill in the contours
![alt text](image-21.png)

# need to make line more smooth
# got smoother but issues with blobbyness
![alt text](image-22.png)
changed some settings and got this. which is not bad

![alt text](image-24.png)

still bad output
![](image-25.png)
## im thinking now its the outline to svg causing the issues
![alt text](image-26.png)
hmm maybe not. the edge looks bad

# found a cool algo called 
# Ramer–Douglas–Peucker algorithm
[Ramer–Douglas–Peucker algorithm | EKbana ML Study Group](https://ekbanaml.github.io/remote%20sensing%20and%20satellite%20image%20processing/RDP_algorithm/)
![alt text](image-23.png)

# trying this approach
`pip install rdp`

results wernt that impressive 
and didnt solve my line width issue


# trying another achetcture approach
backend python
front end javascript. with the goal of the javascript and opencv.js to polygon cut out the shapes

pip install flask rembg pillow
python app.py
# got the polygon crop to work
![alt text](image-27.png)
# and the background remobal but the two combained is hard
![alt text](image-28.png)

# semi working crop
![alt text](image-29.png)
![alt text](image-30.png)


# cool wow factor stuff
![alt text](image-31.png)
https://openjscad.xyz/#


# cool color scheme doesnt work for arbitrary shapes
![alt text](image-32.png)
https://maker.js.org/playground/?script=Slot

great polygon crop demo
https://netplayer.gr/crop/

![alt text](image-33.png)


# razterizer
https://github.com/jankovicsandras/imagetracerjs?tab=readme-ov-file#examples
# Summary
### -  *[Installation](#Installation)*
<!-- ### -  *[Deveopment](#For-developers)* -->
<!-- ### -  *[Links](#Links)* -->
### -  *[Contributors](#Contributors)*
### -  *[License](#License)*


<!-- 
--------------
# Screenshots
- <img src="NNNNNN" width="400"> 
 

-------------- 
# Development
### 
```bash
```

# Deployment to surge.sh
### 
```bash
bash deploy_to_surge_sh.sh
```

---
# Links
###
-->

--------------
# Contributors

[![](https://contrib.rocks/image?repo=wisehackermonkey/voidtray)](https://github.com/wisehackermonkey/voidtray/graphs/contributors)

##### Made with [contributors-img](https://contrib.rocks).

--------------


# License

#### MIT © wisehackermonkey
<img src="https://upload.wikimedia.org/wikipedia/commons/archive/c/c0/20230603054722%21Osi_standard_logo.png" width="100">

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
```bash
by oran collins
github.com/wisehackermonkey
oranbusiness@gmail.com
20250716
```

#### [More of my Projects](https://github.com/wisehackermonkey/)