from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon,QPixmap
import QuadraticSplineInterpolation as qsi
import PolynomialRegression as pr
import Optimization as opt

def readCSV(filepath):
  x = []
  y = []

  try:
    file_handle = open(filepath,'r')
  except Exception:
    return x,y

  while True:
    line = file_handle.readline()
    if len(line) == 0: break
    vi = line.split(',')
    x.append(float(vi[0]))
    y.append(float(vi[1]))

  file_handle.close()
  return x,y

class MainWindow(QWidget):

  def __init__(self,parent=None):
    super(MainWindow,self).__init__(parent)

    regButton = QPushButton('Regression')
    regButton.clicked.connect(self.regButton_onClick)
    qsiButton = QPushButton('QSI')
    qsiButton.clicked.connect(self.qsiButton_onClick)
    optButton = QPushButton('Optimization')
    optButton.clicked.connect(self.optButton_onClick)

    layout = QVBoxLayout()
    layout.addWidget(regButton)
    layout.addWidget(qsiButton)
    layout.addWidget(optButton)

    self.move(0,0)
    self.resize(200,100)
    self.setLayout(layout)
    self.setWindowTitle('CMSC150')

  def setRegWindow(self,regWindow):
    self.regWindow = regWindow

  def setQSIWindow(self,qsiWindow):
    self.qsiWindow = qsiWindow

  def setOptWindow(self,optWindow):
    self.optWindow = optWindow

  def regButton_onClick(self,event):
    self.regWindow.show()
    self.hide()

  def qsiButton_onClick(self,event):
    self.qsiWindow.show()
    self.hide()

  def optButton_onClick(self,event):
    self.optWindow.show()
    self.hide()

class RegWindow(QWidget):
  def __init__(self,mainWindow,parent=None):
    super(RegWindow,self).__init__(parent)

    self.x = []
    self.y = []
    self.mainWindow = mainWindow
    layout = QHBoxLayout()

    self.initLeft()
    self.initRight()
    layout.addWidget(self.left)
    layout.addWidget(self.right)

    self.move(0,0)
    # self.setFixedSize(420,300)
    self.left.move(0,0)
    self.setLayout(layout)
    self.setWindowTitle('CMSC 150 ~ Regression')
  
  def initLeft(self):
    self.left = QFrame()
    self.left.setFixedSize(250,320)
    layout = QVBoxLayout()

    openButton = QPushButton()
    openButton.setFixedSize(235,25)
    openButton.setIcon(QIcon('images/folder_open.png'))
    openButton.clicked.connect(self.file_dialog)

    self.table = QTableWidget(0,2)
    self.table.setHorizontalHeaderLabels(['X','Y'])
    # self.table.setReadOnly(True)
    self.table.setEditTriggers(QTableWidget.NoEditTriggers)
    self.table.setFixedSize(235,210)

    frame1 = QFrame()
    N = QLineEdit()
    runButton = QPushButton('go')
    runButton.setFixedSize(30,30)
    runButton.clicked.connect(lambda: self.go(N.text()))
    layout1 = QHBoxLayout()
    layout1.addWidget(QLabel('N: '))
    layout1.addWidget(N)
    layout1.addWidget(runButton)
    frame1.setLayout(layout1)

    layout.addWidget(openButton)
    layout.addWidget(self.table)
    layout.addWidget(frame1)
    self.left.move(0,0)
    self.left.setLayout(layout)
  
  def initRight(self):
    self.right = QFrame()
    self.right.resize(200,300)
    self.fxn = QLineEdit()
    self.fxn.setReadOnly(True)
    self.fxn.resize(150,100)

    frame1 = QFrame()
    layout1 = QFormLayout()
    self.input_ = QLineEdit()
    self.output_= QLineEdit()
    self.output_.setReadOnly(True)
    runButton = QPushButton('estimate')
    runButton.clicked.connect(self.estimate)
    layout1.addWidget(QLabel('X: '))
    layout1.addWidget(self.input_)
    layout1.addWidget(QLabel('f(X): '))
    layout1.addWidget(self.output_)
    layout1.addWidget(runButton)
    frame1.setLayout(layout1)

    layout = QFormLayout()
    layout.addWidget(QLabel('Estimating Functions:'))
    layout.addWidget(self.fxn)
    layout.addWidget(frame1)

    self.right.setLayout(layout)
  
  def estimate(self,event):
    try:
      fx = self.f(float(self.input_.text()))
    except Exception:
      fx = ''
    self.output_.setText(str(fx))

  def file_dialog(self):
    filename,filetype = QFileDialog.getOpenFileName(self,'Open File','~','CSV Files  (*.csv)')
    self.x,self.y = readCSV(filename)

    self.table.clear()
    i = len(self.x) - self.table.rowCount()
    while i > 0:
      self.table.insertRow(0)
      i -= 1
    for i in range(len(self.x)):
      self.table.setItem(i,0,QTableWidgetItem(str(self.x[i])))
      self.table.setItem(i,1,QTableWidgetItem(str(self.y[i])))

  def go(self,N):
    try:
      N = int(N)
    except Exception:
      N = 1
    fxn, f = pr.regression(self.x,self.y,N)
    self.fxn.setText(fxn)
    self.f = f

  def closeEvent(self,event):
    self.table.clear()
    self.x.clear()
    self.y.clear()
    self.f = None
    self.input_.setText('')
    self.output_.setText('')
    self.mainWindow.show()
    self.hide()
  
