import paho.mqtt.client as mqtt
import time
from Calculations import Calculations
import RPi.GPIO as GPIO

c = Calculations()
counterTilt = 0
counterPan = 0

try:

    STEPPIN_PAN = 20
    DIRPIN_PAN = 21
    STEPPIN_TILT = 14
    DIRPIN_TILT = 15
    M_PINS = (13, 19, 26)
    DELAYTILT = 0.0025
    DELAYPAN = 0.00025
    RESOLUTION = {'Full': (0, 0, 0),
                  'Half': (1, 0, 0),
                  '1/4': (0, 1, 0),
                  '1/8': (1, 1, 0),
                  '1/16': (0, 0, 1),
                  '1/32': (1, 0, 1)}

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(STEPPIN_PAN, GPIO.OUT)
    GPIO.setup(DIRPIN_PAN, GPIO.OUT)
    GPIO.setup(STEPPIN_TILT, GPIO.OUT)
    GPIO.setup(DIRPIN_TILT, GPIO.OUT)
    GPIO.setup(M_PINS, GPIO.OUT)
    GPIO.output(M_PINS, RESOLUTION['Half'])
except Exception:
    print("Something went wrong with GPIO SETUP")

buffer = 50
anker_x = 250
anker_y = 125
x_max = int(anker_x + (buffer / 2))
x_min = int(anker_x - (buffer / 2))
y_max = int(anker_y + (buffer / 2))
y_min = int(anker_y - (buffer / 2))

# MQTT_SERVER = "m24.cloudmqtt.com"
MQTT_SERVER = "diegopi"
# MQTT_PATH = "test_channel"
PORT = 8883


# user = "kcxqqglz"
# password = "sDPJ7cBDyool"
# The callback for when the client receives a CONNACK response from the server.

def turn_tilt(steps, direction):
    GPIO.output(DIRPIN_TILT, direction)
    print("Tilt_Direction: ", direction)
    count = 0
    for i in range(steps):
        count += 1
        print(count)
        GPIO.output(STEPPIN_TILT, GPIO.HIGH)
        time.sleep(DELAYTILT)
        GPIO.output(STEPPIN_TILT, GPIO.LOW)
        time.sleep(DELAYTILT)
    print("steps: ", count)


def turn_pan(steps, direction):
    GPIO.output(DIRPIN_PAN, direction)
    print("Pan_Direction: ", direction)
    count = 0
    for i in range(steps):
        count += 1
        print(count)
        GPIO.output(STEPPIN_PAN, GPIO.HIGH)
        time.sleep(DELAYPAN)
        GPIO.output(STEPPIN_PAN, GPIO.LOW)
        time.sleep(DELAYPAN)
    print("steps: ", count)


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("openCV")
    client.subscribe("ui")


def on_message(client, userdata, msg):
    global counterTilt, counterPan

    mess = msg.payload.decode()
    messStr = str(mess)
    messlist = messStr.split("'")
    cleanV = str(messlist[0])

    x = int(messlist[1])

    y = int(messlist[2])

    if msg.topic == "ui" and cleanV == "start":
        client.unsubscribe("openCV")
        if x == 1 and counterPan <= 300:
            turn_pan(steps=abs(15), direction=0)
            counterPan = counterPan + 15

        if x == -1 and counterPan >= -300:
            turn_pan(steps=abs(15), direction=1)
            counterPan = counterPan - 15

        if y == 1 and counterTilt <= 60:
            turn_tilt(steps=abs(3), direction=0)
            counterTilt = counterTilt + 3

        if y == -1 and counterTilt >= -60:
            turn_tilt(steps=abs(3), direction=1)
            counterTilt = counterTilt - 3

    if msg.topic == "ui" and cleanV == "exit":
        client.subscribe("openCV")
        print("subscribe")

    if msg.topic == "openCV" and cleanV == "opencv":
        print(x, y)
        if x > x_min and x < x_max:
            print("face in range X ")
        # BACKWARD INTERLEAVE step
        elif x > x_max and counterPan <= 300:
            turn_pan(steps=abs(15), direction=0)
            counterPan = counterPan + 15
        # FORWARD INTERLEAVE step
        elif x < x_min and counterPan >= -300:
            turn_pan(steps=abs(15), direction=1)
            counterPan = counterPan - 15
        # Filtering Y
        if y > y_min and y < y_max:
            print("face in range (Y) ")
        # BACKWARD INTERLEAVE step
        elif y > y_max and counterTilt >= -60:
            turn_tilt(steps=abs(3), direction=1)
            counterTilt = counterTilt - 3
        # FORWARD INTERLEAVE step
        elif y < y_min and counterTilt <= 60:
            turn_tilt(steps=abs(3), direction=0)
            counterTilt = counterTilt + 3


client = mqtt.Client()
# client.username_pw_set(user, password=password)
print("setting  password")
client.username_pw_set(username="diego", password="potato")
client.tls_set("/etc/mosquitto/certs/ca.crt")
# client.tls_insecure_set(True)
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_SERVER, PORT)
client.loop_forever()
