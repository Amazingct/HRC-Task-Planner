import criterion as cr
from tkinter import*

win = Tk()
win.geometry("1950x1500")

Button(win, text= "Upload Tasks file", command = cr.openTasks).pack()
Button(win, text= "Upload Safety file", command = cr.openSafety).pack()
Button(win, text = "Proceed", command = cr.proceed).pack(pady=5)
Button(win, text ="Skip", command = cr.default_file).pack(pady=5)

    

win.mainloop()




# import pip
# pip.main(["install", "openpyxl"])

