# Reference: https://www.geeksforgeeks.org/create-countdown-timer-using-python-tkinter/

import time
from tkinter import *
from tkinter import messagebox

# Color
timerEntryBG = "#cfff24"
timerEntryFG = "black"
btnBG = "#ee1982"
btnFG = "#cfff24"
background = "#23bbe2"
labelBG = background
labelFG = "black"
taskLabelGB = background
taskLabelFG = "black"

# creating Tk window
root = Tk()

# setting geometry of tk window
root.geometry("300x250")
root['background'] = background

# Using title() to display a message in
# the dialogue box of the message in the
# title bar.
root.title("Interval Time Counter")

# Declaration of variables
hour=StringVar()
minute=StringVar()
second=StringVar()

chour=StringVar()
cminute=StringVar()
csecond=StringVar()

repeat=StringVar()

# setting the default value as 0
hour.set("00")
minute.set("00")
second.set("00")

chour.set("00")
cminute.set("00")
csecond.set("00")

repeat.set("00")

worklabel = Label(root, text="Work", font=("Arial",10,""), bg=labelBG, fg=labelFG)
worklabel.place(x=40,y=20)

chilllabel = Label(root, text="Break", font=("Arial",10,""), bg=labelBG, fg=labelFG)
chilllabel.place(x=40,y=60)

# Use of Entry class to take input from the user
hourEntry= Entry(root, width=3, font=("Arial",18,""), textvariable=hour, bg=timerEntryBG, fg=timerEntryFG)
hourEntry.place(x=80,y=20)

minuteEntry= Entry(root, width=3, font=("Arial",18,""), textvariable=minute, bg=timerEntryBG, fg=timerEntryFG)
minuteEntry.place(x=130,y=20)

secondEntry= Entry(root, width=3, font=("Arial",18,""), textvariable=second, bg=timerEntryBG, fg=timerEntryFG)
secondEntry.place(x=180,y=20)

# Chill
chillhourEntry= Entry(root, width=3, font=("Arial",18,""), textvariable=chour, bg=timerEntryBG, fg=timerEntryFG)
chillhourEntry.place(x=80,y=60)

chillminuteEntry= Entry(root, width=3, font=("Arial",18,""), textvariable=cminute, bg=timerEntryBG, fg=timerEntryFG)
chillminuteEntry.place(x=130,y=60)

chillsecondEntry= Entry(root, width=3, font=("Arial",18,""), textvariable=csecond, bg=timerEntryBG, fg=timerEntryFG)
chillsecondEntry.place(x=180,y=60)

tasklabel = Label(root, font=("Arial",18,"bold"), bg=taskLabelGB, fg=taskLabelFG)
btn = Button(root, text='Start', bd='5', font=("Arial",18,""), bg=btnBG, fg=btnFG)

# interval
repeatEntry= Entry(root, width=3, font=("Arial",18,""), textvariable=repeat, bg=timerEntryBG, fg=timerEntryFG)
repeatEntry.place(x=130,y=100)

def new_layout(repeatTime):
	hourEntry.place(x=80, y=80)
	minuteEntry.place(x=130, y=80)
	secondEntry.place(x=180, y=80)
	chillhourEntry.place_forget()
	chillminuteEntry.place_forget()
	chillsecondEntry.place_forget()
	worklabel.place(x=20, y=180)
	worklabel.config(text='Work: 0/%d' %(repeatTime))
	chilllabel.place(x=20, y=200)
	chilllabel.config(text='Break: 0/%d' %(repeatTime - 1))
	tasklabel.place(x=120, y=30)
	btn.place_forget()
	repeatEntry.place_forget()

def reset_layout():
	hourEntry.place(x=80,y=20)
	minuteEntry.place(x=130,y=20)
	secondEntry.place(x=180,y=20)
	chillhourEntry.place(x=80,y=60)
	chillminuteEntry.place(x=130,y=60)
	chillsecondEntry.place(x=180,y=60)
	worklabel.place(x=40,y=20)
	worklabel.config(text='Work')
	chilllabel.place(x=40,y=60)
	chilllabel.config(text='Break')
	tasklabel.place_forget()
	btn.place(x = 120,y = 150)
	hour.set("00")
	minute.set("00")
	second.set("00")
	chour.set("00")
	cminute.set("00")
	csecond.set("00")
	repeat.set("00")
	repeatEntry.place(x=130,y=100)

def submit():
	try:
		# the input provided by the user is
		# stored in here :temp
		temp = int(hour.get())*3600 + int(minute.get())*60 + int(second.get())
		chilltmp = int(chour.get())*3600 + int(cminute.get())*60 + int(csecond.get())
		worktimer = temp
		work = True
		worktime = 0
		chilltime = 0
		tasklabel.config(text="Work")
		repeatTime = int(repeat.get())
		new_layout(repeatTime)
	except:
		print("Please input the right value")
	while temp >-1 and (worktime < repeatTime or chilltime < repeatTime - 1):
		# divmod(firstvalue = temp//60, secondvalue = temp%60)
		mins,secs = divmod(temp,60)

		# Converting the input entered in mins or secs to hours,
		# mins ,secs(input = 110 min --> 120*60 = 6600 => 1hr :
		# 50min: 0sec)
		hours=0
		if mins >60:
			hours, mins = divmod(mins, 60)
		
		# using format () method to store the value up to
		# two decimal places
		hour.set("{0:2d}".format(hours))
		minute.set("{0:2d}".format(mins))
		second.set("{0:2d}".format(secs))

		# updating the GUI window after decrementing the
		# temp value every time
		root.update()
		time.sleep(1)

		# when temp value = 0; then a messagebox pop's up
		# with a message:"Time's up"
		if (temp == 0):
			messagebox.showinfo("Timer", "Time's up ")
			if work:
				temp = chilltmp
				worktime += 1
				work = False
				tasklabel.config(text='Break')
				worklabel.config(text='Work: %d/%d' %(worktime, repeatTime))
			else:
				temp = worktimer
				work = True
				chilltime += 1
				tasklabel.config(text='Work')
				chilllabel.config(text='Break: %d/%d' %(chilltime, repeatTime - 1))
		
		# after every one sec the value of temp will be decremented
		# by one
		temp -= 1
	
	reset_layout()

# button widget
btn.config(command=submit)
btn.place(x = 120,y = 150)

# infinite loop which is required to
# run tkinter program infinitely
# until an interrupt occurs
root.mainloop()
