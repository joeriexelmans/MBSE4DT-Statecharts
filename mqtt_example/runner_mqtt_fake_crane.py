import random
import threading
import time

from paho.mqtt import client as mqtt_client

from mqtt_example.mqtt_params import BROKER, PORT, TOPIC, REPLY_DELAY

CLIENT_ID = f'bip-mbse4dt/crane-{random.randint(0, 1000000)}'

# A very simple headless listener for move, hoist and stopAllMovement events,
# that replies to all of them after a fixed delay.
# Intended to be replaced by the REAL CRANE CONTROLLER.
# We assume that the crane is only capable of doing one thing at a time: moving horizontally, vertically, or stopping movement. Therefore, if a new request comes in (e.g., stopAllMovement) before the previous request has completed (e.g., hoist), then the new request 'interrupts' the previous request, and only the last request will be replied to (with a 'doneMoving') event.
if __name__ == "__main__":
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    def on_message(client, userdata, msg):
        pending_timer = None
        textreceived = msg.payload.decode()
        if textreceived.startswith("request:"):
            print(f'got request. topic={msg.topic}. will reply after about {REPLY_DELAY} s...')
            def reply():
                print(f'replying to msg {msg.topic}')
                client.publish(msg.topic, "doneMoving")
            # cancel previous timer, if there is one
            if pending_timer != None:
                pending_timer.cancel()
            # don't block the handler thread, sleep and reply in new thread:
            pending_timer = threading.Timer(REPLY_DELAY, reply)
            pending_timer.start()

    # Set Connecting Client ID
    client = mqtt_client.Client(CLIENT_ID)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER, PORT)

    # must subscribe after connecting
    client.subscribe(TOPIC+'/move')
    client.subscribe(TOPIC+'/hoist')
    client.subscribe(TOPIC+'/stopAllMovement')

    # client.loop_start()
    client.loop_forever() # starts new thread that responds to incoming messages
