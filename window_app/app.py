from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from finBERT.finbert.finbert import predict
from pytorch_pretrained_bert.modeling import BertForSequenceClassification

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

        self.status = QStatusBar()
        self.setStatusBar(self.status)

        file_toolbar = QToolBar()
        file_toolbar.setIconSize(QSize(20, 20))
        self.addToolBar(file_toolbar)

        open_file_action = QAction(QIcon(os.path.join('images', 'blue-folder-open-document.png')), "Open file...", self)
        open_file_action.setStatusTip("Open file")
        open_file_action.triggered.connect(self.file_open)
        file_toolbar.addAction(open_file_action)

        run_action = QAction(QIcon(os.path.join('images', 'blue-folder-open-document.png')), "Open file...", self)
        run_action.setStatusTip("Open file")
        run_action.triggered.connect(self.click_run_button)
        file_toolbar.addAction(run_action)

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
        model = BertForSequenceClassification.from_pretrained('/src/models/classifier_model/finbert-sentiment',
                                                              num_labels=3, cache_dir=None)
        text = self.editor
        print(predict(text, model).to_json(orient='records'))
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

    def check_check_state(self, i):
        if not i.isCheckable():  # Skip data columns.
            return


if __name__ == '__main__':

    app = QApplication(sys.argv)
    app.setApplicationName("finBERT App")

    window = MainWindow()
    app.exec_()
