import time
from tkinter import *
from tkinter import messagebox

FONT = "Segoe UI"
FONT_S = 10 # Small
FONT_M = 18 # Medium
BACKGROUND = "#ff6347"
TIMER_ENTRY_BG = "#ff8064" # light tomato
TIMER_ENTRY_FG = "white"
LABEL_BG = BACKGROUND
LABEL_FG = "white"
LABEL_HIGHLIGHT = "red"
BTN_BG = "#ffef00"
BTN_FG = "black"

# creating Tk window
root = Tk()
root.geometry("300x250")
root['background'] = BACKGROUND
root.title("Pomodoro")

class ClockEntry:
    def __init__(self,
                entry_x,
                entry_y,
                font_family=FONT,
                font_size=FONT_M,
                entry_bg=TIMER_ENTRY_BG,
                entry_fg=TIMER_ENTRY_FG):
        self.entry_x = entry_x
        self.entry_y = entry_y
        self.font_family = font_family
        self.font_size = font_size
        self.entry_bg = entry_bg
        self.entry_fg = entry_fg

        self.text = StringVar()
        self.entry = Entry(root, width=3, font=(self.font_family, self.font_size, ""), textvariable=self.text, bg=self.entry_bg, fg=self.entry_fg)
        self.entry.place(x=self.entry_x, y=self.entry_y)

        self.reset()
        self.entry_label = None

    def set_text(self, text):
        self.text.set(text)

    def get_text(self):
        return self.text.get()

    def get_int(self):
        try:
            n = int(self.text.get())
            if n < 0:
                messagebox.showerror("Error", "Please input non-negative integer")
                return -1
            return n
        except:
            messagebox.showerror("Error", "Please input non-negative integer")
            return -1

    def disabled(self):
        self.entry.config(state='disabled')

    def enabled(self):
        self.entry.config(state="normal")

    def reset(self):
        self.set_text("{0:2d}".format(0))

    def set_label(self,
                text,
                padding_right=None,
                label_font_size=FONT_S,
                label_bg=LABEL_BG,
                label_fg=LABEL_FG):
        self.entry_label = Label(root, text=text, font=(self.font_family, label_font_size, ""), bg=label_bg, fg=label_fg)
        self.entry_label.place(x=self.entry_x - (padding_right or self.entry_padding), y=self.entry_y)
    

class ClockHMS:
    def __init__(self,
                entry_x,
                entry_y,
                entry_padding,
                font_family=FONT,
                font_size=FONT_M,
                entry_bg=TIMER_ENTRY_BG,
                entry_fg=TIMER_ENTRY_FG):
        self.font_family = font_family
        self.font_size = font_size
        self.entry_bg = entry_bg
        self.entry_fg = entry_fg
        self.entry_x = entry_x
        self.entry_y = entry_y
        self.entry_padding = entry_padding

        self.hour = ClockEntry(self.entry_x, self.entry_y)
        self.minute = ClockEntry(self.entry_x + self.entry_padding, self.entry_y)
        self.second = ClockEntry(self.entry_x + self.entry_padding * 2, self.entry_y)

        self.clock_label = None

    def reset(self):
        self.hour.reset()
        self.minute.reset()
        self.second.reset()

    def set_HMS(self, hours, mins, secs):
        self.hour.set_text(hours)
        self.minute.set_text(mins)
        self.second.set_text(secs)

    def set_label(self,
                text,
                padding_right=None,
                label_font_size=FONT_S,
                label_bg=LABEL_BG,
                label_fg=LABEL_FG):
        self.clock_label = Label(root, text=text, font=(self.font_family, label_font_size, ""), bg=label_bg, fg=label_fg)
        self.clock_label.place(x=self.entry_x - (padding_right or self.entry_padding), y=self.entry_y)

    def get_seconds(self):
        try:
            seconds = int(self.hour.get_text())*3600 + int(self.minute.get_text())*60 + int(self.second.get_text())
            if seconds < 0:
                messagebox.showerror("Error", "Please input non-negative integer")
                return -1
            return seconds
        except:
            messagebox.showerror("Error", "Please input non-negative integer")
            return -1

    def disabled_clock(self):
        self.hour.disabled()
        self.minute.disabled()
        self.second.disabled()

    def enabled_clock(self):
        self.hour.enabled()
        self.minute.enabled()
        self.second.enabled()

    def change_label_color(self, background_color=LABEL_HIGHLIGHT):
        self.clock_label.config(bg=background_color)

work_clock = ClockHMS(120, 20, 50)
work_clock.set_label("Work", padding_right=90)

short_break_clock = ClockHMS(120, 60, 50)
short_break_clock.set_label("Short Break", padding_right=90)

long_break_clock = ClockHMS(120, 100, 50)
long_break_clock.set_label("Long Break", padding_right=90)

session_clock = ClockEntry(120, 140)
session_clock.set_label("Session", padding_right=90)

btn = Button(root, text='Start', bd='5', font=(FONT,FONT_M,""), bg=BTN_BG, fg=BTN_FG)

def decrement_clock(clock, seconds):
    while seconds >= 0:
        mins, secs = divmod(seconds, 60)
        hours = 0
        if mins > 60:
            hours, mins = divmod(mins, 60)

        clock.set_HMS("{0:2d}".format(hours), "{0:2d}".format(mins), "{0:2d}".format(secs))
        root.update()
        time.sleep(1)
        seconds -= 1

def start_clock():
    work = work_clock.get_seconds()
    shortbreak = short_break_clock.get_seconds()
    longbreak = long_break_clock.get_seconds()
    session = session_clock.get_int()

    if work >= 0 and shortbreak >= 0 and longbreak >= 0 and session >= 0:
        work_clock.disabled_clock()
        short_break_clock.disabled_clock()
        long_break_clock.disabled_clock()
        session_clock.disabled()

        task = 0
        counter = 0
        while session > 0:
            if task == 0:
                work_clock.change_label_color()
                counter = (counter + 1) % 4
                decrement_clock(work_clock, work)
                session -= 1
                session_clock.set_text("{0:2d}".format(session))
                work_clock.change_label_color(BACKGROUND)
                task = 2 if counter % 4 == 0 else 1
            elif task == 1:
                short_break_clock.change_label_color()
                decrement_clock(short_break_clock, shortbreak)
                short_break_clock.change_label_color(BACKGROUND)
                task = 0
            else:
                long_break_clock.change_label_color()
                decrement_clock(long_break_clock, longbreak)
                long_break_clock.change_label_color(BACKGROUND)
                task = 0
    
        work_clock.enabled_clock()
        short_break_clock.enabled_clock()
        long_break_clock.enabled_clock()
        session_clock.enabled()

def main():
    btn.config(command=start_clock)
    btn.place(x=120, y=180)
    root.mainloop()

if __name__ == "__main__":
    main()