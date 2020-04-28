'''
    this widget inherits from QWidget and 
    contains widgets to select the data required 
    for plotting raw data
'''

from python_qt_binding import QtCore, QtGui
from python_qt_binding.QtWidgets import (QWidget, QGridLayout, 
                                         QVBoxLayout, QPushButton,
                                         QRadioButton, QFrame, QGroupBox)

from valueSelector_widget import ValueSelectorWidget
from id_selector_widget import IDSelectorWidget
from Rosbag_Analysis import Rosbag_Analysis

class RawDataTab(QWidget):
    
    def __init__(self, bagFiles):
        super(RawDataTab, self).__init__()
        self.layout = QGridLayout()
        
        self.bagFiles = bagFiles
        self.selectedBag = 0
        self.selectedValue = ('', '') # contains value as a tupel like ('<message>', '<value>')      
        
        # init the widgets
        self.bagSelector = self.initBagSelector()
        self.layout.addWidget(self.bagSelector, 1, 1)
        self.valueWidget = ValueSelectorWidget()
        self.layout.addWidget(self.valueWidget, 1, 2)
        self.idSelector = IDSelectorWidget()
        self.layout.addWidget(self.idSelector, 1, 3)
        
        # init the start button
        startBtn = QPushButton("Start")
        startBtn.clicked.connect(self.getPlotData)
        self.layout.addWidget(startBtn, 2, 3)
        
        self.setLayout(self.layout)
        
        self.newPlotData()
        
    def initBagSelector(self):
        '''
            determines which of the two bag file 
            should be shown in the plot
        '''
        bagSelector = QGroupBox('Select Bag')
        bagSelectorLayout = QVBoxLayout()
        bag1RadioBtn = QRadioButton('BagFile1')
        bag1RadioBtn.clicked.connect(self.btn1Clicked)
        bag2RadioBtn = QRadioButton('BagFile2')
        bag2RadioBtn.clicked.connect(self.btn2Clicked)
        bagSelectorLayout.addWidget(bag1RadioBtn)
        bagSelectorLayout.addWidget(bag2RadioBtn)
        bagSelector.setLayout(bagSelectorLayout)
        
        return bagSelector
    
    def btn1Clicked(self):
        self.selectedBag = 1
        
    def btn2Clicked(self):
        self.selectedBag = 2
              
    def getPlotData(self):
        # is called when start button is clicked
        bagfile = self.bagFiles[self.selectedBag]
        obj_id = 1
        category = "geometric"
        attribute = "x"
        plotData = RosbagAnalysis.getRawData(bagfile, obj_id, category, attribute)
        
        # todo: emit signal with data
        # close dialog
        
        
        
        
        
        