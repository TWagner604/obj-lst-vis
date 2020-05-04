# USAGE
# python real_time_object_detection.py --prototxt MobileNetSSD_deploy.prototxt.txt --model MobileNetSSD_deploy.caffemodel

# import the necessary packages
from PIL import Image
from mss import mss
import numpy as np
import argparse
import imutils
import cv2
import sys
import glob
import os

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla

import random
import time

IM_WIDTH = 800
IM_HEIGTH = 600

i1 = 0

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
#ap.add_argument("-i", "--image", required=True,
#   help="path to input image")
ap.add_argument("-y", "--yolo", required=True,
    help="base path to YOLO directory")
ap.add_argument("-c", "--confidence", type=float, default=0.5,
    help="minimum probability to filter weak detections")
ap.add_argument("-t", "--threshold", type=float, default=0.3,
    help="threshold when applyong non-maxima suppression")
args = vars(ap.parse_args())

# load the COCO class labels our YOLO model was trained on
labelsPath = os.path.sep.join([args["yolo"], "coco.names"])
LABELS = open(labelsPath).read().strip().split("\n")

# initialize a list of colors to represent each possible class label
np.random.seed(42)
COLORS = np.random.randint(0, 255, size=(len(LABELS), 3),
    dtype="uint8")

# derive the paths to the YOLO weights and model configuration
weightsPath = os.path.sep.join([args["yolo"], "yolov3.weights"])
configPath = os.path.sep.join([args["yolo"], "yolov3.cfg"])

# load our YOLO object detector trained on COCO dataset (80 classes)
print("[INFO] loading YOLO from disk...")
net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)



def myprocess(image):
    # loop over the frames from the video stream
    print(image.frame_number)
    array = np.array(image.raw_data)
    i = array.reshape(IM_HEIGTH,IM_WIDTH,4)
    frame = i[:,:,:3]
    # Graphische Ausgabe des Sensorbilds

    (H, W) = frame.shape[:2]
    

    # determine only the *output* layer names that we need from YOLO
    ln = net.getLayerNames()
    ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    # construct a blob from the input image and then perform a forward
    # pass of the YOLO object detector, giving us our bounding boxes and
    # associated probabilities
    blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416),
        swapRB=True, crop=False)
    net.setInput(blob)
    start = time.time()
    layerOutputs = net.forward(ln)
    end = time.time()
    
    # show timing information on YOLO
    print("[INFO] YOLO took {:.6f} seconds".format(end - start))

    # initialize our lists of detected bounding boxes, confidences, and
    # class IDs, respectively
    boxes = []
    confidences = []
    classIDs = [] 

    # loop over each of the layer outputs
    for output in layerOutputs:
        # loop over each of the detections
        for detection in output:
            # extract the class ID and confidence (i.e., probability) of
            # the current object detection
            scores = detection[5:]
            classID = np.argmax(scores)
            confidence = scores[classID]

            # filter out weak predictions by ensuring the detected
            # probability is greater than the minimum probability
            if confidence > args["confidence"]:
                # scale the bounding box coordinates back relative to the
                # size of the image, keeping in mind that YOLO actually
                # returns the center (x, y)-coordinates of the bounding
                # box followed by the boxes' width and height
                box = detection[0:4] * np.array([W, H, W, H])
                (centerX, centerY, width, height) = box.astype("int")

                # use the center (x, y)-coordinates to derive the top and
                # and left corner of the bounding box
                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))

                # update our list of bounding box coordinates, confidences,
                # and class IDs
                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                classIDs.append(classID)

    # apply non-maxima suppression to suppress weak, overlapping bounding
    # boxes
    idxs = cv2.dnn.NMSBoxes(boxes, confidences, args["confidence"],
        args["threshold"])

    # ensure at least one detection exists
    if len(idxs) > 0:
        # loop over the indexes we are keeping
        for i in idxs.flatten():
            # extract the bounding box coordinates
            (x, y) = (boxes[i][0], boxes[i][1])
            (w, h) = (boxes[i][2], boxes[i][3])
            print(LABELS[classIDs[i]])
            print(boxes[i][0], boxes[i][1], boxes[i][2], boxes[i][3])

            i1 = boxes[i][0]

            # draw a bounding box rectangle and label on the image
            #color = [int(c) for c in COLORS[classIDs[i]]]
            #cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            #text = "{}: {:.4f}".format(LABELS[classIDs[i]], confidences[i])
            #cv2.putText(frame, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,
            #    0.5, color, 2)
    else:
        print("none")
    # show the output image
    #cv2.imshow("Image", frame)
    #cv2.waitKey(1)
    #cv2.destroyAllWindows()

    #frame = pyautogui.screenshot(region=(60, 20, 1280, 800))
    #frame = cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR)
    #frame = imutils.resize(frame, width=400)

    # grab the frame dimensions and convert it to a blob
    #(h, w) = frame.shape[:2]
    #blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)),
    #    0.007843, (300, 300), 127.5)

    # pass the blob through the network and obtain the detections and
    # predictions
    #net.setInput(blob)
    #detections = net.forward()


    #cv2.imshow('bild', i2)
    #cv2.waitKey(10) 
    return image
    #cv2.destroyAllWindows()
    

