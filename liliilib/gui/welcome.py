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

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton, qApp
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QSize, QTranslator, QLocale


class WelcomeWidget(QWidget):

    lang_list = {"ca_ES.UTF-8" : "Català", "de_DE.UTF-8" : "Deutsch", "en_US.UTF-8" : "English (US)", "es_ES.UTF-8" : "Español",
                 "fr_FR.UTF-8" : "Français", "hu.UTF-8" : "Magyar", "it_IT.UTF-8" : "Italiano", "nl_NL.UTF-8" : "Nederlands",
                 "pl.UTF-8" : "Polski", "pt_BR.UTF-8" : "Português (Brasil)", "ru_RU.UTF-8" : "Pусский",
                 "sw_SE.UTF-8" : "Svenska", "tr_TR.UTF-8" : "Türkçe"}

    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.setWindowTitle(self.tr("Hoşgeldiniz"))

        self.setLayout(QVBoxLayout())
        self.layout().setAlignment(Qt.AlignCenter)

        titleLabel = QLabel()
        titleLabel.setAlignment(Qt.AlignCenter)
        titleLabel.setText(self.tr("<h1>Lime Linux Sistem Kurulumuna Hoşgeldiniz.</h1>"))
        self.layout().addWidget(titleLabel)

        descLabel = QLabel()
        descLabel.setAlignment(Qt.AlignCenter)
        descLabel.setText(self.tr("Bu program size bazı sorular soracak ve sisteminize Lime Linux kuracaktır."))
        self.layout().addWidget(descLabel)

        lLayout = QHBoxLayout()
        lLayout.setAlignment(Qt.AlignCenter)
        self.layout().addLayout(lLayout)

        imageLabel = QLabel()
        imageLabel.setPixmap(QPixmap(":/images/welcome.svg"))
        imageLabel.setScaledContents(True)
        imageLabel.setFixedSize(256, 256)
        lLayout.addWidget(imageLabel)

        langLayout = QHBoxLayout()
        langLayout.setAlignment(Qt.AlignCenter)
        self.layout().addLayout(langLayout)

        langLabel = QLabel()
        langLabel.setText(self.tr("Dil:"))
        langLayout.addWidget(langLabel)

        langComboBox = QComboBox()
        langComboBox.setFixedWidth(250)
        langLayout.addWidget(langComboBox)

        linkLayout = QHBoxLayout()
        linkLayout.setAlignment(Qt.AlignCenter)
        self.layout().addLayout(linkLayout)

        aboutButton = QPushButton()
        aboutButton.setText(self.tr("Hakkında"))
        aboutButton.setIcon(QIcon(":/images/about.svg"))
        aboutButton.setIconSize(QSize(18,18))
        aboutButton.setStyleSheet("border: none;")
        linkLayout.addWidget(aboutButton)

        bugButton = QPushButton()
        bugButton.setText(self.tr("Bilinen Hatalar"))
        bugButton.setIcon(QIcon(":/images/bug.svg"))
        bugButton.setIconSize(QSize(18,18))
        bugButton.setStyleSheet("border: none;")
        linkLayout.addWidget(bugButton)

        releaseButton = QPushButton()
        releaseButton.setText(self.tr("Sürüm Notları"))
        releaseButton.setIcon(QIcon(":/images/release-note.svg"))
        releaseButton.setIconSize(QSize(18,18))
        releaseButton.setStyleSheet("border: none;")
        linkLayout.addWidget(releaseButton)

        langComboBox.addItems(["Català", "Deutsch", "English (US)", "Español", "Français", "Magyar", "Italiano",
                               "Nederlands", "Polski", "Português (Brasil)", "Pусский", "Svenska", "Türkçe"])

        for k, v in self.lang_list.items():
            if QLocale.system().name()+".UTF-8" == k:
                langComboBox.setCurrentText(v)
                self.parent.lilii_settings["lang"] = k

        langComboBox.currentTextChanged.connect(self.langSelect)

    def langSelect(self, lang):
        print(lang)
        for k, v in self.lang_list.items():
            if lang == v:
                self.parent.lilii_settings["lang"] = k
                print(self.parent.lilii_settings, k.split(".")[0])
                translator = QTranslator(qApp)
                translator.load("/usr/share/lilii/languages/{}.qm".format(k.split(".")[0]))
                qApp.installTranslator(translator)
