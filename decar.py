import cv2

cap = cv2.VideoCapture("C:/Users/ACER/Desktop/detect car/เสียงรถวิ่งบนท้องถนน.mp4")

car_cascade = cv2.CascadeClassifier("C:/Users/ACER/Desktop/detect car/Computer-Vision---Object-Detection-in-Python-master/xml files/cars.xml")

while True:
    # reads frames from a video
    ret,frames = cap.read()
    # convert to gray scale of each frames
    gray = cv2.cvtColor(frames, cv2.COLOR_BGR2GRAY)
    # Detects cars of different sizes in the input image
    cars = car_cascade.detectMultiScale( gray, 1.1, 1)
    # To draw a rectangle in each cars
    for (x,y,w,h) in cars:
        cv2.rectangle(frames,(x,y),(x+w,y+h),(0,0,255),2)
    font = cv2.FONT_HERSHEY_DUPLEX
    cv2.putText(frames, "Car",('x + 6, y — 6'), font, 0.5, (0, 0, 255), 1)
    # Display frames in a window
    cv2.imshow("Car Detection", frames)
    # Wait for Enter key to stop
    if cv2.waitKey(33) == 13:
        break