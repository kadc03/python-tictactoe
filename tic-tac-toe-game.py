from tkinter import *
import os

def play_with_computer():
    os.system("python tic-tac-toe-bot.py")

def play_with_friend():
    os.system("python tic-tac-toe-2players.py")

window = Tk()
window.title("Cờ Caro")
window.geometry("500x300")

# Add a background color
window.configure(bg="#f2f2f2")

# Create a label
label_title = Label(window, text="Tic Tac Toe", font=("Arial", 20), fg="#333333", bg="#f2f2f2")
label_title.pack(pady=10)

# Create a frame for buttons
frame_buttons = Frame(window, bg="#f2f2f2")
frame_buttons.pack(pady=20)

# Customize button style
button_style = {"font": ("Arial", 14), "width": 20, "height": 2, "bg": "#ffffff", "fg": "#333333", "relief": "solid"}

# Create buttons
btn_computer = Button(frame_buttons, text="Chơi với máy", command=play_with_computer, **button_style)
btn_computer.pack(pady=10)

btn_friend = Button(frame_buttons, text="Chơi với bạn", command=play_with_friend, **button_style)
btn_friend.pack(pady=10)

label_title = Label(window, text="Phiên bản beta by it.kaira_", font=("Arial", 12), fg="red", bg="#f2f2f2")
label_title.pack(pady=3)

window.mainloop()
