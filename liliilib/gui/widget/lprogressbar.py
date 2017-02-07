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

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QFont, QColor
from PyQt5.QtCore import Qt, QRect


class LProgressBar(QWidget):

    text_color = QColor("#000")
    active_color = QColor("#394050")
    passive_color = QColor("#95a5a6")
    item_index = 0

    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self._item_count = self.parent.count()
        self._stick_count = self._item_count - 1

        self.setFixedWidth(32 + (self._item_count * 100) + 24 + 32)


    def setIndex(self, index):
        self.item_index = index
        self.repaint()

    def setTextColor(self, color): #QColor
        self.text_color = color
        self.repaint()

    def setActiveColor(self, color):
        self.active_color = color
        self.repaint()

    def setPassiveColor(self, color):
        self.passive_color = color
        self.repaint()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        for index in range(self._stick_count):
            if self.item_index >= index +1:
                painter.setPen(self.active_color)
                painter.setBrush(self.active_color)
                painter.drawRect(56+(index*100), 24, 76, 6)

            else:
                painter.setPen(self.passive_color)
                painter.setBrush(self.passive_color)
                painter.drawRect(56+(index*100), 24, 76, 6)

        for index in range(self._item_count):
            if self.item_index >= index:
                painter.setPen(self.active_color)
                painter.setBrush(self.active_color)

                painter.drawEllipse(32 + (index * 100), 16, 24, 24)

                painter.setPen(Qt.black)
                painter.drawText(32 + (index * 100), 16, 24, 84, Qt.AlignCenter | Qt.TextWordWrap | Qt.TextDontClip,
                                 self.parent.widget(index).windowTitle())

            else:
                painter.setPen(self.passive_color)
                painter.setBrush(self.passive_color)

                painter.drawEllipse(32+(index*100), 16, 24, 24)

                painter.setPen(Qt.black)
                painter.drawText(32+(index*100), 16, 24, 84, Qt.AlignCenter | Qt.TextWordWrap | Qt.TextDontClip,
                                 self.parent.widget(index).windowTitle())



