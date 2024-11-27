import random
import threading

from paho.mqtt import client as mqtt_client
from mqtt_example.mqtt_params import BROKER, PORT, TOPIC, REPLY_DELAY

from lib.yakindu.rx import Observer

CLIENT_ID = f'bip-mbse4dt/crane-{random.randint(0, 1000000)}'

# Translates crane control output events to MQTT-publish
# Intended to respond to 'move' and 'hoist' output events
class NetworkedCraneControl(Observer):
    def __init__(self, client, controller, sc, event, crane_status_callback):
        self.client = client
        self.controller = controller
        self.sc = sc
        self.event = event
        self.crane_status_callback = crane_status_callback

    # respond to 'move' or 'hoist' event by publishing on MQTT topic:
    def next(self, value=None):
        msg = f"{self.event} ({value}), expected to take about {REPLY_DELAY} seconds."
        self.crane_status_callback(msg) # display message (in terminal or GUI)
        self.client.publish(TOPIC+'/'+self.event, "request:"+str(value))

def setup_networked_crane_control(controller, sc, sim, crane_status_callback):
    client = mqtt_client.Client(CLIENT_ID)

    connected_condition = threading.Condition()
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
            with connected_condition:
                connected_condition.notify_all()
        else:
            print("Failed to connect, return code %d\n", rc)
    client.on_connect = on_connect

    client.connect(BROKER, PORT)

    # subscribe to topics (for receiving ACKs)
    client.subscribe(TOPIC+'/move')
    client.subscribe(TOPIC+'/hoist')
    client.subscribe(TOPIC+'/stopAllMovement')

    # translate Statechart output events to MQTT outbound messages
    sc.crane_control.move_observable.subscribe(NetworkedCraneControl(client, controller, sc.crane_control, "move", crane_status_callback))
    sc.crane_control.hoist_observable.subscribe(NetworkedCraneControl(client, controller, sc.crane_control, "hoist", crane_status_callback))
    sc.crane_control.stop_all_movement_observable.subscribe(NetworkedCraneControl(client, controller, sc.crane_control, "stopAllMovement", crane_status_callback))

    # translate MQTT inbound messages to Statechart input events
    def on_message(client, userdata, msg):
        # react to 'doneMoving' message by raising statechart input event:
        textreceived = msg.payload.decode()
        if textreceived == "doneMoving":
            sim.add_input_now(sc.crane_control, 'done_moving') # s to ns

    client.on_message = on_message

    return client, connected_condition