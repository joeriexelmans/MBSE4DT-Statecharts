import functools
from lib.test import run_scenario
from common import setup

# For each test scenario, sends a sequence of timed input events to the statechart, and checks if the expected sequence of timed output events occurs.

# Each timed event is a tuple (timestamp, event_name, parameter_value)
# For events that don't have a parameter, the parameter value is always 'None'.
# Timestamps are in nanoseconds since simulation start!

SCENARIOS = [
    {
        "name": "2 pickups, 2 drop-offs",
        "input_events": [
            (100000000, "scheduler.set_target_x", 0.0),
            (100000000, "scheduler.set_target_y", 2.0),
            (100000000, "scheduler.make_move", None),
            (100000000, "crane_control.done_moving", None),
            (1589949493, "crane_control.done_moving", None),
            (3579898986, "crane_control.done_moving", None),
            (4179898986, "scheduler.set_target_x", 1000.0),
            (4179898986, "scheduler.set_target_y", 3.0),
            (4179898986, "scheduler.make_move", None),
            (7342176646, "crane_control.done_moving", None),
            (8827062426, "crane_control.done_moving", None),
            (10811948206, "crane_control.done_moving", None),
            (11411948206, "scheduler.set_target_x", 0.0),
            (11411948206, "scheduler.set_target_y", 2.0),
            (11411948206, "scheduler.make_move", None),
            (14574225866, "crane_control.done_moving", None),
            (16064175359, "crane_control.done_moving", None),
            (18054124852, "crane_control.done_moving", None),
            (18654124852, "scheduler.set_target_x", 1000.0),
            (18654124852, "scheduler.set_target_y", 4.0),
            (18654124852, "scheduler.make_move", None),
            (21816402512, "crane_control.done_moving", None),
            (23296198409, "crane_control.done_moving", None),
            (25275994306, "crane_control.done_moving", None),
        ],
        "output_events": [
            (0, "scheduler.ready", None),
            (100000000, "crane_control.move", 0.0),
            (600000000, "crane_control.hoist", 2.0),
            (2089949493, "crane_control.magnet_on", None),
            (2589949493, "crane_control.hoist", 100),
            (4079898986, "scheduler.ready", None),
            (4179898986, "crane_control.move", 1000.0),
            (7842176646, "crane_control.hoist", 3.0),
            (9327062426, "crane_control.magnet_off", None),
            (9827062426, "crane_control.hoist", 100),
            (11311948206, "scheduler.ready", None),
            (11411948206, "crane_control.move", 0.0),
            (15074225866, "crane_control.hoist", 2.0),
            (16564175359, "crane_control.magnet_on", None),
            (17064175359, "crane_control.hoist", 100),
            (18554124852, "scheduler.ready", None),
            (18654124852, "crane_control.move", 1000.0),
            (22316402512, "crane_control.hoist", 4.0),
            (23796198409, "crane_control.magnet_off", None),
            (24296198409, "crane_control.hoist", 100),
            (25775994306, "scheduler.ready", None),
        ],
    },
    {
        "name": "Emergency stop",
        "input_events": [
            (0, "scheduler.set_target_x", 0.0),
            (0, "scheduler.set_target_y", 2.0),
            (0, "scheduler.make_move", None),
            (0, "crane_control.done_moving", None),
            (1489949493, "crane_control.done_moving", None),
            (1964149573, "emergency.stop", None),
            (2464149573, "crane_control.done_moving", None),
            (5092280059, "emergency.resume", None),
            (5891932040, "emergency.stop", None),
            (7172595898, "emergency.resume", None),
            (11162545391, "crane_control.done_moving", None),
            (11662545391, "scheduler.set_target_x", 1000.0),
            (11662545391, "scheduler.set_target_y", 3.0),
            (11662545391, "scheduler.make_move", None),
        ],
        "output_events": [
            (0, "scheduler.ready", None),
            (0, "crane_control.move", 0.0),
            (500000000, "crane_control.hoist", 2.0),
            (1964149573, "crane_control.stop_all_movement", None),
            (9672595898, "crane_control.magnet_on", None),
            (10172595898, "crane_control.hoist", 100),
        ],
    },
]

# The following output events are safe to repeat: (with same value)
# This will be taken into account while comparing traces.
# Do not change this:
IDEMPOTENT = [
    "scheduler.ready",
    "crane_control.magnet_on",
    "crane_control.magnet_off",
    "crane_control.hoist",
    "crane_control.move",
]

# We pretend that initially, these events occur:
# Do not change this:
INITIAL = [
    # ("crane_control.magnet_off", None),
    # ("crane_control.hoist", 100.0), # initially at safe altitude
    # ("crane_control.move", 0), # initially at position 0
]

if __name__ == "__main__":
    s = functools.partial(setup, print_trace_at_the_end=False)
    ok = True
    for scenario in SCENARIOS:
        print(f"Running scenario: {scenario["name"]}")
        ok = run_scenario(scenario["input_events"], scenario["output_events"], s, INITIAL, IDEMPOTENT, verbose=False) and ok
    if ok:
        print("All scenarios passed.")
    else:
        print("Some scenarios failed.")
