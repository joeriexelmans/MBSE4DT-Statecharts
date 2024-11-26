# Real-time simulation, integrated with (in this case) TkInter event loop.

from common import setup, setup_wall_clock, setup_fake_scheduler, setup_fake_crane_control
from gui import GUI
from src.realtime.event_loop import EventLoopRealTimeSimulation
from src.realtime.tk_event_loop import TkEventLoopAdapter

import tkinter
import tkinter.constants

if __name__ == "__main__":
    controller, sc, _ = setup()
    gui = GUI(controller, sc)

    sched = setup_fake_scheduler(controller, sc, move_status_callback=lambda msg: gui.var_sched_status.set(msg))
    setup_fake_crane_control(controller, sc, crane_status_callback=lambda msg: gui.var_crane_status.set(msg))

    # Real-time simulation...
    wall_clock = setup_wall_clock()
    sim = EventLoopRealTimeSimulation(controller, TkEventLoopAdapter(gui.tk), wall_clock)

    # for GUI events, we use 'add_input_now' which will interrupt (wake up) the event loop, if necessary
    gui.on_click_emergency = lambda: sim.add_input_now(sc, 'emergency.stop')
    gui.on_click_resume = lambda: sim.add_input_now(sc, 'emergency.resume')

    wall_clock.record_start_time() # start_time is NOW!
    sc.enter() # enter default state(s)
    sim.poke() # wake up the event loop
    gui.mainloop()
