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
                             QFrame, QButtonGroup, QTreeWidget, QTreeWidgetItem)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, Qt, QProcess, pyqtSignal
from ..tools import *
from .widget.diskeditwidget import DiskEditWidget
import parted


class PartitionWidget(QWidget):

    first_show = True
    selected_disk = diskInfo(disksList()[0])
    applyPage = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.setWindowTitle(self.tr("Disk Partition"))
        self.setLayout(QVBoxLayout())

        self.parent.lilii_settings["/"] = None
        self.parent.lilii_settings["/home"] = None

        hlayout = QHBoxLayout()
        self.layout().addLayout(hlayout)

        hlayout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Maximum))

        label1 = QLabel()
        label1.setText(self.tr("Select where the Lime GNU/Linux is going to be installed: "))
        hlayout.addWidget(label1)

        self.combo_box = QComboBox()
        self.combo_box.setFixedWidth(400)
        for disk in disksList():
            self.combo_box.addItem("{} - {} ({})".format(disk.model, mbToGB(disk.getSize()), disk.path))

        hlayout.addWidget(self.combo_box)

        self.label2 = QPushButton()
        self.label2.setStyleSheet("border: none;")
        self.label2.setIcon(QIcon(":/images/disk.svg"))
        self.label2.setIconSize(QSize(20, 20))
        self.label2.setText("{}".format(diskType(disksList()[0]) or self.tr("Unknown")))
        hlayout.addWidget(self.label2)

        self.refreshButton = QPushButton()
        self.refreshButton.setIcon(QIcon(":/images/refresh.svg"))
        self.refreshButton.setIconSize(QSize(24, 24))
        self.refreshButton.setToolTip(self.tr("Refresh disk information"))
        hlayout.addWidget(self.refreshButton)

        hlayout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Maximum))

        self.treePartitionWidget = QTreeWidget()
        self.layout().addWidget(self.treePartitionWidget)

        header = self.treePartitionWidget.headerItem()
        header.setText(0, self.tr("Disk Part"))
        header.setText(1, self.tr("File System"))
        header.setText(2, self.tr("Mount Point"))
        header.setText(3, self.tr("Size"))

        self.treePartitionWidget.setColumnWidth(0, 450)
        self.treePartitionWidget.setColumnWidth(1, 150)
        self.treePartitionWidget.setColumnWidth(2, 200)
        self.treePartitionWidget.setColumnWidth(3, 100)


        hlayout = QHBoxLayout()
        self.layout().addLayout(hlayout)

        hlayout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Maximum))

        self.editPartitionButton = QPushButton()
        self.editPartitionButton.setText(self.tr("Edit"))
        hlayout.addWidget(self.editPartitionButton)

        self.zeroPartitionButton = QPushButton()
        self.zeroPartitionButton.setText(self.tr("Reset"))
        hlayout.addWidget(self.zeroPartitionButton)



        if not is_efi():
            hlayout = QHBoxLayout()
            self.layout().addLayout(hlayout)

            hlayout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Maximum))

            bootLabel = QLabel()
            bootLabel.setText(self.tr("Where to install the bootloader:"))
            hlayout.addWidget(bootLabel)

            self.combo_box2 = QComboBox()
            self.combo_box2.setFixedWidth(400)
            for disk in disksList():
                self.combo_box2.addItem("{} - {} ({})".format(disk.model, mbToGB(disk.getSize()), disk.path))

            self.parent.lilii_settings["bootloader"] = disksList()[0].path
            hlayout.addWidget(self.combo_box2)

            hlayout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Maximum))
            self.combo_box2.currentIndexChanged.connect(self.bootloaderDiskSelect)


            self.parent.lilii_settings["/boot"] = None

        else:
            self.parent.lilii_settings["/boot/efi"] = None

        self.editPartitionButton.clicked.connect(self.diskConnect)
        self.combo_box.currentIndexChanged.connect(self.diskSelect)
        self.zeroPartitionButton.clicked.connect(self.diskPartitionClear)
        self.refreshButton.clicked.connect(self.diskRefresh)

        self.diskPartitionList(diskInfo(disksList()[self.combo_box.currentIndex()]))


    def diskSelect(self, index):
        self.label2.setText("{}".format(diskType(disksList()[index])))
        self.selected_disk = diskInfo(disksList()[0])
        self.diskPartitionList(diskInfo(disksList()[self.combo_box.currentIndex()]))

    def diskRefresh(self):
        self.diskPartitionList(diskInfo(disksList()[self.combo_box.currentIndex()]))

    def bootloaderDiskSelect(self, index):
        self.parent.lilii_settings["bootloader"] = disksList()[index].path

    def diskPartitionClear(self):
        for index in list(range(self.treePartitionWidget.topLevelItemCount())):
            item = self.treePartitionWidget.topLevelItem(index)
            item.setText(2, "")

        self.parent.lilii_settings["/"] = None
        self.parent.lilii_settings["/home"] = None

        if is_efi():
            self.parent.lilii_settings["/boot/efi"] = None

        else:
            self.parent.lilii_settings["/boot"] = None

        self.partitionSelectControl()

    def diskPartitionList(self, disk):
        self.treePartitionWidget.clear()
        try:
            for partition in disk.partitions:
                try:
                    part_item = QTreeWidgetItem()
                    part_item.setText(0, partition.path)
                    part_item.setText(1, partition.fileSystem.type)
                    part_item.setText(2, "")
                    part_item.setText(3, mbToGB(partition.getSize()))
                    self.treePartitionWidget.addTopLevelItem(part_item)

                except AttributeError:
                    part_item = QTreeWidgetItem()
                    part_item.setText(0, partition.path)
                    part_item.setText(1, self.tr("Unknown"))
                    part_item.setText(2, "")
                    part_item.setText(3, mbToGB(partition.getSize()))
                    self.treePartitionWidget.addTopLevelItem(part_item)

        except (parted.DiskLabelException, AttributeError):
            part_item = QTreeWidgetItem()
            part_item.setText(0, self.tr("Partition table not Found"))
            self.treePartitionWidget.addTopLevelItem(part_item)


    def diskConnect(self):
        if self.treePartitionWidget.selectedItems():
            item = self.treePartitionWidget.selectedItems()[0]
            disk = DiskEditWidget(self)
            disk.partition = item
            disk.exec_()


    def showEvent(self, event):
        if self.first_show:
            QProcess.startDetached("sudo gparted")
            self.first_show = False

        self.partitionSelectControl()

    def partitionSelectControl(self):
        if self.parent.lilii_settings["/"] != None:
            if is_efi() and self.parent.lilii_settings["/boot/efi"] != None:
                self.applyPage.emit(True)

            elif not is_efi():
                self.applyPage.emit(True)

        else:
            self.applyPage.emit(False)