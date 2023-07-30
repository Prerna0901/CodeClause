from tkinter import *
from tkinter import filedialog
from tkinter import font
from tkinter import colorchooser

root = Tk()
root.title("TextEditor")
root.geometry("1200x660")

global open_status_name
open_status_name = False

global selected
selected = False

#Create new file function
def new_file():
    my_text.delete("1.0", END)
    root.title('New File - TextPad!')
    status_bar.config(text="New File        ")

    global open_status_name
    open_status_name = False

#Open files
def open_file():
    my_text.delete("1.0", END)
    text_file = filedialog.askopenfilename(initialdir="C:/gui/", title="Open File", filetypes=(("Text Files", "*.txt"), ("HTML Files", "*.html"), ("Python Files", "*.py"), ("All Files", "*.*")))

    if text_file:
        global open_status_name
        open_status_name = text_file

    name = text_file
    status_bar.config(text=f'{name}        ')
    name = name.replace("C:/gui/", "")
    root.title(f'{name} - TextPad!')
    text_file = open(text_file, 'r')
    stuff = text_file.read()
    my_text.insert(END, stuff)
    text_file.close()

#Save As file
def save_as():
    text_file = filedialog.asksaveasfilename(defaultextension=".*", initialdir="C:/gui/", title="Save File", filetypes=(("Text Files", "*.txt"),("HTML Files", "*.html"), ("Python Files", "*.py"), ("All Files", "*.*")))
    if text_file:
        name = text_file
        name = name.replace("C:/gui/","")
        root.title(f'{name} - TextPad!')
        status_bar.config(text=f'Saved: {name}        ')
        text_file = open(text_file, 'w')
        text_file.write(my_text.get(1.0, END))
        text_file.close()

#Save file
def save_file():
    global open_status_name
    if open_status_name:
        text_file = open(text_file, 'w')
        text_file.write(my_text.get(1.0, END))
        text_file.close()

        status_bar.config(text=f'Saved: {open_status_name}        ')
    else:
        save_as()

def cut_text(e):
    global selected
    if e:
        selected = root.clipboard_get()
    else:
        if my_text.selection_get():
         selected = my_text.selection_get()     
         my_text.delete("sel.first", "sel.last")
         root.clipboard_clear()
         root.clipboard_append(selected)


def copy_text(e):
    global selected
    if e:
        selected = root.clipboard_get()

    if my_text.selection_get():
        selected = my_text.selection_get()
        root.clipboard_clear()
        root.clipboard_append(selected)

def paste_text(e):
    global selected
    if e:
        selected = root.clipboard_get()
    else:
        if selected:position = my_text.index(INSERT)
        my_text.insert(position, selected)

def bold_it():
    bold_font = font.Font(my_text, my_text.cget("font"))
    bold_font.configure(weight="bold")
    
    my_text.tag_configure("bold", font=bold_font)

    current_tags = my_text.tag_names("sel.first")
    if "bold" in current_tags:
        my_text.tag_remove("bold", "sel.first", "sel.last")
    else:
        my_text.tag_add("bold", "sel.first", "sel.last")


def italics_it():
    italics_font = font.Font(my_text, my_text.cget("font"))
    italics_font.configure(slant="italic")
    
    my_text.tag_configure("italic", font=italics_font)

    current_tags = my_text.tag_names("sel.first")
    if "italic" in current_tags:
        my_text.tag_remove("italic", "sel.first", "sel.last")
    else:
        my_text.tag_add("italic", "sel.first", "sel.last")


#Create a toolbar frame
toolbar_frame = Frame(root)
toolbar_frame.pack(pady=5)

#Create main frame
my_frame = Frame(root)
my_frame.pack(pady=5)

#Create our scrollbar for the text box
scrollbar = Scrollbar(my_frame)
scrollbar.pack(side=RIGHT, fill=Y)

hor_scroll = Scrollbar(my_frame, orient='horizontal')
hor_scroll.pack(side=BOTTOM, fill=X)

#Create Text box
my_text = Text(my_frame, width=97, height=25, font=("Helvetica", 16), selectbackground="yellow", selectforeground="black", undo=True, yscrollcommand=Scrollbar.set, wrap="none", xscrollcommand=hor_scroll.set)
my_text.pack()

#Configure our scrollbar
scrollbar.config(command=my_text.yview)
hor_scroll.config(command=my_text.xview)

#Create menu
my_menu = Menu(root)
root.config(menu=my_menu)

#Add file menu
file_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_command(label="Save as", command=save_as)
file_menu.add_command(label="Print")
file_menu.add_separator()
file_menu.add_command(label="Close tab")
file_menu.add_command(label="Close window")
file_menu.add_command(label="Exit")

#Add Edit menu
edit_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Undo", command=my_text.edit_undo, accelerator="(Ctrl+z)")
edit_menu.add_command(label="Cut", command=lambda: cut_text(False), accelerator="(Ctrl+x)")
edit_menu.add_command(label="Copy", command=lambda: copy_text(False), accelerator="(Ctrl+c)")
edit_menu.add_command(label="Paste            ", command=lambda: paste_text(False), accelerator="(Ctrl+v)")
edit_menu.add_command(label="Delete")
edit_menu.add_command(label="Print")


#Add Status bar to Bottom of App

status_bar = Label(root, text='Ready        ',anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=15)

root.bind('<Control-Key-x>', cut_text)
root.bind('<Control-Key-c>', copy_text)
root.bind('<Control-Key-v>', paste_text)

#Create Bold Button
bold_button = Button(toolbar_frame, text="Bold", command=bold_it)
bold_button.grid(row=0, column=0, sticky=W, padx=5)

#Create Italics Button
italic_button = Button(toolbar_frame, text="Italic", command=italics_it)
italic_button.grid(row=0, column=1, padx=5)

#Undo Button
undo_button = Button(toolbar_frame, text="Undo", command=my_text.edit_undo)
undo_button.grid(row=0, column=2, padx=5)


root.mainloop()