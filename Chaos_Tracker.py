# Written March 28, 2024 for a friend's D&D Campaign
# Updated March 30, 2024 to have save backups, and be able to edit config settings and save file



import tkinter as tk
import tkinter.messagebox
import random
import shutil
from datetime import datetime



# A function to handle the "+" button click
def increase_chaos(row):
    chaos_values[row] += 1
    update_chaos_label(row)

    # Prompts saving the changed data to the save data text file
    save_data()

# A function to handle the "-" button click
def decrease_chaos(row):
    if chaos_values[row] > 0:
        chaos_values[row] -= 1
        update_chaos_label(row)

        # Prompts saving the changed data to the save data text file
        save_data()

# A function to update the chaos label for its own row
def update_chaos_label(row):
    label_chaos[row].config(text=f"Chaos Value = {chaos_values[row]}")

# A function to handle the 'Reset' button being clicked
def reset_chaos():
    # Displays a message popup asking for confirmation
    confirmed = tkinter.messagebox.askyesno("Reset Confirmation", "Are you sure you want to reset?")

    # If the user confirms the reset
    if confirmed:
        # Create a formatted date string to make unique backup filenames
        date_str = datetime.now().strftime("%m.%d.%Y %H.%M.%S")

        # Copies the current chaos values file to a backup text file with the date and time appended
        shutil.copyfile("Chaos Values.txt", f"Chaos Values (Backup) {date_str}.txt")

        # Resets the chaos values
        for row in range(len(chaos_values)):
            chaos_values[row] = 0
            update_chaos_label(row)

        # Shows a message confirming a backup has been made
        tkinter.messagebox.showinfo("Backup Created", "A backup of previous values has been made in the directory. \n\nJust in case. :) \n\n(you will need to manually restore the data)")

        # Prompts saving the changed data to the save data text file
        save_data()

# Saves the data to the main text file on request
def save_data():
    data_to_save = []

    # Iterates through both names and chaos values, and appends them to the list save data list
    for name, value in zip(names, chaos_values):
        data_to_save.append(f"{name} {value}")

    # Adds empty lines for text file readability
    data_to_save.extend(["", "", ""])

    # Appends both the threshold interval and chaos modifier values
    data_to_save.append(f"Threshold_Interval {threshold_interval}")
    data_to_save.append(f"Chaos_Modifier {chaos_modifier}")

    # Joins together and then writes the newly built data to the text file
    with open("Chaos Values.txt", "w") as file:
        file.write("\n".join(data_to_save))

