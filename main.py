import json
import random
from tkinter import *
from tkinter import messagebox

import pyperclip

# ---------------------------- CONSTANTS ------------------------------- #
FONT = ("Calibri", 10, "normal")


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = [random.choice(letters) for _ in range(0, nr_letters)]
    password_list += [random.choice(symbols) for _ in range(0, nr_symbols)]
    password_list += [random.choice(numbers) for _ in range(0, nr_numbers)]

    random.shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)
    messagebox.showinfo(title="Copied", message="Your password has been copied")


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }
    if website == "" or password == "":
        messagebox.showwarning(title="WARNING", message="You didn't enter everything")
        is_ok = False
    else:
        is_ok = messagebox.askokcancel(title=website,
                                       message=f"""These are the details entered:\n
                                       Website:{website}\n
                                       Email: {email}\n
                                       Password:{password}\n
                                       Is it OK to save?""")
    if is_ok:
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            data.update(new_data)
            with open("data.json", "w") as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- SEARCH JSON ----------------------------- #
# Search engine
def search_book():
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showwarning(title="NO DATA", message="There's no data")
    else:
        search_entry = website_entry.get()
        if search_entry in data:
            messagebox.showinfo(title="Search results",
                                message=f"Website: {search_entry}\n Password: {data[search_entry]['password']}\n")
        else:
            messagebox.showinfo(title="No results",
                                message=f"""There is no website: {search_entry}\n""")


# ---------------------------- UI SETUP ------------------------------- #
# Window
window = Tk()
window.title("Password Manager")
window.config(bg="white", padx=50, pady=50)

# Canvas
canvas = Canvas(width=200, height=200, bg="white", highlightthickness=0)
lock_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=lock_img)
canvas.grid(column=1, row=0)

# Labels
website_label = Label(text="Website:", font=FONT, bg="white")
website_label.grid(column=0, row=1)
email_label = Label(text="Email/username:", font=FONT, bg="white")
email_label.grid(column=0, row=2)
password_label = Label(text="Password:", font=FONT, bg="white")
password_label.grid(column=0, row=3)

# Entries
website_entry = Entry(width=34)
website_entry.grid(column=1, row=1, columnspan=1)
website_entry.focus()
email_entry = Entry(width=52)
email_entry.insert(0, "jarema.piekutowski@gmail.com")
email_entry.grid(column=1, row=2, columnspan=2)
password_entry = Entry(width=34)
password_entry.insert(0, "")
password_entry.grid(column=1, row=3)

# Buttons

search_button = Button(text="Search", bg="white", bd=1, width=14, command=search_book)
search_button.grid(column=2, row=1)

password_button = Button(text="Generate password", bg="white", bd=1, command=generate_password)
password_button.grid(column=2, row=3)

add_button = Button(text="Add", anchor="center", width=44, bg="white", command=save_password)
add_button.grid(column=1, row=4, columnspan=2)

window.mainloop()
