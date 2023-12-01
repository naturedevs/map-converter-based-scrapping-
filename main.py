import subprocess
import sys
import os
import pkg_resources

from PyQt6.QtWidgets import (
    QApplication, QLabel, 
    QWidget, QPushButton, 
    QHBoxLayout, QVBoxLayout, QGridLayout,
    QLineEdit, QFormLayout, QFileDialog,
    QDialog, QDialogButtonBox, QMessageBox,
)
from PyQt6.QtGui import (
    QIcon,
)
from utils.FS1 import FS
   
def bspToMap(bspPath, mapPath):
    exe_path = pkg_resources.resource_filename(__name__, 'myconverter.exe')
    subprocess.run([exe_path,"-convert", "-format", "map", "-map", bspPath, "-game", "wolf"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    mapFile = bspPath.replace('.bsp','_converted.map').replace('/','\\')
    with open(os.getcwd() + "\\" + mapFile, 'r+') as fp:
        lines = fp.readlines()
        fp.seek(0)
        fp.truncate()
        fp.writelines(lines[1:])
    os.system("move {} {}".format(mapFile, mapPath.replace('/','\\')))

def bspsToMaps(bspsPath, mapPath):
    os.system("mkdir {}".format(mapPath.replace('/','\\')))
    for bsp in bspsPath:
        bspToMap(bsp, mapPath)
    
def extractBspFromPK3(pk3Path, bspPath):
    if not pk3Path.endswith('.pk3'):
        return ([], False)
    time = 1
    bsps = []
    for maps in FS.getPK3Package(pk3Path).namelist():
        # print(maps)
        if maps.startswith("maps/"):
            if not FS.isDir(maps):
                if time == 1:
                    time += 1
                else:
                    if maps.endswith('.bsp'):
                        bsp = FS.getPK3Package(pk3Path).extract(maps, bspPath)
                        bsps.append(bsp)
                    # file = FS.getPK3Package(fileName).open(maps)
                    # file.extract()
                    # data = file.read()
                    # decodedData = str(data.decode("utf-8"))
                    # jsonData = json.loads(decodedData)
                    # map.append(jsonData)
                    # map.append(maps)
    # print(map)
    if len(bsps) == 0:
        return ([], False)
    return (bsps, True)
    
class Window(QDialog):
    def __init__(self):
        super().__init__(parent=None)
        ico_path = pkg_resources.resource_filename(__name__, '2.ico')
        self.setWindowIcon(QIcon(ico_path))
        self.setWindowTitle("PK3 to map Converter")
        dialogLayout = QVBoxLayout()
        # formLayout
        formLayout = QFormLayout()
        # layout1
        layout1 = QHBoxLayout()
        
        label1 = QLabel("Input:")
        label1.setFixedWidth(50)
        lineEdit1 = QLineEdit()
        setattr(self, "lineEdit1", lineEdit1)
        button1 = QPushButton("open")
        button1.clicked.connect(self.on_button_click)
        
        layout1.addWidget(label1)
        layout1.addWidget(lineEdit1)
        layout1.addWidget(button1)
        # layout2
        layout2 = QHBoxLayout()
        
        label2 = QLabel("Output:")
        label2.setFixedWidth(50)
        lineEdit2 = QLineEdit()
        lineEdit2.setFixedWidth(300)
        lineEdit2.setText(os.getcwd() + '\\output\\')
        setattr(self, "lineEdit2", lineEdit2)
        button2 = QPushButton("select")
        button2.clicked.connect(self.on_button_click)
        
        layout2.addWidget(label2)
        layout2.addWidget(lineEdit2)
        layout2.addWidget(button2)
        # add layouts
        formLayout.addRow(layout1)
        formLayout.addRow(layout2)
        
        dialogLayout.addLayout(formLayout)
        buttons = QDialogButtonBox()
        buttons.setStandardButtons(
            QDialogButtonBox.StandardButton.Cancel
            | QDialogButtonBox.StandardButton.Ok
        )
        dialogLayout.addWidget(buttons)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        self.setLayout(dialogLayout)
        msgDone = QMessageBox()
        msgDone.setWindowTitle("Result")
        setattr(self, "messageDone", msgDone)
    def accept(self):
        fileName = self.lineEdit1.text()
        if fileName.endswith('.pk3'):
            bsps, res = extractBspFromPK3(fileName, 'temp')
            if res == True:
                bspsToMaps(bsps, self.lineEdit2.text())
                self.messageDone.setIcon(QMessageBox.Icon.Information)
                self.messageDone.setText("converted successfully : generated {} maps".format(len(bsps)))
                self.messageDone.exec()
                os.system("rmdir temp /s /q")
            else :
                self.messageDone.setIcon(QMessageBox.Icon.Critical)
                self.messageDone.setText("error .pk3 file doesn't contain any maps")
                self.messageDone.exec()
        elif fileName.endswith('.bsp'):
            bspToMap(fileName, self.lineEdit2.text())            
        else :
            print('unknown error')
    def on_button_click(self):
        button = self.sender()
        if button.text() == "open":
            fileName, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Packages(*.pk3)")
            self.lineEdit1.setText(fileName.replace('/','\\'))               
        elif button.text() == "select":
            folderName = QFileDialog.getExistingDirectory(self, "Select Directory")
            self.lineEdit2.setText(folderName.replace('/','\\'))
        else :
            print('on_button_click unknown error')

if __name__ == "__main__":
    app = QApplication([])
    window = Window()
    window.show()
    sys.exit(app.exec())
# app = QApplication([])
# window = QWidget()
# window.setWindowTitle("QFormLayout")

# layout = QFormLayout()
# layout.addRow("Name:", QLineEdit())
# layout.addRow("Age:", QLineEdit())
# layout.addRow("Job:", QLineEdit())
# layout.addRow("Hobbies:", QLineEdit())
# window.setLayout(layout)

# window.show()
# sys.exit(app.exec())
# app = QApplication([])
# window = QWidget()
# window.setWindowTitle("PK3 Converter")
# window.setGeometry(200, 200, 300, 300)
# helloMsg = QLabel("<h1>Hello, World!</h1>", parent=window)
# helloMsg.move(60, 15)
# window.show()
# sys.exit(app.exec())
# app = QApplication([])
# window = QWidget()
# window.setWindowTitle("QHBoxLayout")

# layout = QHBoxLayout()
# layout.addWidget(QPushButton("Left"))
# layout.addWidget(QPushButton("Center"))
# layout.addWidget(QPushButton("Right"))
# window.setLayout(layout)

# window.show()
# sys.exit(app.exec())
# app = QApplication([])
# window = QWidget()
# window.setWindowTitle("QGridLayout")

# layout = QGridLayout()
# layout.addWidget(QPushButton("Button (0, 0)"), 0, 0)
# layout.addWidget(QPushButton("Button (0, 1)"), 0, 1)
# layout.addWidget(QPushButton("Button (0, 2)"), 0, 2)
# layout.addWidget(QPushButton("Button (1, 0)"), 1, 0)
# layout.addWidget(QPushButton("Button (1, 1)"), 1, 1)
# layout.addWidget(QPushButton("Button (1, 2)"), 1, 2)
# layout.addWidget(QPushButton("Button (2, 0)"), 2, 0)
# layout.addWidget(
#     QPushButton("Button (2, 1) + 2 Columns Span"), 2, 1, 1, 2
# )
# window.setLayout(layout)

# window.show()
# sys.exit(app.exec())
# if __name__ == '__main__':
#     if len(sys.argv) == 1:
#         print('you should provide the file')
#     else :
#         print(sys.argv[1])
#         print(os.getcwd())
#         target = os.getcwd() + "\\" + sys.argv[1]
#         target = os.getcwd() + "\\" + "battery.bsp"
#         # subprocess.run([".\q3map2.exe -convert -format map -map E:\Project\pk3\project\battery.bsp -game wolf"])
#         # print(".\q3map2.exe -convert -format map -map " + target + " -game wolf")
#         subprocess.run([".\q3map2.exe","-convert", "-format", "map", "-map", sys.argv[1], "-game", "wolf"])
