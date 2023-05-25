import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import socket
from PyQt5 import uic
from utils import *



# Define a custom signal
class SignalSender(QObject):
    signal = pyqtSignal()

class JoystickWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('./Joystick.ui',self)
        self.upbutton=self.findChild(QPushButton,'Up')
        self.rightbutton=self.findChild(QPushButton,'Right')
        self.leftbutton=self.findChild(QPushButton,'Left')
        self.downbutton=self.findChild(QPushButton,'Down')
        self.Backbutton=self.findChild(QPushButton,'Back')
        self.Feedbutton = self.findChild(QPushButton, 'Feed')
        self.Laserbutton = self.findChild(QPushButton, 'Laser')
        self.Dancebutton = self.findChild(QPushButton, 'Dance')

        self.upbutton.clicked.connect(self.send_signal_up)
        self.rightbutton.clicked.connect(self.send_signal_right)
        self.leftbutton.clicked.connect(self.send_signal_left)
        self.downbutton.clicked.connect(self.send_signal_down)
        self.Backbutton.clicked.connect(self.send_signal_back)
        self.Feedbutton.clicked.connect(self.send_signal_feed)
        self.Laserbutton.clicked.connect(self.send_signal_laser)
        self.Dancebutton.clicked.connect(self.send_signal_dance)
   
    
    def send_signal_feed(self):
        # Create a signal sender objectq
        signal_sender = SignalSender()

        # Connect the signal sender's signal to a slot function
        signal_sender.signal.connect(self.send_to_raspberry_pi_feeding)

        # Emit the signal
        signal_sender.signal.emit()

    def send_signal_laser(self):
        # Create a signal sender objectq
        signal_sender0 = SignalSender()

        # Connect the signal sender's signal to a slot function
        signal_sender0.signal.connect(self.send_to_raspberry_pi_laser)

        # Emit the signal
        signal_sender0.signal.emit()        
        
    def send_signal_up(self):
        # Create a signal sender objectq
        signal_sender1 = SignalSender()

        # Connect the signal sender's signal to a slot function
        signal_sender1.signal.connect(self.send_to_raspberry_pi_up)

        # Emit the signal
        signal_sender1.signal.emit()

    def send_signal_right(self):
        # Create a signal sender objectq
        signal_sender2 = SignalSender()

        # Connect the signal sender's signal to a slot function
        signal_sender2.signal.connect(self.send_to_raspberry_pi_right)

        # Emit the signal
        signal_sender2.signal.emit()      

    def send_signal_left(self):
        # Create a signal sender objectq
        signal_sender3 = SignalSender()

        # Connect the signal sender's signal to a slot function
        signal_sender3.signal.connect(self.send_to_raspberry_pi_left)

        # Emit the signal
        signal_sender3.signal.emit()
            
    def send_signal_down(self):
        # Create a signal sender objectq
        signal_sender4 = SignalSender()

        # Connect the signal sender's signal to a slot function
        signal_sender4.signal.connect(self.send_to_raspberry_pi_down)

        # Emit the signal
        signal_sender4.signal.emit()

    def send_signal_back(self):
        sceneStack.setCurrentIndex(0)
        # Create a signal sender objectq
        signal_sender5 = SignalSender()

        # Connect the signal sender's signal to a slot function
        signal_sender5.signal.connect(self.send_to_raspberry_pi_back)

        # Emit the signal
        signal_sender5.signal.emit()
    
    def send_signal_dance(self):
       
        # Create a signal sender objectq
        signal_sender6 = SignalSender()

        # Connect the signal sender's signal to a slot function
        signal_sender6.signal.connect(self.send_to_raspberry_pi_dance)

        # Emit the signal
        signal_sender6.signal.emit()           

    def send_to_raspberry_pi_feeding(self):
        # Raspberry Pi IP address and port
        pi_ip = '192.168.108.93'
        pi_port = 1115

        # Create a socket object
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            # Connect to the Raspberry Pi
            sock.connect((pi_ip, pi_port))

            # Send the signal data
            signal_data = "Feeding Pet"
            sock.sendall(signal_data.encode())

            # Close the connection
            sock.close()
        except ConnectionRefusedError:
            print("Failed to connect to the Raspberry Pi.")

        print("Signal sent to the Raspberry Pi!")

    def send_to_raspberry_pi_laser(self):
        # Raspberry Pi IP address and port
        pi_ip = '192.168.108.93'
        pi_port = 1115

        # Create a socket object
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            # Connect to the Raspberry Pi
            sock.connect((pi_ip, pi_port))

            # Send the signal data
            signal_data = "laser"
            sock.sendall(signal_data.encode())

            # Close the connection
            sock.close()
        except ConnectionRefusedError:
            print("Failed to connect to the Raspberry Pi.")

        print("Signal sent to the Raspberry Pi!") 
           
    def send_to_raspberry_pi_left(self):
        # Raspberry Pi IP address and port
        pi_ip = '192.168.108.93'
        pi_port = 1115

        # Create a socket object
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            # Connect to the Raspberry Pi
            sock.connect((pi_ip, pi_port))

            # Send the signal data
            signal_data = "L"
            sock.sendall(signal_data.encode())
            
            # Close the connection
            sock.close()
        except ConnectionRefusedError:
            print("Failed to connect to the Raspberry Pi.")

        print("Signal sent to the Raspberry Pi!")
        
    def send_to_raspberry_pi_up(self):
        # Raspberry Pi IP address and port
        pi_ip = '192.168.108.93'
        pi_port = 1115

        # Create a socket object
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            # Connect to the Raspberry Pi
            sock.connect((pi_ip, pi_port))

            # Send the signal data
            signal_data = "U"
            sock.sendall(signal_data.encode())
            
            # Close the connection
            sock.close()
        except ConnectionRefusedError:
            print("Failed to connect to the Raspberry Pi.")

        print("Signal sent to the Raspberry Pi!")

    def send_to_raspberry_pi_right(self):
        # Raspberry Pi IP address and port
        pi_ip = '192.168.108.93'
        pi_port = 1115

        # Create a socket object
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            # Connect to the Raspberry Pi
            sock.connect((pi_ip, pi_port))

            # Send the signal data
            signal_data = "R"
            sock.sendall(signal_data.encode())
            
            # Close the connection
            sock.close()
        except ConnectionRefusedError:
            print("Failed to connect to the Raspberry Pi.")

        print("Signal sent to the Raspberry Pi!")
        
    def send_to_raspberry_pi_down(self):
        # Raspberry Pi IP address and port
        pi_ip = '192.168.108.93'
        pi_port = 1115

        # Create a socket object
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            # Connect to the Raspberry Pi
            sock.connect((pi_ip, pi_port))

            # Send the signal data
            signal_data = "D"
            sock.sendall(signal_data.encode())
            
            # Close the connection
            sock.close()
        except ConnectionRefusedError:
            print("Failed to connect to the Raspberry Pi.")

        print("Signal sent to the Raspberry Pi!")

    def send_to_raspberry_pi_back(self):
        # Raspberry Pi IP address and port
        pi_ip = '192.168.108.93'
        pi_port = 1115

        # Create a socket object
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            # Connect to the Raspberry Pi
            sock.connect((pi_ip, pi_port))

            # Send the signal data
            signal_data = "B"
            sock.sendall(signal_data.encode())
            
            # Close the connection
            sock.close()
        except ConnectionRefusedError:
            print("Failed to connect to the Raspberry Pi.")

        print("Signal sent to the Raspberry Pi!")   

    def send_to_raspberry_pi_dance(self):
        # Raspberry Pi IP address and port
        pi_ip = '192.168.108.93'
        pi_port = 1115

        # Create a socket object
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            # Connect to the Raspberry Pi
            sock.connect((pi_ip, pi_port))

            # Send the signal data
            signal_data = "Dance"
            sock.sendall(signal_data.encode())
            
            # Close the connection
            sock.close()
        except ConnectionRefusedError:
            print("Failed to connect to the Raspberry Pi.")

        print("Signal sent to the Raspberry Pi!")        
      

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = JoystickWindow()
    window.show()
    sys.exit(app.exec_())