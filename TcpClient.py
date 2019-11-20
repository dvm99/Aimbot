import socket
import numpy
import cv2

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # tcp
s.connect(('127.0.0.1', 1234))
data = ""
i = 0

while True:

    msg = s.recv(921600)  #921600  is the buffer for the framing
    data = msg

    frame = numpy.frombuffer(data, dtype=numpy.uint8)
    try:
        frame = frame.reshape(480, 640, 3)
        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    except: print("cannot reshape array of size .... into shape (480,640,3)")

    data = ""
