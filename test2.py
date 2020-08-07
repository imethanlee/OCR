import tkinter as tk
from PIL import Image, ImageTk
win = tk.Tk()
win.geometry("600x400+200+100")
canvas = tk.Canvas(win, bg="orange")
canvas.pack()
bg_image = Image.open("bg.jpg")
bg = ImageTk.PhotoImage(bg_image)
canvas.create_image(0, 0, image=bg)



btn = tk.Button(canvas, text="删除")
btn.place(relx=0.4, rely=0.8)

win.mainloop()