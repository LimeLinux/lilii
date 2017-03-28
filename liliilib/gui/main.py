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

from PyQt5.QtWidgets import (QWidget, QApplication, QStackedWidget, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy,
                             QPushButton, QDesktopWidget, QLabel, qApp, QMessageBox)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QObject, QTranslator, QLocale, pyqtSignal
from PyQt5.QtNetwork import QLocalServer, QLocalSocket
from .welcome import WelcomeWidget
from .finish import FinishWidget
from .install import InstallWidget
from .keyboard import KeyboardWidget
from .location import LocationWidget
from .partition import PartitionWidget
from .summary import SummaryWidget
from .user import UserWidget
from .widget.lprogressbar import LProgressBar

import sys
from .. import resource


class SingleApplication(QObject):

    newInstance = pyqtSignal()
    urlPost = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.mServer = QLocalServer()
        self.mServer.newConnection.connect(self.newConnection)

    def listen(self, client):
        self.mServer.removeServer(client)
        self.mServer.listen(client)
        print(self.mServer.errorString())

    def hasPrevious(self, name, args):
        socket = QLocalSocket()
        socket.connectToServer(name, QLocalSocket.ReadWrite)
        if socket.waitForConnected():
            if len(args) > 1:
                socket.write(args[1])

            else:
                pass

            socket.flush()
            return True

        return False

    def newConnection(self):
        self.newInstance.emit()
        self.mSocket = self.mServer.nextPendingConnection()
        self.mSocket.readyRead.connect(self.readyRead)

    def readyRead(self):
        self.urlPost.emit(str(self.mSocket.readAll()))
        self.mSocket.close()

class TitleWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.setFixedHeight(100)
        self.setLayout(QHBoxLayout())
        self.layout().addSpacing(0)

        self.logo = QLabel()
        self.logo.setFixedSize(72, 72)
        self.logo.setScaledContents(True)
        self.logo.setPixmap(QPixmap(":/images/lime-logo.svg"))
        self.layout().addWidget(self.logo)

        self.layout().addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Expanding))

        self.lprogressBar = LProgressBar(self.parent)
        self.layout().addWidget(self.lprogressBar)

        self.parent.currentChanged.connect(self.lprogressBar.setIndex)



class FooterWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.setFixedHeight(50)
        self.setLayout(QHBoxLayout())

        self.layout().addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Expanding))

        self.cancelButton = QPushButton()
        self.cancelButton.setIcon(QIcon(":/images/cancel.svg"))
        self.cancelButton.setText(self.tr("Vazgeç"))
        self.layout().addWidget(self.cancelButton)

        self.layout().addItem(QSpacerItem(40, 20, QSizePolicy.Maximum, QSizePolicy.Maximum))

        self.backButton = QPushButton()
        self.backButton.setIcon(QIcon(":/images/back.svg"))
        self.backButton.setText(self.tr("Geri"))
        self.layout().addWidget(self.backButton)

        self.continueButton = QPushButton()
        self.continueButton.setIcon(QIcon(":/images/forward.svg"))
        self.continueButton.setText(self.tr("Devam"))
        self.layout().addWidget(self.continueButton)

        self.applyButton = QPushButton()
        self.applyButton.setIcon(QIcon(":/images/apply.svg"))
        self.applyButton.setText(self.tr("Bitti"))
        self.layout().addWidget(self.continueButton)

        self.parent.currentChanged.connect(self.buttonStatus)
        self.continueButton.clicked.connect(self.nextWidget)
        self.backButton.clicked.connect(self.proviousWidget)
        self.cancelButton.clicked.connect(self.cancelQuestion)

        if self.parent.currentIndex() == 0:
            self.backButton.setDisabled(True)

    def cancelQuestion(self):
        question = QMessageBox.question(self, self.tr("Vazgeçmek mi istiyorsun?"),
                                        self.tr("Lime GNU/Linux Sistem Yükleyicisi'nden çıkmak istiyor musunuz?"))

        if question == QMessageBox.Yes:
            qApp.quit()


    def buttonStatus(self, current):
        self.backButton.setEnabled(True)
        if current == 0:
            self.backButton.setDisabled(True)

        if current+1 == self.parent.count():
            self.continueButton.setText(self.tr("Çıkış"))
            self.continueButton.setIcon(QIcon(":/images/exit.svg"))
            self.continueButton.clicked.connect(qApp.quit)
            self.backButton.setDisabled(True)
            self.cancelButton.setDisabled(True)

        if current == 6:
            self.backButton.setDisabled(True)
            self.cancelButton.setDisabled(True)

    def nextWidget(self):
        if self.parent.currentIndex() == 5:
            warning = QMessageBox.warning(self, self.tr("Dikkat Edin!"),
                                          self.tr("Sonraki adımda kurulum başlayacak ve "
                                          "bu adımda belirtilen işlemler sisteminize "
                                          "uygulanacaktır."), QMessageBox.Yes|QMessageBox.No)

            if warning == QMessageBox.Yes:
                self.parent.setCurrentIndex(self.parent.currentIndex() + 1)

            else: pass

        else:
            self.parent.setCurrentIndex(self.parent.currentIndex()+1)

    def proviousWidget(self):
        self.parent.setCurrentIndex(self.parent.currentIndex() - 1)

        if self.parent.currentIndex() == 4 or 3:
            self.continueButton.setEnabled(True)


