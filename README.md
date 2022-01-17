# <img src="./Images/360RAT_logo.png" alt="drawing" width="100"/> 360RAT - 360 - ROI Annotator Tool


![Image](./Images/PrincipalWindow.PNG?raw=true)

* Tool to annotate spatially regions of interest for omnidirectional visual data in EPR.
* Developed using [Equirectangular-toolbox](https://github.com/NitishMutha/equirectangular-toolbox), [OpenCV](https://pypi.org/project/opencv-python/), [PyQt5 5.15.4](https://pypi.org/project/PyQt5/), and [python 3.9.5](https://www.python.org/).

* If you use this software in your project, please site the repository:

       @software{360RAT,
       author = {Mylène Farias, Myllena Prado and Lucas Althoff},
       title = {360RAT - 360 - ROI Annotator Tool},
       url = {https://gitlab.com/gpds-unb/360rat},
       version = {0.1.0},
       year = {2021},
       }

# Requisites

* [Python 3.9.5](https://www.python.org/)

* [Pip 21.2.4](https://pypi.org/project/pip/)

  (Install pip together with python.)

* [OpenCV 4.5.2](https://pypi.org/project/opencv-python/)

       pip install opencv-python-headless
       
* [PyQt5 5.15.4](https://pypi.org/project/PyQt5/)

       pip install PyQt5
       
* [Matplotlib](https://matplotlib.org/stable/users/installing.html)

       pip install -U matplotlib

* [Numpy](https://numpy.org/install/)

       pip install numpy


       
# TIP

To decrease the fps or cut the videos you can use [FFMPEG 4.4](https://www.ffmpeg.org/download.html)

Full release : https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-full.7z

* Change the fps:

       ffmpeg -i <input> -filter:v fps=30 <output>

* Cut the video:

       ffmpeg -ss 00:01:00 -i input.mp4 -to 00:02:00 -c copy output.mp4

* Change the resolution:

       ffmpeg -i input.mp4 -vf scale=480:320 output_320.mp4


# Use operation

`cd 360RAT`


`python .\360RAT.py`

