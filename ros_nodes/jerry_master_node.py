#!/usr/bin/env python3
import rospy
from std_msgs.msg import String
import serial


def camera_clbk(received_msg):
    # this will be called each time the topic
    # receives a message
    global camera_status , cam_flag
    camera_status = received_msg.data
    print("Camera Callback", camera_status)
    if camera_status == "Cat" and cam_flag == 0:
        cam_flag == 1
        print("Cat found camera callback")
        #mega_serial.write(b'P')
        #time.sleep(0.05)
        mega_serial.write(b'S')
        rospy.sleep(0.5)
        
def gui_clbk(received_msg):
    # this will be called each time the topic
    # receives a message
    global gui_command
    gui_command = received_msg.data   


def Get_readings (event):
    global Front_reading , Right_reading , Left_reading , IR_reading , data
    # read byte from serial connection
    data = (uno_serial.read())
    #rospy.sleep(0.1)
    Front_reading = (Front_reading & 0x00) | ((int.from_bytes(data , 'big') >> 3 ) & 0x01 ) 
    Right_reading = (Right_reading & 0x00) | ( (int.from_bytes(data , 'big') >> 2) & 0x01 )
    Left_reading =  (Left_reading & 0x00) | ((int.from_bytes(data , 'big') >> 1) & 0x01 )
    IR_reading =    (IR_reading & 0x00) | ((int.from_bytes(data , 'big') >> 0) & 0x01  )
        # print data
   # print("______________________________________________-")
   # print("Received data:", data)
   # print("****************************")
#     print("Front_reading:", Front_reading)
#     print("Right_reading:", Right_reading)
#     print("Left_reading:", Left_reading)
#     print("IR_reading:", IR_reading)
    #print("______________________________________________-")
       
