import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.Qt import Qt

from flick import Flick

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Flick Tool'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480

        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
    
        self.openFileNamesDialog()
        self.openFileNameDialog()
        self.saveDirDialog()
        self.show_info()
        self.show_buttons()
        
        self.show()
    
    def show_info(self):

        label2 = QLabel('Overlay video: {}'.format(self.v2_file),self)
        label2.move(50,50)
        label3 = QLabel('Output folder is: {}'.format(self.v3_dir),self)
        label3.move(50,80)
        label = QLabel('You selected: {} files.'.format(len(self.v1_files)),self)
        label.move(50,110)
        pos_y = 110

        for idx, v1_file in enumerate(self.v1_files):
            QLabel('*** Video {}: {}'.format(idx+1, v1_file),self).move(60, pos_y+20*(idx+1))
    
    def show_buttons(self):
        button = QPushButton('Generate Videos', self)
        button.setToolTip('This will generate videos based on loaded information')
        button.move(30,20)

        button_c = QPushButton('Clear Settings', self)
        button_c.setToolTip('This is to clear all information loaded in the application.')
        button_c.move(350,20)

        button.clicked.connect(self.make_videos)
        button_c.clicked.connect(self.clear_settings)

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"Please select overlay video (V2)", "","All Files (*)", options=options)
        if fileName:
            self.v2_file = fileName
    
    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self,"Please select background video(s) (V1)", "","All Files (*)", options=options)
        if files:
            self.v1_files = files
    
    def saveDirDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        dirName = QFileDialog.getExistingDirectory(self,"Please select the folder for the final videos to be saved","",QFileDialog.ShowDirsOnly)
        if dirName:
            self.v3_dir = dirName
    
    def make_videos(self):
        for v1 in self.v1_files:
            foo = Flick(v1, self.v2_file, os.path.join(self.v3_dir, os.path.basename(v1)))
            foo.run()
    
    def clear_settings(self):
        self.v1_files = []
        self.v2_file = ""
        self.v3_dir = ""

        self.show_info()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())