"""
CPSC6240 - Log Analyzer Project
Asher Antao
"""

from loganalyzer2 import Ui_Form
from PyQt6.QtWidgets import QWidget, QApplication, QFileDialog, QListWidget, QListWidgetItem, QLineEdit
from logmine_pkg.log_mine import LogMine

import sys
import io

class AppWindow(QWidget):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.BrowseFiles.clicked.connect(self.BrowseDir)
        self.ui.listWidget.itemClicked.connect(self.fileClick)
        self.ui.Search.clicked.connect(self.SearchText)
        self.ui.ClusterData.clicked.connect(self.Clustering)
        self.fpath = []
        self.clusterPath = []
        self.ui.Distance_Cluster.valueChanged.connect(self.setSliderLabel)
    def BrowseDir(self):
        #print("Browser Clickerd")
        self.clusterPath = []
        fileBrowser = QFileDialog()
        fileBrowser.setFileMode(QFileDialog.FileMode.ExistingFile)
        fileNames = fileBrowser.getOpenFileNames()
        #print(fileNames[0])
        #try:
        #    self.ui.listWidget.addItems(fileNames[0])
        #except Exception as error:
        #    print(error)
        self.ui.listWidget.addItems(fileNames[0])

        #for nameF in fileNames:
        #    item = QListWidgetItem(nameF, self.ui.listWidget)
    def fileClick(self, filepath):
        try:
            #print(filepath.text())
            text = open(filepath.text()).read()
            self.fpath = filepath.text()
            self.ui.textEdit.setText(text)
            self.clusterPath.append([filepath.text()])
        except Exception as error:
            print(error)

    
    def Clustering(self):
        #print(filepath.text())
        #fpath = [self.fpath]
        #print(fpath)
        k = self.ui.Distance_Cluster.value() / 100.0
        print(k)
        cluster_config = {
            'max_dist': k,
            'variables': [],
            'delimeters': '\\s+',
            'min_members': 2,
            'k1': 1,
            'k2': 1,
        }
        #Changing Highlight Variables and Patterns to False
        #Since QTextEdit doesn't support ANSI Codes
        output_options = {
            'sorted': 'desc',
            'number_align': True,
            'pattern_placeholder': None,
            'mask_variables': True,
            'highlight_patterns': False,
            'highlight_variables': False,
        }
        processor_config = {'single_core': True}
        lm = LogMine(processor_config, cluster_config, output_options)
        #lm = LogMine()
        buffer = io.StringIO()
        lm.output.set_output_file(file=buffer)
        #lm.run(fpath)
        for fpath in self.clusterPath:
            lm.run(fpath)
        clusterText = buffer.getvalue()
        #clusterText.replace('\33[31m', '<span style="color: red">')
        #clusterText.replace('\33[33m', '<span style="color: blue">')
        #clusterText.replace('\033[0m', '</span>')
        #print(clusterText)
        self.ui.textEdit.setText(clusterText)
        self.clusterPath = []
    
    
    def setSliderLabel(self, value):
        #value = self.ui.Distance_Cluster.value()
        self.ui.sliderValue.setText(f"{value/100.0}")
    def SearchText(self):
        fpath = self.fpath
        #print("hello")
        #print(fpath)
        #search_test = "error"
        #line_Edit = QLineEdit()
        #search_text = line_Edit.text()
        search_text = self.ui.lineEdit.text()
        #print(search_text)
        nl ='\n'
        res = []
        #multi_res = f"Search Results: {nl}"
        try:
            with open(fpath, 'r') as fp:
                for l_num, text_line in enumerate(fp):
                    if search_text in text_line:
                        res.append(text_line)
                        #multi_res.join(f"{l_num}: {text_line} {nl}")
            #search_restext
            multi_res = f"Search results:{nl} {nl.join(map(str, res))}"
            self.ui.textEdit.setText(multi_res)
        except Exception as error:
            print(error)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    #Create object of AppWindow
    appWindow = AppWindow()
    #
    appWindow.show()
    sys.exit(app.exec())

