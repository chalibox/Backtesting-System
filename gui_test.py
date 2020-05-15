'''
This is the first version of the GUI
'''


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QMessageBox
from PyQt5.QtGui import QIcon

from test import *

# Create the main window
class Ui_MainWindow(object):
    
    def openWindow(self):
      
      '''
      Define a function to open the sub window when correct file is imported
      '''

      self.window = QtWidgets.QMainWindow()
      self.ui = Ui_OtherWindow()

      # Take the file path parameter in order to check correctness of file type
      self.ui.setupUi(self.window, self.file_path)
      self.window.show()

    
    def setupUi(self, MainWindow):
        
        '''
        Set up the style for the main window
        '''

        # Basic window geometry
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 752)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        # Create main title
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(140, 10, 561, 91))
        font = QtGui.QFont()
        font.setFamily("Bookman Old Style")
        font.setPointSize(48)
        self.label.setFont(font)
        self.label.setAutoFillBackground(False)
        self.label.setObjectName("label")
        
        # Create sub title
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(220, 420, 491, 161))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(18)
        font.setItalic(True)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        
        # Create description
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(290, 640, 281, 51))
        font = QtGui.QFont()
        font.setFamily("Arial Narrow")
        font.setPointSize(16)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        
        # Create foot note
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(110, 110, 591, 341))
        self.label_4.setText("")
        self.label_4.setPixmap(QtGui.QPixmap("775889491-min.jpg"))
        self.label_4.setObjectName("label_4")
        
        # Create the button that will trigger the open file event 
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(270, 540, 251, 81))
        font = QtGui.QFont()
        font.setFamily("Arial Narrow")
        font.setPointSize(16)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        
        # Define menu bar section for use in the future if needed
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # Set text and functions for the above widgets
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    
    def retranslateUi(self, MainWindow):
        
        '''
        Main function for setting readable text and calling event functions
        '''

        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "V1.0"))
        self.label.setText(_translate("MainWindow", "Backtest System"))
        self.label_2.setText(_translate("MainWindow", "Test your strategy within seconds !"))
        self.label_3.setText(_translate("MainWindow", "-  Forex   Stocks   Bitcoin  -"))
        self.pushButton.setText(_translate("MainWindow", "Open File"))
        # connect the function that handles the button
        self.pushButton.clicked.connect(self.pushButton_handler)

    
    def pushButton_handler(self):

        '''
        This function will be called when the button is clicked from the main window
        '''
        
        try:
          
          # This function opens the file selector
          if self.open_dialog_box() == False:
            
            # if file type is not correct, shows error message
            self.show_popup()
          else:
            
            # If file type is correct, open the sub window
            self.openWindow()
        
        except:
          self.show_popup()

          
    def open_dialog_box(self):

        '''
        This function is used to open the file selector
        '''

        # Read file path
        filename = QFileDialog.getOpenFileName()
        self.file_path = filename[0]
        # Open file 
        with open(self.file_path, "r") as f:
          # This is to ensure that the file contains historical data for a ticker
          if 'date' and 'open' and 'high' and 'low' and 'close' in f.readline().lower():
            return self.file_path
          else:
            return False

    
    def show_popup(self):

      '''
      Shows error message
      '''

      msg = QMessageBox()
      msg.setWindowTitle('Error')
      msg.setText('Please select a CSV file. Date, Open, High, Low, Close must be included in the headline. Make sure there is data to read.')
      x = msg.exec_()


