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

        self.Inver_btn = QPushButton("Image Inversion", self)
        self.Inver_btn.clicked.connect(self.inverse_function)
        layout.addWidget(self.Inver_btn, 1, 0, 1, 2)

        self.GC_btn = QPushButton("Gamma Correction", self)
        self.GC_degree = QSpinBox()
        self.GC_degree.setValue(2)
        self.GC_degree.setRange(0,100)

        self.Ori_btn = QPushButton("Original image", self)
        self.Ori_btn.clicked.connect(self.origin_function)
        layout.addWidget(self.Ori_btn, 3, 0, 1, 2)

        layout.addWidget(self.HE_btn, 0, 0, 1, 2)
        
        layout.addWidget(self.GC_btn, 2, 0, 1, 1)
        layout.addWidget(self.GC_degree, 2, 1, 1, 1)
        

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
        
        self.img = 255 - self.img
        self.show_function(self.img)

    def origin_function(self):
        if not self.original_flag:
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