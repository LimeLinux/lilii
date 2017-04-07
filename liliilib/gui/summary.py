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

from PyQt5.QtWidgets import QWidget, QTextBrowser, QLabel, QVBoxLayout
from ..tools import is_efi


class SummaryWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.setWindowTitle(self.tr("Installation Information"))
        self.setLayout(QVBoxLayout())

        label1 = QLabel()
        label1.setText(self.tr("<h3>Take a look at the summary of your choices for the installation.</h3>"))
        self.layout().addWidget(label1)

        label2 = QLabel()
        label2.setText(self.tr("<h1>System Location</h1>"))
        self.layout().addWidget(label2)

        self.textbrowser1 = QTextBrowser()
        self.layout().addWidget(self.textbrowser1)

        label3 = QLabel()
        label3.setText(self.tr("<h1>Keyboard Layout</h1>"))
        self.layout().addWidget(label3)

        self.textbrowser2 = QTextBrowser()
        self.layout().addWidget(self.textbrowser2)

        label4 = QLabel()
        label4.setText(self.tr("<h1>Disk Partition</h1>"))
        self.layout().addWidget(label4)

        self.textbrowser3 = QTextBrowser()
        self.layout().addWidget(self.textbrowser3)

    def showEvent(self, event):
        self.textbrowser1.setText(self.tr("System time will be set to {}.\nSystem language will be set to {}.")
                                  .format(self.parent.lilii_settings["timezone"], self.parent.lilii_settings["lang"]))

        variant = None
        if self.parent.lilii_settings["keyboard_variant"] != None:
            variant = self.parent.lilii_settings["keyboard_variant"][-1]
        else:
            variant = "Default"

        self.textbrowser2.setText(self.tr("Keyboard model is choosen as {}.\nKeyboard kind is choosen as {}/{}.")
                                  .format(self.parent.lilii_settings["keyboard_model"][-1],
                                          self.parent.lilii_settings["keyboard_layout"][-1], variant))

        self.textbrowser3.clear()
        if self.parent.lilii_settings["/"]:
            self.textbrowser3.append(self.tr("Root directory is {}.").format(self.parent.lilii_settings["/"]))

        if self.parent.lilii_settings["/home"]:
            self.textbrowser3.append(self.tr("Home directory is {}.").format(self.parent.lilii_settings["/home"]))

        if is_efi() and self.parent.lilii_settings["/boot/efi"]:
            self.textbrowser3.append(self.tr("Bootloader installation directory is {}.").format(self.parent.lilii_settings["/boot/efi"]))

        else:
            self.textbrowser3.append(self.tr("Bootloader installation disk: {}").format(self.parent.lilii_settings["bootloader"]))