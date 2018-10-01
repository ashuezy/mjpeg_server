import cv2 
import numpy as np
import socket
import base64
import time
import json
import logging

def rescale_frame(frame, percent=20):
    width = int(frame.shape[1] * percent/ 100)
    height = int(frame.shape[0] * percent/ 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation =cv2.INTER_AREA)

logger = logging.Logger('catch_all')
cap = cv2.VideoCapture(0)
i =0

while True:
    try: 
        ret, img = cap.read()
        pre = time.time()
        img = rescale_frame(img)
        ret2, buf = cv2.imencode('.jpg',img)
        if(ret2==True):
            i+=1
            jpg_as_text = base64.b64encode(buf)
            jpg_as_ascii = jpg_as_text.decode('ascii')
            if len(jpg_as_text)>0:
                x =  '{ "cameraId":"1", "fno":'+str(i)+', "frame":"'+str(jpg_as_ascii)+'"}'
                print(x)
                clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                clientsocket.connect(('localhost', 9000))
                clientsocket.send(x.encode())
                post = time.time()
                print("sending data.."+str(i))
                print(post-pre)
    except Exception as e:
        logger.error('Exception: '+ str(e))
        
# Close the window
cap.release()
 
# De-allocate any associated memory usage
cv2.destroyAllWindows() 