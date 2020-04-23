#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 14:58:20 2020
@author: daisuke
"""
import sys, os
from PyQt5 import QtWidgets as QTW
from PyQt5 import QtCore as QTC
from PyQt5 import QtGui as QTG
class FirstWindow(QTW.QMainWindow):
    ''' This is just the first window that uses a widget to show some options'''
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        #setting first widget
        self.setWindowTitle('Primeira Janela')
        self.first_window_widget = FirstWindowWidget()

        self.setCentralWidget(self.first_window_widget)
        self.show()

class FirstWindowWidget(QTW.QWidget):
    '''widget which will fill the first window'''
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        #setting 3 buttons to chose from -------------------------------------
        self.numeric_model_btn = QTW.QPushButton('Numeric Model')
        self.simulation_btn = QTW.QPushButton('Simulation')
        self.real_btn = QTW.QPushButton('Real')

        #layout for buttoms -------------------------------------------------
        self.v_box = QTW.QVBoxLayout()
        self.v_box.addWidget(self.numeric_model_btn)

        #trigger when the user click numeric_model_btn --------------------------------
        self.numeric_model_btn.clicked.connect(self.numeric_model_open)  #runs the method

        self.setLayout(self.v_box)

        self.show() #show layout

    def numeric_model_open(self):
        '''opens the numericModel Mainwindow'''
        self.w = NumericModel()
        #self.close()

#-----------------------------------------------------------------------------

class NumericModel(QTW.QMainWindow):
    ''' Maindwindow responsable for receiving numeric model'''
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Numeric Model')

        # central_widget will be responsable for changing widgets
        self.central_widget = QTW.QStackedWidget()
        self.setCentralWidget(self.central_widget)

        self.param_widget = ParamWidget() #widget to receive parameters
        self.net_widget = Network()  # widget to set neural layers
        self.import_widget = ImportWidget(self) #widget to import and run another .py program
        #Self is needed as a parameter because the QMainWindow will be inherited to run .py program

        #adding both widgets and setting current widget
        self.central_widget.addWidget(self.param_widget)
        self.central_widget.addWidget(self.net_widget)
        self.central_widget.addWidget(self.import_widget)
        self.central_widget.setCurrentWidget(self.param_widget)

        #signals to change widgets for NEXT widget, look for .emit
        self.param_widget.n_cge_wdgt_clicked.connect(lambda: self.central_widget.setCurrentWidget(self.net_widget))
        self.net_widget.n_cge_wdgt_clicked.connect(lambda: self.central_widget.setCurrentWidget(self.import_widget))

        #signals to change widgets for BACK widget, look for .emit
        self.net_widget.b_cge_wdgt_clicked.connect(lambda: self.central_widget.setCurrentWidget(self.param_widget))
        self.import_widget.b_cge_wdgt_clicked.connect(lambda: self.central_widget.setCurrentWidget(self.net_widget))

        self.show()


class ParamWidget(QTW.QWidget):

    n_cge_wdgt_clicked = QTC.pyqtSignal() #signal to go next widgets

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('NumericModel')

        self.n_param = 8 #number of params excluding the 8th

        #texts for params
        self.param_lists = [QTW.QTextEdit() for i in range(self.n_param)]
        self.param_lbl_lists = [QTW.QLabel() for i in range(self.n_param)]

        #label of params
        self.param_lbl_lists[0] = QTW.QLabel('Nome da simulacao')
        self.param_lbl_lists[1] = QTW.QLabel('Numero de episodios')
        self.param_lbl_lists[2] = QTW.QLabel('Quantidade de timesteps por episodio')
        self.param_lbl_lists[3] = QTW.QLabel('Gamma')
        self.param_lbl_lists[4] = QTW.QLabel('Taxa de decaimento (Epsilon Decay)')
        self.param_lbl_lists[5]= QTW.QLabel('Taxa minima de exploracao (Epsilon min)')
        self.param_lbl_lists[6] = QTW.QLabel('Learning Rate')
        self.param_lbl_lists[7]= QTW.QLabel('Tamanho do batch do experience replay')

        #parameter 8 is a radiobox choice
        self.param_lbl_lists.append(QTW.QLabel())
        self.param_lbl_lists[8] = QTW.QLabel('Renderizar simulação durante treinamento?')
        self.yes_rd_btn = QTW.QRadioButton('sim')
        self.no_rd_btn = QTW.QRadioButton('nao')

        self.confirm_btn = QTW.QPushButton('Confirm')

        #values that are already written in the .txt file
        with open('parametros.txt', 'r') as r:
            self.param_lines = r.readlines()

        #write
        for i in range (self.n_param):
            self.param_lists[i].setText(self.param_lines[i].strip())

        #write for parameter 8
        if self.param_lines[8].strip() == '1':
            self.yes_rd_btn.setChecked(True)
        else:
            self.no_rd_btn.setChecked(True)

        #Horizontal box
        self.h_box_lists = [QTW.QHBoxLayout() for i in range(self.n_param)]

        #adding the labels and texts in horizontal box
        for i in range(self.n_param):
            self.h_box_lists[i].addWidget(self.param_lists[i])
            self.h_box_lists[i].addWidget(self.param_lbl_lists[i])

        #label and radio button for parameter 8
        self.h_box_lists.append(QTW.QHBoxLayout())
        self.h_box_lists[8].addWidget(self.yes_rd_btn)
        self.h_box_lists[8].addWidget(self.no_rd_btn)
        self.h_box_lists[8].addWidget(self.param_lbl_lists[8])

        #vertical_box
        self.v_box = QTW.QVBoxLayout()
        for i in range(self.n_param): #adding the horizontal boxes
            self.v_box.addLayout(self.h_box_lists[i])
        self.v_box.addLayout(self.h_box_lists[8])
        self.v_box.addWidget(self.confirm_btn)

        #when user clicks the confirm_btn, this two events will be triggered
        self.confirm_btn.clicked.connect(self.write_txt)
        self.confirm_btn.clicked.connect(self.n_cge_wdgt_clicked.emit) #change current widget

        self.setLayout(self.v_box)

    def write_txt(self):
        ''' This method will be called  when the confirm button is pressed, modifying the parameters .txt file'''
        self.txt_name = 'parametros.txt'
        self.rd_btn_check = None

        #reading the RadioButton
        if self.yes_rd_btn.isChecked(): #if yes rd btn is selected
            self.rd_btn_check = '1'
        else: #if no rd btn is selected
            self.rd_btn_check = '0'

        # cleaning the file
        self.file_clean = open(self.txt_name, "w")
        self.file_clean.close()

        self.param_txt_lists = []
        #creating an array with the str from the param_lists
        for i in range(self.n_param):
            self.param_txt_lists.append(self.param_lists[i].toPlainText().strip())

        with open(self.txt_name, 'a') as a: #a for append
            for i in range(self.n_param):
                a.write(self.param_txt_lists[i] + '\n')
            a.write(self.rd_btn_check)

    def clear_Layout(self, layout):
        '''You can clear layout with it, but i didn't use'''
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clear_Layout(item.layout())

class Network(QTW.QWidget):
    '''widget to open another widget with the number of layouts'''
    n_cge_wdgt_clicked = QTC.pyqtSignal()
    b_cge_wdgt_clicked = QTC.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('ImportWidget')

        #buttons ----------------------------------------------------------------------------
        self.back_btn = QTW.QPushButton('Back') # back_btn to go to the param widget again
        self.edit_btn = QTW.QPushButton('Edit') #open Network_1
        self.next_btn = QTW.QPushButton('Next') #nexr_btn to go to the import widget

        #label and texts ----------------------------------------------------------------------
        self.n_label_1 = QTW.QLabel('Write how many layers')
        self.layer_n_t = QTW.QTextEdit('')

        #box layouts --------------------------------------------------------------------------
        self.v_box = QTW.QVBoxLayout()
        self.h_box = QTW.QHBoxLayout()

        #setting layout-----------------------------------------------------------------------
        self.v_box.addWidget(self.n_label_1)
        self.v_box.addWidget(self.layer_n_t)
        self.h_box.addWidget(self.back_btn)
        self.h_box.addWidget(self.edit_btn)
        self.h_box.addWidget(self.next_btn)
        self.v_box.addLayout(self.h_box)

        self.setLayout(self.v_box)

        #setting button signals ----------------------------------------------------------
        self.back_btn.clicked.connect(self.b_cge_wdgt_clicked.emit) #send signal to go back
        self.edit_btn.clicked.connect(self.open_network_1)
        self.next_btn.clicked.connect(self.n_cge_wdgt_clicked.emit) #send signal to go next

    def open_network_1(self):
        layer_n = int(self.layer_n_t.toPlainText().strip()) #number of layers
        self.w = Network_1(layer_n) #opens the other widget

class Network_1(QTW.QWidget):
    def __init__(self, layer_n):
        super().__init__()
        self.layer_n = layer_n #numbers of layers
        self.text_lists_txt = []
        self.init_ui()

    def init_ui(self):
        self.ok_btn = QTW.QPushButton('Ok')

        self.v_box = QTW.QVBoxLayout()

        #gerando widgets dependendo do tamanho do layer_n
        self.h_box_lists = [QTW.QHBoxLayout() for i in range(self.layer_n)]
        self.label_lists = [QTW.QLabel('Layer :' + str(i)) for i in range(self.layer_n)]
        self.text_lists = [QTW.QTextEdit() for i in range(self.layer_n)]

        #setting the widgets created
        for i in range(self.layer_n):
            self.h_box_lists[i].addWidget(self.label_lists[i])
            self.h_box_lists[i].addWidget(self.text_lists[i])
            self.v_box.addLayout(self.h_box_lists[i])

        #adding ok_btn
        self.v_box.addWidget(self.ok_btn)
        self.ok_btn.clicked.connect(self.ok_pressed)

        self.setLayout(self.v_box)
        self.show()  # show layout

    def ok_pressed(self):
        self.write_txt()
        self.close()

    def write_txt(self):
        ''' This method will be called  when the confirm button is pressed, modifying the parameters .txt file'''
        self.txt_name = 'network.txt'

        #cleaning the file
        self.file_clean = open(self.txt_name, "w")
        self.file_clean.close()

        # create an array of str values from text_lists
        for i in range(self.layer_n):
            self.text_lists_txt.append(self.text_lists[i].toPlainText().strip())

        with open(self.txt_name, 'a') as a:  # a for append
            for i in range(self.layer_n):
                a.write(self.text_lists_txt[i] + '\n')


class ImportWidget(QTW.QWidget):
    '''Import and execute another .py program'''

    b_cge_wdgt_clicked = QTC.pyqtSignal()

    def __init__(self, qmainwindow):
        super().__init__()
        self.qmainwindow = qmainwindow

        self.init_ui()

    def init_ui(self):

        self.setWindowTitle('ImportWidget')

        #back_btn to set the param widget again
        self.back_btn = QTW.QPushButton('Back')
        self.back_btn.clicked.connect(self.b_cge_wdgt_clicked.emit)

        #run the .py using Process class
        self.start_process = QTW.QPushButton('Start')
        self.start_process.clicked.connect(self.do_something)

        #Where print from .py is going to be printed
        self.prompt_copy = QTW.QTextEdit()

        self.v_box = QTW.QVBoxLayout()
        self.v_box.addWidget(self.back_btn)
        self.v_box.addWidget(self.start_process)
        self.v_box.addWidget(self.prompt_copy)
        self.setLayout(self.v_box)

    def do_something(self):
        '''It just instantiate and run the Process Class'''
        process = Process(self.qmainwindow, self.prompt_copy)
        process.begin_process()



class Process():
    ''' Class responsable for running .py with QProcess, it receives the qmainwindow and qtextedit as parameters'''
    def __init__(self, qmainwindow, qtextedit):
        self.qmainwindow = qmainwindow
        self.qtextedit = qtextedit #where it is going to be printed

    def begin_process(self):
        print('Connecting Process')
        self.process = QTC.QProcess(self.qmainwindow)

        #Signals to trigger events
        self.process.readyRead.connect(lambda: self.stdoutReady()) #triggers when something is flushed to prompt

        #self.process.readyReadStandardOutput(lambda: self.stdoutReady())
        #self.process.readyReadStandardError.connect(lambda: self.stderrReady())

        #signals to signal begin and end
        self.process.started.connect(lambda: print('Started!'))
        self.process.finished.connect(lambda: print('Finished!'))

        print('Starting process', flush = true)
        self.process.start('python', ['InvertedPendulum.py']) #starting the process

    def append(self, text):
        '''Append in the end'''
        cursor = self.qtexedit.textCursor()
        cursor.movePosition(cursor.End)
        cursor.insertText(text)
        #self.qmainwindow.output.ensureCursorVisible()

    def stdoutReady(self):
        '''Reads all standard output'''
        text = str(self.process.readAllStandardOutput())
        print('out')
        #print(text.strip())
        self.qtextedit.append(text)

    def stderrReady(self):
        '''Reads all standard error'''
        text = str(self.process.readAllStandardError())
        print('error \n')
        print(text.strip())
        self.qtextedit.append(text)

class Image_plot(QTW.QWidget): #--------------------------------------------------------------------------------
    def __init__(self, layer_n):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.img = qtw.QLabel()
        #self.img.setPixmap(QtGui.QPixmap('cat.jpeg'))


        self.show()  # show layout

#-------------------------------------------------------------------------


app = QTW.QApplication(sys.argv)
main_window = FirstWindow()
main_window.show()
sys.exit(app.exec_())