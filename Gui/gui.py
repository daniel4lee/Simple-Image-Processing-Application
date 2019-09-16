import math

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QCoreApplication, QObject, QRunnable, QThread, QThreadPool, pyqtSignal, pyqtSlot 
from PyQt5.QtGui import QIntValidator, QDoubleValidator, QPixmap, QImage

import sys
import os
from os.path import join, isfile

import cv2 as cv

import numpy

class GuiRoot(QWidget):
    # Root of Gui
    def __init__(self):
        super().__init__()     
        self.ui_init()

    def ui_init(self):
        # Set window
        self.file_gui()
        self.process_image_gui()
        self.setFixedSize(1080, 560) # due to unfix image size
        self.center()
        self.setWindowTitle('Hw1')
        self.img = numpy.ndarray(())
        self.image_label = QLabel() # label for image display
        self.image_label.resize(960, 539)
        
        self.original_flag = False
        # control panel layout
        hbox = QHBoxLayout()
        vbox = QVBoxLayout()

        vbox.addWidget(self.file_qgroupbox)
        vbox.addWidget(self.process_qgroupbox)
        vbox.setStretchFactor(self.file_qgroupbox, 1)
        vbox.setStretchFactor(self.process_qgroupbox, 3)
        vbox.insertSpacing(-1, 280)
        hbox.addLayout(vbox)
        hbox.addWidget(self.image_label)
        hbox.setStretchFactor(self.image_label, 3)
        self.setLayout(hbox)
        self.show()

    def file_gui(self):
        self.file_qgroupbox = QGroupBox("File: ")
        layout = QGridLayout()

        # open image related gui
        self.open_image_btn = QPushButton("Open Image", self)
        self.open_image_btn.clicked.connect(self.open_function)

        # save current image related gui
        self.save_image_btn = QPushButton("Save Image", self)
        self.save_image_btn.clicked.connect(self.save_function)
        
        layout.addWidget(self.open_image_btn, 0, 0, 1, 1)
        layout.addWidget(self.save_image_btn, 0, 1, 1, 1)
        self.file_qgroupbox.setLayout(layout)
        
    def process_image_gui(self):
        self.process_qgroupbox = QGroupBox("Image Process: ")
        layout = QGridLayout()
        layout.setSpacing(50)
        # process image related gui
        self.HE_btn = QPushButton("Histogram Equalization", self)
        self.HE_btn.clicked.connect(self.histogram_equation_function)
        layout.addWidget(self.HE_btn, 0, 0, 1, 2)

        self.Inver_btn = QPushButton("Image Inversion", self)
        self.Inver_btn.clicked.connect(self.inverse_function)
        layout.addWidget(self.Inver_btn, 1, 0, 1, 2)

        self.GC_btn = QPushButton("Gamma Correction", self)
        self.GC_btn.clicked.connect(self.GC_function)
        self.GC_degree = QDoubleSpinBox()
        self.GC_degree.setDecimals(2)
        self.GC_degree.setValue(0.22)
        self.GC_degree.setRange(0,10)
        layout.addWidget(self.GC_btn, 2, 0, 1, 1)
        layout.addWidget(self.GC_degree, 2, 1, 1, 1)

        self.Ori_btn = QPushButton("Original image", self)
        self.Ori_btn.clicked.connect(self.origin_function)
        layout.addWidget(self.Ori_btn, 3, 0, 1, 2)        

        layout.setVerticalSpacing(0)
        layout.setHorizontalSpacing(0)
        self.process_qgroupbox.setLayout(layout)

    def open_function(self):
        # open image function
        datapath = os.path.realpath(os.path.join(os.getcwd(), "ImageData"))
        file_name = QFileDialog.getOpenFileName(self, 'Open image', 
        datapath, "Image files(*.jpg *.png *.tif *.bmp *.raw)")
        
        if file_name[0]:
            self.img = cv.imread(file_name[0], -1)
        
            if 'raw' in file_name[0]:
                # imread function is not support raw file
                self.img = numpy.fromfile(file_name[0], dtype=numpy.uint8)
                self.img = self.img.reshape(512, 512)
                self.img = numpy.stack((self.img,)*3, axis=-1)
            
            self.original_img = self.img
            self.original_flag = True
            self.show_function(self.img)

    def show_function(self, img):
        # get the size and channel of image
        height, width, channel = img.shape
        bytesPerLine = channel*width

        # turn image of opencv into Qimage
        qImg = QImage(img.data, width, height, bytesPerLine,
            QImage.Format_RGB888).rgbSwapped()
        # show Qimage on label
        self.image_label.setPixmap(QPixmap.fromImage(qImg))

    def save_function(self):
        # save current image function
        file_name = QFileDialog.getSaveFileName(
            self, 'Save Image', './save_img', 'Image files(*.png *.jpg *.tif *.raw *.bmp)')
        if file_name[0]:
            cv.imwrite(file_name[0], self.img)

    def inverse_function(self):
        # use 255(the largest value of color) to minus the current value
        # by doing so, the image become negative
        if self.original_flag:
            self.img = cv.cvtColor(self.img, cv.COLOR_BGR2GRAY)
            self.img = 255 - self.img
            self.img = numpy.stack((self.img,)*3, axis=-1)
            self.show_function(self.img)
    
    def histogram_equation_function(self):
        def transform_function(cdf, height, width):
            # wiki: https://tinyurl.com/yxjfwskj
            temp = numpy.zeros_like(self.img)
            cdf_min = numpy.amin(cdf)
            table = [0]*256
            for i in range(256):
                    table[i] = round(255 * (cdf[i] - cdf_min) 
                    / (height * width -cdf_min), 0)
            
            for i in range(height):
                for j in range(width):
                    self.img[i, j] = table[self.img[i, j]]
        if self.original_flag:
            self.img = cv.cvtColor(self.img, cv.COLOR_BGR2GRAY) # turn to gray scale
            height, width = self.img.shape

            histogram = [0]*256 # create the histogram
            for h in range(height):
                for w in range(width):
                    histogram[self.img[h, w]] += 1
        
            cdf = [0]*256 # calculate cumulative distribution function
            for i in range(len(histogram)):
                cdf[i] = sum(histogram[:i+1])
            cdf = numpy.array(cdf)
            '''
            transform = numpy.uint8(255 * cdf / height / width) #finding transfer function values
            temp = numpy.zeros_like(self.img)
            for h in range(height):
                for w in range(width):
                    temp[h, w] = transform[self.img[h, w]]
            '''
            transform_function(cdf, height, width)
            self.img = numpy.stack((self.img,)*3, axis=-1)
            self.show_function(self.img)
    def GC_function(self):
        # Gamma correction function
        if self.original_flag:
            a = float(self.GC_degree.value()) # Gamma value
            height, width, channel= self.img.shape 
            table =  [ [0]*256 for i in range(3)] # table could accerlate the computation

            for channel in range(3): 
                max_value = numpy.amax(self.img[:, :, channel])
                for index in range(256):
                    table[channel][index] = numpy.power(index / max_value, a) * max_value
                    # calculate correspounding value for the 0 ~ 255 shades

            for channel in range(3):
                for h in range(height):
                    for w in range(width):
                        self.img[h, w, channel] = table[channel][self.img[h, w, channel]]
                        # mapping the image by gamma correction table
            self.img = numpy.uint8(self.img)
            self.show_function(self.img)
    def origin_function(self):
        # return the original image 
        if not self.original_flag:
            # haven't open any image file
            pass
        else:
            self.img = self.original_img
            self.show_function(self.img)

    def center(self):
        # Place window in the center
        qr = self.frameGeometry()
        central_p = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(central_p)
        self.move(qr.topLeft())