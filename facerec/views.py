from django.shortcuts import render
from django.shortcuts import render,redirect,HttpResponse
import threading
import cv2,os
from django.views.decorators import gzip
from django.http import StreamingHttpResponse
import face_recognition
import numpy as np


def findencodings(images):
    encodelist =[]
    for img in images:
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodelist.append(encode)
    return encodelist


def video(request):
    return render(request , "searchFace.html")


@gzip.gzip_page
def opencv(request):
    try:
        cam = VideoCamera()
        #logic
        return StreamingHttpResponse(gen(cam), content_type='multipart/x-mixed-replace;boundary=frame')
    except:
        pass
    return render(request,"searchFace.html")



class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        (self.grabbed , self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def update(self):
        path = "D:/Django+OpenCV/test-img"
        images = []
        classname = []
        mylist = os.listdir(path)
        print(mylist)

        for cl in mylist:
            curimg = cv2.imread(f"{path}/{cl}")
            images.append(curimg)
            classname.append(os.path.splitext(cl)[0])
        print(classname)

        encodelistknown = findencodings(images)
        print("Encoding complete")
        while True:
            (self.grabbed, self.frame) = self.video.read()
            try:
                imgS = cv2.resize(self.frame, (0, 0), None, 0.25, 0.25)
                imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
                facesCurFrame = face_recognition.face_locations(imgS)
                encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

                for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
                    matches = face_recognition.compare_faces(encodelistknown, encodeFace)
                    faceDis = face_recognition.face_distance(encodelistknown, encodeFace)
                    matchIndex = np.argmin(faceDis)

                    if matches[matchIndex] and faceDis[matchIndex] < 0.5:
                        name = classname[matchIndex].upper()
                        # print(name)
                        y1, x2, y2, x1 = faceLoc
                        y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                        cv2.rectangle(self.frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.rectangle(self.frame, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                        cv2.putText(self.frame, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

            except:
                print("No face found")




def gen(camera):
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')