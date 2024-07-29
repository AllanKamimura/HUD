from PySide2.QtGui import QBrush, QPen, QPainter, QMatrix, QTransform, QColor, QTextOption, QVector3D, QImage, QPixmap, QFont
from PySide2.QtCore import Qt, Slot, Signal, QThread, QByteArray, QDataStream, QBuffer
from PySide2.QtWidgets import QMainWindow, QApplication, QWidget, QGraphicsScene, QGraphicsView, QPushButton, QVBoxLayout, QLabel

import sys
import numpy as np

class Window(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("aaaaaaaaaaaaa")
        # self.setGeometry(0, 0, 680, 480) 
        
        self.scene  = QGraphicsScene(self)
        self.view   = QGraphicsView(self.scene, self)
        
        self.create_ui(680, 480)

    def create_ui(self, width, height):
        self.width  = width
        self.height = height

        color = Qt.darkGreen

        pen1 = QPen(color, 3, Qt.SolidLine)
        pen2 = QPen(color, 3, Qt.DashLine)
        pen3 = QPen(color, 2, Qt.SolidLine)
        
        self.anchor = self.scene.addEllipse(-5, -5, 10, 10)
        self.elipse = self.scene.addEllipse(-5, -5, 10, 10, pen1)
        self.group = self.scene.createItemGroup([self.elipse])

        self.anchor.setTransformOriginPoint(0, 0)
        self.elipse.setTransformOriginPoint(0, 0)
        self.group.setTransformOriginPoint(0, 0)

        for i in range(-80, 80, 1): 
            if i == 0:
                x = 220

                line = self.scene.addLine(-x, 0, x, 0, pen3)
                self.group.addToGroup(line)

            elif (i%5 == 0) and (i > 0): 
                x = 50
                y = 12 * i
                d = 80

                line = self.scene.addLine(-x, y, x - d, y, pen2)
                self.group.addToGroup(line)

                line = self.scene.addLine(-x, y, -x, y - 5, pen2)
                self.group.addToGroup(line)

                line = self.scene.addLine(d - x, y, x, y, pen2)
                self.group.addToGroup(line)

                line = self.scene.addLine(x, y, x, y - 5, pen2)
                self.group.addToGroup(line)

                text = self.scene.addText(str(-1 * i).rjust(4), QFont("Times", 15, QFont.Bold))
                text.setPos(-x-38, y-20)
                text.setTextWidth(200)

                self.group.addToGroup(text)

            elif (i%5 == 0) and (i < 0): 
                x = 50
                y = 12 * i
                d = 80

                line = self.scene.addLine(-x, y, x - d, y, pen1)
                self.group.addToGroup(line)

                line = self.scene.addLine(-x, y, -x, y + 5, pen1)
                self.group.addToGroup(line)

                line = self.scene.addLine(d - x, y, x, y, pen1)
                self.group.addToGroup(line)

                line = self.scene.addLine(x, y, x, y + 5, pen1)
                self.group.addToGroup(line)             

                text = self.scene.addText(str(-1 * i).rjust(4), QFont("Times", 15, QFont.Bold))
                text.setPos(-x-38, y-13)
                text.setTextWidth(200)

                self.group.addToGroup(text)

        self.view.setTransformationAnchor(self.view.AnchorViewCenter)    
        # self.view.setGeometry(self.width * 0.25, self.height * 0.25, self.width//2, self.height//2)
        # self.view.setFixedSize(self.width//2, self.height)
        # self.view.setSceneRect(-self.width // 2, -self.height // 2, self.width, self.height)

        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setStyleSheet("background: transparent")

        self.view.setRenderHint(QPainter.Antialiasing)  # Optional, for better rendering quality
        self.view.setRenderHint(QPainter.SmoothPixmapTransform)  # Optional, for smooth transformation
        self.view.setRenderHint(QPainter.HighQualityAntialiasing) 
        self.view.setRenderHint(QPainter.TextAntialiasing) 

    def rotate(self, angle):
        self.view.centerOn(self.anchor)
        t2 = QTransform().rotate(angle)
        self.view.setTransform(t2, False)    

    def move(self, angle):
        t1 = QTransform().translate(0, angle / 5 * 60)
        self.group.setTransform(t1, False)

    @Slot(dict)
    def update(self, data):
        theta = data["theta"]
        phi   = data["phi"]
        
        self.rotate(phi)
        self.move(theta)

