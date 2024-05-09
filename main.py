import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import filedialog
from tkinter.ttk import Combobox
import os
root = Tk()

#title
root.title("Text To Speech")
root.geometry("900x450+250+150")
root.resizable(False,False)
root.configure(bg="#305065")

import pyttsx3
import PyPDF2

engine=pyttsx3.init()
speaker=pyttsx3.init()
        
def speaknow():
    print("speaking")
    text = text_area.get(1.0, END)
    gender = gender_combobox.get()
    speed = speed_combobox.get()
    voices = engine.getProperty('voices')

    def setvoice():
        if gender == 'Male':
            engine.setProperty('voice', voices[0].id)
        else:
            engine.setProperty('voice', voices[1].id)

        if speed == 'Fast':
            engine.setProperty('rate', 250)
        elif speed == 'Normal':
            engine.setProperty('rate', 150)
        else:
            engine.setProperty('rate', 50)

        engine.say(text)
        engine.runAndWait()

    if text.strip():  # Check if text is not empty
        setvoice()
    else:
        print("No text to speak")
            
def download():
    text=text_area.get(1.0,END)
    gender=gender_combobox.get()
    speed=speed_combobox.get()
    voices = engine.getProperty('voices')
    
    def setvoice():
        if (gender=='Male'):
            engine.setProperty('voice',voices[0].id)
            path=filedialog.askdirectory()
            os.chdir(path)
            engine.save_to_file(text,'text.mp3')
            engine.runAndWait()
        else:
            engine.setProperty('voice',voices[1].id)
            path=filedialog.askdirectory()
            os.chdir(path)
            engine.save_to_file(text,'text.mp3')
            engine.runAndWait()
    
    if (text):
        if (speed=='Fast'):
            engine.setProperty('rate',250)
            setvoice()
        elif (speed=='Normal'):   
            engine.setProperty('rate',150)
            setvoice()
        else:
            engine.setProperty('rate',50)
            setvoice()    
    
#icon
icon_image = PhotoImage(file="speak.png")
root.iconphoto(True, icon_image)

#TopFrame
Top_frame=Frame(root,bg="white",width=900,height=100)
Top_frame.place(x=0,y=0)

logo=PhotoImage(file="speaker logo.png")
Label(Top_frame,image=logo,bg="white").place(x=10,y=1)
Label(Top_frame,text="TEXT TO SPEECH",font="arial 20 bold",bg="white",fg="black").place(x=100,y=35)  

text_area=Text(root,font="Robote 20",bg="white",relief=GROOVE,wrap=WORD)
text_area.place(x=10,y=150,width=500,height=150)

# Page number and choose file area
page_number_frame = Frame(root, bg="#305065", highlightbackground="white")
page_number_frame.place(x=10, y=310, width=500, height=40)

label_page = Label(page_number_frame, text="Start Page Number:", font="arial 12", bg="#305065", fg="white").pack(side=LEFT)
start_page_number_entry = Entry(page_number_frame, font="arial 12", width=5)
start_page_number_entry.pack(side=LEFT)

label_page1 = Label(page_number_frame, text="End Page Number:", font="arial 12", bg="#305065", fg="white").pack(side=LEFT)
ending_page_number_entry = Entry(page_number_frame, font="arial 12", width=5)
ending_page_number_entry.pack(side=LEFT, padx=10)  # Place after start page number

selected_file_path = ""

def fileDialog():
    global selected_file_path
    path = filedialog.askopenfilename()
    selected_file_path = path
    print("Selected file path:", selected_file_path)
    book = open(path, 'rb')
    pdfReader = PyPDF2.PdfReader(book)
    pages = len(pdfReader.pages)

    try:
        start_page_number = int(start_page_number_entry.get())
        end_page_number = int(ending_page_number_entry.get())
    except ValueError:
        print("Please enter valid page numbers (integers).")
        return

    # Ensure end page number is within document boundaries
    if end_page_number > pages:
        print(f"Error: Ending page number ({end_page_number}) exceeds total pages ({pages}).")
        return

    # Clear existing text in the text area
    text_area.delete(1.0, END)

    for num in range(start_page_number - 1, end_page_number):  # Adjust for zero-based indexing
        page = pdfReader.pages[num]
        txt = page.extract_text()   
        
        # Append the text to the text area
        text_area.insert(END, txt + "\n\n")
        
        # Read aloud the text
        speaker.say(txt)
        speaker.runAndWait()

    book.close() 

# Update the "Choose File" button command to call the modified fileDialog() function
choose_file_button = Button(page_number_frame, text="Choose File", font="arial 12", command=fileDialog)
choose_file_button.pack(side=RIGHT)


def speech():
    speaknow()
    if button_clicked:
        fileDialog()

# Add a global variable to track whether the "speech" button is clicked
button_clicked = False

def on_speech_button_click():
    global button_clicked
    button_clicked = True
    speech()

#voice and speed dropdown
Label(root,text="VOICE",font="arial 15 bold",bg="#305065",fg="white").place(x=580,y=160)
Label(root,text="SPEED",font="arial 15 bold",bg="#305065",fg="white").place(x=760,y=160)

gender_combobox=Combobox(root,values=['Male','Female'],font="arial 14",state='r',width=10)
gender_combobox.place(x=550,y=200)
gender_combobox.set('Male')

speed_combobox=Combobox(root,values=['Slow','Normal','Fast'],font="arial 14",state='r',width=10)
speed_combobox.place(x=730,y=200)
speed_combobox.set('Normal')

imageicon1=PhotoImage(file="speak.png")
btn=Button(root,text="Speak",compound=LEFT,image=imageicon1,width=125,font="arial 14 bold",command=speech) 
btn.place(x=550,y=290)

imageicon2=PhotoImage(file="download.png")
save=Button(root,text="Save",compound=LEFT,image=imageicon2,width=125,font="arial 14 bold",command=download)
save.place(x=730,y=290)

root.mainloop()  