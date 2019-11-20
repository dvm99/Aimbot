import cv2
# import socket
import PySimpleGUI as sg
import webbrowser
import paho.mqtt.client as paho

# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # tcp
# s.bind(('192.168.137.151', 9099))
# s.listen(5)
# clientsocket, address = s.accept()  # get clients socket address
# print("Connection established")
# print(address)

cap = cv2.VideoCapture(0)
faceCascade = cv2.CascadeClassifier(
    '/Users/temp/PycharmProjects/test_4/venv/lib/python3.7/site-packages/cv2/data/haarcascade_frontalface_alt.xml')
sideCascade = cv2.CascadeClassifier(
    '/Users/temp/PycharmProjects/test_4/venv/lib/python3.7/site-packages/cv2/data/haarcascade_profileface.xml')

# # calling the client method for the mqtt lib
client1 = paho.Client("controll1")
# # sending username and password to the borker
client1.username_pw_set(username="diego", password="potato")
#
# # sending the certificate to the broker
client1.tls_set("C:\Program Files (x86)\mosquitto\certs\ca.crt")
# # connect with the borker on port 8883 and hostname diegopi
client1.connect("diegopi", 8883, 60)

XREFMID = 480
YREF = 640
MARGE = 150
x1 = 50
y1 = 90
x2 = 400
y2 = 400
xcoor = 0
ycoor = 0

# weblauncher o
new = 2
url = 'http://192.168.137.1:8088'

# Multiple windows pattern  - First window remains active

layout = [
    [sg.Button('vMix'), sg.Button('Remote'), sg.Button('Aimbot'), sg.Button('Exit', button_color=('black', 'orange'))]]

win1 = sg.Window('Aimbot', layout)

win2_active = False

global frame
global ret


def gui(win2_active):
    while True:
        ev1, vals1 = win1.Read(timeout=100)
        if ev1 is None or ev1 == 'Exit':
            exit()

        if not win2_active and ev1 == 'vMix':
            webbrowser.open(url, new=new)

        if not win2_active and ev1 == 'Remote':
            win2_active = True
            layout2 = [[sg.Text('Remote Control')],
                       [sg.T(' ' * 10), sg.RealtimeButton('Up')],
                       [sg.RealtimeButton('Left'), sg.T(' ' * 15), sg.RealtimeButton('Right')],
                       [sg.T(' ' * 10), sg.RealtimeButton('Down', )],
                       [sg.T('')],
                       [sg.CButton('Close', button_color=('black', 'orange'))]
                       ]

            win2 = sg.Window('Remote Control', layout2, auto_size_text=True)

            manual(win2)

            if win2_active is True:
                ev2, vals2 = win2.Read(timeout=100)
                if ev2 is None or ev2 == 'Close':
                    print('exit')
                    win2_active = False
                    client1.publish("ui", "exit'123'123'123")
                    win2.Close()

        if not win2_active and ev1 == 'Aimbot':
            opencv()

        ret, frame = cap.read()
        # d = frame.flatten()
        # data = d.tostring()
        # clientsocket.send(data)
        cv2.imshow('frame', frame)


def manual(win2):
    while True:
        ret, frame = cap.read()
        # d = frame.flatten()
        # data = d.tostring()
        # clientsocket.send(data)
        cv2.imshow('frame', frame)
        # This is the code that reads and updates the window
        event, values = win2.Read(timeout=10)
        if event is 'Right':
            stri = "start" + "'" + str(1) + "'" + str(0)
            print(stri)
            client1.publish("ui", stri)
        if event is 'Left':
            stri = "start" + "'" + str(-1) + "'" + str(0)
            print(stri)
            client1.publish("ui", stri)
        if event is 'Up':
            stri = "start" + "'" + str(0) + "'" + str(1)
            print(stri)
            client1.publish("ui", stri)
        if event is 'Down':
            stri = "start" + "'" + str(0) + "'" + str(-1)
            print(stri)
            client1.publish("ui", stri)
        if event == 'Quit' or values is None:
            break


def locatie(x, y, w, h, frame):
    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    stri = "opencv" + "'" + str(x) + "'" + str(y) + "'" + str(x + w)
    client1.publish("openCV", stri)
    print("send")


def opencv():
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        # d = frame.flatten()
        # data = d.tostring()
        # clientsocket.send(data)

        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )

        # side = sideCascade.detectMultiScale(
        #     gray,
        #     scaleFactor=1.1,
        #     minNeighbors=5,
        #     minSize=(30, 30)
        # )

        for (x, y, w, h) in faces:
            print(faces)
            maxValueFace = 0

        try:
            for i in range(faces.size):
                if (x + w) - x > maxValueFace:
                    maxIndex = i
                    maxValueFace = (x + w) - x
                    print(maxIndex)
                    locatie(x, y, w, h, frame)
        except:
            print("No faces")

        # for (x, y, w, h) in side:
        #     log.info(side)
        #     locatie(x, y, w, h, frame)

        cv2.imshow('frame', frame)

        # Display the resulting frame
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == '__main__':
    gui(win2_active)
