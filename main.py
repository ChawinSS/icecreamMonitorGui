import tkinter as tk
from tkinter import *
from random import randrange
import random
from time import sleep
from threading import Thread, Event
import string
from tkinter import messagebox  
import json
import os

#Static
string.ascii_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


#Data#
stations = []
event = Event()

firstStation = {"StationId" : "MK76Y", "Date" : "5/26/2006", "Target" : 42, "Actual" : 33}
secondStation = {"StationId" : "NV140", "Date" : "4/12/2009", "Target" : 30, "Actual" : 10}
thirdStation = {"StationId" : "RN452", "Date" : "7/2/2012", "Target" : 15, "Actual" : 22}


def readFromFile():
    if os.path.isfile("./out.json"):
       f = open("out.json")
       data = json.load(f)
       for i in data:
           stations.append(i)
    else:
        stations.append(firstStation)
        stations.append(secondStation)
        stations.append(thirdStation)

def saveListToFile():
    with open("out.json", "w") as fout:
        json.dump(stations, fout)




def findStationById(stationId):
    for index, station in enumerate(stations):
        if(station["StationId"] == stationId):
            return station
        
def updateDateById(stationId, date):
    for index, station in enumerate(stations):
         if(station["StationId"] == stationId):
             station["Date"] = date

def updateActualValueById(stationId, actual):
    for index, station in enumerate(stations):
         if(station["StationId"] == stationId):
             station["Actual"] = actual

def updateVarianceById(stationId):
    entry_variance.delete(0, END)
        
    variance = findStationById(stationId)["Actual"] - findStationById(stationId)["Target"]
        
    entry_variance.config(state = NORMAL)
    entry_variance.delete(0, END)
    entry_variance.insert(0, variance)
    entry_variance.config(state = DISABLED)
    

readFromFile()
root = tk.Tk()


sv_date = StringVar()
sv_actual = StringVar()

def dateCallback():
    updateDateById(entry_station.get(), sv_date.get())
    return True

def actualCallback():
    updateActualValueById(entry_station.get(), int(sv_actual.get()))
    updateVarianceById(entry_station.get())
    return True

def onKeyPress(event):
    root.focus()



root.geometry("600x350")
root.title("Assesment Record")
root.resizable(False, False)


#Elements-Labels
label_station = tk.Label(root, text="Station ID")
label_station.place(x = 220, y = 100)
#
label_date = tk.Label(root, text = "Date")
label_date.place(x = 220, y = 140)
#
label_target = tk.Label(root, text = "Target")
label_target.place(x = 220, y = 180)
#
label_actual = tk.Label(root, text = "Actual")
label_actual.place(x = 220, y = 220)
#
label_variance = tk.Label(root, text = "Variance")
label_variance.place(x = 220, y = 260)
#Elements-Entrys
entry_station = tk.Entry(root)
entry_station.place(x = 300, y = 98)
#
entry_date = tk.Entry(root, validate="focusout", validatecommand=dateCallback, textvariable=sv_date)
entry_date.place(x = 300, y = 138)
#
entry_target = tk.Entry(root)
entry_target.place(x = 300, y = 178)
#
entry_actual = tk.Entry(root, validate="focusout", validatecommand=actualCallback, textvariable=sv_actual)
entry_actual.place(x = 300, y = 218)
#
entry_variance = tk.Entry(root)
entry_variance.place(x = 300, y = 258)

#Elements

Lb1 = Listbox(root)

for index, station in enumerate(stations):
    Lb1.insert(index, station["StationId"])


Lb1.place(x = 20, y = 100)


def callback(event):
    selection = event.widget.curselection()
    if selection:
        index = selection[0]
        data = event.widget.get(index)
        #Working on the fields
        entry_station.config(state = NORMAL)
        entry_station.delete(0,END)
        entry_station.insert(0, data)
        entry_station.config(state = DISABLED)
        
        entry_date.delete(0, END)
        entry_date.insert(0, findStationById(data)["Date"])

        entry_target.config(state = NORMAL)
        entry_target.delete(0, END)
        entry_target.insert(0, findStationById(data)["Target"])
        entry_target.config(state = DISABLED)

        entry_actual.delete(0, END)
        entry_actual.insert(0, findStationById(data)["Actual"])
       
        
        updateVarianceById(data)
        
        print(data)

Lb1.bind("<<ListboxSelect>>", callback)

root.bind("<Return>", onKeyPress)



def appendRandomStation():
    
    broke = False

    while True:

        station_id = random.choice(string.ascii_letters) + random.choice(string.ascii_letters) + str(randrange(999))
        date = str(randrange(1, 12)) + "/" + str(randrange(1,31))  + "/" + str(randrange(2000, 2025))
        target = randrange(1, 80)
        actual = randrange(0, 100)
        
        time = randrange(100) # 300 in production
        print(f"Sleep for {time}")
        
        for i in range(time - 1):
            if event.is_set():
                broke = True
                break
            sleep(1)
        
        if broke == True:
            break

        random_station = {"StationId" : station_id, "Date" : date, "Target" : target, "Actual" : actual}
        stations.append(random_station)
        Lb1.insert(Lb1.size(), station_id)
        print("Station Added") 
        print(random_station)

        messagebox.showinfo("Allert!","A new station was added")  
        


t1 = Thread(target=appendRandomStation)
t1.start()

def closeWindow():
    print("Closeddd")
    event.set()
    exit_box = messagebox.askyesno(title="Save ?", message="Do you want to save ?")
    if(exit_box == True):
        print("Saving file......")
        saveListToFile()
        root.destroy()
    else:
        root.destroy()
    
        
    

root.protocol("WM_DELETE_WINDOW", closeWindow)
root.mainloop()