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

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QComboBox, QHBoxLayout, QPushButton, QSpacerItem, QSizePolicy,
                             QFrame, QButtonGroup)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, Qt
from .widget.partitionwidget import LPartitionWidget
from ..tools import *


class PartitionWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.setWindowTitle(self.tr("Disk Bölümleme"))
        self.setLayout(QVBoxLayout())

        hlayout = QHBoxLayout()
        self.layout().addLayout(hlayout)

        label1 = QLabel()
        label1.setText(self.tr("Lime Linux kurulacak diski seçin: "))
        hlayout.addWidget(label1)

        combo_box = QComboBox()
        combo_box.setFixedWidth(400)
        for disk in disksList():
            combo_box.addItem("{} - {} ({})".format(disk.model, mbToGB(disk.getSize()), disk.path))
        hlayout.addWidget(combo_box)

        self.label2 = QPushButton()
        self.label2.setStyleSheet("border: none;")
        self.label2.setIcon(QIcon(":/images/disk.svg"))
        self.label2.setIconSize(QSize(20, 20))
        self.label2.setText("{}".format(diskType(disksList()[0])))
        hlayout.addWidget(self.label2)

        hlayout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Maximum))

        self.layout().addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Maximum, QSizePolicy.Expanding))

        vlayout = QVBoxLayout()
        vlayout.setAlignment(Qt.AlignCenter)
        self.layout().addLayout(vlayout)

        hlayout1 = QHBoxLayout()
        hlayout2 = QHBoxLayout()

        vlayout.addLayout(hlayout1)
        vlayout.addLayout(hlayout2)

        self.button_group = QButtonGroup()

        self.diskOnBurn = QPushButton()
        self.diskOnBurn.setStyleSheet("text-align: left; padding-left: 10px;")
        self.diskOnBurn.setIcon(QIcon(":/images/disk-burn.svg"))
        self.diskOnBurn.setIconSize(QSize(32, 32))
        self.diskOnBurn.setFixedWidth(250)
        self.diskOnBurn.setCheckable(True)
        self.diskOnBurn.setText(self.tr("Disk bölümü üzerine yaz."))
        self.button_group.addButton(self.diskOnBurn)
        hlayout1.addWidget(self.diskOnBurn)

        self.diskSpace = QPushButton()
        self.diskSpace.setStyleSheet("text-align: left; padding-left: 10px;")
        self.diskSpace.setIcon(QIcon(":/images/disk-space.svg"))
        self.diskSpace.setIconSize(QSize(32, 32))
        self.diskSpace.setFixedWidth(250)
        self.diskSpace.setCheckable(True)
        self.diskSpace.setText(self.tr("Disk alanında yer aç."))
        self.button_group.addButton(self.diskSpace)
        hlayout1.addWidget(self.diskSpace)

        self.diskDeleteAndBurn = QPushButton()
        self.diskDeleteAndBurn.setStyleSheet("text-align: left; padding-left: 10px;")
        self.diskDeleteAndBurn.setIcon(QIcon(":/images/disk-delete.svg"))
        self.diskDeleteAndBurn.setIconSize(QSize(32, 32))
        self.diskDeleteAndBurn.setFixedWidth(250)
        self.diskDeleteAndBurn.setCheckable(True)
        self.diskDeleteAndBurn.setText(self.tr("Diski Sil ve Lime Linux Kur."))
        self.button_group.addButton(self.diskDeleteAndBurn)
        hlayout2.addWidget(self.diskDeleteAndBurn)

        self.diskManuelPartition = QPushButton()
        self.diskManuelPartition.setStyleSheet("text-align: left; padding-left: 10px;")
        self.diskManuelPartition.setIcon(QIcon(":/images/manuel-partition.svg"))
        self.diskManuelPartition.setIconSize(QSize(32, 32))
        self.diskManuelPartition.setFixedWidth(250)
        self.diskManuelPartition.setCheckable(True)
        self.diskManuelPartition.setText(self.tr("Elle Bölümle."))
        self.button_group.addButton(self.diskManuelPartition)
        hlayout2.addWidget(self.diskManuelPartition)

        self.layout().addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Maximum, QSizePolicy.Expanding))

        self.line = QFrame()
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.layout().addWidget(self.line)

        self.infoLabel = QLabel()
        self.infoLabel.hide()
        self.layout().addWidget(self.infoLabel)

        self.partitionwidget = LPartitionWidget(self)
        self.partitionwidget.setDisk(diskInfo(disksList()[0]))
        self.layout().addWidget(self.partitionwidget)

        self.partitionwidget2 = LPartitionWidget(self)
        self.partitionwidget2.hide()
        self.partitionwidget2.setDisk(diskInfo(disksList()[0]))
        self.layout().addWidget(self.partitionwidget2)

        combo_box.currentIndexChanged.connect(self.diskSelect)
        self.button_group.buttonClicked.connect(self.diskOnBurnSelect)

    def diskSelect(self, index):
        self.label2.setText("{}".format(diskType(disksList()[index])))
        self.partitionwidget.setDisk(diskInfo(disksList()[index]))

    def diskOnBurnSelect(self, state):
        self.infoLabel.show()
        if self.diskOnBurn == state:
            self.infoLabel.setText(self.tr("<b>Yükleyeceğin disk bölümünü seç:</b>"))

        elif self.diskSpace == state:
            self.infoLabel.setText(self.tr("<b>Küçültmek için bir bölüm seçin ve boyutlandırın</b>"))

        elif self.diskDeleteAndBurn == state:
            self.infoLabel.hide()

        elif self.diskManuelPartition == state:
            self.infoLabel.hide()