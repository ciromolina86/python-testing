import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class SrcButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.srcFileName = None

    def mousePressEvent(self, e: QMouseEvent) -> None:
        self.srcFileName = self.choose_src_file()
        print(self.srcFileName)
        SrcLabel.setText(self.srcFileName)

    def choose_src_file(self):
        file_path, _ = QFileDialog.getOpenFileName(caption='Choose source file',
                                                   filter='Source Code Files (*.AWL)')
        return file_path


class DstButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def mousePressEvent(self, e: QMouseEvent) -> None:
        self.choose_dst_file()

    def choose_dst_file(self):
        file_path, _ = QFileDialog.getSaveFileName(caption="Choose destination file",
                                                   filter='Logix Designer XML Files (*.L5X)')
        print(file_path)

        # if file_path != '':
        #     self.var_dst_file_name.set(file_path)


class ConvertButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def mousePressEvent(self, e: QMouseEvent) -> None:
        self.convert_file()

    def convert_file(self):
        if self.var_src_file_name.get()[-4:] == ".AWL":
            try:
                self.var_convert_stat.set('Converting...')
                # converter.db_to_udt(self.var_src_file_name.get(), self.var_dst_file_name.get())
                self.var_convert_stat.set('Conversion Finished Successfully!')
            except:
                self.var_convert_stat.set('Failed to convert file!')
        else:
            self.var_convert_stat.set("Filename must be a .AWL")


class SrcLabel(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class DstLabel(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ConvertLabel(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # set window title
        self.setWindowTitle('DB to UDT Converter')

        # create Central Widget objects
        self.mainLabel = QLabel('Converts Siemens Datablock source code (.AWL) \n'
                                'to Allen-Bradley UDT source code (.L5X)')

        self.srcButton = QPushButton('Choose Source File')
        self.srcLabel = QLabel('Choose source file...')
        self.srcFileName = None

        self.dstButton = QPushButton('Choose Destination File')
        self.dstLabel = QLabel('Choose destination file...')
        self.dstFileName = None

        self.convertButton = QPushButton('Convert file!')
        self.convertLabel = QLabel('Waiting to convert file...')

        # configure/set Central Widget
        centralWidget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.mainLabel, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.srcButton, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.srcLabel, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.dstButton, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.dstLabel, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.convertButton, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.convertLabel, alignment=Qt.AlignmentFlag.AlignCenter)
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

        # configure signals and slots
        self.srcButton.clicked.connect(self.chooseSrcFile)
        self.dstButton.clicked.connect(self.chooseDstFile)
        self.convertButton.clicked.connect(self.convertFile)

    def chooseSrcFile(self):
        self.srcFileName, _ = QFileDialog.getOpenFileName(caption='Choose source file',
                                                          filter='Source Code Files (*.AWL)')
        if self.srcFileName:
            self.srcLabel.setText(self.srcFileName)

    def chooseDstFile(self):
        self.dstFileName, _ = QFileDialog.getSaveFileName(caption="Choose destination file",
                                                          filter='Logix Designer XML Files (*.L5X)')
        if self.dstFileName:
            self.srcLabel.setText(self.dstFileName)

    def convertFile(self):
        if self.srcFileName[-4:] == ".AWL":
            try:
                self.convertLabel.setText('Converting...')
                # converter.db_to_udt(self.var_src_file_name.get(), self.var_dst_file_name.get())
                self.convertLabel.setText('Conversion Finished Successfully!')
            except:
                self.convertLabel.setText('Failed to convert file!')
        else:
            self.convertLabel.setText("Filename must be a .AWL")

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()


def myApp():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec_()


if __name__ == '__main__':
    myApp()
