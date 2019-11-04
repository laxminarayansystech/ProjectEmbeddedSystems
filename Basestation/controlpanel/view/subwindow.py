import os
import threading
import time
import multiprocessing
from concurrent.futures import thread

from PyQt5 import QtCore, QtGui, QtWidgets
import pyqtgraph as pg
import random
from PyQt5 import QtCore, QtGui, QtWidgets
import pyqtgraph as pg
import controlpanel.model.units as units


class Ui_SubWindow(object):
    def setupUi(self, SubWindow, unit):
        self.unit = unit
        SubWindow.setObjectName("SubWindow")
        SubWindow.setMinimumSize(450, 280)

        SubWindow.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMaximizeButtonHint)

        self.centralwidget = QtWidgets.QWidget(SubWindow)

        self.centralwidget.setObjectName("centralwidget")
        # gridLayout 1 and 2
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        # the maxInput
        self.maxInput = QtWidgets.QDoubleSpinBox(self.centralwidget)

        self.maxInput.setObjectName("maxInput")
        self.maxInput.setSingleStep(0.1)
        self.maxInput.setMinimum(0.0)
        self.maxInput.setMaximum(2.5)
        self.maxInput.setValue(units.Units.get_unit_max(self.unit))
        self.maxInput.valueChanged.connect(lambda x: self.set_max_input_value())
        self.gridLayout.addWidget(self.maxInput, 4, 0, 1, 1)
        # the downButton
        self.downButton = QtWidgets.QPushButton(self.centralwidget)

        self.downButton.setObjectName("downButton")
        self.downButton.clicked.connect(lambda x: units.Units.roll_out_unit(self.unit))
        self.gridLayout.addWidget(self.downButton, 4, 3, 1, 1)
        # the minInput
        self.minInput = QtWidgets.QDoubleSpinBox(self.centralwidget)

        self.minInput.setObjectName("minInput")
        self.minInput.setSingleStep(0.1)
        self.minInput.setMinimum(0.0)
        self.minInput.setMaximum(2.5)
        self.minInput.setValue(units.Units.get_unit_min(self.unit))
        self.minInput.valueChanged.connect(lambda x: self.set_min_input_value())
        self.gridLayout.addWidget(self.minInput, 2, 0, 1, 1)
        # spacer 1
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 2, 2, 1, 1)
        # the setMaxButton
        self.setMaxButton = QtWidgets.QPushButton(self.centralwidget)

        self.setMaxButton.setObjectName("setMaxButton")
        self.maxInputValue = self.maxInput.value()
        self.setMaxButton.clicked.connect(lambda x: units.Units.set_unit_max(self.unit, self.maxInputValue))
        self.gridLayout.addWidget(self.setMaxButton, 4, 1, 1, 1)
        # spacer 2
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 4, 2, 1, 1)
        # the setMinButton
        self.setMinButton = QtWidgets.QPushButton(self.centralwidget)
        self.setMinButton.setEnabled(True)

        self.setMinButton.setObjectName("setMinButton")
        self.minInputValue = self.minInput.value()
        self.setMinButton.clicked.connect(lambda x: units.Units.set_unit_min(self.unit, self.minInputValue))
        self.gridLayout.addWidget(self.setMinButton, 2, 1, 1, 1)
        # the upButton
        self.upButton = QtWidgets.QPushButton(self.centralwidget)

        self.upButton.setObjectName("upButton")
        self.upButton.clicked.connect(lambda x: units.Units.roll_in_unit(self.unit))
        self.gridLayout.addWidget(self.upButton, 2, 3, 1, 1)

        # the tabwidget
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setEnabled(True)
        self.tabWidget.setMinimumSize(QtCore.QSize(0, 0))
        self.tabWidget.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.tabWidget.setFocusPolicy(QtCore.Qt.TabFocus)
        self.tabWidget.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)

        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Triangular)
        self.tabWidget.setElideMode(QtCore.Qt.ElideNone)
        self.tabWidget.setTabBarAutoHide(False)
        self.tabWidget.setObjectName("tabWidget")
        # the data tab and gridLayout 3
        self.Data = QtWidgets.QWidget()

        self.Data.setObjectName("Data")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.Data)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.tabWidget.addTab(self.Data, "")
        # the stauts tab and gridLayout 4
        self.Status = QtWidgets.QWidget()

        self.Status.setObjectName("Status")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.Status)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.tabWidget.addTab(self.Status, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 4)
        self.gridLayout_2.addLayout(self.gridLayout, 1, 1, 1, 1)
        # the graph op Data tab
        self.pen = QtGui.QPen()
        self.pen.setColor(QtGui.QColor(125, 175, 25))
        self.pen.setWidth(.7)
        self.pen.setStyle(QtCore.Qt.SolidLine)
        self.pen2 = QtGui.QPen()
        self.pen2.setColor(QtGui.QColor(125, 25, 25))
        self.pen2.setWidth(.7)
        self.pen2.setStyle(QtCore.Qt.SolidLine)

        self.graph = pg.PlotWidget(self.Data, title="Data")
        self.graph.setWindowTitle("Sunblind data")
        self.graph.addLegend()
        #self.legend = pg.LegendItem(offset=70)
        #self.legend.setParentItem(self.graph.getPlotItem())

        temperature_data = units.Units.get_data_temp(self.unit)
        light_data = units.Units.get_data_light(self.unit)

        # TODO: Replace x with something useful.
        self.graph_temp = self.graph.plotItem.plot([*range(len(temperature_data))],
                                                   temperature_data,
                                                   pen=self.pen, name="_Temperature")
        self.graph_light = self.graph.plotItem.plot([*range(len(light_data))],
                                                    light_data,
                                                    pen=self.pen2, name="_Light")

        #self.legend.addItem(self.graph_light, '_light')
        #self.legend.addItem(self.graph_temp, '_temp')

        #self.update_graph()
        labelStyle = {'color': '#FFF', 'font-size': '10pt'}
        self.graph.setLabel('left', 'Temperature (°C)', **labelStyle)
        self.graph.setLabel('bottom', 'Datapoint', **labelStyle)
        self.gridLayout_3.addWidget(self.graph, 0, 0, 1, 1)

        # statusText on status tab
        self.statusText = QtWidgets.QLabel(self.Status)
        font2 = QtGui.QFont()
        font2.setPointSize(15)
        font2.setBold(False)
        font2.setItalic(False)
        font2.setWeight(50)
        font2.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.statusText.setFont(font2)

        self.statusText.setAlignment(QtCore.Qt.AlignHCenter)
        self.statusText.setText("Status")
        self.gridLayout_4.addWidget(self.statusText, 0, 0, 1, 1)
        # status table
        self.tableWidget = QtWidgets.QTableWidget(self.Data)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy)
        self.tableWidget.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.tableWidget.setFrameShape(QtWidgets.QFrame.Box)
        self.tableWidget.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.tableWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.tableWidget.setTextElideMode(QtCore.Qt.ElideMiddle)
        self.tableWidget.setShowGrid(True)
        self.tableWidget.setGridStyle(QtCore.Qt.NoPen)
        self.tableWidget.setWordWrap(True)
        self.tableWidget.setCornerButtonEnabled(True)
        self.tableWidget.setRowCount(4)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(3)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(0, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(0, 2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(1, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(1, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(1, 2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(2, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(2, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(2, 2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(3, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(3, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(3, 2, item)
        self.tableWidget.horizontalHeader().setVisible(True)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(True)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(109)
        self.tableWidget.horizontalHeader().setHighlightSections(True)
        self.tableWidget.horizontalHeader().setMinimumSectionSize(109)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(True)
        self.tableWidget.horizontalHeader().setStretchLastSection(False)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget.verticalHeader().setDefaultSectionSize(18)
        self.tableWidget.verticalHeader().setHighlightSections(True)
        self.tableWidget.verticalHeader().setMinimumSectionSize(18)
        self.tableWidget.verticalHeader().setStretchLastSection(False)
        self.gridLayout_4.addWidget(self.tableWidget, 1, 0, 1, 1)

        # text on in the top from the window
        self.sunBlindName = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.sunBlindName.setFont(font)

        self.sunBlindName.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignHCenter)
        self.sunBlindName.setObjectName("sunblindName")
        self.gridLayout_2.addWidget(self.sunBlindName, 0, 1, 1, 1)

        SubWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(SubWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(SubWindow)

        '''
        # start new thread to update
        #lock = threading.Lock()
        #lock.acquire(True)
        #lock.release(True)
        self.t = threading.Thread(target=self.update)
        self.t.daemon = True
        self.t.start()
        '''

    def retranslateUi(self, SubWindow):
        _translate = QtCore.QCoreApplication.translate
        SubWindow.setWindowTitle(_translate("SubWindow", "unit" + str(self.unit)))
        self.downButton.setText(_translate("SubWindow", "DOWN"))
        self.setMaxButton.setText(_translate("SubWindow", "Set max"))
        self.setMinButton.setText(_translate("SubWindow", "Set min"))
        self.upButton.setText(_translate("SubWindow", "UP"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Data), _translate("SubWindow", "Data"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Status), _translate("SubWindow", "Status"))
        self.sunBlindName.setText(_translate("SubWindow", "Unit " + str(self.unit)))
        self.update_status()

    def set_status(self):
        if units.Units.get_status(self.unit) == "open":
            self.statusText.setText("This sun blind is open.")
        else:
            self.statusText.setText("This sun blind is closed.")

    def set_min_input_value(self):
        self.minInputValue = self.minInput.value()

    def set_max_input_value(self):
        self.maxInputValue = self.maxInput.value()

    def update_graph(self):
        units.Units.generate_new_data(self.unit)

        temperature_data = units.Units.get_data_temp(self.unit)
        light_data = units.Units.get_data_light(self.unit)

        self.graph_temp.setData(x=[*range(len(temperature_data))], y=temperature_data)
        self.graph_light.setData(x=[*range(len(light_data))], y=light_data)

    def update_status(self):
        status = units.Units.get_status(self.unit)
        data_light = units.Units.get_last_data_light(self.unit)
        data_temp = units.Units.get_last_data_temp(self.unit)
        data_ultrasoon = units.Units.get_last_data_ultrasoon(self.unit)

        item = self.tableWidget.item(0, 0)
        _translate = QtCore.QCoreApplication.translate
        item.setText(_translate("SubWindow", "light sensor"))
        item = self.tableWidget.item(0, 1)
        item.setText(_translate("SubWindow", status[0]))
        item = self.tableWidget.item(0, 2)
        item.setText(_translate("SubWindow", str(data_light)))
        item = self.tableWidget.item(1, 0)
        item.setText(_translate("SubWindow", "temperature sensor"))
        item = self.tableWidget.item(1, 1)
        item.setText(_translate("SubWindow", status[1]))
        item = self.tableWidget.item(1, 2)
        item.setText(_translate("SubWindow", str(data_temp)))
        item = self.tableWidget.item(2, 0)
        item.setText(_translate("SubWindow", "ultrasoon sensor"))
        item = self.tableWidget.item(2, 1)
        item.setText(_translate("SubWindow", status[2]))
        item = self.tableWidget.item(2, 2)
        item.setText(_translate("SubWindow", str(data_ultrasoon)))
        item = self.tableWidget.item(3, 0)
        item.setText(_translate("SubWindow", "sun blind"))
        item = self.tableWidget.item(3, 1)
        item.setText(_translate("SubWindow", status[3]))
        item = self.tableWidget.item(3, 2)
        item.setText(_translate("SubWindow", "NA"))
        self.tableWidget.update()

    def update(self):
        self.update_graph()
        self.update_status()
