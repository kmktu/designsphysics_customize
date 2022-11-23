from PySide import QtGui

from mod.translation_tools import __
from mod.stdout_tools import log
import os, sys
import inspect

# PARAVIEWPATH = "C:/Users/mgkang.DI-SOLUTION/Desktop/KANG/PYcharm_project/" \
#                "git/FreeCad/DesignSPHysics-master/paraview_build/bin"
# # PARAVIEWPATH = "../../paraview_build/bin"
# PARAVIEW_LIB = "C:/Users/mgkang.DI-SOLUTION/Desktop/KANG/PYcharm_project/" \
#                "git/FreeCad/DesignSPHysics-master/paraview_build/bin/Lib"
# # PARAVIEW_LIB = "../../paraview_build/bin/Lib"
# PARAVIEW_SITE_PACKAGES = "C:/Users/mgkang.DI-SOLUTION/Desktop/KANG/PYcharm_project/" \
#                          "git/FreeCad/DesignSPHysics-master/paraview_build/bin/Lib/site-packages"
# # PARAVIEW_SITE_PACKAGES = "../../paraview_build/bin/Lib/site-packages"
#
# sys.path.append(PARAVIEWPATH)
# sys.path.append(PARAVIEW_LIB)
# sys.path.append(PARAVIEW_SITE_PACKAGES)
#
# PYTHONPATH = PARAVIEWPATH +";" + PARAVIEW_LIB + ";" + PARAVIEW_SITE_PACKAGES

# os.environ['PYTHONPATH'] = PYTHONPATH
# from paraview.simple import *
# from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
#
# print("pATH1 : ", inspect.getfile(paraview))
# print("pATH2 : ", inspect.getfile(QVTKRenderWindowInteractor))
# print("PYTHONPATH : ", os.environ['PYTHONPATH'])


import glob
import subprocess

class SimulationVisualDialog(QtGui.QDialog):
    MINIMUM_WIDTH = 600
    MINIMUM_HEIGHT = 600

    def __init__(self, input_text: str):
        super().__init__()
        self.input_text = input_text
        self.simulation_visualization_window = QtGui.QDialog()
        self.simulation_visualization_window.setWindowTitle(__("Simulation Visualization"))

        self.simulation_visualization_button = QtGui.QPushButton(__("Import"))
        self.cancel_button = QtGui.QPushButton(__("취소"))

        self.simulation_visualization_layout = QtGui.QVBoxLayout()
        self.button_layout = QtGui.QHBoxLayout()
        self.button_layout.addStretch(1)
        self.button_layout.addWidget(self.cancel_button)
        self.button_layout.addWidget(self.simulation_visualization_button)

        self.cancel_button.clicked.connect(self.cancel_button_pressed)
        self.simulation_visualization_button.clicked.connect(self.sv_button_pressed)
        # self.simulation_visualization_button.clicked.connect(self.sv_button_pressed)

        self.simulation_visualization_window_layout = QtGui.QVBoxLayout()
        self.simulation_visualization_window_layout.addLayout(self.simulation_visualization_layout)
        self.simulation_visualization_window_layout.addLayout(self.button_layout)
        self.setLayout(self.simulation_visualization_window_layout)

        self.setMinimumWidth(self.MINIMUM_WIDTH)
        self.setMinimumHeight(self.MINIMUM_HEIGHT)
        self.resize(self.MINIMUM_WIDTH, self.MINIMUM_HEIGHT)

        self.exec_()

    def cancel_button_pressed(self):
        self.reject()

    def sv_button_pressed(self):
        print("Test")
        # 대실패
        # import paraview
        # from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
        # print("pATH1 : ", inspect.getfile(paraview))
        # print("pATH2 : ", inspect.getfile(QVTKRenderWindowInteractor))
        #
        # split_list = self.input_text.split("!!")
        # case_path = split_list[0]
        # case_name = split_list[1]
        # options_file_name = split_list[2]
        # renderview = simple.GetActiveViewOrCreate('RenderView')
        # renderWidget = QVTKRenderWindowInteractor(rw=renderview.GetRenderWindow(), iren=renderview.GetInteractor())
        #
        # renderWidget.Initialize()
        #
        # file_list = glob.glob(case_path +"/" + case_name + "_out/" + options_file_name + "_*.vtk")
        # reader = simple.OpenDataFile(file_list)
        # view_display = Show(reader, renderview)
        # renderWidget.show()


        # 빌드된 paraview 폴더를 designsphysics 폴더로 옮겼을때
        # 시스템 변수에 파라뷰 설치 위치 추가 후 사용

        # os.system("pvpython " + "../../mod/widgets/paraview_visualization.py -i " + self.input_text)

        # input_args = str(self.input_text)
        sorce_path = "../../mod/widgets/paraview_visualization.py"
        print("sorce_path : ", sorce_path)
        command = "pvpython" + " " + sorce_path
        print("Command : ", command)

        proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
        out, err = proc.communicate(input=bytes(self.input_text, encoding='utf-8'))
        # while True:
        #
        #     if out == '' and proc.poll() is not None:
        #         break
        #     if out:
        #         print("out_output : ", out.decode('utf-8'))
        #         print("err_output : ", err.decode('euc-kr'))  # 왜 한글로 나오지

        print("out_output : ", out.decode('utf-8'))
        print("err_output : ", err.decode('euc-kr'))  # 왜 한글로 나오지

        # proc.wait()
        # process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        # while True:
        #     output = process.stdout.readline()
        #     if output == '' and process.poll() is not None:
        #         break
        #     if output:
        #         print(output.strip())
