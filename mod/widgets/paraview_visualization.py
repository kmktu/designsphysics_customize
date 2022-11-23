import os, sys

PARAVIEWPATH = "C:/Users/mgkang.DI-SOLUTION/Desktop/KANG/PYcharm_project/" \
               "git/FreeCad/DesignSPHysics-master/paraview_build/bin"
PARAVIEW_LIB = "C:/Users/mgkang.DI-SOLUTION/Desktop/KANG/PYcharm_project/" \
               "git/FreeCad/DesignSPHysics-master/paraview_build/bin/Lib"
PARAVIEW_SITE_PACKAGES = "C:/Users/mgkang.DI-SOLUTION/Desktop/KANG/PYcharm_project/" \
                         "git/FreeCad/DesignSPHysics-master/paraview_build/bin/Lib/site-packages"
sys.path.append(PARAVIEWPATH)
sys.path.append(PARAVIEW_LIB)
sys.path.append(PARAVIEW_SITE_PACKAGES)

from paraview.simple import *
import argparse
import glob
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

import time

def add_vtk(input_text):
    split_list = input_text.split("!!")
    case_path = split_list[0]
    case_name = split_list[1]
    options_file_name = split_list[2]

    # renderView = GetActiveViewOrCreate('RenderView')
    renderView = CreateRenderView('RenderView')
    renderView.ViewSize = [1280, 400]
    renderView.OrientationAxesVisibility = 0

    # renderWidget = QVTKRenderWindowInteractor(rw=renderView.GetRenderWindow(), iren=renderView.GetInteractor())
    # renderWidget.Initialize()

    # Create a list of names of all the files in the file series.
    file_list = glob.glob(case_path + "/" + case_name + "_out/" + options_file_name + "_*.vtk")

    reader = OpenDataFile(file_list)

    layout = GetLayoutByName("LAYOUT")
    AssignViewToLayout(view=renderView, layout=layout, hint=0)
    SetActiveView(renderView)

    view_display = Show(reader, renderView)
    view_display.SetScalarBarVisibility(renderView, True)

    # renderView.CameraParallelScale = 50
    # renderView.CameraPosition =[-20, -5, -5]

    # c = GetActiveCamera()
    # c.Elevation(-45)
    #
    scene = GetAnimationScene()
    scene.NumberOfFrames = len(file_list)
    # # scene.GoToNext()
    scene.PlayMode = 'Sequence'
    #
    # scene.Play()

    scene.Play()
    # Render()

    # scene.GoToFirst()
    # time.sleep(3)

    # track = GetAnimationTrack('Origin', index=2, proxy=reader)
    # Render()
    try:
        while True:
            scene.Play()
    except KeyboardInterrupt:
        pass


def read_args():
    paraser = argparse.ArgumentParser()
    paraser.add_argument("-i", "--input_text", type=str)
    args = paraser.parse_args()
    print("args : ", args)
    input_text = args.input_text
    return input_text


def visualization_main():
    # print("stdin.read : ", sys.stdin.readline())
    # input_text = sys.stdin.readline()

    # test
    input_text = read_args()

    # print("input_text !!!! : ", input_text)
    add_vtk(input_text=input_text)

class Paraview_dialog(QWidget):
    def __init__(self):
        super().__init__()
        self.input_text = sys.stdin.readline()
        # self.initUI(self.input_text)

        self.main_view_layout = QVBoxLayout()
        self.setWindowTitle("ParaView Visualization")
        self.setGeometry(200, 200, 1080, 800)

        self.button_layout = QHBoxLayout()

        self.render_view = CreateRenderView()
        self.render_widget = QVTKRenderWindowInteractor(rw=self.render_view.GetRenderWindow(),
                                                        iren=self.render_view.GetInteractor())
        self.render_widget.Initialize()

        # self.render_layout.addWidget(self.render_widget)
        self.go_to_first_button = QPushButton("Go To First")
        self.play_button = QPushButton("Play")
        self.button_layout.addWidget(self.go_to_first_button)
        self.button_layout.addWidget(self.play_button)

        self.main_view_layout.addWidget(self.render_widget)
        self.main_view_layout.addLayout(self.button_layout)

        self.go_to_first_button.clicked.connect(self.go_to_first_button_clicked)
        self.play_button.clicked.connect(self.play_button_clicked)

        split_list = self.input_text.split("!!")
        case_path = split_list[0]
        case_name = split_list[1]
        options_file_name = split_list[2]

        self.file_list = glob.glob(case_path + "/" + case_name + "_out/" + options_file_name + "_*.vtk")

        self.reader = OpenDataFile(self.file_list)

        # layout = GetLayoutByName("LAYOUT")
        # AssignViewToLayout(view=renderView, layout=layout, hint=0)
        # SetActiveView(renderView)

        self.scene = GetAnimationScene()
        self.scene.NumberOfFrames = len(self.file_list)
        self.scene.PlayMode = 'Sequence'

        c = GetActiveCamera()
        c.Elevation(-45)

        view_display = Show(self.reader, self.render_view)
        # self.render_widget.show()

        # self.main_view_layout.addLayout(self.render_layout)

        self.setLayout(self.main_view_layout)
        # self.show()
        # scene.Play()

    def go_to_first_button_clicked(self):
        self.scene.GoToFisrt()

    def play_button_clicked(self):
        self.scene.Play()


if __name__ == '__main__':
    # input_text = sys.stdin.readline()
    app = QApplication(sys.argv)
    main_dialog = Paraview_dialog()
    main_dialog.show()
    # main_dialog.scene.Play()
    app.exec_()

# app = QtWidgets.QApplication(sys.argv)
# visualization_main()
# sys.exit(app.exec())
