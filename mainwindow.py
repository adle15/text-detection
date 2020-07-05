import sys
import numpy as np

import cv2
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow
from PyQt5.uic import loadUi


class tehseencode(QDialog):
    def __init__(self):
        super(tehseencode, self).__init__()
        # loadUi("mainwindow.ui",self)
        loadUi("mainwindow.ui", self)

        self.title = "Plate Number Recognition Prototype"


        self.logic = 0
        self.value = 1
        self.Connect.clicked.connect(self.onClicked)
        self.TEXT.setText("Kindly Press 'Connect' to connect with webcam.")
        self.Capture.clicked.connect(self.CaptureClicked)
        self.setWindowIcon(QtGui.QIcon('logo.png'))
        self.setWindowTitle(self.title)
        self.show()


    @pyqtSlot()
    def onClicked(self):
        self.TEXT.setText('Kindly Press "Capture Image " to Capture image')
        cap = cv2.VideoCapture(0)
        # while (True):
        # print(cap.read())
        while (cap.isOpened()):
            ret, frame = cap.read()

            if ret == True:
                print('here')
                self.displayImage(frame, 1)
                cv2.waitKey()
                if (self.logic == 2):
                    self.value = self.value + 1
                    cv2.imwrite('C:/Users/sltnaldo/Pictures/Saved Pictures/%s.png' % (self.value), frame)
                    self.logic = 1
                    self.TEXT.setText('your Image have been Saved')
            else:
                print('not found')
        cap.release()
        cv2.destroyAllWindows()

    def CaptureClicked(self):
        self.logic = 2

    def displayImage(self, img, window=1):
        qformat = QImage.Format_Indexed8
        if len(img.shape) == 3:
            if (img.shape[2]) == 4:
                qformat = QImage.Format_RGBA888
            else:
                qformat = QImage.Format_RGB888
        img = QImage(img, img.shape[1], img.shape[0], qformat)
        img = img.rgbSwapped()
        self.imgLabel.setPixmap(QPixmap.fromImage(img))
        self.imgLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)



app = QApplication(sys.argv)
window = tehseencode()
window.show()
try:
    sys.exit(app.exec_())
except:
    print('exiting')
