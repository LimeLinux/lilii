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

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QComboBox, QLabel, QLineEdit, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import os
import json


class KeyboardWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.setWindowTitle(self.tr("Klavye Düzeni"))
        self.setLayout(QVBoxLayout())
        self.layout().setAlignment(Qt.AlignCenter)

        centerLayout = QHBoxLayout()
        self.layout().addLayout(centerLayout)

        keyLabel = QLabel()
        keyLabel.setFixedSize(283*3.5, 80*3.5)
        keyLabel.setScaledContents(True)
        keyLabel.setPixmap(QPixmap(":/images/keyboard.svg"))
        centerLayout.addWidget(keyLabel)

        hlayoutx = QHBoxLayout()
        self.layout().addLayout(hlayoutx)

        modelLabel = QLabel()
        modelLabel.setFixedWidth(150)
        modelLabel.setText(self.tr("Klavye Modeli:"))
        hlayoutx.addWidget(modelLabel)

        self.modelList = QComboBox()
        hlayoutx.addWidget(self.modelList)

        hlayout = QHBoxLayout()
        self.layout().addLayout(hlayout)

        countryLabel = QLabel()
        countryLabel.setText(self.tr("Dil:"))
        hlayout.addWidget(countryLabel)

        self.countryList = QComboBox()
        self.countryList.setFixedWidth(400)
        hlayout.addWidget(self.countryList)

        hlayout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Preferred, QSizePolicy.Expanding))

        keyboardLabel = QLabel()
        keyboardLabel.setText(self.tr("Klavye:"))
        hlayout.addWidget(keyboardLabel)

        self.keyboardVList = QComboBox()
        self.keyboardVList.setFixedWidth(400)
        hlayout.addWidget(self.keyboardVList)

        self.testEdit = QLineEdit()
        self.testEdit.setPlaceholderText(self.tr("Klavyeni test et."))
        #self.testEdit.setFixedWidth(800)
        self.layout().addWidget(self.testEdit)

        self.keyboard_list = None
        if os.path.isfile("/usr/share/lilii/data/models.json"):
            self.keyboard_list = json.loads(open("/usr/share/lilii/data/models.json").read())

        self.layout_list = None
        if os.path.isfile("/usr/share/lilii/data/layouts.json"):
            self.layout_list = json.loads(open("/usr/share/lilii/data/layouts.json").read())

        self.variant_list = None
        if os.path.isfile("/usr/share/lilii/data/variants.json"):
            self.variant_list = json.loads(open("/usr/share/lilii/data/variants.json").read())

        for model, value in self.keyboard_list.items():
            self.modelList.addItem(value)
            if model == "pc105":
                self.modelList.setCurrentText(value)
                self.parent.lilii_settings["keyboard_model"] = model, value

        for k, v in self.layout_list.items():
            self.countryList.addItem(v)

        default = self.layout_list.get(self.parent.lilii_settings["lang"][:2], "us")
        if default == "us":
            self.countryList.setCurrentText(self.layout_list[default])
            self.parent.lilii_settings["keyboard_layout"] = default, self.layout_list[default]

        else:
            self.countryList.setCurrentText(default)
            self.parent.lilii_settings["keyboard_layout"] = self.parent.lilii_settings["lang"][:2], default

        self.keyboardVList.addItem("Default")
        for k, v in self.variant_list.items():
            if k == self.parent.lilii_settings["keyboard_layout"][0]:
                for i in v:
                    self.keyboardVList.addItems(i.values())
        self.parent.lilii_settings["keyboard_variant"] = None

        self.modelList.currentTextChanged.connect(self.keyboardModelSelect)
        self.countryList.currentTextChanged.connect(self.countrySelect)
        self.keyboardVList.currentTextChanged.connect(self.keyboardTypeSelect)

    def keyboardModelSelect(self, value):
        for model in self.keyboard_list.keys():
            if self.keyboard_list[model] == value:
                self.parent.lilii_settings["keyboard_model"] = model, value

    def countrySelect(self, value):
        for layout in self.layout_list.keys():
            if self.layout_list[layout] == value:
                self.parent.lilii_settings["keyboard_layout"] = layout, value

        self.keyboardVList.clear()
        self.parent.lilii_settings["keyboard_variant"] = None
        self.keyboardVList.addItem("Default")
        for k, v in self.variant_list.items():
            if k == self.parent.lilii_settings["keyboard_layout"][0]:
                for i in v:
                    self.keyboardVList.addItems(i.values())

        os.system("setxkbmap -layout {} -variant \"\"".format(self.parent.lilii_settings["keyboard_layout"][0]))

    def keyboardTypeSelect(self, value):
        if value == "Default":
            os.system("setxkbmap -variant \"\"")
            self.parent.lilii_settings["keyboard_variant"] = None

        else:
            for variant in self.variant_list.keys():
                if variant in self.parent.lilii_settings["keyboard_layout"]:
                    for key in self.variant_list[variant]:
                        if key[list(key.keys())[0]] == value:
                            self.parent.lilii_settings["keyboard_variant"] = list(key.keys())[0], list(key.values())[0]
                            os.system("setxkbmap -variant {}".format(self.parent.lilii_settings["keyboard_variant"][0]))