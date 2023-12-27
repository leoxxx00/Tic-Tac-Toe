from tkinter import *
from tkinter import messagebox

root = Tk()
root.title('Tic-Tac-Toe')
root.iconbitmap('rock.png')

clicked = True
count = 0

# Create buttons as a list for easier handling
buttons = [Button(root, text="", font=("Helvetica", 20), height=3, width=6, bg="SystemButtonFace", command=lambda i=i: b_click(i)) for i in range(9)]

def disable_all_buttons():
    for button in buttons:
        button.config(state=DISABLED)

def check_if_won():
    global count
    winner = False

    # Define winning combinations
    winning_combinations = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                             (0, 3, 6), (1, 4, 7), (2, 5, 8),
                             (0, 4, 8), (2, 4, 6)]

    for combination in winning_combinations:
        if buttons[combination[0]]["text"] == buttons[combination[1]]["text"] == buttons[combination[2]]["text"] != "":
            winner = True
            for index in combination:
                buttons[index].config(bg="red")
            messagebox.showinfo("Tic Tac Toe", f"Congratulations {buttons[combination[0]]['text']} wins")
            disable_all_buttons()
            break

    if count == 9 and not winner:
        messagebox.showinfo("Tic Tac Toe", "It's A Tie\nNo one wins")
        disable_all_buttons()

def b_click(i):
    global clicked, count

    if buttons[i]["text"] == "" and clicked:
        buttons[i]["text"] = "X"
        clicked = False
        count += 1
        check_if_won()
    elif buttons[i]["text"] == "" and not clicked:
        buttons[i]["text"] = "O"
        clicked = True
        count += 1
        check_if_won()
    else:
        messagebox.showerror("Tic Tac Toe", "Hey... That box is already selected...\nPick another one...")

def reset():
    global clicked, count
    clicked = True
    count = 0

    for button in buttons:
        button.config(text="", state=NORMAL, bg="SystemButtonFace")

reset_button = Button(root, text="Reset Game", command=reset)
reset_button.grid(row=3, column=0, columnspan=3)

# Grid the buttons
for i, button in enumerate(buttons):
    button.grid(row=i // 3, column=i % 3)

root.mainloop()
