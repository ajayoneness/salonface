from django.shortcuts import render,HttpResponse
import threading
import cv2
from django.views.decorators import gzip
from django.http import StreamingHttpResponse
import face_recognition
import numpy as np
from cregister.models import CustomerTable
from django.core import serializers


def customerDetails(idd):
    customerObj = CustomerTable.objects.get(id=idd)
    serialized_object = serializers.serialize('json', [customerObj])
    print(serialized_object)
    return HttpResponse(f"{serialized_object}")


def findencodings(images):
    encodelist =[]
    for img in images:
        try:
            img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodelist.append(encode)
        except:
            continue
    return encodelist



def video(request):
    return render(request , "searchFace.html", {'idd': 0})


@gzip.gzip_page
def opencv(request):
    try:
        cam = VideoCamera()

        #logic
        return StreamingHttpResponse(gen(cam), content_type='multipart/x-mixed-replace;boundary=frame')
    except:
        print("no camera found")
    return render(request,"searchFace.html")


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.idd = 0
        (self.grabbed , self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()


    def get_frame(self):
        image = self.frame
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def update(self):
        images = []
        classname = []
        profileImg = CustomerTable.objects.all()

        for i in profileImg:
            curimg = cv2.imread(i.profilePic.path)
            images.append(curimg)
            classname.append(str(i.id))
        print(images)
        print("class name id,",classname)
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
                        self.idd = int(name)
                        cusobj = CustomerTable.objects.get(id=int(name))
                        cusName  =cusobj.fname

                        y1, x2, y2, x1 = faceLoc
                        y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                        cv2.rectangle(self.frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.rectangle(self.frame, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                        cv2.putText(self.frame, cusName, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                        #customerDetails(int(name))
            except:
                print("No face found")


def gen(camera):
    while True:
        frame = camera.get_frame()
        idd = camera.idd
        #customerDetails(int(idd))

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n' + str(idd).encode() + b'\r\n\r\n')