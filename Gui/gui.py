import math
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QCoreApplication, QObject, QRunnable, QThread, QThreadPool, pyqtSignal, pyqtSlot 
from PyQt5.QtGui import QIntValidator, QDoubleValidator, QPixmap
import sys
import os
from os.path import join, isfile

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
        """ self.setFixedSize(960, 800) # due to unfix image size"""
        self.center()
        self.setWindowTitle('HW1')
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
        # save related gui
        self.save_btn = QPushButton("Save", self)


    def open(self):
        # open image function
        datapath = os.path.realpath(os.path.join(os.getcwd(), "ImageData"))
        print(datapath)
        fname = QFileDialog.getOpenFileName(self, 'Open image', 
        datapath, "Image files (*.jpg *.png *.tif *.bmp *.raw)")
        imagePath = fname[0]
        pixmap = QPixmap(imagePath)
        self.image_label.setPixmap(QPixmap(pixmap))
        self.resize(pixmap.width(), pixmap.height())

    def center(self):
        # Place window in the center
        qr = self.frameGeometry()
        central_p = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(central_p)
        self.move(qr.topLeft())