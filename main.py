# -*- coding: utf-8 -*-

from PyQt4 import QtGui
from PyQt4.QtCore import pyqtSignature
import sys
import random
import xlrd
from groupingui import Ui_MainWindow
from grouping import run_grouping

class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self,parent=None,gename_file=None,conflicts_file=None,num_of_groups=None,method = run_grouping):
        self.gename_file = gename_file
        self.conflicts_file = conflicts_file
        self.num_of_groups = num_of_groups
        self.method = method
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        
    @pyqtSignature("")
    def on_pushButton_clicked(self):
        self.gename_file = str(QtGui.QFileDialog.getOpenFileName(self,u'打开文件','/'))
        self.lineEdit.setText(self.gename_file)
        self.textEdit.append(self.gename_file)

    @pyqtSignature("")
    def on_pushButton_2_clicked(self):
        self.conflicts_file = str(QtGui.QFileDialog.getOpenFileName(self,u'打开文件','/'))
        self.lineEdit_2.setText(self.conflicts_file)
        self.textEdit.append(self.conflicts_file)

    @pyqtSignature("")
    def on_pushButton_5_clicked(self):
        self.num_of_groups = self.spinBox.value()

    @pyqtSignature("")
    def on_pushButton_4_clicked(self):
        job = self.method(self.gename_file, self.conflicts_file, self.num_of_groups)
##        print xlrd.open_workbook(self.gename_file).sheets()[0]
##        print self.conflicts_file
##        print self.num_of_groups
        self.textEdit.append('Please wait...')
        job.run()
        self.textEdit.append('Done!')
        

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    dialog = MainWindow()
    dialog.show()
    sys.exit(app.exec_())

