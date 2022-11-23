#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Constants Configuration Dialog."""


from PySide import QtCore, QtGui

from mod.translation_tools import __
from mod.stdout_tools import log
from mod.enums import HelpText

from mod.widgets.hoverable_label import HoverableLabel
from mod.widgets.focusable_line_edit import FocusableLineEdit

from mod.dataobjects.case import Case

from mod.widgets.advanced_constants_dialog import AdvancedConstantsDialog
from mod.freecad_tools import get_fc_main_window


class ConstantsDialog(QtGui.QDialog):
    """ A window to define and configure the constants of the case for later execution
        in the DualSPHysics simulator. """

    LABEL_DEFAULT_TEXT = "<i>{}</i>".format(__("Select an input to show help about it."))
    MINIMUM_WIDTH = 415
    MINIMUM_HEIGHT = 200

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setWindowTitle(__("상수 설정"))
        self.help_label: QtGui.QLabel = QtGui.QLabel(self.LABEL_DEFAULT_TEXT)

        self.ok_button = QtGui.QPushButton(__("확인"))
        self.cancel_button = QtGui.QPushButton(__("취소"))

        self.advanced_button = QtGui.QPushButton(__("고급설정"))

        # Gravity
        self.gravity_layout = QtGui.QHBoxLayout()
        self.gravity_label = HoverableLabel(__("중력 [X, Y, Z]:"))

        self.gravityx_input = QtGui.QLineEdit()
        self.gravityx_input = FocusableLineEdit()
        self.gravityx_input.set_help_text(HelpText.GRAVITYX)
        self.gravityx_input.setMaxLength(10)

        self.gravityx_input.focus.connect(self.on_help_focus)

        self.gravityx_validator = QtGui.QDoubleValidator(-200, 200, 8, self.gravityx_input)
        self.gravityx_input.setText(str(Case.the().constants.gravity[0]))
        self.gravityx_input.setValidator(self.gravityx_validator)

        self.gravityy_input = QtGui.QLineEdit()
        self.gravityy_input = FocusableLineEdit()
        self.gravityy_input.set_help_text(HelpText.GRAVITYY)
        self.gravityy_input.setMaxLength(10)

        self.gravityy_input.focus.connect(self.on_help_focus)

        self.gravityy_validator = QtGui.QDoubleValidator(-200, 200, 8, self.gravityy_input)
        self.gravityy_input.setText(str(Case.the().constants.gravity[1]))
        self.gravityy_input.setValidator(self.gravityy_validator)

        self.gravityz_input = QtGui.QLineEdit()
        self.gravityz_input = FocusableLineEdit()
        self.gravityz_input.set_help_text(HelpText.GRAVITYZ)
        self.gravityz_input.setMaxLength(10)

        self.gravityz_input.focus.connect(self.on_help_focus)

        self.gravityz_validator = QtGui.QDoubleValidator(-200, 200, 8, self.gravityz_input)
        self.gravityz_input.setText(str(Case.the().constants.gravity[2]))
        self.gravityz_input.setValidator(self.gravityz_validator)

        self.gravity_label2 = QtGui.QLabel("m/s<span style='vertical-align:super'>2</span>")

        self.gravity_layout.addWidget(self.gravity_label)
        self.gravity_layout.addWidget(self.gravityx_input)  # For X
        self.gravity_layout.addWidget(self.gravityy_input)  # For Y
        self.gravity_layout.addWidget(self.gravityz_input)  # For Z
        self.gravity_layout.addWidget(self.gravity_label2)

        # Reference density of the fluid: layout and components
        self.rhop0_layout = QtGui.QHBoxLayout()
        self.rhop0_label = QtGui.QLabel(__("유체 기준 밀도:"))

        self.rhop0_input = QtGui.QLineEdit()
        self.rhop0_input = FocusableLineEdit()
        self.rhop0_input.set_help_text(HelpText.RHOP0)
        self.rhop0_input.setMaxLength(10)

        self.rhop0_input.focus.connect(self.on_help_focus)

        self.rhop0_validator = QtGui.QIntValidator(0, 10000, self.rhop0_input)
        self.rhop0_input.setText(str(Case.the().constants.rhop0))
        self.rhop0_input.setValidator(self.rhop0_validator)
        self.rhop0_label2 = QtGui.QLabel("kg/m<span style='vertical-align:super'>3<span>")

        self.rhop0_layout.addWidget(self.rhop0_label)
        self.rhop0_layout.addWidget(self.rhop0_input)
        self.rhop0_layout.addWidget(self.rhop0_label2)

        self.ok_button.clicked.connect(self.on_ok)
        self.cancel_button.clicked.connect(self.on_cancel)
        self.advanced_button.clicked.connect(self.on_advanced_constants_definition_button_pressed)

        # Button layout definition
        self.cw_button_layout = QtGui.QHBoxLayout()
        self.cw_button_layout.addStretch(1)
        self.cw_button_layout.addWidget(self.ok_button)
        self.cw_button_layout.addWidget(self.cancel_button)
        self.cw_button_layout.addWidget(self.advanced_button)

        # START Main layout definition and composition.
        self.cw_main_layout_scroll = QtGui.QScrollArea()
        self.cw_main_layout_scroll.setWidgetResizable(True)
        self.cw_main_layout_scroll_widget = QtGui.QWidget()
        self.cw_main_layout = QtGui.QVBoxLayout()

        # Lattice was removed on 0.3Beta - 1 of June
        # self.cw_main_layout.addLayout(self.lattice_layout)
        # self.cw_main_layout.addLayout(self.lattice2_layout)
        self.cw_main_layout.addLayout(self.gravity_layout)
        self.cw_main_layout.addLayout(self.rhop0_layout)
        self.cw_main_layout.addStretch(1)

        self.cw_main_layout_scroll_widget.setLayout(self.cw_main_layout)
        self.cw_main_layout_scroll.setWidget(self.cw_main_layout_scroll_widget)
        self.cw_main_layout_scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.constants_window_layout = QtGui.QVBoxLayout()
        self.constants_window_layout.addWidget(self.cw_main_layout_scroll)
        self.constants_window_layout.addWidget(self.help_label)
        self.constants_window_layout.addLayout(self.cw_button_layout)

        self.setLayout(self.constants_window_layout)
        self.setMinimumWidth(self.MINIMUM_WIDTH)
        self.setMinimumHeight(self.MINIMUM_HEIGHT)
        self.resize(self.MINIMUM_WIDTH, self.MINIMUM_HEIGHT)

        self.exec_()

    def on_advanced_constants_definition_button_pressed(self):
        AdvancedConstantsDialog(parent=get_fc_main_window())

    def on_help_focus(self, help_text):
        """ Reacts to focus signal setting a help text. """
        self.help_label.setText("<b>{}: </b>{}".format(__("Help"), help_text))

    def on_ok(self):
        """ Applies the current dialog data onto the main data structure. """
        Case.the().constants.gravity = [float(self.gravityx_input.text()), float(self.gravityy_input.text()), float(self.gravityz_input.text())]
        Case.the().constants.rhop0 = float(self.rhop0_input.text())
        log("Constants changed")
        self.accept()

    def on_cancel(self):
        """ Closes the dialog rejecting it. """
        log("Constants not changed")
        self.reject()
