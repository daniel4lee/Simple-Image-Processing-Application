# Simple-Image-Processing-Application

A practice of Nvlab summer school.

## Preview

![preview](https://i.imgur.com/eF12fsF.gif)

## Introduction

* __Histogram Equalization__
  * __Overview__: This method is to improve the contrast of images by spreading the clustered intensities value over the whole range.
  
    ![](https://i.imgur.com/FMpJXSm.png)
    * __Steps__:
        1. Create the histogram of grey scale value for source image.
        2. Form the table of correspounding cumulative distribution function.
        3. Make transition by subtituting the original gray scale value into the *general histogram equalization formula* as below.

            ![](https://i.imgur.com/uAKEVap.png)
             > Note: cdf-min is the minimum non-zero value, M × N gives the image's number of pixels, and L is the number of grey levels used (in this case is 256).
    * __advantage__:
        1. Increases the global contrast of images (especially images have close contrast values).
        2. Intensities can be better distributed on the histogram (backgrounds and foregrounds are both bright or dark).
        3. It is a invertible operation.
        4. Computation is not big.
    * __disadvantage__:
        1. It is indiscriminat (may increase the contrast of background noise and decrease the usable signal).
* __Gamma Correction__
  * __Overview__: The corrections is to translate between eye's light sensitivity and the camera (twice the light to camera means twice the signial, however to eyes percieves as non-linear relationship).
    ![Eyes are more sensitive in dark tones than in bright tones](https://i.imgur.com/B5ubC1p.png=200x200)

    * __Definition__: *Vout = Vin^gamma* (*Vout* is the output luminance value and *Vin* is the input/actual luminance value)
    * __Gamma Workflow__:
        1. Image Gamma: This is applied whenever a captured image is converted into JPEG. Redistributing native camera tonal levels into more perceptually uniform one (eyes). Also, making the most efficient use of given bit depth.
        2. Display Gamma: This refers to compensate for file's gamma, ensuring the image isn't unrealistically brightened when displayed on screen.
        3. System Gamma: This represents the net effect of all gamma values applied to the image (ideally be close to gamma = 1).
        ![](https://i.imgur.com/UmyDFGD.png)
* __Image Inversion__
  * __Overview__: Colors are reversed into their respective complementary colors.
  * The formula is simple `F(X) = COLOR_MAX - COLOR X`.

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

* [Numpy](http://www.numpy.org/)

* [Opencv-Python](https://pypi.org/project/opencv-python/)

* [PyQt5](https://riverbankcomputing.com/software/pyqt/intro)

## Reflection

It has been about one year since I write the program last time. So, by doing the program, I not only learned the basic knowledge of image process but got familiar with coding. However, I think there still are many points which I can improve, such as coding style. I should keep on learning and refining my ability.

## Reference

* [__Wiki Histogram Equalization__](https://en.wikipedia.org/wiki/Histogram_equalization)
* [__Wiki Gamma Correction__](https://en.wikipedia.org/wiki/Gamma_correction)
* [__Cambridge in Color__](https://www.cambridgeincolour.com/tutorials/gamma-correction.htm)
