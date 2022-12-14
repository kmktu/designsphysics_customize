from PySide import QtCore, QtGui

from mod.translation_tools import __
from mod.stdout_tools import log
from mod.enums import HelpText

from mod.widgets.hoverable_label import HoverableLabel
from mod.widgets.focusable_line_edit import FocusableLineEdit

from mod.dataobjects.case import Case

class AdvancedConstantsDialog(QtGui.QDialog):
    LABEL_DEFAULT_TEXT = "<i>{}</i>".format(__("Select an input to show help about it."))
    MINIMUM_WIDTH = 415
    MINIMUM_HEIGHT = 500

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setWindowTitle(__("상수 고급 설정"))
        self.help_label: QtGui.QLabel = QtGui.QLabel(self.LABEL_DEFAULT_TEXT)

        self.ok_button = QtGui.QPushButton(__("확인"))
        self.cancel_button = QtGui.QPushButton(__("취소"))
        self.default_button = QtGui.QPushButton(__("기본값"))

        # Lattice for boundaries layout and components
        self.lattice_layout = QtGui.QHBoxLayout()
        self.lattice_label = QtGui.QLabel(__("Lattice for Boundaries:"))
        self.lattice_input = QtGui.QComboBox()
        self.lattice_input.insertItems(0, [__("Lattice 1"), __("Lattice 2")])
        self.lattice_input.setCurrentIndex(Case.the().constants.lattice_bound - 1)

        self.lattice_layout.addWidget(self.lattice_label)
        self.lattice_layout.addWidget(self.lattice_input)
        self.lattice_layout.addStretch(1)

        # Lattice for fluids layout and components
        self.lattice2_layout = QtGui.QHBoxLayout()
        self.lattice2_label = QtGui.QLabel(__("Lattice for Fluids: "))
        self.lattice2_input = QtGui.QComboBox()
        self.lattice2_input.insertItems(0, [__("Lattice 1"), __("Lattice 2")])
        self.lattice2_input.setCurrentIndex(Case.the().constants.lattice_fluid - 1)

        self.lattice2_layout.addWidget(self.lattice2_label)
        self.lattice2_layout.addWidget(self.lattice2_input)
        self.lattice2_layout.addStretch(1)

        # Maximum still water level to calc.  spdofsound using coefsound: layout and
        # components
        self.hswlauto_layout = QtGui.QHBoxLayout()
        self.hswlauto_chk = QtGui.QCheckBox(__("Auto HSWL"))
        if Case.the().constants.hswl_auto:
            self.hswlauto_chk.setCheckState(QtCore.Qt.Checked)
        else:
            self.hswlauto_chk.setCheckState(QtCore.Qt.Unchecked)

        self.hswlauto_chk.toggled.connect(self.on_hswlauto_check)
        self.hswlauto_layout.addWidget(self.hswlauto_chk)

        self.hswl_layout = QtGui.QHBoxLayout()
        self.hswl_label = QtGui.QLabel(__("HSWL:"))
        self.hswl_input = QtGui.QLineEdit()
        self.hswl_input = FocusableLineEdit()
        self.hswl_input.set_help_text(HelpText.HSWL)
        self.hswl_input.setMaxLength(10)

        self.hswl_input.focus.connect(self.on_help_focus)

        self.hswl_validator = QtGui.QIntValidator(0, 10000, self.hswl_input)
        self.hswl_input.setText(str(Case.the().constants.hswl))
        self.hswl_input.setValidator(self.hswl_validator)
        self.hswl_label2 = QtGui.QLabel(__("metres"))

        self.hswl_layout.addWidget(self.hswl_label)
        self.hswl_layout.addWidget(self.hswl_input)
        self.hswl_layout.addWidget(self.hswl_label2)

        # Manually trigger check for the first time
        self.on_hswlauto_check()

        # gamma: layout and components
        self.gamma_layout = QtGui.QHBoxLayout()
        self.gamma_label = QtGui.QLabel(__("Gamma:"))
        self.gamma_input = QtGui.QLineEdit()
        self.gamma_input = FocusableLineEdit()
        self.gamma_input.set_help_text(HelpText.GAMMA)
        self.gamma_input.setMaxLength(3)

        self.gamma_input.focus.connect(self.on_help_focus)

        self.gamma_validator = QtGui.QIntValidator(0, 999, self.gamma_input)
        self.gamma_input.setText(str(Case.the().constants.gamma))
        self.gamma_input.setValidator(self.gamma_validator)
        self.gamma_label2 = QtGui.QLabel("units")

        self.gamma_layout.addWidget(self.gamma_label)
        self.gamma_layout.addWidget(self.gamma_input)
        self.gamma_layout.addWidget(self.gamma_label2)

        # Speedsystem: layout and components
        self.speedsystemauto_layout = QtGui.QHBoxLayout()
        self.speedsystemauto_chk = QtGui.QCheckBox(__("Auto Speedsystem"))
        if Case.the().constants.speedsystem_auto:
            self.speedsystemauto_chk.setCheckState(QtCore.Qt.Checked)
        else:
            self.speedsystemauto_chk.setCheckState(QtCore.Qt.Unchecked)

        self.speedsystemauto_chk.toggled.connect(self.on_speedsystemauto_check)
        self.speedsystemauto_layout.addWidget(self.speedsystemauto_chk)

        self.speedsystem_layout = QtGui.QHBoxLayout()
        self.speedsystem_label = QtGui.QLabel(__("Speedsystem:"))
        self.speedsystem_input = QtGui.QLineEdit()
        self.speedsystem_input = FocusableLineEdit()
        self.speedsystem_input.set_help_text(HelpText.SPEEDSYSTEM)
        self.speedsystem_input.setMaxLength(10)

        self.speedsystem_input.focus.connect(self.on_help_focus)

        self.speedsystem_validator = QtGui.QIntValidator(0, 10000, self.speedsystem_input)
        self.speedsystem_input.setText(str(Case.the().constants.speedsystem))
        self.speedsystem_input.setValidator(self.speedsystem_validator)
        self.speedsystem_label2 = QtGui.QLabel("m/s")

        self.speedsystem_layout.addWidget(self.speedsystem_label)
        self.speedsystem_layout.addWidget(self.speedsystem_input)
        self.speedsystem_layout.addWidget(self.speedsystem_label2)

        # Manually trigger check for the first time
        self.on_speedsystemauto_check()

        # coefsound: layout and components
        self.coefsound_layout = QtGui.QHBoxLayout()
        self.coefsound_label = QtGui.QLabel(__("Coefsound:"))
        self.coefsound_input = QtGui.QLineEdit()
        self.coefsound_input = FocusableLineEdit()
        self.coefsound_input.set_help_text(HelpText.COEFSOUND)
        self.coefsound_input.setMaxLength(3)

        self.coefsound_input.focus.connect(self.on_help_focus)

        self.coefsound_validator = QtGui.QIntValidator(0, 999, self.coefsound_input)
        self.coefsound_input.setText(str(Case.the().constants.coefsound))
        self.coefsound_input.setValidator(self.coefsound_validator)
        self.coefsound_label2 = QtGui.QLabel("units")

        self.coefsound_layout.addWidget(self.coefsound_label)
        self.coefsound_layout.addWidget(self.coefsound_input)
        self.coefsound_layout.addWidget(self.coefsound_label2)

        # Speedsound: layout and components
        self.speedsoundauto_layout = QtGui.QHBoxLayout()
        self.speedsoundauto_chk = QtGui.QCheckBox(__("Auto Speedsound "))
        if Case.the().constants.speedsound_auto:
            self.speedsoundauto_chk.setCheckState(QtCore.Qt.Checked)
        else:
            self.speedsoundauto_chk.setCheckState(QtCore.Qt.Unchecked)

        self.speedsoundauto_chk.toggled.connect(self.on_speedsoundauto_check)
        self.speedsoundauto_layout.addWidget(self.speedsoundauto_chk)

        self.speedsound_layout = QtGui.QHBoxLayout()
        self.speedsound_label = QtGui.QLabel(__("Speedsound:"))
        self.speedsound_input = QtGui.QLineEdit()
        self.speedsound_input = FocusableLineEdit()
        self.speedsound_input.set_help_text(HelpText.SPEEDSOUND)
        self.speedsound_input.setMaxLength(10)

        self.speedsound_input.focus.connect(self.on_help_focus)

        self.speedsound_validator = QtGui.QIntValidator(0, 10000, self.speedsound_input)
        self.speedsound_input.setText(str(Case.the().constants.speedsound))
        self.speedsound_input.setValidator(self.speedsound_validator)
        self.speedsound_label2 = QtGui.QLabel("m/s")

        self.speedsound_layout.addWidget(self.speedsound_label)
        self.speedsound_layout.addWidget(self.speedsound_input)
        self.speedsound_layout.addWidget(self.speedsound_label2)

        # Manually trigger check for the first time
        self.on_speedsoundauto_check()

        # coefh: layout and components
        self.coefh_layout = QtGui.QHBoxLayout()
        self.coefh_label = QtGui.QLabel(__("CoefH:"))
        self.coefh_input = QtGui.QLineEdit()
        self.coefh_input = FocusableLineEdit()
        self.coefh_input.set_help_text(HelpText.COEFH)
        self.coefh_input.setMaxLength(10)

        self.coefh_input.focus.connect(self.on_help_focus)

        self.coefh_validator = QtGui.QDoubleValidator(0, 10, 8, self.coefh_input)
        self.coefh_input.setText(str(Case.the().constants.coefh))
        self.coefh_input.setValidator(self.coefh_validator)
        self.coefh_label2 = QtGui.QLabel(__("units"))

        self.coefh_layout.addWidget(self.coefh_label)
        self.coefh_layout.addWidget(self.coefh_input)
        self.coefh_layout.addWidget(self.coefh_label2)

        # cflnumber: layout and components
        self.cflnumber_layout = QtGui.QHBoxLayout()
        self.cflnumber_label = QtGui.QLabel(__("cflnumber: "))
        self.cflnumber_input = QtGui.QLineEdit()
        self.cflnumber_input = FocusableLineEdit()
        self.cflnumber_input.set_help_text(HelpText.CFLNUMBER)
        self.cflnumber_input.setMaxLength(10)

        self.cflnumber_input.focus.connect(self.on_help_focus)

        self.cflnumber_validator = QtGui.QDoubleValidator(0, 10, 8, self.coefh_input)
        self.cflnumber_input.setText(str(Case.the().constants.cflnumber))
        self.cflnumber_input.setValidator(self.cflnumber_validator)
        self.cflnumber_label2 = QtGui.QLabel(__("units"))

        self.cflnumber_layout.addWidget(self.cflnumber_label)
        self.cflnumber_layout.addWidget(self.cflnumber_input)
        self.cflnumber_layout.addWidget(self.cflnumber_label2)

        # h: layout and components
        self.hauto_layout = QtGui.QHBoxLayout()
        self.hauto_chk = QtGui.QCheckBox(__("Auto Smoothing length"))
        if Case.the().constants.h_auto:
            self.hauto_chk.setCheckState(QtCore.Qt.Checked)
        else:
            self.hauto_chk.setCheckState(QtCore.Qt.Unchecked)

        self.hauto_chk.toggled.connect(self.on_hauto_check)
        self.hauto_layout.addWidget(self.hauto_chk)

        self.h_layout = QtGui.QHBoxLayout()
        self.h_label = QtGui.QLabel(__("Smoothing Length:"))
        self.h_input = QtGui.QLineEdit()
        self.h_input = FocusableLineEdit()
        self.h_input.set_help_text(__("Smoothing Length"))
        self.h_input.setMaxLength(10)

        self.h_input.focus.connect(self.on_help_focus)

        self.h_validator = QtGui.QDoubleValidator(0, 100, 8, self.h_input)
        self.h_input.setText(str(Case.the().constants.h))
        self.h_input.setValidator(self.h_validator)
        self.h_label2 = QtGui.QLabel(__("metres"))

        self.h_layout.addWidget(self.h_label)
        self.h_layout.addWidget(self.h_input)
        self.h_layout.addWidget(self.h_label2)

        # Manually trigger check for the first time
        self.on_hauto_check()

        # b: layout and components
        self.bauto_layout = QtGui.QHBoxLayout()
        self.bauto_chk = QtGui.QCheckBox(__("Auto b constant for EOS"))
        if Case.the().constants.b_auto:
            self.bauto_chk.setCheckState(QtCore.Qt.Checked)
        else:
            self.bauto_chk.setCheckState(QtCore.Qt.Unchecked)

        self.bauto_chk.toggled.connect(self.on_bauto_check)
        self.bauto_layout.addWidget(self.bauto_chk)

        self.b_layout = QtGui.QHBoxLayout()
        self.b_label = QtGui.QLabel(__("B constant:"))
        self.b_input = QtGui.QLineEdit()
        self.b_input = FocusableLineEdit()
        self.b_input.set_help_text(__("B constant"))
        self.b_input.setMaxLength(10)

        self.b_input.focus.connect(self.on_help_focus)

        self.b_validator = QtGui.QDoubleValidator(0, 100, 8, self.b_input)
        self.b_input.setText(str(Case.the().constants.b))
        self.b_input.setValidator(self.b_validator)
        self.b_label2 = QtGui.QLabel(__("Pascal"))

        self.b_layout.addWidget(self.b_label)
        self.b_layout.addWidget(self.b_input)
        self.b_layout.addWidget(self.b_label2)

        # Manually trigger check for the first time
        self.on_bauto_check()

        self.ok_button.clicked.connect(self.on_ok)
        self.cancel_button.clicked.connect(self.on_cancel)
        self.default_button.clicked.connect(self.default_button_pressed_ev)

        self.acw_button_layout = QtGui.QHBoxLayout()
        self.acw_button_layout.addStretch(1)
        self.acw_button_layout.addWidget(self.ok_button)
        self.acw_button_layout.addWidget(self.cancel_button)
        self.acw_button_layout.addWidget(self.default_button)

        self.acw_main_layout_scroll = QtGui.QScrollArea()
        self.acw_main_layout_scroll.setWidgetResizable(True)
        self.acw_main_layout_scroll_widget = QtGui.QWidget()
        self.acw_main_layout = QtGui.QVBoxLayout()

        self.acw_main_layout.addLayout(self.hswlauto_layout)
        self.acw_main_layout.addLayout(self.hswl_layout)
        self.acw_main_layout.addLayout(self.gamma_layout)
        self.acw_main_layout.addLayout(self.speedsystemauto_layout)
        self.acw_main_layout.addLayout(self.speedsystem_layout)
        self.acw_main_layout.addLayout(self.coefsound_layout)
        self.acw_main_layout.addLayout(self.speedsoundauto_layout)
        self.acw_main_layout.addLayout(self.speedsound_layout)
        self.acw_main_layout.addLayout(self.coefh_layout)
        self.acw_main_layout.addLayout(self.cflnumber_layout)
        self.acw_main_layout.addLayout(self.hauto_layout)
        self.acw_main_layout.addLayout(self.h_layout)
        self.acw_main_layout.addLayout(self.bauto_layout)
        self.acw_main_layout.addLayout(self.b_layout)
        self.acw_main_layout.addStretch(1)

        self.acw_main_layout_scroll_widget.setLayout(self.acw_main_layout)
        self.acw_main_layout_scroll.setWidget(self.acw_main_layout_scroll_widget)
        self.acw_main_layout_scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.advanced_constants_window_layout = QtGui.QVBoxLayout()
        self.advanced_constants_window_layout.addWidget(self.acw_main_layout_scroll)
        self.advanced_constants_window_layout.addWidget(self.help_label)
        self.advanced_constants_window_layout.addLayout(self.acw_button_layout)

        self.setLayout(self.advanced_constants_window_layout)
        self.setMinimumWidth(self.MINIMUM_WIDTH)
        self.setMinimumHeight(self.MINIMUM_HEIGHT)
        self.resize(self.MINIMUM_WIDTH, self.MINIMUM_HEIGHT)

        self.exec_()

    def on_hswlauto_check(self):
        """ Reacts to the user selectin auto HSWL. """
        if self.hswlauto_chk.isChecked():
            self.hswl_input.setEnabled(False)
        else:
            self.hswl_input.setEnabled(True)

    def on_help_focus(self, help_text):
        """ Reacts to focus signal setting a help text. """
        self.help_label.setText("<b>{}: </b>{}".format(__("Help"), help_text))

    def on_speedsystemauto_check(self):
        """ Reacts to the speedsystemauto checkbox enabling/disabling its input. """
        if self.speedsystemauto_chk.isChecked():
            self.speedsystem_input.setEnabled(False)
        else:
            self.speedsystem_input.setEnabled(True)

    def on_speedsoundauto_check(self):
        """ Reacts to the speedsoundauto checkbos enabling/disabling its inputs. """
        if self.speedsoundauto_chk.isChecked():
            self.speedsound_input.setEnabled(False)
        else:
            self.speedsound_input.setEnabled(True)

    def on_hauto_check(self):
        """ Reacts to the hauto checkbox being pressed enabling/disabling its inputs. """
        if self.hauto_chk.isChecked():
            self.h_input.setEnabled(False)
        else:
            self.h_input.setEnabled(True)

    def on_bauto_check(self):
        """ Reacts to the bauto checkbox being pressed enabling/disabling its inputs. """
        if self.bauto_chk.isChecked():
            self.b_input.setEnabled(False)
        else:
            self.b_input.setEnabled(True)

    def on_ok(self):
        """ Applies the current dialog data onto the main data structure. """
        Case.the().constants.lattice_bound = self.lattice_input.currentIndex() + 1
        Case.the().constants.lattice_fluid = self.lattice2_input.currentIndex() + 1
        Case.the().constants.hswl = float(self.hswl_input.text())
        Case.the().constants.hswl_auto = self.hswlauto_chk.isChecked()
        Case.the().constants.gamma = float(self.gamma_input.text())
        Case.the().constants.speedsystem = float(self.speedsystem_input.text())
        Case.the().constants.speedsystem_auto = self.speedsystemauto_chk.isChecked()
        Case.the().constants.coefsound = float(self.coefsound_input.text())
        Case.the().constants.speedsound = float(self.speedsound_input.text())
        Case.the().constants.speedsound_auto = self.speedsoundauto_chk.isChecked()
        Case.the().constants.coefh = float(self.coefh_input.text())
        Case.the().constants.cflnumber = float(self.cflnumber_input.text())
        Case.the().constants.h = float(self.h_input.text())
        Case.the().constants.h_auto = self.hauto_chk.isChecked()
        Case.the().constants.b = float(self.b_input.text())
        Case.the().constants.b_auto = self.bauto_chk.isChecked()
        log("Constants changed")
        self.accept()

    def on_cancel(self):
        """ Closes the dialog rejecting it. """
        log("Constants not changed")
        self.reject()

    def default_button_pressed_ev(self):
        self.hswlauto_chk.setCheckState(QtCore.Qt.Checked)
        self.hswl_input.setText(str(Case.the().constants.hswl))
        self.gamma_input.setText(str(Case.the().constants.gamma))
        self.speedsystemauto_chk.setCheckState(QtCore.Qt.Checked)
        self.speedsystem_input.setText(str(Case.the().constants.speedsystem))
        self.coefsound_input.setText(str(Case.the().constants.coefsound))
        self.speedsoundauto_chk.setCheckState(QtCore.Qt.Checked)
        self.speedsound_input.setText(str(Case.the().constants.speedsound))
        self.coefh_input.setText(str(Case.the().constants.coefh))
        self.cflnumber_input.setText(str(Case.the().constants.cflnumber))
        self.hauto_chk.setCheckState(QtCore.Qt.Checked)
        self.h_input.setText(str(Case.the().constants.h))
        self.bauto_chk.setCheckState(QtCore.Qt.Checked)
        self.b_input.setText(str(Case.the().constants.b))

