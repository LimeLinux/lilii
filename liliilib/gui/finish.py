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

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QSizePolicy, QSpacerItem, qApp
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize, QProcess


class CustomButton(QPushButton):

    def enterEvent(self, event):
        self.setIcon(QIcon(":/images/restart-red.svg"))

    def leaveEvent(self, event):
        self.setIcon(QIcon(":/images/restart.svg"))


class FinishWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.setWindowTitle(self.tr("Finish"))
        self.setLayout(QVBoxLayout())

        titleText = QLabel()
        self.layout().addWidget(titleText)
        titleText.setAlignment(Qt.AlignCenter)
        titleText.setText(self.tr("<h1>All of the process is completed.</h1>"))

        descText = QLabel()
        descText.setWordWrap(True)
        descText.setAlignment(Qt.AlignCenter)
        descText.setText(self.tr("Lime GNU/Linux, has been installed successfully to your system.\nTo use the newly installed system "
                                 "you can restart or you can continue to use Lime GNU/Linux Live system."))
        self.layout().addWidget(descText)

        hlayout = QHBoxLayout()
        self.layout().addLayout(hlayout)

        hlayout.addItem(QSpacerItem(40, 20, QSizePolicy.Preferred, QSizePolicy.Preferred))

        restartButton = CustomButton()
        restartButton.setFlat(True)
        restartButton.setIcon(QIcon(":/images/restart.svg"))
        restartButton.setIconSize(QSize(128, 128))
        restartButton.setFixedSize(130, 130)
        hlayout.addWidget(restartButton)

        hlayout.addItem(QSpacerItem(40, 20, QSizePolicy.Preferred, QSizePolicy.Preferred))

        restartButton.clicked.connect(self.systemRestart)

    def systemRestart(self):
        QProcess.startDetached("reboot", ["-n"])
        qApp.quit()