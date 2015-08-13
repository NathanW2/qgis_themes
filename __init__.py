#-----------------------------------------------------------
# Copyright (C) 2015 Martin Dobias
#-----------------------------------------------------------
# Licensed under the terms of GNU GPL 2
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#---------------------------------------------------------------------
import os

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.uic import loadUiType

import themes

def resolve(name):
    f = os.path.join(os.path.dirname(__file__), name)
    return f


widget, base = loadUiType(resolve(os.path.join("ui", "picker.ui")))

def apply_theme(name):
    if name == "default" or not name:
        name = "default"
        data = ''
    else:
        try:
            data = themes.get_theme(name)
        except KeyError:
            data = ''

    QApplication.instance().setStyleSheet(data)
    settings = QSettings()
    settings.setValue("plugins/qgis-themes/theme", name)



class ThemePicker(widget, base):
    def __init__(self, parent=None):
        super(ThemePicker, self).__init__(parent)
        self.setupUi(self)
        self._theme = "default"

        self.themes.currentTextChanged.connect(self.apply_theme)

        apply = self.buttons.button(QDialogButtonBox.Apply)
        apply.clicked.connect(self.apply_theme)

    def set_theme(self, name):
        item = self.themes.findItems(name, Qt.MatchCaseSensitive)[0]
        self.themes.setCurrentItem(item)
        self._theme = name

    def load_themes(self, themes):
        self.themes.addItem("default")
        self.themes.addItems(themes)

    def apply_theme(self):
        apply_theme(self.themes.currentItem().text())

    def reject(self):
        apply_theme(self._theme)
        super(ThemePicker, self).reject()


def theme_from_settings():
    settings = QSettings()
    theme = settings.value("plugins/qgis-themes/theme", "default")
    return theme


def load_theme():
    apply_theme(theme_from_settings())


def open_file(path):
    import subprocess
    try:
        subprocess.Popen([os.environ['EDITOR'], path])
    except KeyError:
        QDesktopServices.openUrl(QUrl.fromLocalFile(path))


def classFactory(iface):
    return ThemePlugin(iface)


class ThemePlugin:
    def __init__(self, iface):
        self.iface = iface
        self.iface.initializationCompleted.connect(load_theme)

    def initGui(self):
        self.action = QAction("Theme it!", self.iface.mainWindow())
        self.action.triggered.connect(self.run)
        self.iface.addPluginToMenu("UI Themes", self.action)

    def unload(self):
        self.iface.removeToolBarIcon(self.action)
        del self.action

    def run(self):
        dlg = ThemePicker(self.iface.mainWindow())
        dlg.load_themes(themes.themes.keys())
        dlg.set_theme(theme_from_settings())
        dlg.exec_()
