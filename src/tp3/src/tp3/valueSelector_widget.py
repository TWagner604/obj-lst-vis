'''
    this small widget is shown in plot dialog
    here the user can select which of the values 
    he wants to plot
'''

from pathlib import Path

from python_qt_binding import QtCore, QtGui
from python_qt_binding.QtWidgets import *
from object_list_msg import obj_list_msg

# TODO: Maybe import ObjectList.msg directly for the tree structure?

class ValueSelectorWidget(QGroupBox):
    
    def __init__(self):
        super(ValueSelectorWidget, self).__init__()
        self.__selectedCategory = ""
        self.__selectedAttribute = ""
        
        self.layout = QVBoxLayout()
        self.setTitle('3.Select Value')
        self.valueTreeWidget = QTreeWidget()
        self.valueTreeWidget.itemSelectionChanged.connect(self.selectionChanged)
        self.buildTree()
        self.layout.addWidget(self.valueTreeWidget)
        self.setLayout(self.layout)
        
    def buildTree(self):
        '''
            fills the treeWidget
            according to the structure of ObjectList.msg
        '''
        for key in obj_list_msg:
            category = QTreeWidgetItem(self.valueTreeWidget)
            category.setText(0, key)
            for att in obj_list_msg[key]:
                attribute = QTreeWidgetItem(category)
                attribute.setText(0, att)
#                 attBtn = QRadioButton(att)
#                 category.addChild(attBtn)

    def selectionChanged(self):
        '''
            is called when the selection of the tree view is changed
            changes the value of the selected
        '''
        # TODO ...
        
                

        
        