class MainWindow(QWidget):

    lilii_settings = {}

    def __init__(self, parent=None):
        super().__init__()
        self.resize(950, 580)
        self.setWindowTitle(self.tr("Lime GNU/Linux Sistem Yükleyicisi"))
        self.setWindowIcon(QIcon(":/images/lilii-logo.svg"))
        self.setWindowFlags(Qt.WindowTitleHint|Qt.WindowMinimizeButtonHint) #Qt.WindowStaysOnTopHint

        x, y = (QDesktopWidget().width()-self.width())/2, (QDesktopWidget().availableGeometry().height()-self.height())/2
        self.move(x, y)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.wizardWidget = QStackedWidget()
        self.wizardWidget.addWidget(WelcomeWidget(self))
        self.wizardWidget.addWidget(LocationWidget(self))
        self.wizardWidget.addWidget(KeyboardWidget(self))
        self.wizardWidget.addWidget(PartitionWidget(self))
        self.wizardWidget.addWidget(UserWidget(self))
        self.wizardWidget.addWidget(SummaryWidget(self))
        self.wizardWidget.addWidget(InstallWidget(self))
        self.wizardWidget.addWidget(FinishWidget(self))

        self.titleWidget = TitleWidget(self.wizardWidget)
        self.footerWidget = FooterWidget(self.wizardWidget)

        layout.addWidget(self.titleWidget)
        layout.addWidget(self.wizardWidget)
        layout.addWidget(self.footerWidget)

        self.footerWidget.cancelButton.clicked.connect(self.close)
        self.wizardWidget.widget(4).applyPage.connect(self.footerWidget.continueButton.setEnabled)
        self.wizardWidget.widget(3).applyPage.connect(self.footerWidget.continueButton.setEnabled)
        self.wizardWidget.widget(6).applyPage.connect(self.footerWidget.continueButton.setEnabled)

    def closeEvent(self, event):
        if not qApp.quitOnLastWindowClosed():
            event.ignore()

        else:
            event.accept()


def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    app.setApplicationVersion("1.0 Alpha")
    locale = QLocale.system().name()
    translator = QTranslator(app)
    translator.load("/usr/share/lilii/languages/{}.qm".format(locale))
    app.installTranslator(translator)

    single = SingleApplication()
    if single.hasPrevious("lilii", app.arguments()):
        return False

    single.listen("lilii")

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())