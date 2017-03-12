#
#
#  Copyright 2017 Metehan Özbek <mthnzbk@gmail.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy, QStackedWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer


class Slide(QWidget):

    def __init__(self):
        super().__init__()
        self.setLayout(QVBoxLayout())

        self.image = QLabel()
        self.layout().addWidget(self.image)

        self.description = QLabel()
        self.layout().addWidget(self.description)

    def setResource(self, resource):
        self.image.setPixmap(QPixmap(resource))

    def setDescription(self, text):
        self.description.setText(text)


class SlideWidget(QStackedWidget):

    duration = 10 * 1000

    def __init__(self, parent=None):
        super().__init__()

        self.timer = QTimer(self)




        self.timer.timeout.connect(self.nextSlide)

    def setSlideDuration(self, second):
        self.duration = second * 1000

    def startSlide(self):
        self.timer.start(self.duration)

    def nextSlide(self):
        current = self.currentIndex()+1
        if self.count() != current:
            self.setCurrentIndex(current)

        else:
            self.setCurrentIndex(0)




