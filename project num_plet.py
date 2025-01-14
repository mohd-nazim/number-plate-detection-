import cv2 as cv
data_set= "E:\.venv\haarcascade_russian_plate_number.xml"
cap = cv.VideoCapture(0)
cap.set(3,440)
cap.set(4, 520)
main_area=500 
count=0
while True:
    success, img = cap.read()
    plat_cap= cv.CascadeClassifier(data_set)
    img_gry=cv.cvtColor(img,cv.COLOR_RGB2GRAY)
    plat=plat_cap.detectMultiScale(img_gry,1.1,4)

    for(x,y,w,h) in plat:
        area=w*h
        if area>main_area:
            cv.rectangle(img,(x,y),(x+w, y+h),(0,255,0),2)
            cv.putText(img,"Number Plate ",(x,y-5),cv.FONT_HERSHEY_COMPLEX_SMALL,1,(255,0,255),2)

            img_rto = img[y: y+h, x:x+w ]
            cv.imshow("result",img )

    cv.imshow("result",img)
    if cv.waitKey(1) & 0xFF == ord("s"):
       cv.imwrite("E:\.venv" + str(count)+ ".jpg" , img_rto)
       cv.rectangle(img,(0,200),(640,300),(0,255,0),cv.FILLED)
       cv.putText(img,"plate saved",(150,265),cv.FONT_HERSHEY_COMPLEX_SMALL, 2 ,(0,255,0),2)
       cv.imshow("reuslte",img)
       cv.waitKey(500)
       count+=1
    elif cv.waitKey(1) & 0xFF == ord("q"):
        break