# A function to handle the 'Roll' button being clicked
def roll_dice(row, name):
    # Generates dice rolls
    d20_result = random.randint(1, 20)
    d10_result = random.randint(1, 10)

    # Sets the 'additional chaos' for each interval of 20 a player has
    additional_chaos = (chaos_values[row] // threshold_interval) * chaos_modifier

     # Checks if the d20 is less than the d10 + it's chaos modifier
    if d20_result < (d10_result + additional_chaos):
        # Gets the difference between the two
        difference = (d10_result + additional_chaos) - d20_result

        # Updates that player's chaos value internally
        chaos_values[row] += difference

        # Updates the displayed chaos value for the player (why is this and the above not pointing to the same variable? oh well)
        update_chaos_label(row)

        # Displays below the difference in the dice rolls, if any
        label_difference.config(text=f"Chaos Gained: {difference}")

        # Prompts saving the changed data to the save data text file
        save_data()

    # If the d20 in equal to or greater than the d10 + chaos modifier, nothing changes
    else:
        label_difference.config(text=f"Chaos Gained: 0")



    # Updates the "Rolled for..." label
    label_name_roll.config(text=f"Rolled for {name}")

    # Updates the dice outcome labels
    label_d20.config(text=f"Hope Roll: {d20_result}")
    if additional_chaos == 0:
        label_d10.config(text=f"Chaos Roll: {d10_result}")
    else:
        label_d10.config(text=f"Chaos Roll: {d10_result} + {additional_chaos}")



# Creates and sets the main application window
window = tk.Tk()

# Sets the title of the window
window.title("Chaos Tracker")

# Sets the size of the window
window.geometry("350x500")

# Sets the background color
background_color = "#c8c8c8"

# Set the background color of the root window
window.configure(bg=background_color)

# Prevents resizing of the window
window.resizable(False, False)

# Load the image
#icon_image = tk.PhotoImage(file="background-window.png")

# Set the window icon
#window.iconphoto(True, icon_image)



# Loads the background image
#background_image = tk.PhotoImage(file="image.png")

# Creates a label with the background image
#background_label = tk.Label(window, image=background_image)
#background_label.place(x=-50, y=100)



# Readies the list of names
names = []

# Readies the list of chaos values
chaos_values = []

# Opens the file in read mode
with open("Chaos Values.txt", "r") as file:
    # Reads the lines of the file into a list
    chaos_values_data = file.readlines()

    # Iterates through the text file's lines
    for line in chaos_values_data:
        if len(line) < 2:  # Skips empty lines 9used in the config file for readability)
            print(line)
            pass

        # Lines with characters
        else:
            split_lines = line.split()

            # Catches the threshold interval value
            if split_lines[0] == "Threshold_Interval":
                threshold_interval = int(split_lines[1])

            # Catches the chaos modifier value
            elif split_lines[0] == "Chaos_Modifier":
                chaos_modifier = int(split_lines[1])

            # Otherwise catches the player names and their respective chaos values
            else:
                names.append(split_lines[0])
                chaos_values.append(int(split_lines[1]))



# Sets lists to store the labels and buttons for each row
label_chaos = []
button_plus_minus = []
button_roll = []



# Creates labels in the style of buttons for each name with, - and + buttons to the right of them, then a Roll button
for i, name in enumerate(names):
    # Creates a frame to hold the label, buttons, the "Chaos Value" text, and the Roll button
    frame = tk.Frame(window, bg=background_color)
    frame.pack(fill=tk.X, pady=5)

    # Creates the label styled like a button for the name
    label_name = tk.Label(frame, text=name, relief=tk.RAISED, padx=10, pady=5, borderwidth=2, width=6)
    label_name.pack(side=tk.LEFT, padx=(10, 5))  # Adjust the padding here

    # Creates the "-" button
    button_minus = tk.Button(frame, text="-", command=lambda row=i: decrease_chaos(row), width=2)
    button_minus.pack(side=tk.LEFT, padx=(5, 2))

    # Creates the "+" button
    button_plus = tk.Button(frame, text="+", command=lambda row=i: increase_chaos(row), width=2)
    button_plus.pack(side=tk.LEFT, padx=(2, 5))

    # Creates the label for "Chaos Value" text
    label_chaos.append(tk.Label(frame, text=f"Chaos Value = {chaos_values[i]}"))
    label_chaos[-1].pack(side=tk.LEFT, padx=10)

    # Creates the "Roll" button
    button_roll.append(tk.Button(frame, text="Roll", command=lambda row=i, name=name: roll_dice(row, name)))
    button_roll[-1].pack(side=tk.LEFT, padx=(5, 10))



# Creates a frame to hold the D20 and D10 display results
frame_dice = tk.Frame(window, borderwidth=2, relief=tk.GROOVE)
frame_dice.pack(pady=20, padx=20, anchor=tk.W)

# Creates labels to display the outcome of the dice rolls within the frame
label_name_roll = tk.Label(frame_dice, text="Waiting for a dice roll!")
label_name_roll.pack()

# The 'Hope' dice roll outcome
label_d20 = tk.Label(frame_dice, text="Hope Roll: ")
label_d20.pack()

# The 'Chaos' dice roll outcome
label_d10 = tk.Label(frame_dice, text="Chaos Roll: ")
label_d10.pack()

# Shows the difference between the two (the chaos now gained)
label_difference = tk.Label(frame_dice, text="Chaos Gained: ")
label_difference.pack()

# Creates a frame to hold the 'Reset' button
frame_reset = tk.Frame(window)
frame_reset.pack(pady=10, padx=20, anchor=tk.W)

# Creates the 'Reset' button within the frame
button_reset = tk.Button(frame_reset, text="RESET", command=reset_chaos, bg="red", fg="black")
button_reset.pack()



# Finally starts the Tkinter main loop
window.mainloop()