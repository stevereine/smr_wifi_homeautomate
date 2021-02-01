#import socket, sys, time, threading, pyqtgraph as pg, numpy

#import PyQt5.QtCore

#from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit

import sys, socket, numpy, time, threading

import PyQt5

from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtCore import QTimer

from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit

from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg

from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg

from PyQt5.QtWidgets import QApplication, QMainWindow

from PyQt5.QtGui import QColor

from datetime import datetime

import math

import faulthandler

class demowind(QWidget):
    #def datad_function(self, parent=None):
    #    dw.scratchpad2.setText("datad_function called")    
    #    mylog()
            
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        
        faulthandler.enable()
        
        self.setGeometry(200, 200, 780, 650)
        self.setWindowTitle('Weather Station')

        myfont = PyQt5.QtGui.QFont('SansSerif', 13)

        yellowpalette = PyQt5.QtGui.QPalette()
        #yellowpalette.setColor(PyQt5.QtGui.QPalette.Text, QColor(255,165,0))
        yellowpalette.setColor(PyQt5.QtGui.QPalette.Text, PyQt5.QtCore.Qt.red)

        cyanpalette = PyQt5.QtGui.QPalette()
        cyanpalette.setColor(PyQt5.QtGui.QPalette.Text, PyQt5.QtCore.Qt.blue)

        redpalette = PyQt5.QtGui.QPalette()
        redpalette.setColor(PyQt5.QtGui.QPalette.Text, PyQt5.QtCore.Qt.red)

        bluepalette = PyQt5.QtGui.QPalette()
        bluepalette.setColor(PyQt5.QtGui.QPalette.Text, PyQt5.QtCore.Qt.blue)

        greenpalette = PyQt5.QtGui.QPalette()
        greenpalette.setColor(PyQt5.QtGui.QPalette.Text, PyQt5.QtCore.Qt.green)

        datad=QPushButton('data\r\ndump', self)
        datad.setFont(myfont)
        datad.setGeometry(10, 10, 90, 620)
        datad.clicked.connect(self.datad_function)

        self.textfield=QLineEdit(self)
        self.textfield.setFont(myfont)
        self.textfield.setGeometry(120, 10, 630, 50)
        self.textfield.setText("time:")

        self.identfield2=QLineEdit(self)
        self.identfield2.setFont(myfont)
        self.identfield2.setGeometry(120, 80, 310, 50)
        self.identfield2.setText("IP: 192.168.1.121")

        self.tempfield2=QLineEdit(self)
        self.tempfield2.setAutoFillBackground(True)
        redpalette.setColor(self.tempfield2.backgroundRole(), PyQt5.QtCore.Qt.white)
        self.tempfield2.setPalette(redpalette)
        self.tempfield2.setFont(myfont)
        self.tempfield2.setGeometry(120, 140, 310, 50)
        self.tempfield2.setText("inside temperature:")        

        self.humidfield2=QLineEdit(self)
        self.humidfield2.setAutoFillBackground(True)
        bluepalette.setColor(self.humidfield2.backgroundRole(), PyQt5.QtCore.Qt.white)
        self.humidfield2.setPalette(bluepalette)
        self.humidfield2.setFont(myfont)
        self.humidfield2.setGeometry(120, 200, 310, 50)
        self.humidfield2.setText("inside humidity:")

        self.pressfield2=QLineEdit(self)
        self.pressfield2.setAutoFillBackground(True)
        greenpalette.setColor(self.pressfield2.backgroundRole(), PyQt5.QtCore.Qt.white)
        self.pressfield2.setPalette(greenpalette)
        self.pressfield2.setFont(myfont)
        self.pressfield2.setGeometry(440, 140, 310, 50)
        self.pressfield2.setText("inside atm pressure:")

        self.battfield2=QLineEdit(self)
        self.battfield2.setFont(myfont)
        self.battfield2.setGeometry(440, 200, 310, 50)
        self.battfield2.setText("battery voltage:")

        self.identfield3=QLineEdit(self)
        self.identfield3.setFont(myfont)
        self.identfield3.setGeometry(120, 300, 310, 50)
        self.identfield3.setText("IP: 192.168.1.113")

        self.tempfield3=QLineEdit(self)
        self.tempfield3.setAutoFillBackground(True)
        yellowpalette.setColor(self.tempfield3.backgroundRole(), PyQt5.QtCore.Qt.white)
        self.tempfield3.setPalette(redpalette)
        self.tempfield3.setFont(myfont)
        self.tempfield3.setGeometry(120, 360, 310, 50)
        self.tempfield3.setText("outside temperature:")

        self.humidfield3=QLineEdit(self)
        self.humidfield3.setAutoFillBackground(True)
        cyanpalette.setColor(self.humidfield3.backgroundRole(), PyQt5.QtCore.Qt.white)
        self.humidfield3.setPalette(bluepalette)
        self.humidfield3.setFont(myfont)
        self.humidfield3.setGeometry(120, 420, 310, 50)
        self.humidfield3.setText("outside humidity:")

        self.pressfield3=QLineEdit(self)
        self.pressfield3.setAutoFillBackground(True)
        #greenpalette.setColor(self.pressfield3.backgroundRole(), PyQt5.QtCore.Qt.black)
        self.pressfield3.setPalette(greenpalette)
        self.pressfield3.setFont(myfont)
        self.pressfield3.setGeometry(440, 360, 310, 50)
        self.pressfield3.setText("outside atm pressure:")

        self.battfield3=QLineEdit(self)
        self.battfield3.setFont(myfont)
        self.battfield3.setGeometry(440, 420, 310, 50)
        self.battfield3.setText("battery voltage:")

        self.scratchpad2=QLineEdit(self)
        self.scratchpad2.setFont(myfont)
        self.scratchpad2.setGeometry(120, 510, 630, 50)
        self.scratchpad2.setText("scratchpad2")

        self.scratchpad3=QLineEdit(self)
        self.scratchpad3.setFont(myfont)
        self.scratchpad3.setGeometry(120, 580, 630, 50)
        self.scratchpad3.setText("scratchpad3")

        self.temp_array2 = numpy.zeros(1000)
        self.humid_array2 = numpy.zeros(1000)
        self.press_array2 = 29.1 + numpy.zeros(1000)
        self.batt_array2 = numpy.zeros(1000)
        self.x2 = numpy.zeros(1000)

        self.temp_array3 = numpy.zeros(1000)
        self.humid_array3 = numpy.zeros(1000)
        self.press_array3 = 29.1 + numpy.zeros(1000)
        self.batt_array3 = numpy.zeros(1000)
        self.x3 = numpy.zeros(1000)
        
        self.time_array = numpy.zeros(1000)

        self.temp_plt=pg.plot()
        self.press_plt=pg.plot()

        pg.setConfigOptions(antialias = True);
        #view = pg.GraphicsView()
        #layout = pg.GraphicsLayout()
        #view.setCentralItem(layout)
        #view.resize(2000,400)

        #self.scratchpad2.setText("sizing")
        #self.scratchpad3.setText("sizing")

        self.temp_plt.setBackground('w')
        self.temp_plt.resize(1000,850)
        
        self.press_plt.setBackground('w')
        self.press_plt.resize(1000,700)
        
        #self.scratchpad2.setText("sized")
        #self.scratchpad3.setText("sized")   

        self.p12=self.temp_plt.plotItem
        self.p12.showAxis('right')
        self.p12.setYRange(0,100)
        
        self.p13=self.press_plt.plotItem
        self.p13.showAxis('right')
        self.p13.setYRange(29,30.5)
        
        self.p22=pg.ViewBox()
        self.p32=pg.ViewBox()
        self.p42=pg.ViewBox()
        
        self.p23=pg.ViewBox()
        
        self.timeplot=pg.ViewBox()
        
        self.p12.scene().addItem(self.p22)
        self.p12.scene().addItem(self.p32)
        self.p12.scene().addItem(self.p42)

        self.p13.scene().addItem(self.p23)
        
        self.p12.scene().addItem(self.timeplot)

        self.p12.getAxis('right').linkToView(self.p22)
        self.p12.getAxis('right').linkToView(self.p32)
        self.p12.getAxis('right').linkToView(self.p42)
        #self.p12.getAxis('left').linkToView(self.p32)
        
        self.p13.getAxis('right').linkToView(self.p23)
        #self.p13.getAxis('left').linkToView(self.p33)
        
        self.p12.getAxis('left').linkToView(self.timeplot)
        
        self.p22.setYRange(0,100)
        self.p32.setYRange(0,100)
        self.p42.setYRange(0,100)

        self.p23.setYRange(29,30.5)
        
        self.timeplot.setYRange(0,100)
        
        self.p22.setXLink(self.p12)
        self.p32.setXLink(self.p12)
        self.p42.setXLink(self.p12)

        self.p23.setXLink(self.p13)
        
        self.timeplot.setXLink(self.p12)
        
        self.p12.setGeometry(self.p12.vb.sceneBoundingRect())
        self.p22.setGeometry(self.p12.vb.sceneBoundingRect())
        self.p32.setGeometry(self.p12.vb.sceneBoundingRect())
        self.p42.setGeometry(self.p12.vb.sceneBoundingRect())

        self.p13.setGeometry(self.p13.vb.sceneBoundingRect())
        self.p23.setGeometry(self.p13.vb.sceneBoundingRect())
        
        self.timeplot.setGeometry(self.p13.vb.sceneBoundingRect())

        #self.mylegend = self.plt.addLegend((100,100),(50,50))
        self.my_temp_legend = self.temp_plt.addLegend()
        self.my_press_legend = self.press_plt.addLegend()

        #self.legend2 = pg.LegendItem()
        #self.legend3 = pg.LegendItem()
        #self.p2.addItem(self.legend2)
        #self.p3.addItem(self.legend3)
        
        #self.curve13=self.plt.plot(x=[] , y=[], pen = pg.mkPen(color=(255,165,0), width=4), name="Outside temperature", style=PyQt5.QtCore.Qt.DotLine)        
        self.curve12=self.temp_plt.plot(x=[] , y=[], pen = pg.mkPen('r', width=6), name="inside temperature", style=PyQt5.QtCore.Qt.DotLine)        
        self.curve13=self.press_plt.plot(x=[] , y=[], pen = pg.mkPen('g', width=6), name="inside air pressure", style=PyQt5.QtCore.Qt.DotLine)        
         
        self.curve22=pg.PlotCurveItem(pen = pg.mkPen('r', width=3), name="outside temperature", style=PyQt5.QtCore.Qt.DotLine)
        self.curve32=pg.PlotCurveItem(pen = pg.mkPen('b', width=6), name="inside humidity", style=PyQt5.QtCore.Qt.DotLine)
        self.curve42=pg.PlotCurveItem(pen = pg.mkPen('b', width=3), name="outside humidity", style=PyQt5.QtCore.Qt.DotLine)

        self.curve23=pg.PlotCurveItem(pen = pg.mkPen('g', width=3), name="outside air pressure")
        
        self.curve_tp=pg.PlotCurveItem(pen = pg.mkPen(QColor(128,128,128), width=4), name="time")

        #self.my_temp_legend.addItem(self.curve12, name = self.curve12.opts['name'])
        self.my_temp_legend.addItem(self.curve22, name = self.curve22.opts['name'])
        self.my_temp_legend.addItem(self.curve32, name = self.curve32.opts['name'])
        self.my_temp_legend.addItem(self.curve42, name = self.curve42.opts['name'])
        
        #self.my_press_legend.addItem(self.curve13, name = self.curve13.opts['name'])
        self.my_press_legend.addItem(self.curve23, name = self.curve23.opts['name'])

        #self.p12.addItem(self.curve12)
        self.p22.addItem(self.curve22)
        self.p32.addItem(self.curve32)
        self.p42.addItem(self.curve42)
        
        #self.p13.addItem(self.curve13)
        self.p23.addItem(self.curve23) 
                                       
        self.timeplot.addItem(self.curve_tp)                                       

        #self.plt_temp = self.plt.plot(self.x, self.temp_array, title = "my plot", pen = pg.mkPen('r', width=4))
        #self.plt_humid = self.plt.plot(self.x, self.humid_array, title = "my plot", pen = pg.mkPen('g', width=4))
        #self.plt_press = self.plt.plot(self.x, self.press_array, title = "my plot", pen = pg.mkPen('b', width=4))

        #threading.Timer(10.0, data_display).start()
        #threading.Timer(10.0, datad_function).start()
        
        #self.scratchpad2.setText("about to start QTimer") 
        
        self.timer = QTimer()
        self.timer.setInterval(120000)
        self.timer.timeout.connect(self.datad_function)
        self.timer.start()
        
        #self.scratchpad2.setText("QTimer should have started")
        
    def test_function(self, parent=None):
        dw.scratchpad2.setText("test_function called")  
        
    def datad_function(self, parent=None):
        dw.scratchpad2.setText("datad_function called")    
        self.mylog()


    def repeat(self):

        #
        #   Arduino 2:  192.168.1.121 
        #
    
        #dw.scratchpad2.setText("starting socket opps")
    
        global temperature_2
        global temperature_3
    
        global temperature_num_2
        global temperature_num_3
    
        global humidity_num_2
        global humidity_num_3
    
        global pressure_num_2
        global pressure_num_3
    
        global V_num_2
        global V_num_3
    
        global I_num_2
        global I_num_3
    
        #update_temp = pyqtSignal(str)
        #update_temp.emit(temperature_2)

        s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #s.setblocking(0)
        HOST='192.168.1.121'
        PORT=80
        s.connect((HOST, PORT))#connect to 192.168.1.121, Arduino 2
        s.sendto("**dump2".encode(), (HOST, PORT))
        message = s.recv(60)

        temperature_2=message.decode('utf-8')
        s.close()
    
        temperature_string=temperature_2[0:4:1]

        #dw.scratchpad2.setText(temperature_2)

        #ts = time.gmtime()
        #time_str = time.strftime("time: %Y-%m-%d %H-%M-%S", ts)
        #dw.textfield.setText(time_str)
        #dw.textfield.setText("current time is %f" % time.time())
        
        now = datetime.now()
        s_s_m = (now - now.replace(hour=0,minute=0,second=0,microsecond=0)).total_seconds()
        
        d=50-(50*math.cos(s_s_m*6.28318/86400))

        if self.isfloat(temperature_string):
            temperature_num_2=(float(temperature_string))/100
            temperature_num_2 = (temperature_num_2*1.8)+32
            #dw.tempfield2.setText("temperature: %0.2f deg F" % temperature_num_2)
            #dw.scratchpad.setText("True")
            i=0
            while i<999:
                dw.temp_array2[i]=dw.temp_array2[i+1]
                dw.time_array[i]=dw.time_array[i+1]
                i+=1
            dw.temp_array2[999]=temperature_num_2
            dw.time_array[999]=d
        #else:
        #   dw.scratchpad2.setText("temp 2 error: %s" % time_str)

        index=temperature_2.find('HM')
        humidity_string=temperature_2[index+2:index+6:1]

        #dw.scratchpad2.setText(humidity_string)

        if self.isfloat(humidity_string):
            humidity_num_2=(float(humidity_string))/100
            #dw.humidfield2.setText("humidity: %0.2f %%" % humidity_num_2)
            i=0
            while i<999:
                dw.humid_array2[i]=dw.humid_array2[i+1]
                i+=1
            dw.humid_array2[999]=humidity_num_2
        #else:
        #   dw.scratchpad2.setText("humidity 2 error: %s" % time_str)

        index=temperature_2.find('PS')
        pressure_string=temperature_2[index+2:index+6:1]

        if self.isfloat(pressure_string):
            pressure_num_2=(float(pressure_string))*0.02953;
            #dw.pressfield2.setText("atm pressure: %0.2f inHg" % pressure_num_2)
            i=0
            while i<999:
                dw.press_array2[i]=dw.press_array2[i+1]
                i+=1
            dw.press_array2[999] = 0.2 * (pressure_num_2 + dw.press_array2[998]  + dw.press_array2[997]+ dw.press_array2[996]+ dw.press_array2[995])
            #dw.scratchpad.setText("atm pressure: %d" % dw.press_array2[359])
        #else:
        #   dw.scratchpad2.setText("atm pressure 2 error: %s" % time_str)

        indexV1=temperature_2.find('LV')
        #indexV2=temperature_2.find('CU')
        V_string=temperature_2[indexV1+2:indexV1+6:1]
        indexI1=temperature_2.find('CU')
        #indexI2=len(temperature_2)
        I_string=temperature_2[indexI1+2:indexI1+7:1]

        if (self.isfloat(V_string) and self.isfloat(I_string)):
            V_num_2=(float(V_string));
            I_num_2=(float(I_string));
            #dw.battfield2.setText("battery: %0.2fmA@%0.2fV" % (I_num_2, V_num_2))
            #i=0
            #while i<359:
            #    dw.batt_array2[i]=dw.batt_array2[i+1]
            #    i+=1
            #dw.batt_array2[359]=V_num
        #else:
        #   dw.scratchpad2.setText("I or V, 2 error: %s" % time_str)

        #s.close()

        #
        #   Arduino 3:  192.168.1.113 
        #

        s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #s.setblocking(0)
        HOST='192.168.1.113'
        PORT=80
        s.connect((HOST, PORT))#connect to 192.168.1.113, Arduino 3
        s.sendto("**dump".encode(), (HOST, PORT))
        message = s.recv(60)

        temperature_3=message.decode('utf-8')
        s.close()
    
        temperature_string=temperature_3[0:4:1]

        #dw.scratchpad3.setText(temperature_3)

        if self.isfloat(temperature_string):
            temperature_num_3=(float(temperature_string))/100
            temperature_num_3 = (temperature_num_3*1.8)+32
            #dw.tempfield3.setText("temperature: %0.2f deg F" % temperature_num_3)
            #dw.scratchpad.setText("True")
            i=0
            while i<999:
                dw.temp_array3[i]=dw.temp_array3[i+1]
                i+=1
            dw.temp_array3[999]=temperature_num_3
        #else:
        #   dw.scratchpad3.setText("temp 3 error: %s" % time_str)

        index=temperature_3.find('HM')
        humidity_string=temperature_3[index+2:index+6:1]

        #dw.scratchpad3.setText(humidity_string)

        if self.isfloat(humidity_string):
            humidity_num_3=(float(humidity_string))/100
            #dw.humidfield3.setText("humidity: %0.2f %%" % humidity_num_3)
            i=0
            while i<999:
                dw.humid_array3[i]=dw.humid_array3[i+1]
                i+=1
            dw.humid_array3[999]=humidity_num_3
        #else:
        #   dw.scratchpad3.setText("humidity 3 error: %s" % time_str)

        index=temperature_3.find('PS')
        pressure_string=temperature_3[index+2:index+6:1]

        if self.isfloat(pressure_string):
            pressure_num_3=(float(pressure_string))*0.02953
            #pressure_num_3 = pressure_num_3 + 0.01
            #dw.pressfield3.setText("atm pressure: %0.2f inHg" % pressure_num_3)
            i=0
            while i<999:
                dw.press_array3[i]=dw.press_array3[i+1]
                i+=1
            dw.press_array3[999] = 0.2 * (pressure_num_3 + dw.press_array3[998]  + dw.press_array3[997]+ dw.press_array3[996]+ dw.press_array3[995])
            #dw.scratchpad.setText("atm pressure: %d" % dw.press_array3[359])
        #else:
        #   dw.scratchpad3.setText("atm pressure 3 error: %s" % time_str)

        indexV1=temperature_3.find('LV')
        #indexV2=temperature_3.find('CU')
        V_string=temperature_3[indexV1+2:indexV1+6:1]
        indexI1=temperature_3.find('CU')
        #indexI2=len(temperature_3)
        I_string=temperature_3[indexI1+2:indexI1+7:1]

        if (self.isfloat(V_string) and self.isfloat(I_string)):
            V_num_3=(float(V_string));
            I_num_3=(float(I_string));
            #dw.battfield3.setText("battery: %0.2fmA@%0.2fV" % (I_num_3, V_num_3))
            #i=0
            #while i<359:
            #    dw.batt_array3[i]=dw.batt_array3[i+1]
            #    i+=1
            #dw.batt_array3[359]=V_num
        #else:
        #   dw.scratchpad3.setText("I or V, 3 error: %s" % time_str)

        #s.close()


    def mylog(self):
    
        #dw.scratchpad2.setText("mylog called")
    
        dw.p22.setGeometry(dw.p12.vb.sceneBoundingRect())
        dw.p32.setGeometry(dw.p12.vb.sceneBoundingRect())
        dw.p42.setGeometry(dw.p12.vb.sceneBoundingRect())

        dw.p23.setGeometry(dw.p13.vb.sceneBoundingRect())
        
        dw.timeplot.setGeometry(dw.p13.vb.sceneBoundingRect())

        self.repeat()
    
        ts = time.localtime()
        time_str = time.strftime("time: %Y-%m-%d %H-%M-%S", ts)
        dw.textfield.setText(time_str)
    
        dw.scratchpad2.setText(temperature_2)
        dw.scratchpad3.setText(temperature_3)
    
        dw.tempfield2.setText("inside temperature: %0.2f deg F" % temperature_num_2)
        dw.tempfield3.setText("outside temperature: %0.2f deg F" % temperature_num_3)
    
        dw.humidfield2.setText("inside humidity: %0.2f %%" % humidity_num_2)
        dw.humidfield3.setText("outside humidity: %0.2f %%" % humidity_num_3)
    
        dw.pressfield2.setText("inside atm pressure: %0.2f inHg" % pressure_num_2)
        dw.pressfield3.setText("outside atm pressure: %0.2f inHg" % pressure_num_3)
    
        dw.battfield2.setText("inside battery: %0.2fmA@%0.2fV" % (I_num_2, V_num_2))
        dw.battfield3.setText("outside battery: %0.2fmA@%0.2fV" % (I_num_3, V_num_3))
    
        #dw.p1.plot(dw.x, dw.temp_array)
        #dw.curve.setData(dw.x, dw.temp_array)
        #dw.plt_humid.setData(dw.x, dw.humid_array)

        dw.curve12.setData(dw.temp_array2)
        dw.curve22.setData(dw.temp_array3)
        dw.curve32.setData(dw.humid_array2)
        dw.curve42.setData(dw.humid_array3)

        dw.curve13.setData(dw.press_array2)
        dw.curve23.setData(dw.press_array3)
        
        dw.curve_tp.setData(dw.time_array)

        #dw.curve.setData(dw.x, dw.temp_array)
        #dw.curve2.setData(dw.x, dw.humid_array)
        
        dw.p22.setGeometry(dw.p12.vb.sceneBoundingRect())
        dw.p32.setGeometry(dw.p12.vb.sceneBoundingRect())
        dw.p42.setGeometry(dw.p12.vb.sceneBoundingRect())

        dw.p23.setGeometry(dw.p13.vb.sceneBoundingRect())

        #dw.scratchpad.setText("resizing")

        #dw.plt.resize(1801,850)
        #dw.plt.resize(1800,850)

        #dw.scratchpad.setText("resized")

        pg.QtGui.QGuiApplication.processEvents()
        #threading.Timer(60.0, self.mylog).start()
    
    def data_display():

        ts = time.localtime()
        time_str = time.strftime("time: %Y-%m-%d %H-%M-%S", ts)
        dw.textfield.setText(time_str)
    
        dw.scratchpad2.setText(temperature_2)
        dw.scratchpad3.setText(temperature_3)
    
        dw.tempfield2.setText("temperature: %0.2f deg F" % temperature_num_2)
        dw.tempfield3.setText("temperature: %0.2f deg F" % temperature_num_3)
    
        dw.humidfield2.setText("humidity: %0.2f %%" % humidity_num_2)
        dw.humidfield3.setText("humidity: %0.2f %%" % humidity_num_3)
    
        dw.pressfield2.setText("atm pressure: %0.2f inHg" % pressure_num_2)
        dw.pressfield3.setText("atm pressure: %0.2f inHg" % pressure_num_3)
    
        dw.battfield2.setText("battery: %0.2fmA@%0.2fV" % (I_num_2, V_num_2))
        dw.battfield2.setText("battery: %0.2fmA@%0.2fV" % (I_num_3, V_num_3))
    
        #threading.Timer(10.0, data_display).start()


    def isfloat(self,s):
        try:
            float(s)
            return True
        except ValueError:
            return False
    
app=QApplication(sys.argv)
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

temperature_2 = '0'
temperature_3 = '0'

temperature_num_2 = 0
temperature_num_3 = 0

humidity_num_2 = 0
humidity_num_3 = 0

pressure_num_2 = 0
pressure_num_3 = 0

V_num_2 = 0
V_num_3 = 0

I_num_2 = 0
I_num_3 = 0

dw=demowind()
dw.show()

#timer = QTimer()
#timer.setInterval(1000)
#timer.timeout.connect(dw.test_function)
#timer.start

sys.exit(app.exec_())