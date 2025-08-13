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
install mini conda (linux)

wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
conda create python=3.10 voidtray

conda create -n voidtray python=3.10
conda activate voidtray

pip3 install "rembg[cpu,cli]" cadquery numpy vtracer ezdxf Flask svgpathtools  matplotlib svgwrite pillow scikit-image cqgridfinity cqkit
pip3 install gunicorn
waitress-serve --host=0.0.0.0 --port=80 server:app
gunicorn -w 4 -b 0.0.0.0:80 server:app

pip install waitress


conda install -c conda-forge scikit-image -y
python -c "import skimage; print(skimage.__version__)"

conda install -c conda-forge matplotlib -y


conda install -c conda-forge jupyterlab -y
# test jupyter
jupyter lab
```



```
sudo nano /etc/systemd/system/voidtray.service

[Unit]
Description=VoidTray Flask Application
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/github/voidtray
Environment=PATH=/home/anaconda/anaconda3/envs/voidtray/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
ExecStart=/home/anaconda/anaconda3/envs/voidtray/bin/waitress-serve --host=0.0.0.0 --port=80 server:app
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target



# Reload systemd configuration
sudo systemctl daemon-reload

# Enable service to start on boot
sudo systemctl enable voidtray.service

# Start the service now
sudo systemctl start voidtray.service

# Check if it's running
sudo systemctl status voidtray.service
sudo journalctl -u voidtray.service -f



# Stop and start to test auto-restart
sudo systemctl stop voidtray.service
sudo systemctl start voidtray.service

# Or restart
sudo systemctl restart voidtray.service
```
```
conda activate voidtray
cd github/voidtray
mkdir static
python server.py

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

# 20250720
tring out pottrace for my bitmask image to vector convertion 
https://pythonhosted.org/pypotrace/tutorial.html
![1753038676613](image/README/1753038676613.png)
pip install pypotrace
doesnt support python 3.11.3 cry
sometimes i picking the correct python version is a black art ARRRG
![1753038993274](image/README/1753038993274.png)

conda create -n bgremove3_9
conda install -c conda-forge pypotrace numpy 

darn potrace and rembg have version conflict
![1753039150452](image/README/1753039150452.png)
https://github.com/danielgatis/rembg


pip install vtracer
![1753039594907](image/README/1753039594907.png)


# successfully made a vector path!
![1753041610699](image/README/1753041610699.png)

i had to invert the vector first
![1753041641307](image/README/1753041641307.png)

# trying a another smoothing way

pip install svgpathtools
![1753042774733](image/README/1753042774733.png)

# super smoonth
 but not centered
 ![1753043033174](image/README/1753043033174.png)
 # best one yet.
 ![1753043092315](image/README/1753043092315.png)
 # too many points
![1753043277448](image/README/1753043277448.png)

 # i downsampled it but it looks kinda shit
 ![1753043264148](image/README/1753043264148.png)
 # much much easier to fix !
 ![1753043340500](image/README/1753043340500.png)
 
 # i have all the major pieces together for the image pipeline
# heres the code structure i like

```python
from dataclasses import dataclass

@dataclass
class Processor:
    image: any

    def gray(self):
        self.image = np.mean(self.image, axis=2)
        return self

    def binary(self, t=128):
        self.image = self.image > t
        return self

    def out(self):
        return self.image

img = Processor(imageio.imread("img.jpg")).gray().binary().out()

```

# more full example
```python
from dataclasses import dataclass
import tempfile
from pathlib import Path
import shutil
# random image name with uuid
@dataclass
class ImagePipeline:
    original_path: Path
    temp_dir: Path = tempfile.mkdtemp()
    current_path: Path = None

    def open_image(self):
        # Load original image and save to temp
        # self.current_path = Path(self.temp_dir) / "step_open.png"
        # ...
        return self

    def remove_background(self, alpha_thresh: int = 128):
        # Use self.current_path -> write new temp file
        # self.current_path = Path(self.temp_dir) / "step_bg_removed.png"
        # ...
        return self

    def create_tool_contour(self, level: float = 0.5):
        # self.current_path = Path(self.temp_dir) / "step_contour.png"
        # ...
        return self

    def bitmask_to_svg(self, **vtracer_options):
        # self.current_path = Path(self.temp_dir) / "step_vector.svg"
        # ...
        return self

    def smooth_vector(self, smoothing: float = 0.1):
        # self.current_path = Path(self.temp_dir) / "step_smoothed.svg"
        # ...
        return self

    def save(self, output_path: Path):
        # shutil.copy(self.current_path, output_path)
        return self

    def cleanup(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

# Example usage
if __name__ == "__main__":
    result = (
        ImagePipeline(Path("input.jpg"))
        .open_image()
        .remove_background(alpha_thresh=128)
        .create_tool_contour(level=0.5)
        .bitmask_to_svg()
        .smooth_vector(smoothing=0.1)
        .save(Path("output.svg"))
    )

```

# the scan worked really well!
![1753044729031](image/README/1753044729031.png)
```javascript
// Parameters
svg_file = "C:\Users\oran\github\voidtray\test\images\smoothed_output.svg";  // Path to your SVG file
extrude_height = 5;        // Height in mm to extrude

linear_extrude(height = extrude_height)
    scale([0.264583, 0.264583])  // scale from px to mm (1 px ≈ 0.264583 mm at 96 DPI)
        import(file = svg_file);

```

tutorial
https://en.wikibooks.org/wiki/OpenSCAD_Tutorial/Chapter_1



# got a demo working for the gridfinity base with a soild inside

![1753046607515](image/README/1753046607515.png)

# got the cut to work
![1753047266253](image/README/1753047266253.png)

kinda working with the cut out
![1753048488559](image/README/1753048488559.png)
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

How to create a customized systemd so the server is built proof using a prompt

# colect this information first
### run the following code within your server
```
pwd;conda info --envs;which python
```
# copy the code to the following prompt:
```bash
act as a linux admin: 

create systemd file for my flask python server using waitresss

main file: <NAME_OF_YOURMAIN_FILE>.py
heres info about my system: 
output of the following commands in my project dir

```
pwd;conda info --envs;which python
```

output:

```
<COMMAND_OUTPUT_HERE>
```


create a systemd file
and simple and short instructions on how to setup
use nano as the editor
```

# create a systemd file
### note
```
sudo nano /etc/systemd/system/voidtray.service
``` 
# copy the output to this 