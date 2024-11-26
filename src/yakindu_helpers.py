# In this module, stuff that is specific to Yakindu's generated code
# Author: Joeri Exelmans

from src.controller import Controller, pretty_time

# for some stupid reason, we have to import the 'Observable' class like this, or `type(obj) == Observable` will fail:
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from yakindu.rx import Observable, Observer

# Adapter to allow Yakindu generated code to (un)set timeouts
# Uses event queue of the underlying Controller, making all timed transitions scheduled in simulated time (instead of wall-clock time as in Yakindu's own TimerService).
class YakinduTimerServiceAdapter:
    def __init__(self, controller: Controller):
        self.controller = controller;
        self.timers = {}

    # Duration: milliseconds
    def set_timer(self, sc, event_id, duration, periodic):
        self.unset_timer(None, event_id)

        controller_duration = duration * 1000000 # ms to ns

        # print("set timer"+str(event_id), "duration", duration)
        e = self.controller.add_input_lowlevel(
            self.controller.simulated_time + controller_duration, # timestamp relative to simulated time
            raise_method=sc.time_elapsed,
            value=event_id,
            event_name="timer"+str(event_id))

        self.timers[event_id] = e

    def unset_timer(self, _, event_id):
        try:
            e = self.timers[event_id]
            e.canceled = True
        except KeyError:
            pass


# Could not find a better way to get list of output events of a YAKINDU statechart
def iter_output_observables(sc):
    for attr in dir(sc):
        obj = getattr(sc, attr)
        if type(obj) == Observable:
            yield (attr[0:-11], obj)


# Useful for debugging
class OutputEventTracer(Observer):
    def __init__(self, controller, event_name, callback):
        self.controller = controller
        self.event_name = event_name
        self.callback = callback

    def next(self, value=None):
        self.callback(self.controller.simulated_time, self.event_name, value)

def trace_output_events(controller, sc, callback, iface=None):
    for event_name, observable in iter_output_observables(getattr(sc, iface)):
        if iface == None:
            full_event_name = event_name
        else:
            full_event_name = iface + '.' + event_name
        observable.subscribe(OutputEventTracer(controller, full_event_name, callback))


# Allows use of a simple callback to respond to an output event
class CallbackObserver(Observer):
    def __init__(self, callback):
        self.callback = callback
    def next(self, value=None):
        self.callback(value)
