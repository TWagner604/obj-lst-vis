import os
from python_qt_binding import QtCore, QtGui
from python_qt_binding.QtWidgets import QWidget, QLineEdit, QPushButton, QGridLayout, QFileDialog

class BagSelectorWidget(QWidget):    
    def __init__(self):
        super(BagSelectorWidget, self).__init__()
        
        # create elements
        self.bag1Edit = QLineEdit()
        self.bag1Btn = QPushButton("bag file 1")
        self.bag1Btn.clicked.connect(self.btn1_clicked)
        self.bag2Edit = QLineEdit()
        self.bag2Btn = QPushButton("bag file 2")
        self.bag2Btn.clicked.connect(self.btn2_clicked)
        
        self.__fileName1 = ""
        self.__fileName2 = ""
        
        self.layout = QGridLayout()
        self.layout.addWidget(self.bag1Edit, 1, 1)
        self.layout.addWidget(self.bag1Btn, 1, 2)
        self.layout.addWidget(self.bag2Edit, 2, 1)
        self.layout.addWidget(self.bag2Btn, 2, 2)
        self.setLayout(self.layout)

    def btn1_clicked(self):
        cwd = os.getcwd() # current working directory
        fileTupel = QFileDialog.getOpenFileName(self, 'Select file', cwd, "Bag files (*.bag)")
        self.__fileName1 = fileTupel[0]
        self.bag1Edit.setText(self.__fileName1) # print filename to lineEdit
        
    def btn2_clicked(self):
        cwd = os.getcwd() # current working directory
        fileTupel = QFileDialog.getOpenFileName(self, 'Select file', cwd, "Bag files (*.bag)")
        self.__fileName2 = fileTupel[0]
        self.bag2Edit.setText(self.__fileName2) # print filename to lineEdit
        
    def getBagFiles(self):
        return [self.__fileName1, self.__fileName2]