actor_list = []

try:
    client = carla.Client('localhost', 2000)
    client.set_timeout(10.0)
    world = client.get_world()

    # Blueprints erstellen
    # Blueprints = Fahrzeuge und Fußgänger
    blueprint_library = world.get_blueprint_library()
    #bp_1 = random.choice(blueprint_library.filter('vehicle'))
    bp_1 = blueprint_library.filter('model3')[0]
    bp_2 = blueprint_library.filter('model3')[0]

    if bp_1.has_attribute('color'):
            color = random.choice(bp_1.get_attribute('color').recommended_values)
            bp_1.set_attribute('color', color)
    
    if bp_2.has_attribute('color'):
            color = random.choice(bp_2.get_attribute('color').recommended_values)
            bp_2.set_attribute('color', color)
    

    # Spwan Points festlegen und Fahrzeugeigenschaften festlegen
    # Koordination durch Probieren
    # spawn_point = random.choice(world.get_map().get_spawn_points())
    spawn_point_bp_1 = carla.Transform(carla.Location(x=130,y=-6,z=1), carla.Rotation(yaw=180))
    spawn_point_bp_2 = carla.Transform(carla.Location(x=140,y=-6,z=1), carla.Rotation(yaw=180))
    vehicle_1 = world.spawn_actor(bp_1, spawn_point_bp_1)
    vehicle_2 = world.spawn_actor(bp_2, spawn_point_bp_2)
    #vehicle_1.set_autopilot(True)
    vehicle_1.apply_control(carla.VehicleControl(throttle=1.0, steer=0.0))
    vehicle_2.apply_control(carla.VehicleControl(throttle=0.8, steer=0.0))
    actor_list.append(vehicle_1)
    actor_list.append(vehicle_2)

    cam_bp_2 = blueprint_library.find('sensor.camera.rgb')
    #cam_bp_2.set_attribute('fov', '110')
    cam_bp_2.set_attribute('image_size_x', '800')
    cam_bp_2.set_attribute('image_size_y', '600')
    cam_bp_2.set_attribute('sensor_tick', '0.5')
    transform = carla.Transform(carla.Location(x=1.5, z=2.4))
    sensor = world.spawn_actor(cam_bp_2, transform, attach_to=vehicle_2)

    #cc = carla.ColorConverter.rgb
    #sensor.listen(lambda image: image.save_to_disk('output/%06d.png' % image.frame, cc))
    

    sensor.listen(lambda image: (myprocess(image)))


    #while True:
        #print(i1)

    time.sleep(55)



finally:
    for actor in actor_list:
        actor.destroy()
        print("All cleaned up!")


