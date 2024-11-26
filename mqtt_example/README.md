## Requirements

Python `paho-mqtt` package.

## Running

To run this example, both runners must be running in separate terminals:

  * `runner_mqtt_eventloop.py` Runs the Statechart and a GUI (uses TkInter). All events meant for the crane are published via MQTT.
  * `runner_mqtt_fake_crane.py` Listens to MQTT events, pretends to process them and replies to each event after a small delay, also by publishing a message via MQTT.

