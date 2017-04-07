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

from PyQt5.QtWidgets import QDialog, QLabel, QComboBox, QHBoxLayout, QVBoxLayout, QDialogButtonBox
from PyQt5.QtGui import QPainter, QFont, QColor
from PyQt5.QtCore import Qt, QRect
from ...tools import is_efi


class DiskEditWidget(QDialog):

    partition = None

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setFixedSize(300, 150)
        self.setLayout(QVBoxLayout())

        hlayout = QHBoxLayout()
        self.layout().addLayout(hlayout)

        label = QLabel()
        label.setText(self.tr("Mount Point:"))
        hlayout.addWidget(label)

        self.combobox = QComboBox()
        hlayout.addWidget(self.combobox)

        self.dialbutton = QDialogButtonBox()
        self.dialbutton.setStandardButtons(QDialogButtonBox.Ok|QDialogButtonBox.Cancel)
        self.layout().addWidget(self.dialbutton)

        self.dialbutton.button(QDialogButtonBox.Ok).setText(self.tr("Ok"))
        self.dialbutton.button(QDialogButtonBox.Cancel).setText(self.tr("Cancel"))

        self.dialbutton.accepted.connect(self.editAccept)
        self.dialbutton.rejected.connect(self.close)


    def editAccept(self):
        self.partition.setText(2, self.combobox.currentText())
        self.parent.parent.lilii_settings[self.combobox.currentText()] = self.partition.text(0)
        self.parent.partitionSelectControl()
        self.accept()

    def showEvent(self, event):
        self.setWindowTitle(self.tr("Disk Partition")+" - "+self.partition.text(0))
        if not self.parent.parent.lilii_settings["/"]:
            self.combobox.addItem("/")

        if not self.parent.parent.lilii_settings["/home"]:
            self.combobox.addItem("/home")

        if is_efi():

            if not self.parent.parent.lilii_settings["/boot/efi"]:
                self.combobox.addItem("/boot/efi")

        else:

            if not self.parent.parent.lilii_settings["/boot"]:
                self.combobox.addItem("/boot")