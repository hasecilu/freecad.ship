#***************************************************************************
#*                                                                         *
#*   Copyright (c) 2011, 2016 Jose Luis Cercos Pita <jlcercos@gmail.com>   *
#*                                                                         *
#*   This program is free software; you can redistribute it and/or modify  *
#*   it under the terms of the GNU Lesser General Public License (LGPL)    *
#*   as published by the Free Software Foundation; either version 2 of     *
#*   the License, or (at your option) any later version.                   *
#*   for detail see the LICENCE text file.                                 *
#*                                                                         *
#*   This program is distributed in the hope that it will be useful,       *
#*   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
#*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
#*   GNU Library General Public License for more details.                  *
#*                                                                         *
#*   You should have received a copy of the GNU Library General Public     *
#*   License along with this program; if not, write to the Free Software   *
#*   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
#*   USA                                                                   *
#*                                                                         *
#***************************************************************************

import math
import FreeCAD as App
import FreeCADGui as Gui
from FreeCAD import Units
from PySide import QtGui, QtCore
from . import Preview
from . import PlotAux
from .. import Ship_rc
from ..import Instance
from ..shipUtils import Locale
from ..shipUtils import Selection
from ..shipHydrostatics import Tools as Hydrostatics
from ..init_gui import QT_TRANSLATE_NOOP


class TaskPanel:
    def __init__(self):
        self.name = "ship areas plotter"
        self.ui = ":/ui/TaskPanel_resistanceAmadeo.ui"
        self.form = Gui.PySideUic.loadUi(self.ui)
        self.preview = Preview.Preview()
        self.ship = None

    def accept(self):
        if not self.ship:
            return False
        return True

    def reject(self):
        return True

    def clicked(self, index):
        pass

    def open(self):
        pass

    def needsFullSpace(self):
        return True

    def isAllowedAlterSelection(self):
        return False

    def isAllowedAlterView(self):
        return True

    def isAllowedAlterDocument(self):
        return False

    def helpRequested(self):
        pass

    def setupUi(self):
        self.form.protuberance = self.widget(QtGui.QLineEdit, "protuberance")
        self.form.max_speed = self.widget(QtGui.QLineEdit, "max_speed")
        self.form.min_speed = self.widget(QtGui.QLineEdit, "min_speed")
        self.form.n_of_speeds = self.widget(QtGui.QLineEdit, "n_of_speeds")
        self.form.trim = self.widget(QtGui.QLineEdit, "trim")
        self.form.num = self.widget(QtGui.QSpinBox, "num")
        self.form.output_data = self.widget(QtGui.QTextEdit, "output_data")
        self.form.doc = QtGui.QTextDocument(self.form.output_data)
        if self.initValues():
            return True

    def getMainWindow(self):
        toplevel = QtGui.QApplication.topLevelWidgets()
        for i in toplevel:
            if i.metaObject().className() == "Gui::MainWindow":
                return i
        raise RuntimeError("No main window found")

    def widget(self, class_id, name):
        """Return the selected widget.

        Keyword arguments:
        class_id -- Class identifier
        name -- Name of the widget
        """
        mw = self.getMainWindow()
        form = mw.findChild(QtGui.QWidget, "AmadeoTaskPanel")
        return form.findChild(class_id, name)

    def initValues(self):
        """ Set initial values for fields
        """
        sel_ships = Selection.get_ships()
        if not sel_ships:
            msg = App.Qt.translate(
                "ship_console",
                "A ship instance must be selected before using this tool")
            App.Console.PrintError(msg + '\n')
            return True
        self.ship = sel_ships[0]
        if len(sel_ships) > 1:
            msg = App.Qt.translate(
                "ship_console",
                "More than one ship have been selected (just the one labelled"
                "'{}' is considered)".format(self.ship.Label))
            App.Console.PrintWarning(msg + '\n')

        self.form.protuberance.setText("0 m")
        self.form.max_speed.setText("0 knot")
        self.form.min_speed.setText("0 knot")
        self.form.n_of_speeds.setText("2")
        return False
    
def createTask():
    panel = TaskPanel()
    Gui.Control.showDialog(panel)
    if panel.setupUi():
        Gui.Control.closeDialog()
        return None
    return panel