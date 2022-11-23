#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Dialog Tools.

Contains general use standard dialogs. """

from PySide import QtGui

from mod.translation_tools import __

from mod.widgets.information_dialog import InformationDialog
from mod.widgets.information_dialog_isosurface import InformationIsoSurfaceDialog

def warning_dialog(warn_text, detailed_text=None):
    """Spawns a warning dialog with the text and details passed."""
    InformationDialog(__("WARNING"), warn_text, detailed_text)


def error_dialog(error_text, detailed_text=None):
    """Spawns an error dialog with the text and details passed."""
    InformationDialog(__("ERROR"), error_text, detailed_text)


def info_dialog(info_text, detailed_text=None, input_text=None):
    """Spawns an info dialog with the text and details passed."""
    text_list = info_text.split(" ")
    if text_list[0] == "IsoSurface":
        InformationIsoSurfaceDialog(__("Information"), info_text, detailed_text, input_text=input_text)
    else:
        InformationDialog(__("Information"), info_text, detailed_text)


# def iso_surface_dialog(info_text, detailed_text=None, input_text=None):
#     InformationIsoSurfaceDialog(__("Information"), info_text, detailed_text, input_text)

def ok_cancel_dialog(title, text):
    """Spawns an okay/cancel dialog with the title and text passed"""
    open_confirm_dialog = QtGui.QMessageBox()
    open_confirm_dialog.setWindowTitle(title)
    open_confirm_dialog.setText(text)
    open_confirm_dialog.setStandardButtons(QtGui.QMessageBox.Ok |
                                           QtGui.QMessageBox.Cancel)
    open_confirm_dialog.setDefaultButton(QtGui.QMessageBox.Ok)
    return open_confirm_dialog.exec_()

def ok_discard_dialog(title, text):
    """Spawns an okay/discard dialog with the title and text passed"""
    open_confirm_dialog = QtGui.QMessageBox()
    open_confirm_dialog.setWindowTitle(title)
    open_confirm_dialog.setText(text)
    open_confirm_dialog.setStandardButtons(QtGui.QMessageBox.Ok |
                                           QtGui.QMessageBox.Discard)
    open_confirm_dialog.setDefaultButton(QtGui.QMessageBox.Ok)
    return open_confirm_dialog.exec_()
