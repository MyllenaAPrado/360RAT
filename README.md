# <img src="./Images/360RAT_logo.png" alt="drawing" width="100"/> 360RAT: 360 - ROI Annotator Tool


![Image](./Images/PrincipalWindow.PNG?raw=true)

* 360RAT is a tool to annotate spatially regions of interest (ROIs) in omnidirectional videos.
* It was developed using [Equirectangular-toolbox](https://github.com/NitishMutha/equirectangular-toolbox), [OpenCV](https://pypi.org/project/opencv-python/), [PyQt5 5.15.4](https://pypi.org/project/PyQt5/), and [python 3.9.5](https://www.python.org/).

* If you use this software in your project, please site the repository:

       @software{360RAT,
       author = {Myllena Prado, Lucas Althoff, and Mylène Farias},
       title = {360RAT: 360 - ROI Annotator Tool},
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

* [Pillow](https://pypi.org/project/Pillow/)

       pip install Pillow
       
# Instructions

Below are isntructions to download and use the software. 

## Download and Install:

- Download the software from this gihub;

- After installing, go to program folder:

       `cd 360RAT`

- Execute the program:

       `python .\360RAT.py`

## Virtual Machine:

1. Dowloand the virtual machine from : [Link to dowload](https://unbbr-my.sharepoint.com/:u:/g/personal/150081197_aluno_unb_br/EWV6dV8g0gRPtMPnkp0_gegBQSGS0vAuDzrFft6N1N-f6g?e=C3jEef)

2. Upload the file on virtual box ([link to help upload a .ova file on virtual box](https://www.alphr.com/ova-virtualbox/))

3. Start the Virtual Machine.

4. Enter

   User: IEUser
   
   password: Passw0rd!

5. Open powerShell

6. Go to directory of program with the command:

       `cd C:\Users\IEUser\Desktop\360rat`

7. Execute the program:
       
       `python .\360RAT.py`
       
## Video Tutorial on "How to annotate a video":

- Video: https://youtu.be/YWhyuafnATI

## Output:

The software outputs a folder with :

- Annotated frames;
- Black frames with ROIs shown in white;
- Video frames with annotated ROIs drawn over original content;
- CSV file with annotation data. This file can be used to later edit a video annotation. This CSV has the follow fields:

|        Field       |                                     Description                                     | Options                                                                                                                                                     |
|:------------------:|:----------------------------------------------------------------------------:|-------------------------------------------------------------------------------------------------------------------------------------------------------------|
|        Type        |                                       Represent the type os ROI saved in csv | 0 - Representing that row is a "Single ROI".  1- Representing one ROI which is part of "compose ROI".  2 - Representing that row is a complete "compose ROI" |
|        Frame       |                                              frame position during the video | Number from 0 to total frame of video                                                                                                                       |
|       ID ROI       | ID of ROI. The count of ID is independent to "single ROI" and "compose ROI". | Number bagin on 0 and increase 1 with each new ROI annotated.                                                                                               |
|   Center_point X   |     X coordinate in the picture frame corresponding to the center of the ROI | Ranging from 0 to 1. Representing the center of "single ROI" or the first ROI of "compose ROI"                                                              |
|   Center_point Y   |     Y coordinate in the picture frame corresponding to the center of the ROI | Ranging from 0 to 1. Representing the center of "single ROI" or the first ROI of "compose ROI"                                                              |
| ROI H              | Horizontal ROI scale                                                         | Ranging from 0 to 1.                                                                                                                                        |
| ROI W              | Vertical ROI scale                                                           | Ranging from 0 to 1.                                                                                                                                        |
| Label              | Semantic classification of the ROI                                           | See file Save_windows.py                                                                                                                                    |
| Movement           | Movement of ROI along the frame and video.                                   | “True” when the ROI is declared to be moving across the frames, “False” when it is declared as static, “*” for the“single ROI”                              |
| Frame_end          | Frame position during the video                                              | Id of frame for type=2. ( Only present for type =2, otherwise equal 0)                                                                                      |
| Center_point_end X |    𝑥 coordinate in the picture frame corresponding to the center of the ROI  | Ranging from 0 to 1.(Only present for type =2 otherwise equal 0.)                                                                                           |
| Center_point_end Y | 𝑦 coordinate in the picture frame corresponding to the center of the ROI     | Ranging from 0 to 1. (Only present for type =2 otherwise equal 0)                                                                                           |
| ROI H              | Horizontal ROI scale                                                         | Ranging from 0 to 1. (Only present for type =2 otherwise equal 0)|
| ROI W              | Vertical ROI scale                                                           | Ranging from 0 to 1.(Only present for type =2 otherwise equal 0) |

# Tips 

To decrease the fps or cut the videos you can use [FFMPEG 4.4](https://www.ffmpeg.org/download.html)

Full release : https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-full.7z

* Change the fps:

       ffmpeg -i <input> -filter:v fps=30 <output>

* Cut the video:

       ffmpeg -ss 00:01:00 -i input.mp4 -to 00:02:00 -c copy output.mp4

* Change the resolution:

       ffmpeg -i input.mp4 -vf scale=480:320 output_320.mp4
