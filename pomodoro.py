import time
from tkinter import *
from tkinter import messagebox

FONT = "Segoe UI"
FONT_S = 10 # Small
FONT_M = 18 # Medium
BACKGROUND = "#1FB2FD" # blue
TIMER_ENTRY_BG = "#FED818" # yellow
TIMER_ENTRY_FG = "black"
LABEL_BG = BACKGROUND
LABEL_FG = "black"
BTN_BG = "#FF1E8C" # pink
BTN_FG = "white"

BREAK_MESSAGE = "Break time!"
WORK_MESSAGE = "Work!"
END_PROGRAM_MESSAGE = "Well done!"

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
        self.label_padding_right = padding_right
        self.entry_label = Label(root, text=text, font=(self.font_family, label_font_size, ""), bg=label_bg, fg=label_fg)
        self.entry_label.place(x=self.entry_x - (self.label_padding_right or self.entry_padding), y=self.entry_y)

    def hide_entry(self):
        self.entry.place_forget()
        if self.entry_label: self.entry_label.place_forget()

    def show_entry(self):
        self.entry.place(x=self.entry_x, y=self.entry_y)
        if self.entry_label: self.entry_label.place(x=self.entry_x - (self.label_padding_right or self.entry_padding), y=self.entry_y)
    

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
        self.label_padding_right = padding_right
        self.clock_label = Label(root, text=text, font=(self.font_family, label_font_size, ""), bg=label_bg, fg=label_fg)
        self.clock_label.place(x=self.entry_x - (self.label_padding_right or self.entry_padding), y=self.entry_y)

    def set_label_text(self, text):
        self.clock_label.config(text=text)

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

    def hide_clock(self):
        self.hour.hide_entry()
        self.minute.hide_entry()
        self.second.hide_entry()
        if self.clock_label: self.clock_label.place_forget()

    def show_clock(self):
        self.hour.show_entry()
        self.minute.show_entry()
        self.second.show_entry()
        if self.clock_label: self.clock_label.place(x=self.entry_x - (self.label_padding_right or self.entry_padding), y=self.entry_y)

work_clock = ClockHMS(120, 20, 50)
work_clock.set_label("Work", padding_right=90)

short_break_clock = ClockHMS(120, 60, 50)
short_break_clock.set_label("Short Break", padding_right=90)

long_break_clock = ClockHMS(120, 100, 50)
long_break_clock.set_label("Long Break", padding_right=90)

session_clock = ClockEntry(120, 140)
session_clock.set_label("Session", padding_right=90)

start_btn = Button(root, text='Start', bd='5', font=(FONT,FONT_M,""), bg=BTN_BG, fg=BTN_FG)
stop_btn = Button(root, text='Stop', bd='5', font=(FONT,FONT_M,""), bg=BTN_BG, fg=BTN_FG)

countdown_clock = ClockHMS(78, 80, 50)
countdown_clock.disabled_clock()
countdown_clock.hide_clock()

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

def show_countdown_layout():
    work_clock.hide_clock()
    short_break_clock.hide_clock()
    long_break_clock.hide_clock()
    session_clock.hide_entry()
    start_btn.place_forget()
    countdown_clock.show_clock()

def hide_countdown_layout():
    work_clock.show_clock()
    short_break_clock.show_clock()
    long_break_clock.show_clock()
    session_clock.show_entry()
    start_btn.place(x=120, y=180)
    countdown_clock.hide_clock()

def start_clock():
    work = work_clock.get_seconds()
    shortbreak = short_break_clock.get_seconds()
    longbreak = long_break_clock.get_seconds()
    session = session_clock.get_int()

    if work >= 0 and shortbreak >= 0 and longbreak >= 0 and session >= 0:
        show_countdown_layout()
        counter_label = Label(root, text=f'Work\nSession: 0/{session}', font=(FONT, FONT_M, ""), bg=BACKGROUND, fg=LABEL_FG)
        counter_label.place(x=83, y=160)

        task, counter, times = 0, 0, session
        while times > 0:
            if task == 0:
                counter += 1
                counter_label.config(text=f'Work\nSession: {counter}/{session}')
                decrement_clock(countdown_clock, work)
                times -= 1
                task = 2 if counter % 4 == 0 else 1
                messagebox.showinfo("Alarm", BREAK_MESSAGE)
            elif task == 1:
                counter_label.config(text=f'Short Break\nSession: {counter}/{session}')
                decrement_clock(countdown_clock, shortbreak)
                task = 0
                messagebox.showinfo("Alarm", WORK_MESSAGE)
            else:
                counter_label.config(text=f'Long Break\nSession: {counter}/{session}')
                decrement_clock(countdown_clock, longbreak)
                task = 0
                messagebox.showinfo("Alarm", WORK_MESSAGE)
    
        messagebox.showinfo("Alarm", END_PROGRAM_MESSAGE)
        hide_countdown_layout()
        counter_label.place_forget()

def main():
    start_btn.config(command=start_clock)
    start_btn.place(x=120, y=180)
    root.mainloop()

if __name__ == "__main__":
    main()