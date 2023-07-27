import csv
import hashlib
import random
import string
from os.path import isfile
from tkinter import *
from tkinter import ttk, messagebox


def password_generator(length=10, letters=True, numbers=True, symbols=True):
    allowed = ''

    if letters:
        allowed += string.ascii_letters
    if numbers:
        allowed += string.digits
    if symbols:
        allowed += string.punctuation

    if length < 1:
        messagebox.showerror("Error", "Password length must be positive!")
        return ''
    elif len(allowed) < 1:
        messagebox.showerror("Error", "You must allow at least one type of character!")
        return ''

    password = ''.join(random.choice(allowed) for i in range(length))
    return password


def create_password():
    
    try:
        length = int(lengthInput.get())
    except Exception:
        length = 10
        
    letters = lettersVar.get()
    numbers = numbersVar.get()
    symbols = symbolsVar.get()
    password = password_generator(length, letters, numbers, symbols)
    
    # Clear the field
    passwordOutput.delete(0, END)
    # Insert the new password in the field
    passwordOutput.insert(0,password)


def copy_password():
    password = passwordOutput.get()
    root.clipboard_clear()
    root.clipboard_append(password)

    # If the password is copied, it means the user probably used it, so we store it's hash
    # and do not allow the application to generate the same password again

    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    if isfile('passwords.csv'):
        with open('passwords.csv', 'r') as file:
            reader = csv.reader(file)
            if hashed_password in list(reader)[0]:
                messagebox.showinfo("Info", "The password already exists, generating a new one.")
                create_password()
                return

    with open('passwords.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([hashed_password])


# __________________________________GUI stuff, will not be enhanced any further_________________________________________
root = Tk()

window_width = 375
window_height = 225 
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

position_top = int(screen_height / 2 - window_height / 2)
position_right = int(screen_width / 2 - window_width / 2)

root.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

root.title("Password Generator")

lengthLabel = Label(root, text="Password length:")
lengthLabel.grid(row=0, column=0, padx=10, pady=10)
lengthInput = ttk.Entry(root)
lengthInput.grid(row=0, column=1, padx=10, pady=10)
lengthInput.focus()

lettersVar = BooleanVar(value=True)
lettersCheck = Checkbutton(root, text="Letters", variable=lettersVar)
lettersCheck.grid(row=1, column=0, padx=10, pady=10)

numbersVar = BooleanVar(value=True)
numbersCheck = Checkbutton(root, text="Numbers", variable=numbersVar)
numbersCheck.grid(row=1, column=1, padx=10, pady=10)

symbolsVar = BooleanVar(value=True)
symbolsCheck = Checkbutton(root, text="Symbols", variable=symbolsVar)
symbolsCheck.grid(row=1, column=2, padx=10, pady=10)

generateButton = ttk.Button(root, text="Generate Password", command=create_password)
generateButton.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

passwordOutput = ttk.Entry(root)
passwordOutput.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

copyButton = ttk.Button(root, text="Copy Password", command=copy_password)
copyButton.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

root.mainloop()
