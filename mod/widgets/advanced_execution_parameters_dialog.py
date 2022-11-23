#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
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

class AdvancedExecutionParametersDialog(QtGui.QDialog):
    LABEL_DEFAULT_TEXT = "<i>{}</i>".format(__("Select an input to show help about it."))
    MINIMUM_WIDTH = 600
    MINIMUM_HEIGHT = 600

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setWindowTitle(__("실행 매개변수 고급설정"))
        self.help_label = QtGui.QLabel(self.LABEL_DEFAULT_TEXT)
        self.ok_button = QtGui.QPushButton(__("확인"))
        self.cancel_button = QtGui.QPushButton(__("취소"))
        self.default_button = QtGui.QPushButton(__("기본값"))

        # Save particle position with double precision
        self.saveposdouble_layout = QtGui.QHBoxLayout()
        self.saveposdouble_label = QtGui.QLabel(__("배정밀도로 입자 위치 저장:"))
        self.saveposdouble_input = FocusableComboBox()
        self.saveposdouble_input.insertItems(0, [__("No"), __("Yes")])
        self.saveposdouble_input.setCurrentIndex(int(Case.the().execution_parameters.saveposdouble))
        self.saveposdouble_input.set_help_text(HelpText.SAVEPOSDOUBLE)
        self.saveposdouble_input.focus.connect(self.on_help_focus)
        self.saveposdouble_layout.addWidget(self.saveposdouble_label)
        self.saveposdouble_layout.addWidget(self.saveposdouble_input)
        self.saveposdouble_layout.addStretch(1)

        # Step Algorithm
        self.stepalgorithm_layout = QtGui.QHBoxLayout()
        self.stepalgorithm_label = QtGui.QLabel(__("단계 알고리즘:"))
        self.stepalgorithm_input = FocusableComboBox()
        self.stepalgorithm_input.insertItems(0, [__("Verlet"), __("Symplectic")])
        self.stepalgorithm_input.setCurrentIndex(int(Case.the().execution_parameters.stepalgorithm) - 1)
        self.stepalgorithm_input.set_help_text(HelpText.STEPALGORITHM)
        self.stepalgorithm_input.focus.connect(self.on_help_focus)
        self.stepalgorithm_input.currentIndexChanged.connect(self.on_step_change)
        self.stepalgorithm_layout.addWidget(self.stepalgorithm_label)
        self.stepalgorithm_layout.addWidget(self.stepalgorithm_input)
        self.stepalgorithm_layout.addStretch(1)

        # Verlet Steps
        self.verletsteps_layout = QtGui.QHBoxLayout()
        self.verletsteps_label = QtGui.QLabel(__("Verlet 단계:"))
        self.verletsteps_input = QtGui.QLineEdit()
        self.verletsteps_input = FocusableLineEdit()
        self.verletsteps_input.set_help_text(HelpText.VERLETSTEPS)
        self.verletsteps_input.setMaxLength(4)
        self.verletsteps_input.focus.connect(self.on_help_focus)
        self.verletsteps_validator = QtGui.QIntValidator(0, 9999, self.verletsteps_input)
        self.verletsteps_input.setText(str(Case.the().execution_parameters.verletsteps))
        self.verletsteps_input.setValidator(self.verletsteps_validator)
        self.verletsteps_layout.addWidget(self.verletsteps_label)
        self.verletsteps_layout.addWidget(self.verletsteps_input)

        # Enable/Disable fields depending on selection
        self.on_step_change(self.stepalgorithm_input.currentIndex)

        # Interaction kernel
        self.kernel_layout = QtGui.QHBoxLayout()
        self.kernel_label = QtGui.QLabel(__("상호작용 커널:"))
        self.kernel_input = FocusableComboBox()
        self.kernel_input.insertItems(0, [__("Cubic spline"), __("Wendland")])
        self.kernel_input.set_help_text(HelpText.KERNEL)
        self.kernel_input.setCurrentIndex(int(Case.the().execution_parameters.kernel) - 1)
        self.kernel_input.focus.connect(self.on_help_focus)
        self.kernel_layout.addWidget(self.kernel_label)
        self.kernel_layout.addWidget(self.kernel_input)
        self.kernel_layout.addStretch(1)

        # Density Diffusion Term
        self.densitydt_type_layout = QtGui.QHBoxLayout()
        self.densitydt_type_label = QtGui.QLabel(__("밀도 확산 기간:"))
        self.densitydt_type_input = QtGui.QComboBox()
        densitydt_option_list = [__('None'), __('Molteni'), __('Fourtakas'), __('Fourtakas (Full)')] \
            if Case.the().executable_paths.supports_ddt_fourtakas() else ['None', 'Molteni']
        self.densitydt_type_input.insertItems(0, densitydt_option_list)
        self.densitydt_type_input.setCurrentIndex(Case.the().execution_parameters.densitydt_type)
        self.densitydt_type_input.currentIndexChanged.connect(self.on_densitydt_type_change)
        self.densitydt_type_layout.addWidget(self.densitydt_type_label)
        self.densitydt_type_layout.addWidget(self.densitydt_type_input)
        self.densitydt_type_layout.addStretch(1)

        # densitydt value
        self.densitydt_layout = QtGui.QHBoxLayout()
        self.densitydt_label = QtGui.QLabel(__("DDT 값:"))
        self.densitydt_input = FocusableLineEdit()
        self.densitydt_input.set_help_text(HelpText.DENSITYDT)
        self.densitydt_input.setMaxLength(10)
        self.densitydt_input.focus.connect(self.on_help_focus)
        self.densitydt_input.setText(str(Case.the().execution_parameters.densitydt_value))
        self.densitydt_layout.addWidget(self.densitydt_label)
        self.densitydt_layout.addWidget(self.densitydt_input)

        if self.densitydt_type_input.currentIndex() == 0:
            self.densitydt_input.setEnabled(False)
        else:
            self.densitydt_input.setEnabled(True)

        # Shifting Mode
        self.shifting_layout = QtGui.QHBoxLayout()
        self.shifting_label = QtGui.QLabel(__("이동(shifting) 방법:"))
        self.shifting_input = FocusableComboBox()
        self.shifting_input.insertItems(0, [__("없음"), __("튐 무시"), __("고정 무시"), __("가득참")])
        self.shifting_input.set_help_text(HelpText.SHIFTING)
        self.shifting_input.focus.connect(self.on_help_focus)
        self.shifting_input.setCurrentIndex(int(Case.the().execution_parameters.shifting))
        self.shifting_input.currentIndexChanged.connect(self.on_shifting_change)
        self.shifting_layout.addWidget(self.shifting_label)
        self.shifting_layout.addWidget(self.shifting_input)
        self.shifting_layout.addStretch(1)

        # Coefficient for shifting
        self.shiftcoef_layout = QtGui.QHBoxLayout()
        self.shiftcoef_label = QtGui.QLabel(__("이동(shifting) 계수:"))
        self.shiftcoef_input = FocusableLineEdit()
        self.shiftcoef_input.set_help_text(HelpText.SHIFTINGCOEF)
        self.shiftcoef_input.setMaxLength(10)
        self.shiftcoef_input.focus.connect(self.on_help_focus)
        self.shiftcoef_input.setText(str(Case.the().execution_parameters.shiftcoef))
        self.shiftcoef_layout.addWidget(self.shiftcoef_label)
        self.shiftcoef_layout.addWidget(self.shiftcoef_input)

        # Free surface detection threshold
        self.shifttfs_layout = QtGui.QHBoxLayout()
        self.shifttfs_label = QtGui.QLabel(__("자유 표면 감지 임계값:"))
        self.shifttfs_input = FocusableLineEdit()
        self.shifttfs_input.set_help_text(HelpText.SHIFTINGTFS)
        self.shifttfs_input.setMaxLength(10)
        self.shifttfs_input.focus.connect(self.on_help_focus)
        self.shifttfs_input.setText(str(Case.the().execution_parameters.shifttfs))
        self.shifttfs_layout.addWidget(self.shifttfs_label)
        self.shifttfs_layout.addWidget(self.shifttfs_input)

        # Enable/Disable fields depending on Shifting mode on window creation.
        self.on_shifting_change(self.shifting_input.currentIndex())

        # Rigid algorithm
        self.rigidalgorithm_layout = QtGui.QHBoxLayout()
        self.rigidalgorithm_label = QtGui.QLabel(__("고체-고체 상호작용:"))
        self.rigidalgorithm_input = FocusableComboBox()
        self.rigidalgorithm_input.insertItems(0, ["SPH", "DEM", "CHRONO"])
        self.rigidalgorithm_input.set_help_text(HelpText.RIGIDALGORITHM)
        self.rigidalgorithm_input.setCurrentIndex(int(Case.the().execution_parameters.rigidalgorithm) - 1)
        self.rigidalgorithm_input.focus.connect(self.on_help_focus)
        self.rigidalgorithm_layout.addWidget(self.rigidalgorithm_label)
        self.rigidalgorithm_layout.addWidget(self.rigidalgorithm_input)
        self.rigidalgorithm_layout.addStretch(1)

        # Sim start freeze time
        self.ftpause_layout = QtGui.QHBoxLayout()
        self.ftpause_label = QtGui.QLabel(__("떠있을때 멈출 시간:"))
        self.ftpause_input = FocusableLineEdit()
        self.ftpause_input.set_help_text(HelpText.FTPAUSE)
        self.ftpause_input.setMaxLength(10)
        self.ftpause_input.focus.connect(self.on_help_focus)
        self.ftpause_input.setText(str(Case.the().execution_parameters.ftpause))
        self.ftpause_label2 = QtGui.QLabel(__("초"))
        self.ftpause_layout.addWidget(self.ftpause_label)
        self.ftpause_layout.addWidget(self.ftpause_input)
        self.ftpause_layout.addWidget(self.ftpause_label2)

        # Coefficient to calculate DT
        self.coefdtmin_layout = QtGui.QHBoxLayout()
        self.coefdtmin_label = QtGui.QLabel(__("최소 시간 간격에 대한 계수:"))
        self.coefdtmin_input = FocusableLineEdit()
        self.coefdtmin_input.set_help_text(HelpText.COEFDTMIN)
        self.coefdtmin_input.setMaxLength(10)
        self.coefdtmin_input.focus.connect(self.on_help_focus)
        self.coefdtmin_input.setText(str(Case.the().execution_parameters.coefdtmin))
        self.coefdtmin_layout.addWidget(self.coefdtmin_label)
        self.coefdtmin_layout.addWidget(self.coefdtmin_input)

        # Minimum rhop valid
        self.rhopoutmin_layout = QtGui.QHBoxLayout()
        self.rhopoutmin_label = QtGui.QLabel(__("유효한 최소 rhop :"))
        self.rhopoutmin_input = FocusableLineEdit()
        self.rhopoutmin_input.set_help_text(HelpText.RHOPOUTMIN)
        self.rhopoutmin_input.setMaxLength(10)
        self.rhopoutmin_input.focus.connect(self.on_help_focus)
        self.rhopoutmin_input.setText(str(Case.the().execution_parameters.rhopoutmin))
        self.rhopoutmin_label2 = QtGui.QLabel("kg/m<span style='vertical-align:super'>3</span>")
        self.rhopoutmin_layout.addWidget(self.rhopoutmin_label)
        self.rhopoutmin_layout.addWidget(self.rhopoutmin_input)
        self.rhopoutmin_layout.addWidget(self.rhopoutmin_label2)

        # Maximum rhop valid
        self.rhopoutmax_layout = QtGui.QHBoxLayout()
        self.rhopoutmax_label = QtGui.QLabel(__("유효한 최대 rhop:"))
        self.rhopoutmax_input = FocusableLineEdit()
        self.rhopoutmax_input.set_help_text(HelpText.RHOPOUTMAX)
        self.rhopoutmax_input.setMaxLength(10)
        self.rhopoutmax_input.focus.connect(self.on_help_focus)
        self.rhopoutmax_input.setText(str(Case.the().execution_parameters.rhopoutmax))
        self.rhopoutmax_label2 = QtGui.QLabel("kg/m<span style='vertical-align:super'>3</span>")
        self.rhopoutmax_layout.addWidget(self.rhopoutmax_label)
        self.rhopoutmax_layout.addWidget(self.rhopoutmax_input)
        self.rhopoutmax_layout.addWidget(self.rhopoutmax_label2)

        # x,y,z Period
        self.period_x_layout = QtGui.QVBoxLayout()
        self.period_x_chk = QtGui.QCheckBox(__("X 주기성"))
        self.period_x_inc_layout = QtGui.QHBoxLayout()
        self.period_x_inc_x_label = QtGui.QLabel(__("X 증가"))
        self.period_x_inc_x_input = FocusableLineEdit()
        self.period_x_inc_y_label = QtGui.QLabel(__("Y 증가"))
        self.period_x_inc_y_input = FocusableLineEdit()
        self.period_x_inc_y_input.set_help_text(HelpText.YINCREMENTX)
        self.period_x_inc_y_input.focus.connect(self.on_help_focus)
        self.period_x_inc_z_label = QtGui.QLabel(__("Z 증가"))
        self.period_x_inc_z_input = FocusableLineEdit()
        self.period_x_inc_z_input.set_help_text(HelpText.ZINCREMENTX)
        self.period_x_inc_z_input.focus.connect(self.on_help_focus)
        self.period_x_inc_layout.addWidget(self.period_x_inc_x_label)
        self.period_x_inc_layout.addWidget(self.period_x_inc_x_input)
        self.period_x_inc_layout.addWidget(self.period_x_inc_y_label)
        self.period_x_inc_layout.addWidget(self.period_x_inc_y_input)
        self.period_x_inc_layout.addWidget(self.period_x_inc_z_label)
        self.period_x_inc_layout.addWidget(self.period_x_inc_z_input)
        self.period_x_layout.addWidget(self.period_x_chk)
        self.period_x_layout.addLayout(self.period_x_inc_layout)
        self.period_x_chk.stateChanged.connect(self.on_period_x_chk)

        self.period_x_chk.setChecked(Case.the().periodicity.x_periodicity.enabled)
        self.period_x_inc_x_input.setText(str(Case.the().periodicity.x_periodicity.x_increment))
        self.period_x_inc_y_input.setText(str(Case.the().periodicity.x_periodicity.y_increment))
        self.period_x_inc_z_input.setText(str(Case.the().periodicity.x_periodicity.z_increment))

        # Change the state of periodicity input on window open
        self.on_period_x_chk()

        self.period_y_layout = QtGui.QVBoxLayout()
        self.period_y_chk = QtGui.QCheckBox(__("Y 주기성"))
        self.period_y_inc_layout = QtGui.QHBoxLayout()
        self.period_y_inc_x_label = QtGui.QLabel(__("X 증가"))
        self.period_y_inc_x_input = FocusableLineEdit()
        self.period_y_inc_x_input.set_help_text(HelpText.XINCREMENTY)
        self.period_y_inc_x_input.focus.connect(self.on_help_focus)
        self.period_y_inc_y_label = QtGui.QLabel(__("Y 증가"))
        self.period_y_inc_y_input = FocusableLineEdit()
        self.period_y_inc_z_label = QtGui.QLabel(__("Z 증가"))
        self.period_y_inc_z_input = FocusableLineEdit()
        self.period_y_inc_z_input.set_help_text(HelpText.ZINCREMENTY)
        self.period_y_inc_z_input.focus.connect(self.on_help_focus)
        self.period_y_inc_layout.addWidget(self.period_y_inc_x_label)
        self.period_y_inc_layout.addWidget(self.period_y_inc_x_input)
        self.period_y_inc_layout.addWidget(self.period_y_inc_y_label)
        self.period_y_inc_layout.addWidget(self.period_y_inc_y_input)
        self.period_y_inc_layout.addWidget(self.period_y_inc_z_label)
        self.period_y_inc_layout.addWidget(self.period_y_inc_z_input)
        self.period_y_layout.addWidget(self.period_y_chk)
        self.period_y_layout.addLayout(self.period_y_inc_layout)
        self.period_y_chk.stateChanged.connect(self.on_period_y_chk)

        self.period_y_chk.setChecked(Case.the().periodicity.y_periodicity.enabled)
        self.period_y_inc_x_input.setText(str(Case.the().periodicity.y_periodicity.x_increment))
        self.period_y_inc_y_input.setText(str(Case.the().periodicity.y_periodicity.y_increment))
        self.period_y_inc_z_input.setText(str(Case.the().periodicity.y_periodicity.z_increment))

        # Change the state of periodicity input on window open
        self.on_period_y_chk()

        self.period_z_layout = QtGui.QVBoxLayout()
        self.period_z_chk = QtGui.QCheckBox(__("Z 주기성"))
        self.period_z_inc_layout = QtGui.QHBoxLayout()
        self.period_z_inc_x_label = QtGui.QLabel(__("X 증가"))
        self.period_z_inc_x_input = FocusableLineEdit()
        self.period_z_inc_x_input.set_help_text(HelpText.XINCREMENTZ)
        self.period_z_inc_x_input.focus.connect(self.on_help_focus)
        self.period_z_inc_y_label = QtGui.QLabel(__("Y 증가"))
        self.period_z_inc_y_input = FocusableLineEdit()
        self.period_z_inc_y_input.set_help_text(HelpText.YINCREMENTZ)
        self.period_z_inc_y_input.focus.connect(self.on_help_focus)
        self.period_z_inc_z_label = QtGui.QLabel(__("Z 증가"))
        self.period_z_inc_z_input = FocusableLineEdit()
        self.period_z_inc_layout.addWidget(self.period_z_inc_x_label)
        self.period_z_inc_layout.addWidget(self.period_z_inc_x_input)
        self.period_z_inc_layout.addWidget(self.period_z_inc_y_label)
        self.period_z_inc_layout.addWidget(self.period_z_inc_y_input)
        self.period_z_inc_layout.addWidget(self.period_z_inc_z_label)
        self.period_z_inc_layout.addWidget(self.period_z_inc_z_input)
        self.period_z_layout.addWidget(self.period_z_chk)
        self.period_z_layout.addLayout(self.period_z_inc_layout)
        self.period_z_chk.stateChanged.connect(self.on_period_z_chk)

        self.period_z_chk.setChecked(Case.the().periodicity.z_periodicity.enabled)
        self.period_z_inc_x_input.setText(str(Case.the().periodicity.z_periodicity.x_increment))
        self.period_z_inc_y_input.setText(str(Case.the().periodicity.z_periodicity.y_increment))
        self.period_z_inc_z_input.setText(str(Case.the().periodicity.z_periodicity.z_increment))

        # Change the state of periodicity input on window open
        self.on_period_z_chk()

        # Initial time step
        self.dtiniauto_layout = QtGui.QHBoxLayout()
        self.dtiniauto_chk = QtGui.QCheckBox(__("초기 시간 단계 (auto)"))
        if Case.the().execution_parameters.dtini_auto:
            self.dtiniauto_chk.setCheckState(QtCore.Qt.Checked)
        else:
            self.dtiniauto_chk.setCheckState(QtCore.Qt.Unchecked)
        
        self.dtiniauto_chk.toggled.connect(self.on_dtiniauto_check)
        self.dtiniauto_layout.addWidget(self.dtiniauto_chk)
        self.dtini_layout = QtGui.QHBoxLayout()
        self.dtini_label = QtGui.QLabel(__("초기 시간 단계:"))
        self.dtini_input = FocusableLineEdit()
        self.dtini_input.set_help_text(HelpText.DTINI)
        self.dtini_input.setMaxLength(10)
        self.dtini_input.focus.connect(self.on_help_focus)

        self.dtini_input.setText(str(Case.the().execution_parameters.dtini))
        self.dtini_label2 = QtGui.QLabel(__("초"))
        self.dtini_layout.addWidget(self.dtini_label)
        self.dtini_layout.addWidget(self.dtini_input)
        self.dtini_layout.addWidget(self.dtini_label2)
        self.on_dtiniauto_check()


        # Minimum time step
        self.dtminauto_layout = QtGui.QHBoxLayout()
        self.dtminauto_chk = QtGui.QCheckBox(__("최소 시간 단계:"))
        if Case.the().execution_parameters.dtmin_auto:
            self.dtminauto_chk.setCheckState(QtCore.Qt.Checked)
        else:
            self.dtminauto_chk.setCheckState(QtCore.Qt.Unchecked)

        self.dtminauto_chk.toggled.connect(self.on_dtminauto_check)
        self.dtminauto_layout.addWidget(self.dtminauto_chk)
        self.dtmin_layout = QtGui.QHBoxLayout()
        self.dtmin_label = QtGui.QLabel(__("최소 시간 단계:"))
        self.dtmin_input = FocusableLineEdit()
        self.dtmin_input.set_help_text(HelpText.DTMIN)
        self.dtmin_input.setMaxLength(10)

        self.dtmin_input.focus.connect(self.on_help_focus)

        self.dtmin_input.setText(str(Case.the().execution_parameters.dtmin))
        self.dtmin_label2 = QtGui.QLabel(__("초"))
        self.dtmin_layout.addWidget(self.dtmin_label)
        self.dtmin_layout.addWidget(self.dtmin_input)
        self.dtmin_layout.addWidget(self.dtmin_label2)
        self.on_dtminauto_check()

        # Fixed DT file
        self.dtfixed_layout = QtGui.QHBoxLayout()
        self.dtfixed_label = QtGui.QLabel(__("Fixed DT file: "))
        self.dtfixed_input = QtGui.QLineEdit()
        self.dtfixed_input.setText(str(Case.the().execution_parameters.dtfixed))
        self.dtfixed_label2 = QtGui.QLabel(__("file"))
        self.dtfixed_layout.addWidget(self.dtfixed_label)
        self.dtfixed_layout.addWidget(self.dtfixed_input)
        self.dtfixed_layout.addWidget(self.dtfixed_label2)

        # Velocity of particles
        self.dtallparticles_layout = QtGui.QHBoxLayout()
        self.dtallparticles_label = QtGui.QLabel(__("Velocity of particles: "))
        self.dtallparticles_input = QtGui.QLineEdit()
        self.dtallparticles_input.setMaxLength(1)
        self.dtallparticles_validator = QtGui.QIntValidator(0, 1, self.dtallparticles_input)
        self.dtallparticles_input.setText(str(Case.the().execution_parameters.dtallparticles))
        self.dtallparticles_input.setValidator(self.dtallparticles_validator)
        self.dtallparticles_label2 = QtGui.QLabel("[0, 1]")
        self.dtallparticles_layout.addWidget(self.dtallparticles_label)
        self.dtallparticles_layout.addWidget(self.dtallparticles_input)
        self.dtallparticles_layout.addWidget(self.dtallparticles_label2)

        # Simulation domain
        self.simdomain_layout = QtGui.QVBoxLayout()
        self.simdomain_chk = QtGui.QCheckBox(__("시뮬레이션 영역"))

        self.simdomain_chk.setChecked(Case.the().domain.enabled)

        self.simdomain_posmin_layout = QtGui.QHBoxLayout()
        self.simdomain_posminx_layout = QtGui.QVBoxLayout()
        self.simdomain_posminy_layout = QtGui.QVBoxLayout()
        self.simdomain_posminz_layout = QtGui.QVBoxLayout()
        self.simdomain_posmax_layout = QtGui.QHBoxLayout()
        self.simdomain_posmaxx_layout = QtGui.QVBoxLayout()
        self.simdomain_posmaxy_layout = QtGui.QVBoxLayout()
        self.simdomain_posmaxz_layout = QtGui.QVBoxLayout()
        self.simdomain_posmin_label = QtGui.QLabel(__("최소 위치(x, y, z):"))
        self.simdomain_posminx_combobox = QtGui.QComboBox()
        self.simdomain_posminx_combobox.insertItems(0, [__("Default"), __("Value"), __("Default - value"),
                                                        __("Default + %")])
        self.simdomain_posminx_line_edit = FocusableLineEdit()
        self.simdomain_posminx_line_edit.set_help_text(HelpText.POSMINX)
        self.simdomain_posminx_line_edit.focus.connect(self.on_help_focus)
        self.simdomain_posminx_line_edit.setText(str(Case.the().domain.posmin_x.value))
        self.simdomain_posminy_combobox = QtGui.QComboBox()
        self.simdomain_posminy_combobox.insertItems(0, [__("Default"), __("Value"), __("Default - value"),
                                                        __("Default + %")])
        self.simdomain_posminy_line_edit = FocusableLineEdit()
        self.simdomain_posminy_line_edit.set_help_text(HelpText.POSMINY)
        self.simdomain_posminy_line_edit.focus.connect(self.on_help_focus)
        self.simdomain_posminy_line_edit.setText(str(Case.the().domain.posmin_y.value))
        self.simdomain_posminz_combobox = QtGui.QComboBox()
        self.simdomain_posminz_combobox.insertItems(0, [__("Default"), __("Value"), __("Default - value"),
                                                        __("Default + %")])
        self.simdomain_posminz_line_edit = FocusableLineEdit()
        self.simdomain_posminz_line_edit.set_help_text(HelpText.POSMINZ)
        self.simdomain_posminz_line_edit.focus.connect(self.on_help_focus)
        self.simdomain_posminz_line_edit.setText(str(Case.the().domain.posmin_z.value))
        self.simdomain_posminx_layout.addWidget(self.simdomain_posminx_combobox)
        self.simdomain_posminx_layout.addWidget(self.simdomain_posminx_line_edit)
        self.simdomain_posminy_layout.addWidget(self.simdomain_posminy_combobox)
        self.simdomain_posminy_layout.addWidget(self.simdomain_posminy_line_edit)
        self.simdomain_posminz_layout.addWidget(self.simdomain_posminz_combobox)
        self.simdomain_posminz_layout.addWidget(self.simdomain_posminz_line_edit)
        self.simdomain_posmin_layout.addWidget(self.simdomain_posmin_label)
        self.simdomain_posmin_layout.addLayout(self.simdomain_posminx_layout)
        self.simdomain_posmin_layout.addLayout(self.simdomain_posminy_layout)
        self.simdomain_posmin_layout.addLayout(self.simdomain_posminz_layout)
        self.simdomain_posmax_label = QtGui.QLabel(__("최대 위치(x, y, z):"))
        self.simdomain_posmaxx_combobox = QtGui.QComboBox()
        self.simdomain_posmaxx_combobox.insertItems(0, [__("Default"), __("Value"), __("Default + value"),
                                                        __("Default + %")])
        self.simdomain_posmaxx_line_edit = FocusableLineEdit()
        self.simdomain_posmaxx_line_edit.set_help_text(HelpText.POSMAXX)
        self.simdomain_posmaxx_line_edit.focus.connect(self.on_help_focus)
        self.simdomain_posmaxx_line_edit.setText(str(Case.the().domain.posmax_x.value))
        self.simdomain_posmaxy_combobox = QtGui.QComboBox()
        self.simdomain_posmaxy_combobox.insertItems(0, [__("Default"), __("Value"), __("Default + value"),
                                                        __("Default + %")])
        self.simdomain_posmaxy_line_edit = FocusableLineEdit()
        self.simdomain_posmaxy_line_edit.set_help_text(HelpText.POSMAXY)
        self.simdomain_posmaxy_line_edit.focus.connect(self.on_help_focus)
        self.simdomain_posmaxy_line_edit.setText(str(Case.the().domain.posmax_y.value))
        self.simdomain_posmaxz_combobox = QtGui.QComboBox()
        self.simdomain_posmaxz_combobox.insertItems(0, [__("Default"), __("Value"), __("Default + value"),
                                                        __("Default + %")])
        self.simdomain_posmaxz_line_edit = FocusableLineEdit()
        self.simdomain_posmaxz_line_edit.set_help_text(HelpText.POSMAXZ)
        self.simdomain_posmaxz_line_edit.focus.connect(self.on_help_focus)
        self.simdomain_posmaxz_line_edit.setText(str(Case.the().domain.posmax_z.value))
        self.simdomain_posmaxx_layout.addWidget(self.simdomain_posmaxx_combobox)
        self.simdomain_posmaxx_layout.addWidget(self.simdomain_posmaxx_line_edit)
        self.simdomain_posmaxy_layout.addWidget(self.simdomain_posmaxy_combobox)
        self.simdomain_posmaxy_layout.addWidget(self.simdomain_posmaxy_line_edit)
        self.simdomain_posmaxz_layout.addWidget(self.simdomain_posmaxz_combobox)
        self.simdomain_posmaxz_layout.addWidget(self.simdomain_posmaxz_line_edit)
        self.simdomain_posmax_layout.addWidget(self.simdomain_posmax_label)
        self.simdomain_posmax_layout.addLayout(self.simdomain_posmaxx_layout)
        self.simdomain_posmax_layout.addLayout(self.simdomain_posmaxy_layout)
        self.simdomain_posmax_layout.addLayout(self.simdomain_posmaxz_layout)

        self.simdomain_posminx_combobox.setCurrentIndex(Case.the().domain.posmin_x.type)
        self.simdomain_posminy_combobox.setCurrentIndex(Case.the().domain.posmin_y.type)
        self.simdomain_posminz_combobox.setCurrentIndex(Case.the().domain.posmin_z.type)
        self.simdomain_posmaxx_combobox.setCurrentIndex(Case.the().domain.posmax_x.type)
        self.simdomain_posmaxy_combobox.setCurrentIndex(Case.the().domain.posmax_y.type)
        self.simdomain_posmaxz_combobox.setCurrentIndex(Case.the().domain.posmax_z.type)

        self.simdomain_layout.addWidget(self.simdomain_chk)
        self.simdomain_layout.addLayout(self.simdomain_posmin_layout)
        self.simdomain_layout.addLayout(self.simdomain_posmax_layout)
        self.simdomain_chk.stateChanged.connect(self.on_simdomain_chk)
        self.simdomain_posmaxx_combobox.currentIndexChanged.connect(self.on_posmaxx_changed)
        self.simdomain_posmaxy_combobox.currentIndexChanged.connect(self.on_posmaxy_changed)
        self.simdomain_posmaxz_combobox.currentIndexChanged.connect(self.on_posmaxz_changed)
        self.simdomain_posminx_combobox.currentIndexChanged.connect(self.on_posminx_changed)
        self.simdomain_posminy_combobox.currentIndexChanged.connect(self.on_posminy_changed)
        self.simdomain_posminz_combobox.currentIndexChanged.connect(self.on_posminz_changed)

        self.on_simdomain_chk()
        self.on_posmaxx_changed()
        self.on_posmaxy_changed()
        self.on_posmaxz_changed()
        self.on_posminx_changed()
        self.on_posminy_changed()
        self.on_posminz_changed()

        self.ok_button.clicked.connect(self.on_ok)
        self.cancel_button.clicked.connect(self.on_cancel)
        self.default_button.clicked.connect(self.default_button_pressed_ev)

        # ok, cancel layout definition
        self.ad_ep_button_layout = QtGui.QHBoxLayout()
        self.ad_ep_button_layout.addStretch(1)
        self.ad_ep_button_layout.addWidget(self.ok_button)
        self.ad_ep_button_layout.addWidget(self.cancel_button)
        self.ad_ep_button_layout.addWidget(self.default_button)

        # START Main Layout definition and composition.
        self.ad_ep_main_layout_scroll = QtGui.QScrollArea()
        self.ad_ep_main_layout_scroll.setWidgetResizable(True)

        self.ad_ep_main_layout_scroll_widget = QtGui.QWidget()

        self.ad_ep_main_layout = QtGui.QVBoxLayout()

        self.ad_ep_main_layout.addLayout(self.saveposdouble_layout)
        self.ad_ep_main_layout.addLayout(self.stepalgorithm_layout)
        self.ad_ep_main_layout.addLayout(self.verletsteps_layout)
        self.ad_ep_main_layout.addLayout(self.kernel_layout)
        self.ad_ep_main_layout.addLayout(self.densitydt_type_layout)
        self.ad_ep_main_layout.addLayout(self.densitydt_layout)
        self.ad_ep_main_layout.addLayout(self.shifting_layout)
        self.ad_ep_main_layout.addLayout(self.shiftcoef_layout)
        self.ad_ep_main_layout.addLayout(self.shifttfs_layout)
        self.ad_ep_main_layout.addLayout(self.rigidalgorithm_layout)
        self.ad_ep_main_layout.addLayout(self.ftpause_layout)
        self.ad_ep_main_layout.addLayout(self.dtiniauto_layout)
        self.ad_ep_main_layout.addLayout(self.dtini_layout)
        self.ad_ep_main_layout.addLayout(self.dtminauto_layout)
        self.ad_ep_main_layout.addLayout(self.dtmin_layout)
        self.ad_ep_main_layout.addLayout(self.coefdtmin_layout)
        self.ad_ep_main_layout.addLayout(self.rhopoutmin_layout)
        self.ad_ep_main_layout.addLayout(self.rhopoutmax_layout)
        self.ad_ep_main_layout.addLayout(self.period_x_layout)
        self.ad_ep_main_layout.addLayout(self.period_y_layout)
        self.ad_ep_main_layout.addLayout(self.period_z_layout)
        self.ad_ep_main_layout.addLayout(self.simdomain_layout)

        self.ad_ep_main_layout_scroll_widget.setLayout(self.ad_ep_main_layout)
        self.ad_ep_main_layout_scroll.setWidget(self.ad_ep_main_layout_scroll_widget)
        self.ad_ep_main_layout_scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        # main layout add other layout
        self.adexecparams_window_layout = QtGui.QVBoxLayout()
        self.adexecparams_window_layout.addWidget(self.ad_ep_main_layout_scroll)
        self.adexecparams_window_layout.addWidget(self.help_label)
        self.adexecparams_window_layout.addLayout(self.ad_ep_button_layout)
        self.setLayout(self.adexecparams_window_layout)

        # main layout configuration width, height for window
        self.setMinimumWidth(self.MINIMUM_WIDTH)
        self.setMinimumHeight(self.MINIMUM_HEIGHT)
        self.resize(self.MINIMUM_WIDTH, self.MINIMUM_HEIGHT)
        self.exec_()

    def on_help_focus(self, help_text):
        """ Reacts to focusing the help setting the corresponding help text. """
        self.help_label.setText("<b>{}: </b>{}".format(__("Help"), help_text))

    def on_step_change(self, index):
        """ Reacts to step algorithm changing enabling/disabling the verletsteps option. """
        self.verletsteps_input.setEnabled(index == 0)

    def on_densitydt_type_change(self, index):
        """ Reacts to densitydt type change enabling/disabling the input. """
        if index == 0:
            self.densitydt_input.setEnabled(False)
        else:
            self.densitydt_input.setEnabled(True)
            self.densitydt_input.setText("0.1")

    def on_shifting_change(self, index):
        """ Reacts to the shifting mode change enabling/disabling its input. """
        if index == 0:
            self.shiftcoef_input.setEnabled(False)
            self.shifttfs_input.setEnabled(False)
        else:
            self.shiftcoef_input.setEnabled(True)
            self.shifttfs_input.setEnabled(True)

    def on_dtiniauto_check(self):
        """ Reacts to the dtini automatic checkbox enabling/disabling its input. """
        if self.dtiniauto_chk.isChecked():
            self.dtini_input.setEnabled(False)
        else:
            self.dtini_input.setEnabled(True)

    def on_dtminauto_check(self):
        """ Reacts to the dtminauto checkbox enabling disabling its input. """
        if self.dtminauto_chk.isChecked():
            self.dtmin_input.setEnabled(False)
        else:
            self.dtmin_input.setEnabled(True)
    def on_period_x_chk(self):
        """ Reacts to the period_x checkbox being pressed enabling/disabling its inputs. """
        if self.period_x_chk.isChecked():
            self.period_x_inc_x_input.setEnabled(False)
            self.period_x_inc_y_input.setEnabled(True)
            self.period_x_inc_z_input.setEnabled(True)
        else:
            self.period_x_inc_x_input.setEnabled(False)
            self.period_x_inc_y_input.setEnabled(False)
            self.period_x_inc_z_input.setEnabled(False)

    def on_period_y_chk(self):
        """ Reacts to the period y checkbox being pressed enabling/disabling its inputs. """
        if self.period_y_chk.isChecked():
            self.period_y_inc_x_input.setEnabled(True)
            self.period_y_inc_y_input.setEnabled(False)
            self.period_y_inc_z_input.setEnabled(True)
        else:
            self.period_y_inc_x_input.setEnabled(False)
            self.period_y_inc_y_input.setEnabled(False)
            self.period_y_inc_z_input.setEnabled(False)

    def on_period_z_chk(self):
        """ Reacts to the period y checkbox being pressed enabling/disabling its inputs. """
        if self.period_z_chk.isChecked():
            self.period_z_inc_x_input.setEnabled(True)
            self.period_z_inc_y_input.setEnabled(True)
            self.period_z_inc_z_input.setEnabled(False)
        else:
            self.period_z_inc_x_input.setEnabled(False)
            self.period_z_inc_y_input.setEnabled(False)
            self.period_z_inc_z_input.setEnabled(False)

    def on_simdomain_chk(self):
        """ Reacts to the simdomain checkbox being pressed enabling/disabling its inputs. """
        if self.simdomain_chk.isChecked():
            self.simdomain_posminx_combobox.setEnabled(True)
            self.simdomain_posminy_combobox.setEnabled(True)
            self.simdomain_posminz_combobox.setEnabled(True)
            self.simdomain_posmaxx_combobox.setEnabled(True)
            self.simdomain_posmaxy_combobox.setEnabled(True)
            self.simdomain_posmaxz_combobox.setEnabled(True)
            if self.simdomain_posminx_combobox.currentIndex() != 0:
                self.simdomain_posminx_line_edit.setEnabled(True)
            else:
                self.simdomain_posminx_line_edit.setEnabled(False)

            if self.simdomain_posminy_combobox.currentIndex() != 0:
                self.simdomain_posminy_line_edit.setEnabled(True)
            else:
                self.simdomain_posminy_line_edit.setEnabled(False)

            if self.simdomain_posminz_combobox.currentIndex() != 0:
                self.simdomain_posminz_line_edit.setEnabled(True)
            else:
                self.simdomain_posminz_line_edit.setEnabled(False)

            if self.simdomain_posmaxx_combobox.currentIndex() != 0:
                self.simdomain_posmaxx_line_edit.setEnabled(True)
            else:
                self.simdomain_posmaxx_line_edit.setEnabled(False)

            if self.simdomain_posmaxy_combobox.currentIndex() != 0:
                self.simdomain_posmaxy_line_edit.setEnabled(True)
            else:
                self.simdomain_posmaxy_line_edit.setEnabled(False)

            if self.simdomain_posmaxz_combobox.currentIndex() != 0:
                self.simdomain_posmaxz_line_edit.setEnabled(True)
            else:
                self.simdomain_posmaxz_line_edit.setEnabled(False)
        else:
            self.simdomain_posminx_combobox.setEnabled(False)
            self.simdomain_posminy_combobox.setEnabled(False)
            self.simdomain_posminz_combobox.setEnabled(False)
            self.simdomain_posmaxx_combobox.setEnabled(False)
            self.simdomain_posmaxy_combobox.setEnabled(False)
            self.simdomain_posmaxz_combobox.setEnabled(False)
            self.simdomain_posminx_line_edit.setEnabled(False)
            self.simdomain_posminy_line_edit.setEnabled(False)
            self.simdomain_posminz_line_edit.setEnabled(False)
            self.simdomain_posmaxx_line_edit.setEnabled(False)
            self.simdomain_posmaxy_line_edit.setEnabled(False)
            self.simdomain_posmaxz_line_edit.setEnabled(False)

    def on_posminx_changed(self):
        """ Reacts to the posminx combobox being changed enabling/disabling its input. """
        if self.simdomain_posminx_combobox.currentIndex() == 0:
            self.simdomain_posminx_line_edit.setEnabled(False)
        else:
            self.simdomain_posminx_line_edit.setEnabled(True)

    def on_posminy_changed(self):
        """ Reacts to the posminy combobox being changed enabling/disabling its input. """
        if self.simdomain_posminy_combobox.currentIndex() == 0:
            self.simdomain_posminy_line_edit.setEnabled(False)
        else:
            self.simdomain_posminy_line_edit.setEnabled(True)

    def on_posminz_changed(self):
        """ Reacts to the posminz combobox being changed enabling/disabling its input. """
        if self.simdomain_posminz_combobox.currentIndex() == 0:
            self.simdomain_posminz_line_edit.setEnabled(False)
        else:
            self.simdomain_posminz_line_edit.setEnabled(True)

    def on_posmaxx_changed(self):
        """ Reacts to the posmaxx combobox being changed enabling/disabling its input. """
        if self.simdomain_posmaxx_combobox.currentIndex() == 0:
            self.simdomain_posmaxx_line_edit.setEnabled(False)
        else:
            self.simdomain_posmaxx_line_edit.setEnabled(True)

    def on_posmaxy_changed(self):
        """ Reacts to the posmaxy combobox being changed enabling/disabling its input. """
        if self.simdomain_posmaxy_combobox.currentIndex() == 0:
            self.simdomain_posmaxy_line_edit.setEnabled(False)
        else:
            self.simdomain_posmaxy_line_edit.setEnabled(True)

    def on_posmaxz_changed(self):
        """ Reacts to the posmaxz combobox being changed enabling/disabling its input. """
        if self.simdomain_posmaxz_combobox.currentIndex() == 0:
            self.simdomain_posmaxz_line_edit.setEnabled(False)
        else:
            self.simdomain_posmaxz_line_edit.setEnabled(True)

    def on_ok(self):
        Case.the().execution_parameters.saveposdouble = int(self.saveposdouble_input.currentIndex())
        Case.the().execution_parameters.stepalgorithm = int(self.stepalgorithm_input.currentIndex() + 1)
        Case.the().execution_parameters.verletsteps = int(self.verletsteps_input.text())
        Case.the().execution_parameters.kernel = int(self.kernel_input.currentIndex() + 1)
        Case.the().execution_parameters.densitydt_type = int(self.densitydt_type_input.currentIndex())
        Case.the().execution_parameters.densitydt_value = float(self.densitydt_input.text())
        Case.the().execution_parameters.shifting = int(self.shifting_input.currentIndex())
        Case.the().execution_parameters.shiftcoef = float(self.shiftcoef_input.text())
        Case.the().execution_parameters.shifttfs = float(self.shifttfs_input.text())
        Case.the().execution_parameters.rigidalgorithm = int(self.rigidalgorithm_input.currentIndex() + 1)
        Case.the().execution_parameters.ftpause = float(self.ftpause_input.text())
        Case.the().execution_parameters.coefdtmin = float(self.coefdtmin_input.text())
        Case.the().execution_parameters.dtini = float(self.dtini_input.text())
        Case.the().execution_parameters.dtini_auto = self.dtiniauto_chk.isChecked()
        Case.the().execution_parameters.dtmin = float(self.dtmin_input.text())
        Case.the().execution_parameters.dtmin_auto = self.dtminauto_chk.isChecked()
        Case.the().execution_parameters.dtfixed = str(self.dtfixed_input.text())
        Case.the().execution_parameters.dtallparticles = int(self.dtallparticles_input.text())
        Case.the().execution_parameters.rhopoutmin = int(self.rhopoutmin_input.text())
        Case.the().execution_parameters.rhopoutmax = int(self.rhopoutmax_input.text())

        Case.the().periodicity = Periodicity()
        Case.the().periodicity.x_periodicity = PeriodicityInfo(
            self.period_x_chk.isChecked(),
            float(self.period_x_inc_x_input.text()),
            float(self.period_x_inc_y_input.text()),
            float(self.period_x_inc_z_input.text())
        )

        Case.the().periodicity.y_periodicity = PeriodicityInfo(
            self.period_y_chk.isChecked(),
            float(self.period_y_inc_x_input.text()),
            float(self.period_y_inc_y_input.text()),
            float(self.period_y_inc_z_input.text())
        )

        Case.the().periodicity.z_periodicity = PeriodicityInfo(
            self.period_z_chk.isChecked(),
            float(self.period_z_inc_x_input.text()),
            float(self.period_z_inc_y_input.text()),
            float(self.period_z_inc_z_input.text())
        )

        if self.simdomain_chk.isChecked():
            Case.the().domain.enabled = True
            # IncZ must be 0 in simulations with specified domain
            Case.the().execution_parameters.incz = 0

            Case.the().domain.posmin_x = SDPositionProperty(self.simdomain_posminx_combobox.currentIndex(),
                                                            float(self.simdomain_posminx_line_edit.text()))
            Case.the().domain.posmin_y = SDPositionProperty(self.simdomain_posminy_combobox.currentIndex(),
                                                            float(self.simdomain_posminy_line_edit.text()))
            Case.the().domain.posmin_z = SDPositionProperty(self.simdomain_posminz_combobox.currentIndex(),
                                                            float(self.simdomain_posminz_line_edit.text()))

            Case.the().domain.posmax_x = SDPositionProperty(self.simdomain_posmaxx_combobox.currentIndex(),
                                                            float(self.simdomain_posmaxx_line_edit.text()))
            Case.the().domain.posmax_y = SDPositionProperty(self.simdomain_posmaxy_combobox.currentIndex(),
                                                            float(self.simdomain_posmaxy_line_edit.text()))
            Case.the().domain.posmax_z = SDPositionProperty(self.simdomain_posmaxz_combobox.currentIndex(),
                                                            float(self.simdomain_posmaxz_line_edit.text()))
        else:
            Case.the().domain.enabled = False
            Case.the().reset_simulation_domain()
        log("변경")
        self.accept()

    def on_cancel(self):
        """ Canceles the dialog rejecting it. """
        log("취소")
        self.reject()

    def default_button_pressed_ev(self):
        self.saveposdouble_input.setCurrentIndex(int(Case.the().execution_parameters.saveposdouble))
        self.stepalgorithm_input.setCurrentIndex(int(Case.the().execution_parameters.stepalgorithm) - 1)
        self.verletsteps_input.setText(str(Case.the().execution_parameters.verletsteps))
        self.kernel_input.setCurrentIndex(int(Case.the().execution_parameters.kernel) - 1)
        self.densitydt_type_input.setCurrentIndex(Case.the().execution_parameters.densitydt_type)
        self.densitydt_input.setText(str(Case.the().execution_parameters.densitydt_value))
        self.shifting_input.setCurrentIndex(int(Case.the().execution_parameters.shifting))
        self.shiftcoef_input.setText(str(Case.the().execution_parameters.shiftcoef))
        self.shifttfs_input.setText(str(Case.the().execution_parameters.shifttfs))
        self.rigidalgorithm_input.setCurrentIndex(int(Case.the().execution_parameters.rigidalgorithm) - 1)
        self.ftpause_input.setText(str(Case.the().execution_parameters.ftpause))
        self.coefdtmin_input.setText(str(Case.the().execution_parameters.coefdtmin))
        self.rhopoutmin_input.setText(str(Case.the().execution_parameters.rhopoutmin))
        self.rhopoutmax_input.setText(str(Case.the().execution_parameters.rhopoutmax))
        self.period_x_chk.setChecked(Case.the().periodicity.x_periodicity.enabled)
        self.period_x_inc_x_input.setText(str(Case.the().periodicity.x_periodicity.x_increment))
        self.period_x_inc_y_input.setText(str(Case.the().periodicity.x_periodicity.y_increment))
        self.period_x_inc_z_input.setText(str(Case.the().periodicity.x_periodicity.z_increment))
        self.period_y_chk.setChecked(Case.the().periodicity.y_periodicity.enabled)
        self.period_y_inc_x_input.setText(str(Case.the().periodicity.y_periodicity.x_increment))
        self.period_y_inc_y_input.setText(str(Case.the().periodicity.y_periodicity.y_increment))
        self.period_y_inc_z_input.setText(str(Case.the().periodicity.y_periodicity.z_increment))
        self.period_z_chk.setChecked(Case.the().periodicity.z_periodicity.enabled)
        self.period_z_inc_x_input.setText(str(Case.the().periodicity.z_periodicity.x_increment))
        self.period_z_inc_y_input.setText(str(Case.the().periodicity.z_periodicity.y_increment))
        self.period_z_inc_z_input.setText(str(Case.the().periodicity.z_periodicity.z_increment))
        self.dtiniauto_chk.setCheckState(QtCore.Qt.Checked)
        self.dtini_input.setText(str(Case.the().execution_parameters.dtini))
        self.dtminauto_chk.setCheckState(QtCore.Qt.Checked)
        self.dtmin_input.setText(str(Case.the().execution_parameters.dtmin))
        self.dtfixed_input.setText(str(Case.the().execution_parameters.dtfixed))
        self.dtallparticles_input.setText(str(Case.the().execution_parameters.dtallparticles))
        self.simdomain_posminx_line_edit.setText(str(Case.the().domain.posmin_x.value))
        self.simdomain_posminy_line_edit.setText(str(Case.the().domain.posmin_y.value))
        self.simdomain_posminz_line_edit.setText(str(Case.the().domain.posmin_z.value))
        self.simdomain_posmaxx_line_edit.setText(str(Case.the().domain.posmax_x.value))
        self.simdomain_posmaxy_line_edit.setText(str(Case.the().domain.posmax_y.value))
        self.simdomain_posmaxz_line_edit.setText(str(Case.the().domain.posmax_z.value))
        self.simdomain_posminx_combobox.setCurrentIndex(Case.the().domain.posmin_x.type)
        self.simdomain_posminy_combobox.setCurrentIndex(Case.the().domain.posmin_y.type)
        self.simdomain_posminz_combobox.setCurrentIndex(Case.the().domain.posmin_z.type)
        self.simdomain_posmaxx_combobox.setCurrentIndex(Case.the().domain.posmax_x.type)
        self.simdomain_posmaxy_combobox.setCurrentIndex(Case.the().domain.posmax_y.type)
        self.simdomain_posmaxz_combobox.setCurrentIndex(Case.the().domain.posmax_z.type)
        self.simdomain_chk.setChecked(Case.the().domain.enabled)


