import cv2
import os
import numpy as np
import matplotlib.pyplot as plt
from pyzbar.pyzbar import decode

input = 'Images'

# user = 'accessuser.txt'
# if os.path.exists(user):
#     os.mkdir(user)

for file in sorted(os.listdir(input)):
    img = cv2.imread(os.path.join(input,file))
    info = decode(img)
    # print(file,len(info)) # number of QR code in image
    for inf in info:
        data = inf.data
        rect = inf.rect
        polygon = inf.polygon

        res = data.decode("utf-8")
        # print(type(res))

        with open('AccessUser.txt','a') as f:
            f.write('{}\n'.format(res))

        img = cv2.rectangle(img,(rect.left,rect.top),(rect.left + rect.width,rect.top+rect.height),(0,255,0),5)
        img = cv2.polylines(img,[np.array(polygon)],True,(255,0,0),5)
        # plt.imshow(cv2.cvtColor(img,cv2.COLOR_BGR2RGB))
        # plt.show()