class QSIWindow(QWidget):
  def __init__(self,mainWindow,parent=None):
    super(QSIWindow,self).__init__(parent)

    self.x = []
    self.y = []
    self.mainWindow = mainWindow
    layout = QHBoxLayout()

    self.initLeft()
    self.initRight()
    layout.addWidget(self.left)
    layout.addWidget(self.right)

    # self.setFixedSize(420,300)
    self.setLayout(layout)
    self.setWindowTitle('CMSC 150 ~ Quadratic Spline Interpolation')
  
  def initLeft(self):
    self.left = QFrame()
    self.left.setFixedSize(250,320)
    layout = QVBoxLayout()

    openButton = QPushButton()
    openButton.setFixedSize(235,25)
    openButton.setIcon(QIcon('images/folder_open.png'))
    openButton.clicked.connect(self.file_dialog)
  
    self.table = QTableWidget(0,2)
    self.table.setHorizontalHeaderLabels(['X','Y'])
    self.table.setEditTriggers(QTableWidget.NoEditTriggers)
    self.table.setFixedSize(235,210)

    runButton = QPushButton('go')
    runButton.setFixedSize(235,25)
    runButton.clicked.connect(self.go)

    layout.addWidget(openButton)
    layout.addWidget(self.table)
    layout.addWidget(runButton)
    self.left.move(0,0)
    self.left.setLayout(layout)
  
  def initRight(self):
    self.right = QFrame()
    self.right.resize(200,300)
    self.fxns = QTableWidget(0,2)
    self.fxns.setHorizontalHeaderLabels(['f(x)','cond'])
    self.fxns.setFixedSize(360,110)

    frame1 = QFrame()
    layout1 = QFormLayout()
    self.input_ = QLineEdit()
    self.output_= QLineEdit()
    runButton = QPushButton('estimate')
    runButton.clicked.connect(self.estimate)
    layout1.addWidget(QLabel('X: '))
    layout1.addWidget(self.input_)
    layout1.addWidget(QLabel('f(X): '))
    layout1.addWidget(self.output_)
    layout1.addWidget(runButton)
    frame1.setLayout(layout1)

    layout = QVBoxLayout()
    layout.addWidget(QLabel('Estimating Functions:'))
    layout.addWidget(self.fxns)
    layout.addWidget(frame1)

    self.right.setLayout(layout)

  def estimate(self,event):
    try:
      fx = self.f(float(self.input_.text()))
    except Exception:
      fx = ''
    self.output_.setText(str(fx))

  def file_dialog(self):
    filename,filetype = QFileDialog.getOpenFileName(self,'Open File','~','CSV Files  (*.csv)')
    self.x,self.y = readCSV(filename)
    print(self.x)
    print(self.y)

    self.table.clear()
    i = len(self.x) - self.table.rowCount()
    while i > 0:
      self.table.insertRow(0)
      i -= 1
    for i in range(len(self.x)):
      self.table.setItem(i,0,QTableWidgetItem(str(self.x[i])))
      self.table.setItem(i,1,QTableWidgetItem(str(self.y[i])))

  def go(self,event):
    fxns, f = qsi.interpolation(self.x,self.y)
    for i in range(len(fxns)):
      self.fxns.insertRow(0)
    for i in range(len(fxns)):
      self.fxns.setItem(i,0,QTableWidgetItem(fxns[i][0]))
      self.fxns.setItem(i,1,QTableWidgetItem(fxns[i][1]))
    self.f = f
    
  def closeEvent(self,event):
    self.fxns.clear()
    self.table.clear()
    self.x.clear()
    self.y.clear()
    self.f = None
    self.input_.setText('')
    self.output_.setText('')
    self.mainWindow.show()
    self.hide()
  
class OptWindow(QWidget):
  def __init__(self,mainWindow,parent=None):
    super(OptWindow,self).__init__(parent)
    self.mainWindow = mainWindow
    # self.setLayout(layout)
    self.setWindowTitle('CMSC 150 ~ Optimization')
 
  def closeEvent(self,event):
    self.mainWindow.show()
    self.hide()


if __name__ == '__main__':

  app = QApplication([])

  mainWindow  = MainWindow()
  regWindow   = RegWindow(mainWindow)
  qsiWindow   = QSIWindow(mainWindow)
  optWindow   = OptWindow(mainWindow)

  mainWindow.setRegWindow(regWindow)
  mainWindow.setQSIWindow(qsiWindow)
  mainWindow.setOptWindow(optWindow)

  mainWindow.show()
  app.exec_()
