from PyQt5.QtCore import QMimeDatabase, Qt
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QGridLayout
from PyQt5 import QtGui, QtCore
import calc_iibb, re, ntpath, pyperclip

class ImageLabel(QLabel):
    def __init__(self):
        super().__init__()

        self.setAlignment(Qt.AlignCenter)
        self.setText('\n\n Patricia, arrastre el PDF por favor...\n\n')
        self.setFont(QtGui.QFont('Arial', 12, QtGui.QFont.Black))
        self.setStyleSheet('''
            QLabel{
                border: 4px dashed #aaa
            }
        ''')

    def setPixmap(self, image):
        super().setPixmap(image)

class Label(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        mainLayout = QVBoxLayout()
        self.setWindowTitle("Retenciones")
        self.setMaximumSize(QtCore.QSize(400, 400))
        self.setMinimumSize(QtCore.QSize(400, 400))
        self.photoViewer = ImageLabel()
        mainLayout.addWidget(self.photoViewer)
        self.setLayout(mainLayout)

    def dragEnterEvent(self, event):
        if self.find_pdf(event.mimeData()):
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if self.find_pdf(event.mimeData()):
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        urls = self.find_pdf(event.mimeData())
        if urls:
            for url in urls:
                print(url.toLocalFile())
            event.accept()
            self.nueva_ventana(url.toLocalFile())
        else:
            event.ignore()

    def find_pdf(self, mimedata):
        urls = list()
        db = QMimeDatabase()
        for url in mimedata.urls():
            mimetype = db.mimeTypeForUrl(url)
            if mimetype.name() == "application/pdf":
                urls.append(url)
        return urls

    def nueva_ventana(self, url):
        self.nw = AnotherWindow(url)
        self.nw.show()


class AnotherWindow(QWidget):
    def __init__(self, url):
        super().__init__()
        rgxpat = r'[A-Z]+?\s[A-Z]+|[A-Z]{2,}'
        filename = ntpath.basename(url)
        tarjeta = re.findall(rgxpat, filename)[0]

        self.valor = "$ {:.2f}".format(calc_iibb.iibb(url))
        pyperclip.copy(self.valor.replace('$', '').replace('.', ','))
        self.titulo = tarjeta

        layout = QGridLayout()

        self.label = QLabel(self.valor)
        self.label.setFont(QtGui.QFont('Times', 20, QtGui.QFont.Black))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.adjustSize()
        w = self.label.size().width() + 200

        self.setWindowTitle(self.titulo)
        self.setMaximumSize(QtCore.QSize(w, 100))
        self.setMinimumSize(QtCore.QSize(w, 100))
        self.move(550, 230)

        layout.addWidget(self.label)
        self.setLayout(layout)



def main():
    app = QApplication([])
    label = Label()
    label.show()
    app.exec_()


if __name__ == "__main__":
    main()