# Create sub window for parameters input
class Ui_OtherWindow(object):
    
    def setupUi(self, OtherWindow, path):

        # read file path from main window class
        self.file_path = path
        
        # Set up Geometry for the window
        OtherWindow.setObjectName("OtherWindow")
        OtherWindow.resize(508, 602)
        self.centralwidget = QtWidgets.QWidget(OtherWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        # Set up the group box that holds all the input area
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(40, 20, 431, 581))
        font = QtGui.QFont()
        font.setFamily("Microsoft Sans Serif")
        font.setPointSize(20)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")

        # Ask for the first input
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(20, 60, 181, 41))
        font = QtGui.QFont()
        font.setFamily("Microsoft Sans Serif")
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit.setGeometry(QtCore.QRect(210, 65, 151, 35))
        self.lineEdit.setObjectName("lineEdit")
        
        # Ask for the second input
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(20, 140, 231, 41))
        font = QtGui.QFont()
        font.setFamily("Microsoft Sans Serif")
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_2.setGeometry(QtCore.QRect(210, 140, 151, 35))
        self.lineEdit_2.setObjectName("lineEdit_2")
        
        # Ask for the third input
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(20, 220, 211, 31))
        font = QtGui.QFont()
        font.setFamily("Microsoft Sans Serif")
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_3.setGeometry(QtCore.QRect(210, 215, 151, 35))
        self.lineEdit_3.setObjectName("lineEdit_3")
        
        # Ask for the fourth input
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(20, 290, 141, 31))
        font = QtGui.QFont()
        font.setFamily("Microsoft Sans Serif")
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.lineEdit_4 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_4.setGeometry(QtCore.QRect(210, 290, 151, 35))
        self.lineEdit_4.setObjectName("lineEdit_4")
        
        # Ask for the fifth input
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setGeometry(QtCore.QRect(20, 370, 161, 21))
        font = QtGui.QFont()
        font.setFamily("Microsoft Sans Serif")
        font.setPointSize(12)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.lineEdit_5 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_5.setGeometry(QtCore.QRect(210, 365, 151, 35))
        self.lineEdit_5.setObjectName("lineEdit_5")
        
        # Ask for the sixth input
        self.label_6 = QtWidgets.QLabel(self.groupBox)
        self.label_6.setGeometry(QtCore.QRect(20, 450, 191, 21))
        font = QtGui.QFont()
        font.setFamily("Microsoft Sans Serif")
        font.setPointSize(12)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.lineEdit_6 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_6.setGeometry(QtCore.QRect(210, 440, 151, 35))
        self.lineEdit_6.setObjectName("lineEdit_6")
        
        # Buttons below are the help buttons that will show help message when clicked
        self.pushButton = QtWidgets.QPushButton(self.groupBox)
        self.pushButton.setGeometry(QtCore.QRect(380, 70, 21, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_2.setGeometry(QtCore.QRect(380, 145, 21, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_3.setGeometry(QtCore.QRect(380, 220, 21, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_4.setGeometry(QtCore.QRect(380, 295, 21, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_5.setGeometry(QtCore.QRect(380, 370, 21, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.pushButton_5.setFont(font)
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_6 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_6.setGeometry(QtCore.QRect(380, 445, 21, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.pushButton_6.setFont(font)
        self.pushButton_6.setObjectName("pushButton_6")

        # This button is the run backtest button, runs backtest on click
        self.pushButton_7 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_7.setGeometry(QtCore.QRect(140, 510, 151, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_7.setFont(font)
        self.pushButton_7.setObjectName("pushButton_7")
        
        # Define menu bar section for use in the future if needed
        OtherWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(OtherWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1122, 23))
        self.menubar.setObjectName("menubar")
        OtherWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(OtherWindow)
        self.statusbar.setObjectName("statusbar")
        OtherWindow.setStatusBar(self.statusbar)

        # Set text and functions for the above widgets
        self.retranslateUi(OtherWindow)
        QtCore.QMetaObject.connectSlotsByName(OtherWindow)

   
    def retranslateUi(self, OtherWindow):
        _translate = QtCore.QCoreApplication.translate
        OtherWindow.setWindowTitle(_translate("OtherWindow", "V1.0"))
        self.groupBox.setTitle(_translate("OtherWindow", "Parameter Setting"))
        self.label.setText(_translate("OtherWindow", "Number of random lines :"))
        self.label_2.setText(_translate("OtherWindow", "Threshold Percentage :"))
        self.label_3.setText(_translate("OtherWindow", "Learning Period :"))
        self.label_4.setText(_translate("OtherWindow", "Test Period :"))
        self.label_5.setText(_translate("OtherWindow", "Predict x days ahead :"))
        self.label_6.setText(_translate("OtherWindow", "Initial Money :"))
        self.pushButton.setText(_translate("OtherWindow", "?"))
        self.pushButton_2.setText(_translate("OtherWindow", "?"))
        self.pushButton_3.setText(_translate("OtherWindow", "?"))
        self.pushButton_4.setText(_translate("OtherWindow", "?"))
        self.pushButton_5.setText(_translate("OtherWindow", "?"))
        self.pushButton_6.setText(_translate("OtherWindow", "?"))
        self.pushButton_7.setText(_translate("OtherWindow", "Run Backtest"))

        # Calling the run backtest function on click
        self.pushButton_7.clicked.connect(self.run_back_test)

        # Shows help message on click
        self.pushButton.clicked.connect(lambda: self.show_popup('Help', 'Please read documentation.'))
        self.pushButton_2.clicked.connect(lambda: self.show_popup('Help', 'Please read documentation.'))
        self.pushButton_3.clicked.connect(lambda: self.show_popup('Help', 'Please read documentation.'))
        self.pushButton_4.clicked.connect(lambda: self.show_popup('Help', 'Please read documentation.'))
        self.pushButton_5.clicked.connect(lambda: self.show_popup('Help', 'Please read documentation.'))
        self.pushButton_6.clicked.connect(lambda: self.show_popup('Help', 'Please read documentation.'))
    
      
    def run_back_test(self):

        '''
        Functions used in this function are imported from test.py.
        These functions handle the strategy part and the calculation part.
        '''

        try:
          
          # Check all inputs
          if check_input(int(self.lineEdit.text()), float(self.lineEdit_2.text()), int(self.lineEdit_3.text()), int(self.lineEdit_4.text()), int(self.lineEdit_5.text()), float(self.lineEdit_6.text())) == True:

              # Form the parameter list as needed for the run_test function
              parameter_list = [int(self.lineEdit.text()), float(self.lineEdit_2.text()), int(self.lineEdit_3.text()), int(self.lineEdit_4.text()), int(self.lineEdit_5.text()), float(self.lineEdit_6.text())]
              try:

                # Read the data 
                data = read_data(self.file_path)

                # Backtest begins
                self.show_popup('Warning', "Backtest started, it might take a few minutes, please don't close the window.")

                # This function does all the calculation and plot the final result
                run_test(data, parameter_list, self.file_path)
              except:

                # Sometimes the date column is not readable and need to be edited
                self.show_popup('false', 'Please edit the date column of the CSV file and re-open it. The format is not readable.')
                return
          else:

              # Shows error message when inputs contain negative number
              self.show_popup('false', 'inputs are not valid. Please check the help video for input types.')
        except:

            # shows error message when inputs contain invalid symbols
            self.show_popup('false', 'inputs are not valid. Please check the help video for input types.')

    
    def show_popup(self, title, message):

        '''
        Function that shows message when triggered
        '''

        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        x = msg.exec_()


# Runs UI
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())