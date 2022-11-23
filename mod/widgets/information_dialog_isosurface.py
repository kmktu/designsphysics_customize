#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics General Information Dialog"""

from PySide import QtGui, QtCore
import os
# from threading
import subprocess

from mod.gui_tools import h_line_generator
from mod.translation_tools import __

from mod.enums import InformationDetailsMode


import ctypes

# from mod.freecad_tools import get_fc_main_window
from mod.widgets.simulation_visual_dialog import SimulationVisualDialog

class InformationIsoSurfaceDialog(QtGui.QDialog):
    """ A resizable information report dialog  """

    MINIMUM_WIDTH = 500
    SHOW_DETAILS_TEXT = __("Show details")
    HIDE_DETAILS_TEXT = __("Hide details")

    def __init__(self, title: str, message: str, detailed_text: str = None, details_lang=InformationDetailsMode.PLAIN,
                 input_text: str = None):
        super().__init__()
        self.main_layout = QtGui.QVBoxLayout()

        self.setWindowTitle(str(title))
        self.setMinimumWidth(self.MINIMUM_WIDTH)
        self.message_label = QtGui.QLabel(str(message))
        self.message_label.setWordWrap(True)
        self.button_layout = QtGui.QHBoxLayout()
        self.details_widget = QtGui.QWidget()
        self.input_text = input_text

        self.show_details_button = QtGui.QPushButton(self.SHOW_DETAILS_TEXT)
        self.ok_button = QtGui.QPushButton("OK")

        # ADD simulation visualization button
        self.run_button_visual = QtGui.QPushButton(__("Simulation Visualization"))

        self.button_layout.addStretch(1)
        self.button_layout.addWidget(self.show_details_button)
        self.button_layout.addWidget(self.ok_button)

        # ADD button_layout for run_button_visual
        self.button_layout.addWidget(self.run_button_visual)

        self.details_textarea = QtGui.QTextEdit()

        if details_lang == InformationDetailsMode.PLAIN:
            self.details_textarea.insertPlainText(str(detailed_text).replace("\\n", "\n"))
        elif details_lang == InformationDetailsMode.HTML:
            self.details_textarea.insertHtml(str(detailed_text).replace("\\n", "\n"))

        self.details_textarea.setReadOnly(True)

        self.details_widget_layout = QtGui.QVBoxLayout()
        self.details_widget_layout.setContentsMargins(0, 0, 0, 0)
        self.details_widget_layout.addWidget(h_line_generator())
        self.details_widget_layout.addWidget(self.details_textarea)
        self.details_widget.setLayout(self.details_widget_layout)
        self.details_widget.setVisible(False)

        self.show_details_button.clicked.connect(self.on_details_button)
        self.ok_button.clicked.connect(self.on_ok_button)

        # ADD connect
        # self.run_button_visual.clicked.connect(self.simulation_visualization_def(str(input_text)))
        self.run_button_visual.clicked.connect(self.simulation_visualization_def)

        self.main_layout.addWidget(self.message_label)
        self.main_layout.addLayout(self.button_layout)
        self.main_layout.addWidget(self.details_widget)

        if not detailed_text:
            self.show_details_button.setVisible(False)

        self.setLayout(self.main_layout)
        self.exec_()

    def on_details_button(self) -> None:
        """ Reacts to the details button being pressed. """
        self.details_widget.setVisible(not self.details_widget.isVisible())
        self.show_details_button.setText(self.HIDE_DETAILS_TEXT if self.details_widget.isVisible() else self.SHOW_DETAILS_TEXT)
        self.adjustSize()

    def on_ok_button(self) -> None:
        """ Reacts to the ok button being pressed. """
        self.accept()

    def simulation_visualization_def(self):
        PARAVIEWPATH = "C:/Users/mgkang.DI-SOLUTION/Desktop/KANG/PYcharm_project/" \
                       "git/FreeCad/DesignSPHysics-master/paraview_build/bin/pvpython.exe"
        sorce_path = "C:/Users/mgkang.DI-SOLUTION/Desktop/KANG/PYcharm_project/git/FreeCad/DesignSPHysics-master/mod/" \
                     "widgets/paraview_visualization.py"
        # abs = os.path.abspath(PARAVIEWPATH)
        #
        # command = [abs, sorce_path]
        #
        # proc = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        # print(proc.stdout)

        # sorce_path = "../../mod/widgets/paraview_visualization.py"
        # print("sorce_path : ", sorce_path)

        command = "pvpython" + " " + sorce_path
        print("Command : ", command)

        proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        out, err = proc.communicate(input=bytes(self.input_text, encoding='utf-8'))
        print("out : ", out.decode('utf-8'))
        print("err : ", err.decode('utf-8'))
        #
        # ctypes.windll.shell32.ShellExecuteA(0, 'open', PARAVIEWPATH, sorce_path, None, 1)
        # os.system(PARAVIEWPATH + " " + sorce_path)


        # p = QtCore.QProcess
        # p.start(abs, ["paraview_visualization.py"])

        # proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE,
        #                         shell=True)
        # out, err = proc.communicate(input=bytes(self.input_text, encoding='utf-8'))
        # print("out_output : ", out.decode('utf-8'))
        # print("err_output : ", err.decode('euc-kr'))  # 왜 한글로 나오지

