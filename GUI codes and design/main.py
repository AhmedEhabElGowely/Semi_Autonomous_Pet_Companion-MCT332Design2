from utils import *
from Joystick import *
from HomeGui import *


def maininit():
    homescene = MainWindow()
    joystickscene = JoystickWindow()
    sceneStack.addWidget(homescene)  # index 0
    sceneStack.addWidget(joystickscene)  # index 1
    sceneStack.setCurrentIndex(0)
    sceneStack.resize(940,540)
    sceneStack.show()
    app.exec_()


if __name__ == '__main__':
    maininit()
