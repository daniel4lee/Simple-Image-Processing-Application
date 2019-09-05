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
        self.open_image()
        self.process_image()
        self.save_image()
        self.setFixedSize(960, 560) # due to unfix image size
        self.center()
        self.setWindowTitle('HW1')
        self.img = numpy.ndarray(())
        self.image_label = QLabel() # label for image display
        
        # control panel layout
        hbox = QHBoxLayout()
        vbox = QVBoxLayout()

        basic_hbox = QHBoxLayout()
        basic_hbox.addWidget(self.open_image_btn)
        basic_hbox.addWidget(self.save_btn)
        vbox.addLayout(basic_hbox)
        vbox.addWidget(self.HE_btn)
        vbox.addWidget(self.Inver_btn)
        GC_hbox =QHBoxLayout()
        GC_hbox.addWidget(self.GC_btn)
        GC_hbox.addWidget(self.GC_degree)
        vbox.addLayout(GC_hbox)
        vbox.addWidget(self.Ori_btn)
        hbox.addLayout(vbox)
        hbox.addWidget(self.image_label)
        self.setLayout(hbox)
        self.show()

    def open_image(self):
        # open image related gui
        self.open_image_btn = QPushButton("Open Image", self)
        self.open_image_btn.clicked.connect(self.open)
        
    def process_image(self):
        # process image related gui
        self.HE_btn = QPushButton("Histogram Equalization", self)
        self.Inver_btn = QPushButton("Image Inversion", self)
        self.GC_btn = QPushButton("Gamma Correction", self)
        self.GC_degree = QSpinBox()
        self.GC_degree.setValue(2)
        self.GC_degree.setRange(0,100)
        self.Ori_btn = QPushButton("Original image", self)

    def save_image(self):
        # save current image related gui
        self.save_btn = QPushButton("Save", self)
        self.save_btn.clicked.connect(self.save)

    def open(self):
        # open image function
        datapath = os.path.realpath(os.path.join(os.getcwd(), "ImageData"))
        file_name = QFileDialog.getOpenFileName(self, 'Open image', 
        datapath, "Image files(*.jpg *.png *.tif *.bmp *.raw)")
        
        self.img = cv.imread(file_name[0], -1)
        # get the size and channel of image, then turn image of opencv into Qimage
        if 'raw' in file_name[0]:
            # imread function is not support raw file
            self.img = numpy.fromfile(file_name[0], dtype=numpy.uint8)
            self.img = self.img.reshape(512, 512)
            self.img = numpy.stack((self.img,)*3, axis=-1)
        height, width, channel = self.img.shape
        bytesPerLine = channel*width

        self.qImg = QImage(self.img.data, width, height, bytesPerLine,
            QImage.Format_RGB888).rgbSwapped()

        # show Qimage on label
        self.image_label.setPixmap(QPixmap.fromImage(self.qImg))
    def save(self):
        # save current image function
        file_name = QFileDialog.getSaveFileName(
            self, 'Save Image', './save_img', 'Image files(*.png *.jpg *.tif *.raw *.bmp)')
        cv.imwrite(file_name[0], self.img)

    def center(self):
        # Place window in the center
        qr = self.frameGeometry()
        central_p = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(central_p)
        self.move(qr.topLeft())