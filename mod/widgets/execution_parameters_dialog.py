#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Execution Parameters Configuration Dialog."""

from PySide import QtCore, QtGui

from mod.translation_tools import __
from mod.stdout_tools import log
from mod.enums import HelpText

from mod.widgets.focusable_combo_box import FocusableComboBox
from mod.widgets.focusable_line_edit import FocusableLineEdit

from mod.dataobjects.case import Case
from mod.dataobjects.periodicity import Periodicity
from mod.dataobjects.periodicity_info import PeriodicityInfo
from mod.dataobjects.sd_position_property import SDPositionProperty

# ADD library
from mod.freecad_tools import get_fc_main_window
from mod.widgets.advanced_execution_parameters_dialog import AdvancedExecutionParametersDialog


class ExecutionParametersDialog(QtGui.QDialog):
    """Defines the execution parameters window.
    Modifies the data dictionary passed as parameter."""

    LABEL_DEFAULT_TEXT = "<i>{}</i>".format(__("Select an input to show help about it."))
    MINIMUM_WIDTH = 300
    MINIMUM_HEIGHT = 300

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        # Creates a dialog and 2 main buttons
        self.setWindowTitle(__("실행 매개변수 설정"))
        self.help_label = QtGui.QLabel(self.LABEL_DEFAULT_TEXT)
        self.ok_button = QtGui.QPushButton(__("확인"))
        self.cancel_button = QtGui.QPushButton(__("취소"))

        # ADD button
        self.advanced_button = QtGui.QPushButton(__("고급설정"))

        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # Boundary method
        self.boundary_layout = QtGui.QHBoxLayout()
        self.boundary_label = QtGui.QLabel(__("경계 설정 방법:"))
        self.boundary_input = FocusableComboBox()
        self.boundary_input.insertItems(0, [__("DBC"), __("mDBC")])
        self.boundary_input.setCurrentIndex(int(Case.the().execution_parameters.boundary) - 1)
        self.boundary_input.set_help_text(HelpText.BOUNDARY)
        self.boundary_input.focus.connect(self.on_help_focus)
        self.boundary_layout.addWidget(self.boundary_label)
        self.boundary_layout.addWidget(self.boundary_input)
        self.boundary_layout.addStretch(1)

        # Viscosity formulation
        self.viscotreatment_layout = QtGui.QHBoxLayout()
        self.viscotreatment_label = QtGui.QLabel(__("점도 공식:"))
        self.viscotreatment_input = FocusableComboBox()
        self.viscotreatment_input.insertItems(0, [__("Artificial"), __("Laminar + SPS")])
        self.viscotreatment_input.set_help_text(HelpText.VISCOTREATMENT)
        self.viscotreatment_input.setCurrentIndex(int(Case.the().execution_parameters.viscotreatment) - 1)
        self.viscotreatment_input.focus.connect(self.on_help_focus)
        self.viscotreatment_layout.addWidget(self.viscotreatment_label)
        self.viscotreatment_layout.addWidget(self.viscotreatment_input)
        self.viscotreatment_layout.addStretch(1)

        # Viscosity value
        self.visco_layout = QtGui.QHBoxLayout()
        self.visco_label = QtGui.QLabel(__("점도 값:"))
        self.visco_input = FocusableLineEdit()
        self.visco_input.set_help_text(HelpText.VISCO)
        self.visco_input.setMaxLength(10)
        self.visco_input.focus.connect(self.on_help_focus)

        self.visco_units_label = QtGui.QLabel(__(""))
        self.visco_layout.addWidget(self.visco_label)
        self.visco_layout.addWidget(self.visco_input)
        self.visco_layout.addWidget(self.visco_units_label)
        self.on_viscotreatment_change(int(Case.the().execution_parameters.viscotreatment) - 1)
        self.visco_input.setText(str(Case.the().execution_parameters.visco))
        self.viscotreatment_input.currentIndexChanged.connect(self.on_viscotreatment_change)

        # Viscosity with boundary
        self.viscoboundfactor_layout = QtGui.QHBoxLayout()
        self.viscoboundfactor_label = QtGui.QLabel(__("경계가 있는 점도 계수: "))
        self.viscoboundfactor_input = FocusableLineEdit()
        self.viscoboundfactor_input.set_help_text(HelpText.VISCOBOUNDFACTOR)
        self.viscoboundfactor_input.setMaxLength(10)
        self.viscoboundfactor_input.focus.connect(self.on_help_focus)
        self.viscoboundfactor_input.setText(str(Case.the().execution_parameters.viscoboundfactor))
        self.viscoboundfactor_layout.addWidget(self.viscoboundfactor_label)
        self.viscoboundfactor_layout.addWidget(self.viscoboundfactor_input)

        # Time of simulation
        self.timemax_layout = QtGui.QHBoxLayout()
        self.timemax_label = QtGui.QLabel(__("시뮬레이션 시간: "))
        self.timemax_input = FocusableLineEdit()
        self.timemax_input.set_help_text(HelpText.TIMEMAX)
        self.timemax_input.setMaxLength(10)
        self.timemax_input.focus.connect(self.on_help_focus)
        self.timemax_input.setText(str(Case.the().execution_parameters.timemax))
        self.timemax_label2 = QtGui.QLabel(__("초"))
        self.timemax_layout.addWidget(self.timemax_label)
        self.timemax_layout.addWidget(self.timemax_input)
        self.timemax_layout.addWidget(self.timemax_label2)

        # Time out data
        self.timeout_layout = QtGui.QHBoxLayout()
        self.timeout_label = QtGui.QLabel(__("시간 초과 데이터: "))
        self.timeout_input = FocusableLineEdit()
        self.timeout_input.set_help_text(HelpText.TIMEOUT)
        self.timeout_input.setMaxLength(10)

        self.timeout_input.focus.connect(self.on_help_focus)

        self.timeout_input.setText(str(Case.the().execution_parameters.timeout))
        self.timeout_label2 = QtGui.QLabel(__("초"))
        self.timeout_layout.addWidget(self.timeout_label)
        self.timeout_layout.addWidget(self.timeout_input)
        self.timeout_layout.addWidget(self.timeout_label2)

        # Max parts out allowed
        self.partsoutmax_layout = QtGui.QHBoxLayout()
        self.partsoutmax_label = QtGui.QLabel(__("허용되는 최대 부품 (%):"))
        self.partsoutmax_input = FocusableLineEdit()
        self.partsoutmax_input.set_help_text(HelpText.PARTSOUTMAX)
        self.partsoutmax_input.setMaxLength(10)
        self.partsoutmax_input.focus.connect(self.on_help_focus)
        self.partsoutmax_input.setText(str(float(Case.the().execution_parameters.partsoutmax) * 100))
        self.partsoutmax_layout.addWidget(self.partsoutmax_label)
        self.partsoutmax_layout.addWidget(self.partsoutmax_input)

        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        self.ok_button.clicked.connect(self.on_ok)
        self.cancel_button.clicked.connect(self.on_cancel)

        # Button layout definition
        self.ep_button_layout = QtGui.QHBoxLayout()
        self.ep_button_layout.addStretch(1)
        self.ep_button_layout.addWidget(self.ok_button)
        self.ep_button_layout.addWidget(self.cancel_button)

        # Add Layout and Button Advanced
        self.ep_button_layout.addWidget(self.advanced_button)
        self.advanced_button.clicked.connect(self.on_advanced_execution_parameters_button_pressed)

        # START Main layout definition and composition.
        self.ep_main_layout_scroll = QtGui.QScrollArea()
        self.ep_main_layout_scroll.setWidgetResizable(True)
        self.ep_main_layout_scroll_widget = QtGui.QWidget()

        self.ep_main_layout = QtGui.QVBoxLayout()

        self.ep_main_layout.addLayout(self.viscotreatment_layout)
        self.ep_main_layout.addLayout(self.visco_layout)
        self.ep_main_layout.addLayout(self.boundary_layout)
        self.ep_main_layout.addLayout(self.viscoboundfactor_layout)
        self.ep_main_layout.addLayout(self.timemax_layout)
        self.ep_main_layout.addLayout(self.timeout_layout)
        self.ep_main_layout.addLayout(self.partsoutmax_layout)

        self.ep_main_layout_scroll_widget.setLayout(self.ep_main_layout)
        self.ep_main_layout_scroll.setWidget(self.ep_main_layout_scroll_widget)
        self.ep_main_layout_scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.execparams_window_layout = QtGui.QVBoxLayout()
        self.execparams_window_layout.addWidget(self.ep_main_layout_scroll)
        self.execparams_window_layout.addWidget(self.help_label)
        self.execparams_window_layout.addLayout(self.ep_button_layout)
        self.setLayout(self.execparams_window_layout)

        self.setMinimumWidth(self.MINIMUM_WIDTH)
        self.setMinimumHeight(self.MINIMUM_HEIGHT)
        self.resize(self.MINIMUM_WIDTH, self.MINIMUM_HEIGHT)
        self.exec_()

    def on_help_focus(self, help_text):
        """ Reacts to focusing the help setting the corresponding help text. """
        self.help_label.setText("<b>{}: </b>{}".format(__("Help"), help_text))


    def on_viscotreatment_change(self, index):
        """ Reacts to viscotreatment change. """
        self.visco_input.setText("0.01" if index == 0 else "0.000001")
        self.visco_label.setText(__("Viscosity value (alpha):") if index == 0 else __("Kinematic viscosity:"))
        self.visco_units_label.setText("" if index == 0 else "m<span style='vertical-align:super'>2</span>/s")

    def on_advanced_execution_parameters_button_pressed(self):
        AdvancedExecutionParametersDialog(parent=get_fc_main_window())

    # ------------ Button behaviour definition --------------
    def on_ok(self):
        """ Applies the data from the dialog onto the main data structure. """

        Case.the().execution_parameters.viscotreatment = int(self.viscotreatment_input.currentIndex() + 1)
        Case.the().execution_parameters.visco = float(self.visco_input.text())
        Case.the().execution_parameters.viscoboundfactor = int(self.viscoboundfactor_input.text())
        Case.the().execution_parameters.boundary = int(self.boundary_input.currentIndex() + 1)
        Case.the().execution_parameters.timemax = float(self.timemax_input.text())
        Case.the().execution_parameters.timeout = float(self.timeout_input.text())
        Case.the().execution_parameters.partsoutmax = float(self.partsoutmax_input.text()) / 100
        log("Execution Parameters changed")
        self.accept()

    def on_cancel(self):
        """ Canceles the dialog rejecting it. """
        log("Execution Parameters not changed")
        self.reject()
