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
        fileName, _ = QFileDialog.getOpenFileName(None,"QFileDialog.getOpenFileName()", "","All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            self.list.append(fileName)
            file = open(fileName,"r")
            self.list.append(file.read())
            file.close()
            print(fileName)
            return fileName
        
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
            self.generateRegressor(score)
            
    
    def generateRegressor(self,score): #Function to Generate Regression Model by pressing the button
        self.textBrowser_2.clear()  #To empty the text boxes
        self.textBrowser_3.clear()
        df = pd.read_csv(fileName,sep="\s+")      # Need to automise the data parsing

        df.columns = ['Time', 'SOH']
        df.head()
        X = df[['SOH']].values
        y = df['Time'].values
        print(X)
        if score != 0:
            '''scoreary=[]
            scorearX=[X[len(X)-1]+1]
            print(scorearX)
            scoreary.append(score)
            np.append(scorearX,X)
            np.append(scoreary,y)'''
            y[len(y)-1] = score
            print(X)
            #y.concatenate(y[len(y)]+1)
            score = 0
        self.openWindow()

        #lr = LinearRegressionGD()
        def lin_regplot(X, y, model):
            plt.scatter(X, y, c='steelblue', edgecolor='white', s=70)
            plt.plot(X, model.predict(X), color='black', lw=2)
            return 


        slr = LinearRegression()
        slr.fit(X, y)
        y_pred = slr.predict(X)
        gradient = slr.coef_[0]
        y_intercept= slr.intercept_
        self.textBrowser_2.append(str(gradient))
        self.textBrowser_3.append(str(y_intercept))
        print(gradient)
        print(y_intercept)
        
        #Calculate day of failure
        day_of_failure= ((y[len(y)-1]+10)-y_intercept) / gradient #Add 10 to simulate difference from the nominal score
        self.textBrowser_5.append(str(day_of_failure))
        
        #NEED TO APPEND SCORE AND DAY OF FAILURE TO MAIN ARRAY
        
        lin_regplot(X, y, slr)
        plt.xlabel('Time in days')
        plt.ylabel('Current score')

        #plt.savefig('images/10_07.png', dpi=300)
        plt.show()
        
        
        
        
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
        self.label_5.setGeometry(QtCore.QRect(700, 250, 60, 16))
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
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.statusbar.setStatusTip(_translate("MainWindow", "hh"))


class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.show()  

app = QApplication(sys.argv)
w = AppWindow()
w.show()
sys.exit(app.exec_())
print("Hello World")