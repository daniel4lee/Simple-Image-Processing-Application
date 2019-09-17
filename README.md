# Simple-Image-Processing-Application

A practice of Nvlab summer school.

## Preview

![preview](https://i.imgur.com/eF12fsF.gif)

## Introduction

* __Histogram Equalization__: Create the histogram of grey scale value for image, then forming the table of correspounding cumulative distribution function. And, to generate the equalized image, we only need to subtitute the original gray scale value into the *general histogram equalization formula* as below.
![general histogram equalization formula](https://i.imgur.com/uAKEVap.png)
where cdf-min is the minimum non-zero value, M × N gives the image's number of pixels, and L is the number of grey levels used (in this case 256).


* Gamma Correction
* Image Inversion

## Installation

Download this project

```bash
git clone https://github.com/daniel4lee/Simple-Image-Processing-Application.git
```

Change directory to the root of the project

```bash
cd Simple-Image-Processing-Application/
```

Run with Python interpreter
```bash
python3 main.py
```

## Image

### Default Image Location

The default location is `/ImageData`. However it is also able to load files in other directories through dialog window.

### Support Image Format

The application could load image files with `*.png, *.tif, *.bmp, *jpg, and *.raw` extension.

## Dependencies

* [numpy](http://www.numpy.org/)

* [opencv-python](https://pypi.org/project/opencv-python/)

* [PyQt5](https://riverbankcomputing.com/software/pyqt/intro)

## Reference
* [__Wiki Histogram equalization__](https://en.wikipedia.org/wiki/Histogram_equalization)