if __name__ == "__main__":
    
    
    rospy.init_node("Jerry_master_node")
    print("Initiate Jerry_master_node")
    data , Front_reading , Right_reading , Left_reading , IR_reading = 0 , 0 , 0 , 0 , 0
    counter1 = 0
    counter2 = 0
    counter3 = 0
    
    cam_flag = 0

    uno_serial = serial.Serial('/dev/ttyUSB0', 57600)
    mega_serial = serial.Serial('/dev/ttyACM0', 57600)
    gui_command = "Stopping"
    camera_status = "No Cat"
    rospy.Subscriber("/jerry_camera_topic", String, camera_clbk)
    rospy.Subscriber("/jerry_gui_topic", String, gui_clbk)
    period = rospy.Duration.from_sec(0.1)
    timer = rospy.Timer(period, Get_readings )  
    while not rospy.is_shutdown():
        if gui_command == "Starting":
            if camera_status == "No Cat" :
                if IR_reading == 1 or Front_reading == 1 :
                    print("Odamo 7aga front aw mafee4 ard IR")
                    mega_serial.write(b'S')#stop
                    print("stop front1")
                    rospy.sleep(0.1)
                    mega_serial.write(b'B')#back 7aga baseeta
                    print("back front1")
                    rospy.sleep(1.5)
                    if Right_reading == 0:
                        mega_serial.write(b'R')#turn right
                        print("Lef ymeen mn el front")
                        rospy.sleep(1.49)
                        mega_serial.write(b'S')#stop
                        rospy.sleep(0.1)
                    elif Left_reading == 0:
                        mega_serial.write(b'L')#turn left
                        print("Lef shemal mn el front")
                        rospy.sleep(1.5)
                        mega_serial.write(b'S')#stop
                        rospy.sleep(0.1)
                    else:
                        while Left_reading == 1 and Right_reading == 1 and cam_flag == 0 and gui_command == "Starting":
                            print("Maznoo2 erg3 l wara l7d ma tb2a fady")
                            mega_serial.write(b'B')#back
                            rospy.sleep(1)
                        mega_serial.write(b'S')
                        print("5alsna el zan2a")
                        rospy.sleep(0.1)
                        if Right_reading == 0:
                            mega_serial.write(b'R')#turn right
                            print("lef ymeen ba3d el zan2a")
                            rospy.sleep(1.49)
                            mega_serial.write(b'S')
                            rospy.sleep(0.1)
                        elif Left_reading == 0:
                            mega_serial.write(b'L')#turn left
                            print("lef 4emal ba3d el zan2a")
                            rospy.sleep(1.5)
                            mega_serial.write(b'S')
                            rospy.sleep(0.1)
                else :       
                    mega_serial.write(b'F')#moveforward
                    print("Laser ON")
                    rospy.sleep(0.1)
                    print("Em4y tawalyyy yabaa")
                    while Front_reading == 0 and IR_reading == 0 and counter1 < 60 and cam_flag == 0 and gui_command == "Starting":
                        print("Loop bta3et forward front 0")
                        rospy.sleep(0.1)
                        counter1+=1
                    if counter1 == 60:
                        counter1 = 0
                        mega_serial.write(b'S')
                        rospy.sleep(0.1)
                        print("5alasna elfront w han3ml scanning")
                        mega_serial.write(b'O')#scanning
                        #.sleep(6.2)
                        while counter2 < 62 and cam_flag == 0 and gui_command == "Starting":
                            print("Loop scan")
                            rospy.sleep(0.1)
                            counter2+=1
                        counter2 =0
                        print("scan 5eles")
                        mega_serial.write(b'S')
                        rospy.sleep(0.1)
                    else:
                        counter1 = 0
                        counter2 = 0
                        
            elif camera_status == "Cat":
               print("la2eena el cat")
               while Front_reading == 0 and gui_command == "Starting":
                    print("tawaly till cat")
                    mega_serial.write(b'F')#moveforward
                
               mega_serial.write(b'S')#stop
               print("stop cat")
               rospy.sleep(0.5)
               uno_serial.write(b'F')#feeding
               print("feeding cat")
               rospy.sleep(2)
               uno_serial.write(b'S')#Stop
               rospy.sleep(0.5)
               uno_serial.write(b'L')#Laser
               rospy.sleep(0.1)
               print("laser cat")
               mega_serial.write(b'D')#dance
               rospy.sleep(0.1)
               print("dance cat")
               #rospy.sleep(9)
               while counter3 < 90 and gui_command == "Starting": 
                   rospy.sleep(0.1)
                   counter3+=1
               counter3 = 0
               print("STOP dance cat")
               mega_serial.write(b'S')#stop
               rospy.sleep(0.1)
               uno_serial.write(b'S')#Stop
               print("SHUTTING DOWNNN!!!!")
               #rospy.sleep(10)
               while counter3 < 100 and gui_command == "Starting": 
                   rospy.sleep(0.1)
                   counter3+=1
               counter3 = 0
               cam_flag = 0
               #rospy.shutdown()
                    
            rospy.sleep(0.1)
        
        elif gui_command == "Stopping" or gui_command == "B":
            
            uno_serial.write(b'S')#Stop
            rospy.sleep(0.1)
            mega_serial.write(b'S')#stop
            rospy.sleep(1)
            
        elif gui_command == "Manual mode":
            uno_serial.write(b'S')#Stop
            rospy.sleep(0.1)
            mega_serial.write(b'S')#stop
            rospy.sleep(1)
            while gui_command != "B":
                if gui_command == "U":
                    mega_serial.write(b'F')#stop
                    rospy.sleep(2)
                    mega_serial.write(b'S')#stop
                    gui_command = "Manual mode"
                elif gui_command == "D":
                    mega_serial.write(b'B')#stop
                    rospy.sleep(2)
                    mega_serial.write(b'S')#stop
                    gui_command = "Manual mode"
                elif gui_command == "R":
                    mega_serial.write(b'R')#stop
                    rospy.sleep(2)
                    mega_serial.write(b'S')#stop
                    gui_command = "Manual mode"
                elif gui_command == "L":
                    mega_serial.write(b'L')#stop
                    rospy.sleep(2)
                    mega_serial.write(b'S')#stop
                    gui_command = "Manual mode"
                elif gui_command == "laser":
                    uno_serial.write(b'L')#stop
                    rospy.sleep(2)
                    uno_serial.write(b'S')#stop
                    gui_command = "Manual mode"
                elif gui_command == "Feeding Pet":
                    uno_serial.write(b'F')#stop
                    rospy.sleep(2)
                    uno_serial.write(b'S')#stop
                    gui_command = "Manual mode"
                rospy.sleep(0.1)
            rospy.sleep(0.1)
        
    rospy.spin()
    
            

    




