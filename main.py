from tkinter import *
from tkinter import messagebox
import numpy as np
import pickle

# Load Q-values from file (if available)
try:
    with open("q_values.pkl", "rb") as f:
        q_values = pickle.load(f)
except FileNotFoundError:
    # Initialize Q-values if the file doesn't exist
    q_values = {}

root = Tk()
root.title('Tic-Tac-Toe')
root.iconbitmap('rock.png')

# Constants for the players
PLAYER_X = 'X'
PLAYER_O = 'O'

# Constants for the Q-learning algorithm
LEARNING_RATE = 0.1
DISCOUNT_FACTOR = 0.9
EXPLORATION_PROB = 0.2

# Variables to track game mode
player_vs_player = False

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

    if buttons[i]["text"] == "":
        if player_vs_player:
            if clicked:
                buttons[i]["text"] = PLAYER_X
            else:
                buttons[i]["text"] = PLAYER_O
            clicked = not clicked
        else:
            buttons[i]["text"] = PLAYER_X
            count += 1
            check_if_won()

            # Let AI make a move
            if count < 9:
                ai_move = get_ai_move()
                buttons[ai_move]["text"] = PLAYER_O
                count += 1
                check_if_won()

def get_state():
    state = tuple(button["text"] for button in buttons)
    return state

def get_q_value(state, action):
    return q_values.get((state, action), 0)

def update_q_value(state, action, value):
    q_values[(state, action)] = value

def get_available_actions(state):
    return [i for i, value in enumerate(state) if value == ""]

def choose_best_action(state):
    available_actions = get_available_actions(state)
    if np.random.rand() < EXPLORATION_PROB:
        # Explore: choose a random action
        return np.random.choice(available_actions)
    else:
        # Exploit: choose the action with the highest Q-value
        q_values_for_state = {action: get_q_value(state, action) for action in available_actions}
        return max(q_values_for_state, key=q_values_for_state.get)

def get_ai_move():
    state = get_state()
    action = choose_best_action(state)
    return action

def update_q_values(winner):
    # Update Q-values based on the game outcome
    if winner == PLAYER_X:
        reward = 1
    elif winner == PLAYER_O:
        reward = -1
    else:
        reward = 0

    for i in range(9):
        state = get_state()
        action = i
        current_q_value = get_q_value(state, action)
        max_next_q_value = max(get_q_value(state, next_action) for next_action in get_available_actions(state))
        new_q_value = (1 - LEARNING_RATE) * current_q_value + LEARNING_RATE * (reward + DISCOUNT_FACTOR * max_next_q_value)
        update_q_value(state, action, new_q_value)

# Function to switch between player vs. player and player vs. AI modes
def switch_mode():
    global player_vs_player, clicked, count
    player_vs_player = not player_vs_player
    clicked = True
    count = 0
    reset()

# Function to reset the game
def reset():
    global clicked, count
    clicked = True
    count = 0
    for button in buttons:
        button.config(text="", state=NORMAL, bg="SystemButtonFace")

# Button to switch game mode
mode_button = Button(root, text="Switch Mode", command=switch_mode)
mode_button.grid(row=3, column=0, columnspan=3)

# Button to reset the game
reset_button = Button(root, text="Reset Game", command=reset)
reset_button.grid(row=4, column=0, columnspan=3)

# Grid the buttons
for i, button in enumerate(buttons):
    button.grid(row=i // 3, column=i % 3)

# Tkinter main loop
root.mainloop()

# Save Q-values to file
with open("q_values.pkl", "wb") as f:
    pickle.dump(q_values, f)
