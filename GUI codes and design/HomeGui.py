import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QWidget
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtGui import QFont, QPixmap
import socket
from utils import *
from PyQt5 import uic


# Define a custom signal


class SignalSender(QObject):
    signal = pyqtSignal()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('./HomeWindow.ui', self)
        #self.Feedbutton = self.findChild(QPushButton, 'Feed')
        self.Startbutton = self.findChild(QPushButton, 'Start')
        self.Stopbutton = self.findChild(QPushButton, 'Stop')
        #self.Laserbutton = self.findChild(QPushButton, 'Laser')
        #self.livestreamingbutton = self.findChild(QPushButton, 'Livestream')
        self.manualmodebutton = self.findChild(QPushButton, 'Manualmode')

        #self.Feedbutton.clicked.connect(self.send_signal_feed)
        self.Startbutton.clicked.connect(self.send_signal_start)
        self.Stopbutton.clicked.connect(self.send_signal_stop)
        #self.Laserbutton.clicked.connect(self.send_signal_laser)
        #self.livestreamingbutton.clicked.connect(self.send_signal_livestreaming)
        self.manualmodebutton.clicked.connect(self.send_signal_manualmode)

        self.Startbutton.setStyleSheet("background-color:green; color: white;")
        self.Stopbutton.setStyleSheet("background-color:red; color: white;")
        

    #def send_signal_feed(self):
        # Create a signal sender objectq
        #signal_sender = SignalSender()

        # Connect the signal sender's signal to a slot function
        #signal_sender.signal.connect(self.send_to_raspberry_pi_feeding)

        # Emit the signal
        #signal_sender.signal.emit()

    def send_signal_start(self):
        # Create a signal sender objectq
        signal_sender2 = SignalSender()

        # Connect the signal sender's signal to a slot function
        signal_sender2.signal.connect(self.send_to_raspberry_pi_starting)

        # Emit the signal
        signal_sender2.signal.emit()

    def send_signal_stop(self):
        # Create a signal sender objectq
        signal_sender3 = SignalSender()

        # Connect the signal sender's signal to a slot function
        signal_sender3.signal.connect(self.send_to_raspberry_pi_stoping)

        # Emit the signal
        signal_sender3.signal.emit()

    #def send_signal_laser(self):
        # Create a signal sender objectq
        #signal_sender4 = SignalSender()

        # Connect the signal sender's signal to a slot function
        #signal_sender4.signal.connect(self.send_to_raspberry_pi_laser)

        # Emit the signal
        #signal_sender4.signal.emit()

    #def send_signal_livestreaming(self):
        # Create a signal sender objectq
        #signal_sender5 = SignalSender()

        # Connect the signal sender's signal to a slot function
        #signal_sender5.signal.connect(self.send_to_raspberry_pi_livestreaming)

        # Emit the signal
        #signal_sender5.signal.emit()

    def send_signal_manualmode(self):
        sceneStack.setCurrentIndex(1)
        signal_sender6 = SignalSender()
        # Connect the signal sender's signal to a slot function
        signal_sender6.signal.connect(self.send_to_raspberry_pi_manualmode)
        # Emit the signal
        signal_sender6.signal.emit()


    #def send_to_raspberry_pi_feeding(self):
        # Raspberry Pi IP address and port
        #pi_ip = '192.168.108.93'
        #pi_port = 1115

        # Create a socket object
        #sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #try:
            # Connect to the Raspberry Pi
            #sock.connect((pi_ip, pi_port))

            # Send the signal data
            #signal_data = "Feeding Pet"
            #sock.sendall(signal_data.encode())

            # Close the connection
            #sock.close()
        #except ConnectionRefusedError:
            #print("Failed to connect to the Raspberry Pi.")

        #print("Signal sent to the Raspberry Pi!")

    def send_to_raspberry_pi_starting(self):
        # Raspberry Pi IP address and port
        pi_ip = '192.168.108.93'
        pi_port = 1115

        # Create a socket object
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            # Connect to the Raspberry Pi
            sock.connect((pi_ip, pi_port))

            # Send the signal data
            signal_data = "Starting"
            sock.sendall(signal_data.encode())

            # Close the connection
            sock.close()
        except ConnectionRefusedError:
            print("Failed to connect to the Raspberry Pi.")

        print("Signal sent to the Raspberry Pi!")

    def send_to_raspberry_pi_stoping(self):
        # Raspberry Pi IP address and port
        pi_ip = '192.168.108.93'
        pi_port = 1115

        # Create a socket object
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            # Connect to the Raspberry Pi
            sock.connect((pi_ip, pi_port))

            # Send the signal data
            signal_data = "Stopping"
            sock.sendall(signal_data.encode())

            # Close the connection
            sock.close()
        except ConnectionRefusedError:
            print("Failed to connect to the Raspberry Pi.")

        print("Signal sent to the Raspberry Pi!")

    #def send_to_raspberry_pi_laser(self):
        # Raspberry Pi IP address and port
        #pi_ip = '192.168.108.93'
        #pi_port = 1115

        # Create a socket object
        #sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #try:
            # Connect to the Raspberry Pi
            #sock.connect((pi_ip, pi_port))

            # Send the signal data
            #signal_data = "laser"
            #sock.sendall(signal_data.encode())

            # Close the connection
            #sock.close()
        #except ConnectionRefusedError:
            #print("Failed to connect to the Raspberry Pi.")

        #print("Signal sent to the Raspberry Pi!")

    #def send_to_raspberry_pi_livestreaming(self):
        # Raspberry Pi IP address and port
        #pi_ip = '192.168.108.93'
        #pi_port = 1115

        # Create a socket object
        #sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #try:
            # Connect to the Raspberry Pi
            #sock.connect((pi_ip, pi_port))

            # Send the signal data
            #signal_data = "Video"
            #sock.sendall(signal_data.encode())

            # Close the connection
            #sock.close()
        #except ConnectionRefusedError:
            #print("Failed to connect to the Raspberry Pi.")

        #print("Signal sent to the Raspberry Pi!")

    def send_to_raspberry_pi_manualmode(self):
        # Raspberry Pi IP address and port
        pi_ip = '192.168.108.93'
        pi_port = 1115

        # Create a socket object
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            # Connect to the Raspberry Pi
            sock.connect((pi_ip, pi_port))

            # Send the signal data
            signal_data = "Manual mode"
            sock.sendall(signal_data.encode())

            # Close the connection
            sock.close()
        except ConnectionRefusedError:
            print("Failed to connect to the Raspberry Pi.")

        print("Signal sent to the Raspberry Pi!")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
