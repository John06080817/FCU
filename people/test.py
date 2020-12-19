# -*- coding: utf-8 -*-
import cv2
import random
# 載入分類器
random.seed(552)
cascPath = "D:\python\邊緣人\haarcascade_frontalface_default.xml"
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)

dect = False
while True:
    ret, img = cap.read()
    if dect == True:
        faces = face_cascade.detectMultiScale(img, scaleFactor=1.1, minNeighbors=5, minSize=(30,30), flags=cv2.CASCADE_SCALE_IMAGE)
        if len(faces) > 0:
            #edge = random.randint(1, len(faces))
            #i = 0
            for (x, y, w, h) in faces:
                #i += 1
                #if i == edge:
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
                #cv2.putText(img, 'Loner', (x,y), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 1, cv2.LINE_AA)
                #loner = img[y:y+h, x:x+w]
                #cv2.putText(loner, 'Loner', (int(h/2)-50,int(w/2)), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0), 2, cv2.LINE_AA)
                #print(img)
                    #cv2.namedWindow('Loner_img')  #正常視窗大小
                    #cv2.imshow('Loner_img', loner)
            cv2.imshow('img', img)
            dect = False
            cv2.waitKey(0)
            cv2.destroyWindow('Loner_img')
# 顯示成果
    cv2.namedWindow('img', cv2.WINDOW_NORMAL)  #正常視窗大小
    cv2.imshow('img', img)                     #秀出圖片
# Stop if escape key is pressed
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    if key == ord('p'):
        dect = True
        
# Release the VideoCapture object
cap.release()
cv2.destroyAllWindows()
