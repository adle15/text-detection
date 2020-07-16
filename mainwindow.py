import cv2
import sys
import numpy as np
import imutils
import pytesseract
from PIL import ImageGrab

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow
from PyQt5.uic import loadUi


class tehseencode(QDialog):
    def __init__(self):
        super(tehseencode, self).__init__()
        # loadUi("student3.ui",self)
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

    def captureScreen(bbox=(300, 300, 1500, 1000)):
        capScr = np.array(ImageGrab.grab(bbox))
        capScr = cv2.cvtColor(capScr, cv2.COLOR_RGB2BGR)
        return capScr

    @pyqtSlot()
    def onClicked(self):
        self.TEXT.setText('Kindly Press "Capture Image " to Capture image')
        cap = cv2.VideoCapture(0)
        # while (True):
        # print(cap.read())
        while (cap.isOpened()):
            ret, frame = cap.read()

            timer = cv2.getTickCount()
            _, img = cap.read()

            # img = captureScreen()
            # DETECTING CHARACTERES
            hImg, wImg, _ = img.shape
            boxes = pytesseract.image_to_boxes(img)
            for b in boxes.splitlines():
                # print(b)
                b = b.split(' ')
                # print(b)
                x, y, w, h = int(b[1]), int(b[2]), int(b[3]), int(b[4])
                cv2.rectangle(img, (x, hImg - y), (w, hImg - h), (50, 50, 255), 2)
                cv2.putText(img, b[0], (x, hImg - y + 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (50, 50, 255), 2)
            fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);
            # cxv2.putText(img, str(int(fps)), (75, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (20,230,20), 2);
            cv2.imshow("Result", img)
            cv2.waitKey(1)

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
