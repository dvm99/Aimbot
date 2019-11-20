import socket
import socket
import cv2

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # tcp
s.bind(('127.0.0.1', 9099))
s.listen(5)
clientsocket, address = s.accept()  # get clients socket address
print("Connection established")
print(address)


def server(frame):
    d = frame.flatten()
    data = d.tostring()
    clientsocket.send(data)  # Data length is 921600


cap = cv2.VideoCapture(0)


while True:
    ret, frame = cap.read()
    server(frame)
