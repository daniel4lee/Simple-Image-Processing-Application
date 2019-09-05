import sys
from PyQt5.QtWidgets import QApplication
from Gui.gui import GuiRoot

if __name__ == '__main__':
    
    sys.argv += ['--style', 'fusion']
    app = QApplication(sys.argv)
    gui_root = GuiRoot() # instance of the gui
    sys.exit(app.exec_())