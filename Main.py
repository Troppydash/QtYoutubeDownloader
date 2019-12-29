import os
import sys
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *



class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle('Youtube Mp3 Downloader')
        self.initUi()

    def initUi(self):
        layout = QVBoxLayout()
        layoutFileWidget = QHBoxLayout()

        # Url
        self.url = QLineEdit()
        urlLabel = QLabel("Url: ")

        urlLayout = QHBoxLayout()
        urlLayout.addWidget(urlLabel)
        urlLayout.addWidget(self.url)

        layout.addLayout(urlLayout)

        # error msg
        errorMsg = QLabel("You shouldn't be seeing this")
        errorMsg.setHidden(True)
        errorMsg.setStyleSheet('QLabel {color: red}')
        self.errorMsg = errorMsg

        errorLayout = QHBoxLayout()
        errorLayout.addWidget(errorMsg)
        layout.addLayout(errorLayout)

        # File
        self.currentFile = QLabel("")
        fileWidget = QPushButton("Select Folder")
        fileWidget.clicked.connect(self.btnClicked)

        layoutFileWidget.addWidget(self.currentFile)
        layoutFileWidget.addWidget(fileWidget)

        layout.addLayout(layoutFileWidget)

        # Confirm
        okButton = QPushButton("Ok")
        okButton.clicked.connect(self.startDownloading)
        okLayout = QHBoxLayout()
        okLayout.setAlignment(Qt.AlignRight | Qt.AlignBottom)

        okLayout.addWidget(okButton)

        layout.addLayout(okLayout)

        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)

    def btnClicked(self, s):
        file = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.currentFile.setText(file)
        # print(self.currentFile.text())

    def startDownloading(self, s):
        url = self.url.text()
        filePath = self.currentFile.text()

        if url == "":
            self.errorMsg.setHidden(False)
            self.errorMsg.setText("Url Field Empty")
            return
        elif filePath == "":
            self.errorMsg.setHidden(False)
            self.errorMsg.setText("File Location Empty")
            return
        else:
            self.errorMsg.setHidden(True)
            self.errorMsg.setText("You shouldn't be seeing this")

        cmd = 'youtube-dl -f 140 "{}" -o {}/%(title)s.%(ext)s'.format(url, filePath)
        buttonReply = QMessageBox.question(self, "Confirmation Box", "Continue?\nCMD: " + cmd, QMessageBox.Yes | QMessageBox.No,
                                           QMessageBox.No)
        if buttonReply == QMessageBox.Yes:
            try:
                os.system(cmd)
            except:
                self.errorMsg.setHidden(False)
                self.errorMsg.setText("Something Went Wrong")

                try:
                    os.system('youtube-dl')
                except:
                    self.errorMsg.setText("Youtube-dl not installed")




app = QApplication([])

window = MainWindow()
window.show()

app.exec_()
