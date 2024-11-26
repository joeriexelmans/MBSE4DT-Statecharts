# Runs the simulation as-fast-as-possible, headless.
# Typically done when testing.

from common import setup, setup_fake_scheduler, setup_fake_crane_control

if __name__ == "__main__":
    controller, sc, _ = setup()

    setup_fake_scheduler(controller, sc, move_status_callback=print)
    setup_fake_crane_control(controller, sc, crane_status_callback=print)

    sc.enter() # enter default state(s)
    
    # Blocking synchronous call:
    controller.run_until(float('inf'))
    # No need to specify a termination condition. The above call returns when event queue empty