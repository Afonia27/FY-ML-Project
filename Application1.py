#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 14 20:22:32 2018
@author: AfanasiChihaioglo
"""
import sys
import obd
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QSizePolicy, QDialog,QPushButton, QVBoxLayout
from PyQt5 import QtCore, QtGui, QtWidgets
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
import random
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

      # Include the GUI.py
# -*- coding: utf-8 -*-
global Days
Days = np.empty([1, 1])
global Error_scores
Error_scores = np.empty([1,1])

class Window(QDialog):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        # a figure instance to plot on
        self.figure = plt.figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)
        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        # Just some button connected to `plot` method
        #self.plot

        # set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def plot(self):
        ''' plot some random stuff '''
        # random data
        data = [random.random() for i in range(10)]

        # instead of ax.hold(False)
        self.figure.clear()

        # create an axis
        ax = self.figure.add_subplot(111)

        # discards the old graph
        # ax.hold(False) # deprecated, see above

        # plot data
        ax.plot(data, '*-')

        # refresh canvas
        self.canvas.draw()



class Ui_MainWindow(object):         # All of these will be imported in header
    
    def openWindow(self):
        self.window = Window()
        self.window.show()
    
    def openFile(self):    #Function to open File by pressing the button
        options = QFileDialog.Options()
        global fileName  #Global in order to be read by other functions
        global Days
        global Error_scores
        fileName, _ = QFileDialog.getOpenFileName(None,"QFileDialog.getOpenFileName()", "","All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            self.list.append(fileName)
            file = open(fileName,"r")
            self.list.append(file.read())
            file.close()
            print(fileName)
            
        df = pd.read_csv(fileName,sep="\s+")      # Need to automise the data parsing

        df.columns = ['Error Scores', 'Days']
        df.head()
        Days = df[['Days']].values
        Error_scores = df['Error Scores'].values  #State of Healh 
        print(str(Error_scores.ndim)+str(Error_scores.shape))
        
        
    def connectVehicle(self):
        connection = obd.OBD() #Establish the connection to the vehicle
        if connection.is_connected() == True:
            self.list.append("Connection is successfully established")
        else:
            self.list.append("Connection could not be established")
        
        cmd = obd.commands.RPM # select an OBD command to check RPM to verify the connection
        response = connection.query(cmd) # send the command, and parse the response
        self.list.append(response.value)
        response = connection.query(obd.commands.GET_DTC)
        self.list.append(response.value)
    
                
    def loadDTC(self):
        options = QFileDialog.Options()
        fileDTC, _ = QFileDialog.getOpenFileName(None,"QFileDialog.getOpenFileName()", "","All Files (*);;Text Files (*.txt)", options=options)
        if fileDTC:
            self.list.append(fileDTC)
            file = open(fileDTC,"r")
            self.list.append(file.read())
            file.close()
            print(fileDTC)
            df = pd.read_csv(fileDTC,header=0, names=['DTC'],sep="\s+")
            global score
            score = 0
            undefined = 0
            DTC = ""
            for i in range(0,len(df['DTC'])):
                DTC = list(df['DTC'][i])
                if DTC[0] == "P":
                    score+=3
                elif DTC[0] == "C":
                    score+=2
                elif DTC[0] == "B":
                    score+=1
                else:
                    undefined+=1
            self.textBrowser_4.clear()
            self.textBrowser_4.append(str(score))
            
            print("Undefined:"+ str(undefined))
            #self.generateRegressor(score)
            
    
    #Function to Generate Regression Model by pressing the 'Generate' button, 
    #should take X and y as input
    def generateRegressor(self,score): 
        global Days
        global Error_scores
        self.textBrowser_2.clear()  #To empty the text boxes
        self.textBrowser_3.clear()
        print("This is X:",Days)
        print("Shape is:",Error_scores.ndim)
        if score != 0:
            '''scoreary=[]
            scorearX=[X[len(X)-1]+1]
            print(scorearX)
            scoreary.append(score)
            np.append(scorearX,X)
            np.append(scoreary,y)'''
            Error_scores[len(Error_scores)-1] = score
            print(Days)
            #y.concatenate(y[len(y)]+1)
            score = 0
        self.openWindow()

        #Function which takes arrays as an input and produces the graph
        def lin_regplot(X, y, model):
            plt.scatter(X, y, c='steelblue', edgecolor='white', s=70)
            plt.plot(X, model.predict(X), color='black', lw=2)
            return 

        #Create linear regressor and append values to boxes
        slr = LinearRegression()    
        slr.fit(Days, Error_scores)
        y_pred = slr.predict(Days)
        gradient = slr.coef_[0]
        y_intercept= slr.intercept_
        self.textBrowser_2.append(str(gradient))
        self.textBrowser_3.append(str(y_intercept))
        print(gradient)
        print(y_intercept)
        
        #Calculate the new Error score
        Nominal_Error_Score = 45
        Last_Error_Score = Error_scores[len(Error_scores)-1]
        New_Error_Score = Last_Error_Score+abs(Nominal_Error_Score-Last_Error_Score)
        
        if New_Error_Score >= Nominal_Error_Score:
            self.list.append("IT IS TIME TO CHECK THE VEHICLE")
        
        
        
        #Calculate day of failure
        day_of_failure= (New_Error_Score-y_intercept) / gradient #Add 10 to simulate difference from the nominal score
        self.textBrowser_5.clear()
        self.textBrowser_5.append(str(day_of_failure))
        #print(X[[0][len(X)-1]])
        #print(X[[len(X)-1][0]])
        #NEED TO APPEND SCORE AND DAY OF FAILURE TO MAIN ARRAY
        
        lin_regplot(Days, Error_scores, slr)
        plt.xlabel('Time in days')
        plt.ylabel('Current score')
        #Title = str("Score=",str(New_Error_Score))
        #"Score="+New_Error_Score+" Day of failure="+day_of_failure
        plt.title("Score= "+str(Last_Error_Score)+" Day of failure="+str(int(day_of_failure)))
        
        #Plot red dotted lines and extend the line
        plt.plot([0,day_of_failure],[New_Error_Score,New_Error_Score],'r--')  
        plt.plot([day_of_failure,day_of_failure],[0,New_Error_Score],'r--')
        plt.plot([0,day_of_failure],[y_intercept,New_Error_Score],'k')

        plt.show()
        return Days
        
        
    def addValue(self):
        #print(Days.shape)
        global Days
        global Error_scores
        print(Days)
        print(Error_scores)
        Days = np.append(Days,[Days[len(Days)-1]+1]) # Add the new Day value on day-axis to host new score
        Days = np.reshape(Days,(np.size(Days),-1)) # Reshape the array to be in correct format
        Error_scores = np.append(Error_scores,[45]) # Add the new point from the text menu
        print(Days)
        print(Error_scores)
        

#        value = 15
#        X= self.generateRegressor(score = 0)
#        print(X)
#        print(X.shape,X.ndim)
        


        
    
    # Define the HMI
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(754, 436)
        MainWindow.setWhatsThis("")
        MainWindow.setAutoFillBackground(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(40, 110, 113, 32))
        self.pushButton.setObjectName("pushButton")
        self.list = QtWidgets.QTextBrowser(self.centralwidget)
        self.list.setGeometry(QtCore.QRect(220, 30, 131, 291))
        self.list.setObjectName("list")
        #self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        #self.graphicsView.setGeometry(QtCore.QRect(410, 30, 256, 192))
        #self.graphicsView.setObjectName("graphicsView")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(600, 250, 60, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(270, 10, 60, 16))
        self.label_2.setObjectName("label_2")
        self.textBrowser_2 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_2.setGeometry(QtCore.QRect(410, 270, 50, 21))
        self.textBrowser_2.setObjectName("textBrowser_2")
        self.textBrowser_3 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_3.setGeometry(QtCore.QRect(500, 270, 50, 21))
        self.textBrowser_3.setObjectName("textBrowser_3")
        self.textBrowser_4 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_4.setGeometry(QtCore.QRect(590, 270, 50, 21))
        self.textBrowser_4.setObjectName("textBrowser_4")
        self.textBrowser_5 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_5.setGeometry(QtCore.QRect(680, 270, 50, 21))
        self.textBrowser_5.setObjectName("textBrowser_5")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(400, 250, 60, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(500, 250, 60, 16))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(670, 250, 80, 16))
        self.label_5.setObjectName("label_4")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(40, 160, 113, 32))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(40, 210, 113, 32))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget) #Button for vehicle connection
        self.pushButton_4.setGeometry(QtCore.QRect(15, 260, 180, 32))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget) 
        self.pushButton_5.setGeometry(QtCore.QRect(15, 310, 180, 32))
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_6 = QtWidgets.QPushButton(self.centralwidget) 
        self.pushButton_6.setGeometry(QtCore.QRect(15, 360, 180, 32))
        self.pushButton_6.setObjectName("pushButton_6")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 754, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        self.pushButton.clicked.connect(self.openFile)
        self.pushButton_3.clicked.connect(self.loadDTC)
        #self.pushButton_2.clicked.connect(self.openWindow)
        self.pushButton_2.clicked.connect(self.generateRegressor)
        self.pushButton_4.clicked.connect(self.connectVehicle)
        self.pushButton_6.clicked.connect(self.addValue)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Program"))
        self.pushButton.setText(_translate("MainWindow", "Load file"))
        self.label.setText(_translate("MainWindow", "Score"))
        self.label_2.setText(_translate("MainWindow", "List"))
        self.label_3.setText(_translate("MainWindow", "Gradient"))
        self.label_4.setText(_translate("MainWindow", "Intercept"))
        self.label_5.setText(_translate("MainWindow", "Failure day"))
        self.pushButton_2.setText(_translate("MainWindow", "Generate"))
        self.pushButton_3.setText(_translate("MainWindow", "Load DTC's"))
        self.pushButton_4.setText(_translate("MainWindow", "Connect to the vehicle"))
        self.pushButton_5.setText(_translate("MainWindow", "Add point (DTC)"))
        self.pushButton_6.setText(_translate("MainWindow", "Add point (Value)"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.statusbar.setStatusTip(_translate("MainWindow", "Welcome!"))


class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.show()  
    

# The initiation of the program
        
if __name__ == "__main__":
    Days = np.empty([1, 1])
    def run_app():
        app = QApplication(sys.argv)
        window = AppWindow()
        window.show()
        app.exec_()
    run_app()