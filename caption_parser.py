from tkinter import *
from tkinter import filedialog
import os.path

window = Tk()
window.title("CaptionParse")
window.geometry('500x600')
window.iconbitmap('CP.ico')
window.filename = 'Please select a file'
window.fileflag = False

label = Label(window, text="Welcome to CaptionParse", font=("Arial Bold", 14), width=40)
label.grid(column=0, row=0, columnspan=2, pady=(10,10))

def srt_parse():
    if window.fileflag:
        srt = open(window.filename, 'r')
        lines = srt.readlines()

        return_string = ''

        counter = 1
        timestamp_flag = True
        for line in lines:
            try:
                if (int(line.strip()) == counter):
                    timestamp_flag = True
                    counter += 1
                    continue
            except:
                pass
                
            if timestamp_flag == True:
                timestamp_flag = False
                continue

            if line == '\n':
                continue

            return_string += line.strip() + ' '

        srt.close()

        text_box.delete('1.0', END)
        text_box.insert(END, return_string)
    else:
        text_box.delete('1.0', END)
        text_box.insert(END, "File not available or is unsupported")
    
def dfxp_parse():
    if window.fileflag:
        dfxp = open(window.filename, 'r')
        array = dfxp.read().split("<div style=\"s0\">")[1].replace("<br/>", " ").replace("<br />", " ").replace("  ", " ").split("\">")

        return_string = ''

        for i in range(1, len(array)):
            return_string += array[i].split("</p>")[0] + " "

        dfxp.close()

        text_box.delete('1.0', END)
        text_box.insert(END, return_string)
    else:
        text_box.delete('1.0', END)
        text_box.insert(END, "File not available or is unsupported")

def select_file():
    window.filename = filedialog.askopenfilename(title="Select A File", filetypes=[("Supported files", ".srt .dfxp .txt"),("all files", ".*")])
    try:
        base, ext = os.path.splitext(window.filename)
        if ext == ".txt":
            file_label.configure(text=window.filename)
            window.fileflag = True
        elif ext == ".dfxp" or ext == ".srt":
            os.rename(window.filename, base + ".txt")
            file_label.configure(text=base + ".txt")
            window.filename = base + ".txt"
            window.fileflag = True
        else:
            file_label.configure(text="Unsupported file type")
            window.fileflag = False
    except FileExistsError:
        file_label.configure(text="Conversion failed, cannot create file with same name")
        window.fileflag = False

file_directions = Label(width=50, wraplength=350, text="Choose a file below (.dfxp, .srt, .txt) are supported. \nNOTE: If using .dfxp or .srt file, it will be automatically converted to .txt. Make sure no other file has the name name with the .txt extension or else the conversion will fail.")
file_directions.grid(column=0, row=1, columnspan=2, pady=(0,10))

file_label = Label(window, text=window.filename, borderwidth=2, relief="sunken", width=50)
file_label.grid(column=0, row=2, columnspan=2)

select_button = Button(window, text="Select File", command=select_file)
select_button.grid(column=0, row=3, columnspan=2)

srt_button = Button(window, text="SRT Parse", command=srt_parse)
srt_button.grid(column=0, row=4, pady=10)

dfxp_button = Button(window, text="DFXP Parse", command=dfxp_parse)
dfxp_button.grid(column=1, row=4, pady=10)

text_box = Text(window, width=40, height=20, font=('Arial', 12), borderwidth=1, relief="sunken")
text_box.grid(column=0, row=5, columnspan=2)

window.resizable(False, False)
window.mainloop()
