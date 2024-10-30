from tkinter import*
import random
import pandas
import pyperclip



BACKGROUND_COLOR = "#B1DDC6"
current_card={}
to_learn = {}
try:
    data=pandas.read_csv("data\words_to_learn.csv")
except FileNotFoundError:
    original_data= pandas.read_csv("data/ceviri.csv")
    to_learn=original_data.to_dict(orient="records")
else:
    to_learn=data.to_dict(orient="records")


def next_card():
    global current_card,flip_timer
    window.after_cancel(flip_timer)
    current_card=random.choice(to_learn)
    pyperclip.copy(current_card["English"])
    canvas.itemconfig(card_title, text="English",fill="black")
    canvas.itemconfig(card_word, text=current_card["English"],fill="black")
    canvas.itemconfig(card_background,image=card_front_img)
    flip_timer=window.after(2000,func=flip_card) #3000ms sonra flip_card fonksiyonuna git
   
def flip_card():
    canvas.itemconfig(card_title, text="Turkish",fill="white")
    canvas.itemconfig(card_word, text=current_card["Turkish"],fill="white")
    canvas.itemconfig(card_background,image=card_back_img)
    
    
def is_known():
    with open("data/bilinen_kelimeler.txt",mode="a",encoding='utf-8') as file:
        file.write(f"{current_card['English']} : {current_card['Turkish']}\n")
        
    to_learn.remove(current_card)
    data= pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()
    
def left_click():
    canvas.itemconfig(card_title, text="English",fill="black")
    canvas.itemconfig(card_word, text=current_card["English"],fill="black")
    canvas.itemconfig(card_background,image=card_front_img)
    

def right_click():
    canvas.itemconfig(card_title, text="Turkish",fill="white")
    canvas.itemconfig(card_word, text=current_card["Turkish"],fill="white")
    canvas.itemconfig(card_background,image=card_back_img)               
     




window =Tk()
window.title("Flash Carp App")
window.resizable(False, False)

window.config(padx=50,pady=50,bg=BACKGROUND_COLOR)

flip_timer=window.after(2000,func=flip_card)


canvas=Canvas(width=820, height=526,bg=BACKGROUND_COLOR)
card_front_img=PhotoImage(file="images/card_front.png")
card_back_img=PhotoImage(file="images/card_back.png")
card_background=canvas.create_image(410, 263, image=card_front_img)
card_title=canvas.create_text(400,150,text="Title",font=("Arial",40,"italic"))
card_word=canvas.create_text(400,263,text="Word",font=("Arial",60,"bold"))
canvas.config(bg=BACKGROUND_COLOR,highlightthickness=0)
canvas.grid(column=1,row=0,columnspan=2)


cross_image = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=cross_image, highlightthickness=0,command=next_card)
unknown_button.grid(column=1,row=1)

check_image = PhotoImage(file="images/right.png")
know_button=Button(image=check_image, highlightthickness=0,command=is_known)
know_button.grid(column=2,row=1)

left_image = PhotoImage(file="images/left.png")
left_button = Button(image=left_image, highlightthickness=0, bg=BACKGROUND_COLOR, command=left_click)
left_button.grid(column=0,row=0,padx=15)

right_image = PhotoImage(file="images/rightbutton.png")
right_button = Button(image=right_image, highlightthickness=0, bg=BACKGROUND_COLOR, command=right_click)
right_button.grid(column=3,row=0)





next_card()

window.mainloop()