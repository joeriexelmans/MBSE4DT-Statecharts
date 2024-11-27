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
            (0, "scheduler.set_target_x", 0.0),
            (0, "scheduler.set_target_y", 2.0),
            (0, "scheduler.make_move", None),
            (100000000, "crane_control.done_moving", None),
            (1589949493, "crane_control.done_moving", None),
            (3579898986, "crane_control.done_moving", None),
            (4079898986, "scheduler.set_target_x", 1000.0),
            (4079898986, "scheduler.set_target_y", 3.0),
            (4079898986, "scheduler.make_move", None),
            (4179898986, "crane_control.done_moving", None),
            (5664784766, "crane_control.done_moving", None),
            (7649670546, "crane_control.done_moving", None),
            (8149670546, "scheduler.set_target_x", 0.0),
            (8149670546, "scheduler.set_target_y", 2.0),
            (8149670546, "scheduler.make_move", None),
            (11311948206, "crane_control.done_moving", None),
            (12801897699, "crane_control.done_moving", None),
            (14791847192, "crane_control.done_moving", None),
            (15291847192, "scheduler.set_target_x", 1000.0),
            (15291847192, "scheduler.set_target_y", 4.0),
            (15291847192, "scheduler.make_move", None),
            (18454124852, "crane_control.done_moving", None),
            (19933920749, "crane_control.done_moving", None),
            (21913716646, "crane_control.done_moving", None),
        ],
        "output_events": [
            (0, "scheduler.ready", None),
            (0, "crane_control.magnet_off", None),
            (0, "crane_control.move", -1),
            (600000000, "crane_control.hoist", 2.0),
            (2089949493, "crane_control.magnet_on", None),
            (2589949493, "crane_control.hoist", 100),
            (4079898986, "scheduler.ready", None),
            (4079898986, "crane_control.move", 0.0),
            (4679898986, "crane_control.hoist", 3.0),
            (6164784766, "crane_control.magnet_off", None),
            (6664784766, "crane_control.hoist", 100),
            (8149670546, "scheduler.ready", None),
            (8149670546, "crane_control.move", 1000.0),
            (11811948206, "crane_control.hoist", 2.0),
            (13301897699, "crane_control.magnet_on", None),
            (13801897699, "crane_control.hoist", 100),
            (15291847192, "scheduler.ready", None),
            (15291847192, "crane_control.move", 0.0),
            (18954124852, "crane_control.hoist", 4.0),
            (20433920749, "crane_control.magnet_off", None),
            (20933920749, "crane_control.hoist", 100),
            (22413716646, "scheduler.ready", None),
        ],
    },
    {
        "name": "Emergency stop",
        "input_events": [
            (0, "scheduler.set_target_x", 0.0),
            (0, "scheduler.set_target_y", 2.0),
            (0, "scheduler.make_move", None),
            (100000000, "crane_control.done_moving", None),
            (1589949493, "crane_control.done_moving", None),
            # while hoisting, the STOP-button is pressed
            (1371070726, "emergency.stop", None),
            (1871070726, "crane_control.done_moving", None),
            (5267128753, "emergency.resume", None),
            # before resume-delay (2s) has passed, the STOP-button is pressed again, canceling the RESUME:
            (5563205273, "emergency.stop", None),
            # finally, we resume (for real this time):
            (6535260132, "emergency.resume", None),
            (8535260132, "crane_control.done_moving", None),
            (10525209625, "crane_control.done_moving", None),
            (11025209625, "scheduler.set_target_x", 1000.0),
            (11025209625, "scheduler.set_target_y", 3.0),
            (11025209625, "scheduler.make_move", None),
            (11125209625, "crane_control.done_moving", None),
        ],
        "output_events": [
            (0, "scheduler.ready", None),
            (0, "crane_control.magnet_off", None),
            (0, "crane_control.move", -1),
            (600000000, "crane_control.hoist", 2.0),
            (1371070726, "crane_control.stop_all_movement", None),
            (8535260132, "crane_control.hoist", 2.0),
            (8535260132, "crane_control.magnet_off", None),
            (9035260132, "crane_control.magnet_on", None),
            (9535260132, "crane_control.hoist", 100),
            (11025209625, "scheduler.ready", None),
            (11025209625, "crane_control.move", 0.0),
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
    ("crane_control.magnet_off", None),
    ("crane_control.hoist", 100.0), # initially at safe altitude
    ("crane_control.move", 0), # initially at position 0
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
