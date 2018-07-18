import cv2

save_path = 'F:\\face_photo_save\\chenym\\'
cascade = cv2.CascadeClassifier(
    "D:\\opencv249\\opencv\\sources\\data\\haarcascades\\haarcascade_frontalface_alt_tree.xml")
cap = cv2.VideoCapture(0)
i = 0
while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rect = cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=9, minSize=(50, 50),
                                    flags=cv2.cv.CV_HAAR_SCALE_IMAGE)
    if not rect is ():
        for x, y, z, w in rect:
            roiImg = frame[y:y + w, x:x + z]
            cv2.imwrite(save_path + str(i) + '.jpg', roiImg)
            cv2.rectangle(frame, (x, y), (x + z, y + w), (0, 0, 255), 2)
            i += 1
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
