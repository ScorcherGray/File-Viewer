import sys
from tkinter import *
from tkinter import simpledialog

if __name__ == '__main__':
   args = sys.argv 
    #assert(len(args) == 3), "Incorrect arguments " #Used in testing

root = Tk()
 
def close(): #destroy the window and close file stream
    global words
    root.destroy()
    words.close()
def page(): #pop up window for to get page numbers
    pagenum = simpledialog.askinteger("Page", "Enter page number: ", parent=root, minvalue=0, maxvalue=max)
    turnpage(pagenum-1)
def prev(n): #Call previous page number
    global pages
    if n > 0:
        n = n-1
    else:
        n = len(pages) -1
    turnpage(n)
def turn(n): #Call next page number
    global pages
    if n < len(pages):
        n = n + 1
    else:
        n = 0
    turnpage(n)
def turnpage(m): #Turn to page of given number
    global fname
    global n
    global words
    global pages
    n = m
    txtarea.config(state=NORMAL)
    txtarea.delete(1.0, END)
    if n == len(pages)-1: #For the last page
        words.seek(pages[n])
        text = words.read(max - pages[n])
        numlines = text.count('\n')
        for i in range(numlines, viewsize): #Fill the unused space with newline returns. May not be needed for GUI
            text = text + '\n'
        txtarea.insert(END, text)
    elif 0 < n < len(pages) - 1: #Any page between first and last
        words.seek(pages[n])
        text = words.read(pages[n+1] - pages[n])
        txtarea.insert(END, text)
    else: #Should only be the first page. Set to return to first page when 'down' called on last page.
        n = 0
        words.seek(0)
        text = words.read(pages[1])
        txtarea.config(state=NORMAL)
        txtarea.insert(END, text)
    root.title(f"{fname} - Page {n+1}") #Set window title
    txtarea.config(state=DISABLED) #Prevent user from adding words because they don't know what they're doing.



#Switch fname assignment for testing. Not sure which was needed
fname = 'yankee.txt'
#fname = args[1]

#Define viewsize/page size based on user input. Default 20
if len(args) == 3:
    viewsize = int(args[2])
else:
    viewsize = 20
pages = [0]
words = open(fname, "r")
words.seek(0,2)#Traverse the entire file collecing positions where each viewsize begins
max = words.tell()
if max == 0:
    print("File is empty!")
    sys.exit()
words.seek(0) # Reset read position to the start of the file
while pages[-1] <= max: #Populate the 'pages' array with bit locations of page size
    for i in range(0, viewsize):
        words.readline()
        i += 1
    pages.append(words.tell())
    if pages[-1] == max: break #probably unnecessary break statement
pages.pop() #Removing the 'page' that starts at the end of the file

#Defining the GUI
txtframe = Frame(master=root)
txtarea = Text(master=txtframe, height=viewsize, width=50, wrap=NONE)
buttonArea = Frame(master=root)
down = Button(master = buttonArea, text="Down", command=lambda: turn(n))
top = Button(master=buttonArea, text="Top", command=lambda: turnpage(0))
upButton = Button(master=buttonArea, text="Up", command =lambda: prev(n))
bottom = Button(master=buttonArea, text="Bottom", command = lambda: turnpage(len(pages) - 1))
pageButton = Button(master=buttonArea, text="Page", command = lambda: page())
closeButton = Button(master=buttonArea, text="Quit", command=close)
root.title(f"{fname} - Page 1")
scrolls = Scrollbar(master = txtframe,orient=HORIZONTAL)
#packing GUI
top.pack(side=LEFT, padx=2, pady=2)
upButton.pack(side=LEFT, padx=2, pady=2)
down.pack(side=LEFT, padx=2, pady=2)
bottom.pack(side=LEFT, padx=2, pady=2)
pageButton.pack(side=LEFT, padx=2, pady=2)
closeButton.pack(side=LEFT, padx=2, pady=2)
txtarea.pack()
txtframe.pack(fill=X)
scrolls.pack(side=BOTTOM,fill=X)
scrolls.config(command=txtarea.xview)
txtarea.config(xscrollcommand=scrolls.set)
buttonArea.pack(fill=X)
txtarea.config(state=DISABLED)
turnpage(0)#Set to first page
root.mainloop()#Display GUI