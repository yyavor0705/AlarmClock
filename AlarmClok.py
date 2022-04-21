import datetime
import playsound
from time import strftime
from threading import Thread, Event
from tkinter.ttk import OptionMenu
from tkinter import Tk, mainloop, IntVar, Frame, Label, RAISED, LEFT, RIGHT


class HourMinuteTime:
    def __init__(self, hour, minute):
        self.__hour = hour
        self.__minute = minute

    @property
    def hour(self):
        return self.__hour

    @property
    def minute(self):
        return self.__minute


class TimeMonitorThread(Thread):
    def __init__(self, alarm_time):
        super().__init__()
        self.__stop_time_monitor_event = Event()
        self.__alarm_time = alarm_time

    def run(self):
        while not self.__stop_time_monitor_event.is_set():
            if self.__alarm_time.hour == datetime.datetime.now().hour and \
                    self.__alarm_time.minute == datetime.datetime.now().minute:
                playsound.playsound("alarm.mp3")
                break

    @staticmethod
    def __play_alarm():
        playsound.playsound("alarm.mp3")

    def stop(self):
        self.__stop_time_monitor_event.set()


class AlarmClockWindow(Tk):
    def __init__(self):
        super().__init__()
        self.title('Alarm Clock')

        frame = Frame(self, relief=RAISED, borderwidth=1)
        frame.pack()

        # hours options menu
        hours = range(24)
        self.__hour_var = IntVar()
        self.__hour_var.set(hours[0])
        hour_options_menu = OptionMenu(frame, self.__hour_var, *hours, command=self.__time_change_event)
        hour_options_menu.pack(side=LEFT)

        # hours options menu
        minutes = range(59)
        self.__minute_var = IntVar()
        self.__minute_var.set(minutes[0])
        minute_options_menu = OptionMenu(frame, self.__minute_var, *minutes, command=self.__time_change_event)
        minute_options_menu.pack(side=RIGHT)

        initial_alarm_time = HourMinuteTime(hours[0], minutes[0])
        self.__time_monitor_thread = TimeMonitorThread(initial_alarm_time)

        # actual clock widget
        self.__actual_clock_label = Label(self, font=('calibri', 40, 'bold'))
        self.__actual_clock_label.pack(anchor="center")

    def __time_changer(self):
        time_formatter = strftime('%H:%M:%S %p')
        self.__actual_clock_label.config(text=time_formatter)
        self.__actual_clock_label.after(1000, self.__time_changer)

    def __time_change_event(self, _):
        self.__time_monitor_thread.stop()
        new_time = HourMinuteTime(self.__hour_var.get(), self.__minute_var.get())
        self.__time_monitor_thread = TimeMonitorThread(new_time)
        self.__time_monitor_thread.start()

    def start_clock(self):
        self.__time_monitor_thread.start()
        self.__time_changer()


if __name__ == "__main__":
    alarm_clock_window = AlarmClockWindow()
    alarm_clock_window.start_clock()
    mainloop()
