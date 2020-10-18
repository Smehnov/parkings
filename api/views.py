from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import numpy as np
# import tensorflow as tf
import cv2 as cv2
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib



# Create your views here.

parking_top_marks = [[i * 70, 180, (i + 1) * 70, 300] for i in range(14)] + [[i * 70, 330, (i + 1) * 70, 450] for i in
                                                                             range(14)] + [
                        [1100, i * 60 + 200, 1250, (i + 1) * 60 + 250] for i in range(15)]
# [[i*70,240,(i+1)*70,300] for i in range(14)] + [[i*70,390,(i+1)*70,450] for i in range(14)]

parkings = {
    "parnas3": {

        "file": "./images/parnas3.jpg",
        "latitude": 112,
        "longitude": 100,
        "marks": [
            [200, 720, 260, 620],

            [50, 780, 100, 900],
            [650, 620, 720, 720],

            [950, 800, 1050, 900],
            [900, 700, 1000, 800],
            [850, 600, 950, 700],
            [800, 500, 900, 600],
            [750, 420, 850, 500],
            [850, 400, 920, 460],
            [920, 400, 1000, 360],
            [830, 400, 910, 360],

            [920, 450, 1000, 410],

            [740, 400, 780, 360],
            [720, 360, 760, 330],

            [680, 310, 740, 270],

            [100, 500, 200, 450],
            [120, 450, 230, 400],

        ]
    },

    "parking-top": {
        "file": "./images/parking_top1.jpeg",
        "latitude": 112,
        "longitude": 100,
        "marks": parking_top_marks

    }

}


def process_camera(cam):
    global parkings
    filename = parkings[cam]['file']
    marks = parkings[cam]['marks']
    # print(marks)

    img = cv2.imread(filename)
    car_cascade = cv2.CascadeClassifier('./cars.xml')

    marks_av = [True] * len(marks)

    # img, center, radius, color, thickness
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Detects cars of different sizes in the input image
    cars = car_cascade.detectMultiScale(gray, 1.1, 1)
    # To draw a rectangle in each cars
    for (x, y, w, h) in cars:
        #     cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)

        for i, mark in enumerate(marks):
            if x >= min(mark[0], mark[2]) and x <= max(mark[0], mark[2]) and y >= min(mark[3], mark[1]) and y <= max(
                    mark[3], mark[1]):
                marks_av[i] = False
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.circle(img, (x, y), 4, (0, 0, 255), -1)
    #     cv2.putText(img, 'Car', (x + 6, y - 6), font, 0.5, (0, 0, 255), 1)

    # print(marks_av)
    for i, mark in enumerate(marks):
        color = (0, 255, 0) if marks_av[i] == True else (0, 0, 255)
        cv2.rectangle(img, (mark[0], mark[1]), (mark[2], mark[3]), color, 4)

    free = marks_av.count(True)
    return free


def process_all_cameras():
    global parkings
    parks = []
    for cam in parkings.keys():
        latitude = parkings[cam]['latitude']
        longitude = parkings[cam]['longitude']
        free = process_camera(cam)

        parks.append([cam, latitude, longitude, free])

    return parks


def send_email_to_admin(sender_login, error_type, sender_message):
    msg = MIMEMultipart()

    message = sender_message
    password = "pass"
    msg['From'] = "client@parcin.com"
    msg['To'] = "support@parcin.com"
    msg['Subject'] = f"{error_type}"

    msg.attach(MIMEText(message, 'plain'))
    server = smtplib.SMTP('smtp.gmail.com: 587')

    server.starttls()

    server.login(msg['From'], "")

    server.sendmail(msg['From'], msg['To'], msg.as_string())

    server.quit()

    print("successfully sent email to %s:" % (msg['To']))
    pass


def email(request):
    return JsonResponse({
        "result": "ok"
    })


def get_parkings(request):
    parks = process_all_cameras()
    parkings = [{
        "id": park[0],
        "latitude": park[1],
        "longitude": park[2],
        "free": park[3]
    } for park in parks]
    # parkings = []

    return JsonResponse({
        "parkings": parkings
    })
