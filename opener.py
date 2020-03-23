from PySide2 import QtCore, QtGui, QtWidgets, QtUiTools
from shiboken2 import wrapInstance

import maya.cmds as mc
import maya.api.OpenMaya as om
import maya.OpenMayaUI as omui


# don't use reload() if you want to keep ui position
class Opener(QtWidgets.QDialog):
    WINDOW_TITLE = "Saver"
    dlg_instance = None

    # override in child class (change 'cls.dlg_instance = TemplateUi()' to 'cls.dlg_instance = ChildClassName()')
    @classmethod
    def show_dialog(cls):
        if not cls.dlg_instance:
            cls.dlg_instance = TemplateUi()

        if cls.dlg_instance.isHidden():
            cls.dlg_instance.show()
        else:
            cls.dlg_instance.raise_()
            # cls.dlg_instance.activateWindow()

    @classmethod
    def maya_main_window(cls):
        """ Return Maya main window as Python Object """
        main_window_ptr = omui.MQtUtil.mainWindow()
        return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)

    def __init__(self):
        super(Opener, self).__init__(self.maya_main_window())

        self.setWindowTitle(self.WINDOW_TITLE)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.geometry = None

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_ui_widget(self, path):

        loader= QtUiTools.QUiLoader()
        return loader.load(path, parentWidget= None)

    def create_widgets(self):

        self.ui= self.create_ui_widget('/home/bapt0710/maya/2018/prefs/scripts/commit_saver/ui_shematics/opener.ui')

    def create_layouts(self):

        self.main_layout= QtWidgets.QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addWidget(self.ui)

    def create_connections(self):
        pass

    def showEvent(self, e):
        super(TemplateUi, self).showEvent(e)
        if self.geometry:
            self.restoreGeometry(self.geometry)

    def closeEvent(self, e):
        if isinstance(self, TemplateUi):
            super(TemplateUi, self).closeEvent(e)
            self.geometry = self.saveGeometry()
