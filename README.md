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