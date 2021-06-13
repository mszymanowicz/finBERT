from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtGui


import os
import sys


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        layout = QVBoxLayout()
        self.editor = QPlainTextEdit()  # Could also use a QTextEdit and set self.editor.setAcceptRichText(False)


        # Setup the QTextEdit editor configuration
        fixedfont = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        fixedfont.setPointSize(12)
        self.editor.setFont(fixedfont)
        self.editor.setStyleSheet("color: black; background-color: #fff09c")
        self.editor.setMaximumHeight(100)
        # self.path holds the path of the currently open file.
        # If none, we haven't got a file open yet (or creating new).
        self.listView = QTableView()
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["Sentence", "prediction", "sentiment score"])
        layout.addWidget(self.editor)
        layout.addWidget(self.listView)

        print(self.editor)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        container.setAutoFillBackground(False)
        container.setStyleSheet(os.path.join('images', 'background.png'))
        #self.setFixedSize(1920, 1080)

        self.status = QStatusBar()
        self.setStatusBar(self.status)

        file_toolbar = QToolBar()
        file_toolbar.setIconSize(QSize(20, 20))
        self.addToolBar(file_toolbar)

        open_file_action = QAction(QIcon(os.path.join('images', 'folder_icon.png')), "Open file...", self)
        open_file_action.setStatusTip("Open file")
        open_file_action.triggered.connect(self.file_open)
        file_toolbar.addAction(open_file_action)

        run_action = QAction(QIcon(os.path.join('images', 'start_icon.png')), "Run ", self)
        run_action.setStatusTip("Open file")
        run_action.triggered.connect(self.click_run_button)
        file_toolbar.addAction(run_action)

        self.setWindowIcon(QtGui.QIcon("images/logo_transparent.png"))
        self.setStyleSheet("color: black; background-color: white")
        self.resize(800, 800)
        self.show()
    def file_open(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open file", "", "Text documents (*.txt);All files (*.*)")

        if path:
            try:
                with open(path, 'rU') as f:
                    text = f.read()

            except Exception as e:
                self.dialog_critical(str(e))

            else:
                self.path = path
                self.editor.setPlainText(text)

    def click_run_button(self):
        text = self.editor
        sentence = QStandardItem()
        sentence_now = self.editor.toPlainText()
        sentence.setText(sentence_now)
        sentence.setColumnCount(1)
        prediction = QStandardItem()
        prediction_value = "positive"
        prediction.setText(prediction_value)
        prediction.setColumnCount(2)
        sentiment_score = QStandardItem()
        sentiment_score_value = "9.32423"
        sentiment_score.setText(sentiment_score_value)
        sentiment_score.setColumnCount(3)
        self.model.setColumnCount(3)
        self.model.appendRow([sentence, prediction, sentiment_score])
        self.model.sort(0)

        self.listView.setModel(self.model)

if __name__ == '__main__':

    app = QApplication(sys.argv)
    app.setApplicationName("finBERT App")

    window = MainWindow()
    app.exec_()
