import cv2
import datetime
import time
import numpy as np
from pyzbar.pyzbar import decode

with open('AccessUser.txt','r') as f:
    authoriseduser = [l[:-1] for l in f.readlines() if len(l)>2]
    f.close()

# print(authoriseduser)

logpath = 'logpath.txt'
most_recent_access = {}

cap = cv2.VideoCapture(0)

while True:
    ret,frame = cap.read()
    info = decode(frame)

    if len(info) > 0:
        qr = info[0]
        data = qr.data
        rect = qr.rect
        polygon = qr.polygon

        if data.decode() in authoriseduser:
            cv2.putText(frame,'ACCESS GRANTED',(rect.left-15,rect.top-15),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),3)            
            frame = cv2.polylines(frame,[np.array(polygon)],True,(0,255,0),5)
            if data.decode() not in most_recent_access.keys() or time.time() - most_recent_access[data.decode()] > 5:
                most_recent_access[data.decode()] = time.time()
                with open(logpath,'a') as f:
                    f.write('{},{}\n'.format(data.decode(),datetime.datetime.now()))
                    f.close()
        else:            
            cv2.putText(frame,'ACCESS DENIED',(rect.left-15,rect.top-15),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),3)
            frame = cv2.polylines(frame,[np.array(polygon)],True,(0,0,255),5)
    
    cv2.imshow('re',frame)
    if cv2.waitKey(10) & 0xFF == ord('s'):
        break

cap.release()
cv2.destroyAllWindows()