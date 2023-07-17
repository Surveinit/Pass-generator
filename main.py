import json
import random
from tkinter import *
from tkinter import messagebox

# Define colors
BLUE = "#525FE1"
TEAL = "#22A699"
RED = "#F24C3D"
DARK_TEAL = "#001e1b"


# ---------------------------- PASSWORD FINDER ------------------------------- #

def find_password():
    find = input_web.get()

    try:
        with open("data.json", mode="r") as file:
            # Read the contents of the file
            json_data = file.read()

            # Parse the JSON data
            data = json.loads(json_data)

            # Access the "website" object using dot notation
            website = data[find.lower()]
            username = website['username']
            password = website['password']

            # print(website)
            messagebox.showinfo(title=find, message=f"U :   {username} \nP :   {password} \n "
                                                    f"\nPress OK to copy password")

            # Automatically allows you to copy password to your clipboard
            window.clipboard_clear()
            window.clipboard_append(password)

    except KeyError:
        messagebox.showwarning(title="Oops", message=f"{find} doesn't exist! \nType carefully")

    except FileNotFoundError:
        messagebox.showerror(title="Oops", message=f"File is missing!")


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def pass_gen():
    letter_small = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
                    's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

    letter_capital = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
                      'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    symbols = ['!', '@', '#', '$', '%', '&', '*', '(', ')', '+', '-', '=', '[', ']', '{', '}', ';', ':', '<', '>', '.',
               ',', '?', '/', '|', '_', '~']

    numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    set1 = f"{random.choice(letter_small)}{random.choice(letter_capital)}{random.choice(symbols)}{random.choice(numbers)}"
    set2 = f"{random.choice(letter_capital)}{random.choice(symbols)}{random.choice(letter_small)}{random.choice(symbols)}"
    set3 = f"{random.choice(numbers)}{random.choice(letter_capital)}{random.choice(symbols)}{random.choice(letter_small)}"
    set4 = f"{random.choice(letter_small)}{random.choice(letter_capital)}{random.choice(symbols)}{random.choice(numbers)}"

    gen_password = set1 + set2 + set3 + set4
    gen_password_list = list(gen_password)  # Convert the string to a list
    random.shuffle(gen_password_list)  # Shuffle the list
    gen_password = ''.join(gen_password_list)  # Convert back to string
    input_pass.delete(0, 'end')
    input_pass.insert(0, gen_password)

    # Automatically allows you to copy password to your clipboard
    window.clipboard_clear()
    window.clipboard_append(gen_password)


# ---------------------------- SAVE PASSWORD ------------------------------- #

def save():
    website = input_web.get()
    username = input_usr.get()
    password = input_pass.get()

    new_data = {website.lower(): {
        "username": username,
        "password": password
    }}

    if len(website) == 0 or len(username) == 0 or len(password) == 0:
        messagebox.showerror(title="Dummy!", message="You just kept your fields empty!")

    else:
        is_ok = messagebox.askokcancel(title=website, message=f"Username:  {username} \nPassword:  {password} "
                                                              f"\nIs it OK to save?")

        if is_ok is True:
            try:
                with open("data.json", mode="r") as file:
                    # Reading old data
                    json_data = file.read()
                    if not json_data:
                        data = {}  # Empty dictionary when file is empty
                    else:
                        data = json.loads(json_data)

            except FileNotFoundError:
                with open("data.json", mode="w") as file:
                    # file.write(f"{website} | {username} | {password} \n")
                    json.dump(new_data, file, indent=4)

            else:
                # Updating old data with new one
                data.update(new_data)

                with open("data.json", mode="w") as file:
                    # file.write(f"{website} | {username} | {password} \n")
                    json.dump(data, file, indent=4)

            finally:
                input_web.delete(0, 'end')
                input_pass.delete(0, 'end')


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pass-gen")
window.config(padx=20, pady=20, bg=TEAL)

canvas = Canvas(window, width=200, height=200, bg=TEAL, highlightthickness=0)
logo_img = PhotoImage(file="logo2.png")
canvas.create_image(100, 112, image=logo_img)
canvas.grid()

# --------WEBSITE--------- #
label_web = Label(text="website:", bg=TEAL, fg=DARK_TEAL, font=("arial", 12, "bold"))
label_web.grid(column=0, row=1)

input_web = Entry(width=20)
input_web.focus()
input_web.grid(column=1, row=1, columnspan=2, sticky="EW")

# Search
button_search = Button(command=find_password, text="SEARCH",
                       bg="#ffffff",
                       font=("arial", 8))
button_search.grid(column=2, row=1, sticky="EW")

# --------USERNAME--------- #
label_usr = Label(text="username:", bg=TEAL, fg=DARK_TEAL, font=("arial", 12, "bold"))
label_usr.grid(column=0, row=2)

input_usr = Entry(width=35)
input_usr.grid(column=1, row=2, columnspan=2, sticky="EW")

# --------PASSWORD--------- #
label_pass = Label(text="password:", bg=TEAL, fg=DARK_TEAL, font=("arial", 12, "bold"))
label_pass.grid(column=0, row=3)

input_pass = Entry(width=20)
input_pass.grid(column=1, row=3, sticky="EW")

button_generate = Button(command=pass_gen, text="GENERATE",
                         bg="#ffffff",
                         font=("arial", 8))
button_generate.grid(column=2, row=3, sticky="EW")

# --------ADD--------- #
button_add = Button(command=save, text="ADD",
                    bg="#ffffff",
                    font=("arial", 8),
                    width=35)
button_add.grid(column=1, row=6, columnspan=2, sticky="EW")

window.mainloop()
