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
from PyQt5.QtGui import QPainter, QColor, QPixmap
from PyQt5.QtCore import Qt, QRectF, QRect
import random
from ...tools import mbToGB


class LPartitionWidget(QWidget):

    color_list = [QColor("#ff2a2a"), QColor("#ff6600"), QColor("#ffd42a"), QColor("#d35fbc"), QColor("#00ccff"),
                  QColor("#bcd35f"), QColor("#8d5fd3"), QColor("#ff9366"), QColor("#ff2a7f"), QColor("#3771c8"),
                  QColor("#37c871"), QColor("#d40000")]

    partitions = []
    max_capacity = 0

    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        random.shuffle(self.color_list)
        self.setMinimumHeight(100)

    def setDisk(self, disk):
        self.max_capacity = int(disk.device.getSize())
        self.partitions.clear()
        self.partitions.extend(disk.partitions)
        self.repaint()

    def __percentage(self, width, capacity, max_capacity):
        return width * (capacity/max_capacity)

    def removePartition(self, partition):
        self.partitions.remove(partition)
        self.repaint()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        width = self.width() - 8
        height = 36

        previous = 0
        percent_up = 0
        for partition in self.partitions:
            color = self.color_list[self.partitions.index(partition)]
            percent = self.__percentage(width, partition.getSize(), self.max_capacity)

            if percent < 10:
                percent += 4
                percent_up += 1

            if percent_up >= 0 and percent >= width/35:
                percent -= 4 * percent_up
                percent_up = 0
            print(percent, width)
            painter.setPen(color)
            painter.setBrush(color)
            painter.drawRect(QRectF(4+previous, 5, percent, 34))
            previous += percent


        #Çerçeve
        painter.setPen(QColor(Qt.black))
        painter.setBrush(Qt.NoBrush)
        painter.drawRoundedRect(QRectF(4, 4, width, height), 4, 4)
        #Parlaklık
        painter.drawPixmap(QRect(6, 6, width-4, height-4), QPixmap(":/images/partitionwidget/light.svg"))

        #kareler
        line = 0
        column = 0
        for partition in self.partitions:
            painter.setPen(Qt.black)
            painter.setBrush(self.color_list[self.partitions.index(partition)])

            if width - (line * 150) <= 150:
                column += 1
                line = 0

            painter.drawRoundedRect(QRectF(4 + (line * 150), (column*32)+64, 12, 12), 2, 2)
            painter.drawText(QRectF(24 + (line * 150), (column*32)+64, 30, 12),
                             Qt.AlignVCenter | Qt.TextDontClip, partition.path)
            painter.setPen(Qt.darkGray)

            if partition.fileSystem:
                painter.drawText(QRectF(24 + (line * 150), (column*32)+78, 40, 12),
                                 Qt.AlignVCenter | Qt.TextDontClip, "{}  {}".format(mbToGB(partition.getSize()),
                                                                                    partition.fileSystem.type))

            else:
                painter.drawText(QRectF(24 + (line * 150), (column*32)+78, 40, 12),
                                 Qt.AlignVCenter | Qt.TextDontClip,
                                 self.tr("{}  Bilinmiyor").format(mbToGB(partition.getSize())))

            line += 1
