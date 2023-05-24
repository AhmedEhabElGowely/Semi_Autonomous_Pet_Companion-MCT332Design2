#!/usr/bin/env python3
import rospy
import socket
from std_msgs.msg import String


if __name__ == "__main__":
    
    rospy.init_node("Jerry_GUI_node")
    gui_pub = rospy.Publisher("/jerry_gui_topic", String, queue_size=10)
    rate = rospy.Rate(10)
# Raspberry Pi IP address and port
    pi_ip = '192.168.1.168'
    pi_port = 1115

    # Create a socket object
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the IP address and port
    sock.bind((pi_ip, pi_port))

    # Listen for incoming connections
    sock.listen(1)

    print("Waiting for a connection...")

    while not rospy.is_shutdown():
        
        gui_msg = String()
        # Accept a connection
        conn, addr = sock.accept()
        
        #print("Connected by:", addr)

        # Receive data from the client
        data = conn.recv(1024).decode()
        
        gui_msg.data= data
        gui_pub.publish(gui_msg)
        #print("Received data:", data)
        print(data)
        # Close the connection
        
        #"Starting"
        #"Stopping"
        #"Video"
        #"Manual mode"
        #"U" up
        #"D" down
        #"R" Right
        #"L" Left
        #"Feeding Pet"
        #"laser"
        #"B" back
        
        conn.close()
        rospy.sleep(0.1)
        
    rospy.spin()
