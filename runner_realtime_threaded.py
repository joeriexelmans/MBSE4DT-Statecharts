# Headless real-time simulation, in a Python thread.

from common import setup, setup_fake_scheduler, setup_fake_crane_control, setup_wall_clock
from lib.realtime.threaded import ThreadedRealTimeSimulation

import threading

if __name__ == "__main__":
    controller, sc, _ = setup()
    sched = setup_fake_scheduler(controller, sc, move_status_callback=print)
    setup_fake_crane_control(controller, sc, crane_status_callback=print)
    wall_clock = setup_wall_clock()

    # Real-time simulation...
    sim = ThreadedRealTimeSimulation(controller, wall_clock,
        # because the headless simulation is non-interactive, we specify a termination condition:
        termination_condition=sched.termination_condition)

    wall_clock.record_start_time() # start_time is NOW!
    sc.enter() # enter default state(s)
    threading.Thread(target=sim.mainloop).start()
