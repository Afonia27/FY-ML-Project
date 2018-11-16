#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 14 20:22:32 2018

@author: AfanasiChihaioglo
"""
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5 import QtCore, QtGui, QtWidgets
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression


      # Include the GUI.py
# -*- coding: utf-8 -*-

def func():
         print("Clicked")

class LinearRegressionGD(object):

    def __init__(self, eta=0.001, n_iter=20):
        self.eta = eta
        self.n_iter = n_iter

    def fit(self, X, y):
        self.w_ = np.zeros(1 + X.shape[1])
        self.cost_ = []

        for i in range(self.n_iter):
            output = self.net_input(X)
            errors = (y - output)
            self.w_[1:] += self.eta * X.T.dot(errors)
            self.w_[0] += self.eta * errors.sum()
            cost = (errors**2).sum() / 2.0
            self.cost_.append(cost)
        return self

    def net_input(self, X):
        return np.dot(X, self.w_[1:]) + self.w_[0]

    def predict(self, X):
        return self.net_input(X)

class Ui_MainWindow(object):         # All of these will be imported in header
    
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
    
    def generateRegressor(self): #Function to Generate Regression Model by pressing the button
        print (fileName)
        df = pd.read_csv(fileName,sep="\s+")

        df.columns = ['CRIM', 'ZN', 'INDUS', 'CHAS', 
              'NOX', 'RM', 'AGE', 'DIS', 'RAD', 
              'TAX', 'PTRATIO', 'B', 'LSTAT', 'MEDV']
        df.head()
        X = df[['RM']].values
        y = df['MEDV'].values



        lr = LinearRegressionGD()
        def lin_regplot(X, y, model):
            plt.scatter(X, y, c='steelblue', edgecolor='white', s=70)
            plt.plot(X, model.predict(X), color='black', lw=2)    
            return 


        slr = LinearRegression()
        slr.fit(X, y)
        y_pred = slr.predict(X)
        self.textBrowser_2.append(str(slr.coef_[0]))
        self.textBrowser_3.append(str(slr.intercept_))
        print(slr.coef_[0])
        print(slr.intercept_)


        lin_regplot(X, y, slr)
        plt.xlabel('Average number of rooms [RM]')
        plt.ylabel('Price in $1000s [MEDV]')

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
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(410, 30, 256, 192))
        self.graphicsView.setObjectName("graphicsView")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(510, 10, 60, 16))
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
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(400, 250, 60, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(500, 250, 60, 16))
        self.label_4.setObjectName("label_4")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(40, 160, 113, 32))
        self.pushButton_2.setObjectName("pushButton_2")
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
        self.pushButton_2.clicked.connect(self.generateRegressor)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Program"))
        self.pushButton.setText(_translate("MainWindow", "Load file"))
        self.label.setText(_translate("MainWindow", "Graph"))
        self.label_2.setText(_translate("MainWindow", "List"))
        self.label_3.setText(_translate("MainWindow", "Gradient"))
        self.label_4.setText(_translate("MainWindow", "Intercept"))
        self.pushButton_2.setText(_translate("MainWindow", "Generate"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.statusbar.setStatusTip(_translate("MainWindow", "hh"))

class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.show()  

print("Hello World")
app = QApplication(sys.argv)
w = AppWindow()
w.show()
sys.exit(app.exec_())
print("Hello World")