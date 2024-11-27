from common import setup, setup_wall_clock, setup_fake_scheduler
from mqtt_example.networked_crane_control import setup_networked_crane_control

from gui import GUI
from lib.realtime.event_loop import EventLoopRealTimeSimulation
from lib.realtime.tk_event_loop import TkEventLoopAdapter


# Runs our Statechart, inside TKInter event loop.
# The fake (or real?) crane_control runs in a separate process (runner_mqtt_fake_crane.py), communication happening via MQTT.
if __name__ == "__main__":
    controller, sc, _ = setup()
    gui = GUI(controller, sc)

    wall_clock = setup_wall_clock()
    sim = EventLoopRealTimeSimulation(controller, TkEventLoopAdapter(gui.tk), wall_clock)

    # for GUI events, we use 'add_input_now' which will interrupt (wake up) the event loop, if necessary
    gui.on_click_emergency = lambda: sim.add_input_now(sc.emergency, 'stop')
    gui.on_click_resume = lambda: sim.add_input_now(sc.emergency, 'resume')

    setup_fake_scheduler(controller, sc, move_status_callback=lambda msg: gui.var_sched_status.set(msg))

    client, connected_condition = setup_networked_crane_control(controller, sc, sim,
        crane_status_callback=lambda msg: gui.var_crane_status.set(msg))

    # starts MQTT event loop in separate thread
    client.loop_start()

    # wait until connected to MQTT broker (not sure if this is really required)
    with connected_condition:
        connected_condition.wait()

    wall_clock.record_start_time() # start_time is NOW!
    sc.enter() # enter default state(s)
    sim.poke() # wake up the event loop
    gui.mainloop() # starts TkInter event loop in THIS thread
