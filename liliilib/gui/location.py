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

from PyQt5.QtWidgets import QWidget, QLabel, QComboBox, QHBoxLayout, QVBoxLayout, QSizePolicy, QSpacerItem
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

import json
import os

zone = set()

if os.path.isfile("/usr/share/lilii/data/zone.json"):
    zone_info = json.loads("/usr/share/lilii/data/zone.json")

    zone = set()

    for k, v in zone_info:
        zone.add(k)

## testing
if os.path.isfile("/home/metehan/PycharmProjects/lilii/data/zone.json"):
    zone_info = json.loads(open("/home/metehan/PycharmProjects/lilii/data/zone.json").read())



    for k, v in zone_info.items():
        zone.add(k)

zone = list(zone)
zone.sort()


class LocationWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.setWindowTitle(self.tr("Sistem Yereli"))
        self.setLayout(QVBoxLayout())
        self.layout().setAlignment(Qt.AlignCenter)

        layout = QHBoxLayout()
        self.layout().addLayout(layout)

        worldMap = QLabel()
        worldMap.setFixedSize(480, 283)
        worldMap.setScaledContents(True)
        worldMap.setPixmap(QPixmap(":/images/world.svg"))
        layout.addWidget(worldMap)

        hlayout = QHBoxLayout()
        self.layout().addLayout(hlayout)

        cLabel = QLabel()
        cLabel.setText(self.tr("Bölge:"))
        hlayout.addWidget(cLabel)

        self.cBox = QComboBox()
        self.cBox.setFixedWidth(300)
        hlayout.addWidget(self.cBox)

        hlayout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Preferred, QSizePolicy.Expanding))

        iLabel = QLabel()
        iLabel.setText(self.tr("Şehir:"))
        hlayout.addWidget(iLabel)

        self.iBox = QComboBox()
        self.iBox.setFixedWidth(300)
        hlayout.addWidget(self.iBox)

        self.cBox.addItems(zone)

        self.iBox.addItems(zone_info[self.cBox.currentText()])

        self.parent.lilii_settings["timezone"] = "{}/{}".format(self.cBox.currentText() , self.iBox.currentText())

        self.cBox.currentTextChanged.connect(self.zoneChanged)
        self.iBox.currentTextChanged.connect(self.cityChanged)

    def zoneChanged(self, zone):
        self.iBox.clear()
        self.iBox.addItems(zone_info[self.cBox.currentText()])
        self.parent.lilii_settings["timezone"] = "{}/{}".format(self.cBox.currentText(), self.iBox.currentText())
        #print(self.parent.lilii_settings["timezone"])

    def cityChanged(self, city):
        self.parent.lilii_settings["timezone"] = "{}/{}".format(self.cBox.currentText(), self.iBox.currentText())
