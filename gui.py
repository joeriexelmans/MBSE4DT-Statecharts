import tkinter
import tkinter.constants

from src.yakindu_helpers import CallbackObserver

class GUI:
    def __init__(self, controller, sc):
        self.tk = tkinter.Tk()
        self.var_sched_status = tkinter.StringVar(self.tk, "ready")
        self.var_crane_status = tkinter.StringVar(self.tk, "crane is still")
        self.var_magnet_status = tkinter.StringVar(self.tk, "magnet is off")

        controller.input_tracers.append(self.set_status)

        sc.magnet_on_observable = CallbackObserver(lambda value: self.var_magnet_status.set("magnet is on"))
        sc.magnet_off_observable = CallbackObserver(lambda value: self.var_magnet_status.set("magnet is off"))

        self.tk.title("Crane SIMULATOR")
        self.tk.geometry("400x150")

        tkinter.Label(self.tk, textvariable=self.var_sched_status).pack()
        tkinter.Label(self.tk, textvariable=self.var_crane_status).pack()
        tkinter.Label(self.tk, textvariable=self.var_magnet_status).pack()

        # Buttons generating input events when clicked:
        tkinter.Button(self.tk, text="Emergency stop",
            command=lambda: self.on_click_emergency()).pack()
        tkinter.Button(self.tk, text="Resume after emergency",
            command=lambda: self.on_click_resume()).pack()

    def set_status(self, timestamp, event_name, value):
        # when the 'done_moving' input event occurs, update the GUI status
        if event_name == "done_moving":
            self.var_crane_status.set("crane is still")

    def mainloop(self):
        self.tk.mainloop()
