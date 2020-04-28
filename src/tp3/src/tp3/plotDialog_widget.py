'''
    dialog widget for selecting the information 
    that should be presented in a new plot
'''

from python_qt_binding import QtCore, QtGui
from python_qt_binding.QtWidgets import QDialog, QTabWidget, QVBoxLayout
from rawdata_tab import RawDataTab
# from Rosbag_Analysis import Rosbag_Analysis

class PlotDialogWidget(QDialog):
    
    def __init__(self, bagFiles):
        super(PlotDialogWidget, self).__init__()
        self.setWindowTitle("Add new Plot")
        # self.setWindowModality(Qt.ApplicationModal)
        self.layout = QVBoxLayout()        
        self.resize(600, 400)
        
        # TabWidget
        self.tabWidget = QTabWidget()
        self.rawDataTab = RawDataTab()
        self.tabWidget.addTab(self.rawDataTab, "Raw Data")
        self.layout.addWidget(self.tabWidget)
        
                # init the start button
        startBtn = QPushButton("Start")
        startBtn.clicked.connect(self.getPlotData)
        self.layout.addWidget(startBtn)
        
        self.setLayout(self.layout)
        
    def getPlotData(self):
        # is called when start button is clicked
        bagfile = self.bagFiles[rawDataTab.selectedBag]
        obj_id = 1
        category = "geometric"
        attribute = "x"
#         plotData = RosbagAnalysis.getRawData(bagfile, obj_id, category, attribute)
        
        # todo: emit signal with data
        # close dialog
        

