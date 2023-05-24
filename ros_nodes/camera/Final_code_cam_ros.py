#!/usr/bin/env python3
import rospy
from std_msgs.msg import String
import cv2

import subprocess

command = "sudo service motion stop"
result = subprocess.run(command.split(), stdout=subprocess.PIPE)
print(result.stdout.decode("utf-8"))

classNames = []
classFile = "/home/pi/ROS_workspaces/final_v1_ws/src/final_v1_pkg/src/camera/coco.names"
with open(classFile,"rt") as f:
    classNames = f.read().rstrip("\n").split("\n")

configPath = "/home/pi/ROS_workspaces/final_v1_ws/src/final_v1_pkg/src/camera/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
weightsPath = "/home/pi/ROS_workspaces/final_v1_ws/src/final_v1_pkg/src/camera/frozen_inference_graph.pb"

net = cv2.dnn_DetectionModel(weightsPath,configPath)
net.setInputSize(125,125)
net.setInputScale(1.0/ 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)


def getObjects(img, thres, nms, draw=True, objects=[]):
    classIds, confs, bbox = net.detect(img,confThreshold=thres,nmsThreshold=nms)
    if len(objects) == 0: objects = classNames
    objectInfo =[]
    if len(classIds) != 0:
        for classId, confidence,box in zip(classIds.flatten(),confs.flatten(),bbox):
            className = classNames[classId - 1]
            if className in objects:
                objectInfo.append([box,className])
                if (draw):
                    cv2.rectangle(img,box,color=(0,255,0),thickness=2)
                    cv2.putText(img,classNames[classId-1].upper(),(box[0]+10,box[1]+30),
                    cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
                    cv2.putText(img,str(round(confidence*100,2)),(box[0]+200,box[1]+30),
                    cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)

    return img,objectInfo


if __name__ == "__main__":
    
    rospy.init_node("Jerry_Camera_node")
    print("Initiate Jerry_camera_node")
    camera_pub = rospy.Publisher("/jerry_camera_topic", String, queue_size=10)
    rate = rospy.Rate(10)
    cap = cv2.VideoCapture(0)
    cap.set(3,640)
    cap.set(4,480)
    #cap.set(10,70)

    while not rospy.is_shutdown():
        
        camera_msg = String()
        success, img = cap.read()
        result, objectInfo = getObjects(img,0.4,0.99,objects=['cat'])

        # Check if cat is detected
        cat_detected = 0
        for obj in objectInfo:
            if obj[1] == 'cat':
                cat_detected = 1
                detection_val = round(obj[0][3], 2)
                break
        
        if cat_detected:
            camera_msg.data = "Cat"
            print("Cat found" , camera_msg.data)
        else:
            camera_msg.data = "No Cat"
            print("Cat Not found" , camera_msg.data)
        
        camera_pub.publish(camera_msg)
        # Print appropriate message based on detection

        cv2.imshow("Output",img)
    
        cv2.waitKey(1)
        rospy.sleep(0.1)
    rospy.spin()