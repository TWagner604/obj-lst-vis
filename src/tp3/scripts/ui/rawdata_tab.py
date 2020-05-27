'''
    this widget inherits from QWidget and 
    contains widgets to select the data required 
    for plotting raw data
'''

from python_qt_binding import QtCore, QtGui
from python_qt_binding.QtWidgets import (QWidget, QGridLayout, 
                                         QVBoxLayout, QPushButton,
                                         QRadioButton, QFrame, QGroupBox,
                                         QDoubleSpinBox)

from valueSelector_widget import ValueSelectorWidget
from id_selector_widget import IDSelectorWidget
from rawDataSelector_box import RawDataSelector
from Rosbag_Analysis import Rosbag_Analysis
import object_list_msg 
import message_module

class RawDataTab(QWidget):
    
    def __init__(self, bagFiles, parent=None):
        super(RawDataTab, self).__init__()
        self.parent = parent
        self.layout = QGridLayout()
    
        self.bagFiles = bagFiles
        self.selectedSource = 3 # no bag is selected
        self.selectedValue = ('', '') # contains value as a tupel like ('<message>', '<value>')      
        
        # init the widgets
        self.sourceSelector = RawDataSelector(self)
        self.sourceSelector.dataSourceChanged.connect(self.sourceChanged)
        self.layout.addWidget(self.sourceSelector, 0, 0)
        self.valueWidget = ValueSelectorWidget()
        self.layout.addWidget(self.valueWidget, 0, 1)
        self.idSelector = IDSelectorWidget()
        self.layout.addWidget(self.idSelector, 0, 2)
        
        self.setLayout(self.layout)
        
         
    def sourceChanged(self, source):
        '''
            if the source in rawDataSelector is changed
            this slot is called
        '''        
        self.selectedSource = source
        
        if source == 0: # ground truth is selected
            self.idSelector.setTitle("3.Select GT-ObjectID")
            try: 
                self.idSelector.refreshList(self.bagFiles[0])
            except:
                message_module.showMessage("Object_IDs could not be parsed. Maybe there is a problem with the selected bag file.")
        
        elif source == 1: # camera is selected
            self.idSelector.setTitle("3.Select Cam-ObjectID")
            try: 
                self.idSelector.refreshList(self.bagFiles[1])
            except:
                message_module.showMessage("Object_IDs could not be parsed. Maybe there is a problem with the selected bag file.")
                
        else: # difference is selected
            self.idSelector.setTitle("3.Select GT-ObjectID")
            try: 
                self.idSelector.refreshList(self.bagFiles[0])
            except:
                message_module.showMessage("Object_IDs could not be parsed. Maybe there is a problem with the selected bag file.")
                
    
    def getPlotData(self):
        '''
            gets the raw data according to the selected parameters
            from Rosbag_Analysis
        '''
        plotInfo = {
            'label' : '',
            'y_label' : '',
            'bag' : 1
            }
        
        selectedValue = self.valueWidget.getCatAndAtt()
        category = selectedValue['category']
        attribute = selectedValue['attribute']  
        # check whether attribute is empty
        # show error message when it is the case
        # and return the function
        if attribute == "":
            raise Exception("Please select a plottable attribute.")            
        
        try:
            obj_id = self.idSelector.getID()
        except ValueError:
            raise Exception("ObjectID is not a number! Insert valid ID.")
        
        if self.selectedSource < 2: # a single bag should be analysed
            
            
            bagfile = self.bagFiles[self.selectedSource]
            if bagfile == "":
                raise Exception("no bag file loaded! Please import bag file in the main interface.")
                        
            try:    
                plotData = Rosbag_Analysis.getRawData(bagfile, obj_id, category, attribute)
            except:
                raise Exception("Sorry, unexpected error occurred.")
            
            bag_id = self.selectedSource + 1
            
            plotInfo['label'] = 'bag' + str(bag_id) + '.'            
            plotInfo['bag'] = bag_id
        
        elif self.selectedSource == 2: # difference is selected
            
            for bag in self.bagFiles:
                if bag == "":
                    raise Exception("Bag file missing! Please import bag file in the main interface.")
                
            threshold = self.sourceSelector.getThreshold()
            
            try:
                plotData = Rosbag_Analysis.getAdvancedData(self.bagFiles[0], self.bagFiles[1], obj_id, category, attribute, 'difference', threshold)
            except ValueError:
                raise Exception("Sorry, unexpected error occurred.")
            
            plotInfo['label'] = 'difference' + '.'            
            plotInfo['y_label'] = object_list_msg.values_units[attribute]
        
        else: # no bag file is selected
            raise Exception("Please select a bag file or difference.")
        
        plotInfo['label'] += 'obj' + str(obj_id) + '.'
        plotInfo['label'] += category + '.'
        plotInfo['label'] += attribute
        plotInfo['label'] += object_list_msg.units[attribute]
        
        plotInfo['y_label'] = object_list_msg.values_units[attribute]
        
        return plotData, plotInfo
    
        
        
        
        