import tkinter as tk
from tkinter import messagebox
import subprocess
import threading

def show_additional_options():
    additional_window = tk.Toplevel(root)
    additional_window.title("Other options")

    sub_option_var = tk.StringVar(value="Boot")  # Impostato su "Boot" di default

    sub_options = ["Boot", "Create FakeFS", "Create BindFS", "Safe mode", "Verbose", "Fix USB"]
    for sub_option in sub_options:
        sub_option_button = tk.Radiobutton(additional_window, text=sub_option, variable=sub_option_var, value=sub_option)
        sub_option_button.pack()

    confirm_button = tk.Button(additional_window, text="Confirm", command=lambda: start_command_thread(sub_option_var.get()))
    confirm_button.pack(pady=10)

def show_additional_options_rootless():
    additional_window = tk.Toplevel(root)
    additional_window.title("Other options rootless")

    sub_option_var = tk.StringVar(value="Safe mode")  # Impostato su "Safe mode" di default

    sub_options = ["Safe mode", "Verbose", "Boot", "Restore"]
    for sub_option in sub_options:
        sub_option_button = tk.Radiobutton(additional_window, text=sub_option, variable=sub_option_var, value=sub_option)
        sub_option_button.pack()

    confirm_button = tk.Button(additional_window, text="Confirm", command=lambda: start_command_thread_rootless(sub_option_var.get()))
    confirm_button.pack(pady=10)

def option_selected(selected_option):
    if selected_option == "Boot":
        messagebox.showinfo("Executing Command", "Command 'palera1n -f'executed succeffuly.")
    elif selected_option == "Create FakeFS":
        command = "palera1n -f -c"
        if verbose_var.get():
            command += " -v"
        run_custom_command(command)
    elif selected_option == "Create BindFS":
        command = "palera1n -f -B"
        if verbose_var.get():
            command += " -v"
        run_custom_command(command)
    elif selected_option == "Safe mode":
        command = "palera1n -f -s"
        if verbose_var.get():
            command += " -v"
        run_custom_command(command)
    elif selected_option:
        messagebox.showinfo("Scelection", f"You have selected 'rootful' with '{selected_option}'") option
    else:
        messagebox.showerror("Error", "Select an option")

def show_usb_commands():
    try:
        subprocess.Popen(["pkexec", "systemctl", "stop", "usbmuxd"])
        subprocess.Popen(["pkexec", "usbmuxd", "-f", "-p"])
    except Exception as e:
        messagebox.showerror("Error" : {str(e)}")

def run_custom_command(command):
    try:
        if command:
            subprocess.run(command.split())
            root.after(1000, check_command_completion)  # Controlla lo stato ogni secondo
    except Exception as e:
        messagebox.showerror("Error", f"Error with starting the command: {str(e)}")

def start_command_thread(selected_option):
    if selected_option in ["Boot", "Create FakeFS", "Create BindFS", "Safe mode", "Sistema USB", "Verbose"]:
        messagebox.showinfo("Executing", "Execunting...")
        if selected_option in ["Create FakeFS", "Create BindFS", "Safe mode"]:
            run_command_with_verbose(selected_option)
        else:
            if selected_option == "FixUSB":
                show_usb_commands()
            else:
                command = get_command(selected_option)
                run_custom_command(command)
    else:
        option_selected(selected_option)

def start_command_thread_rootless(selected_option):
    if selected_option in ["Safe mode", "Verbose", "Boot", "Restore"]:
        messagebox.showinfo("Executing", "Executing...")
        run_command_with_verbose_rootless(selected_option)
    else:
        option_selected(selected_option)

def run_command_with_verbose(selected_option):
    command = get_command(selected_option)
    if verbose_var.get():
        command += " -v"
    run_custom_command(command)

def run_command_with_verbose_rootless(selected_option):
    command = get_command_rootless(selected_option)
    if verbose_var.get():
        command += " -v"
    run_custom_command(command)

def get_command(selected_option):
    if selected_option == "Boot":
        return "palera1n -f"
    elif selected_option == "Create FakeFS":
        return "palera1n -f -c"
    elif selected_option == "Create BindFS":
        return "palera1n -f -B"
    elif selected_option == "Safe mode":
        return "palera1n -f -s"
    elif selected_option == "Restore":
        return "palera1n -f --force-revert"
    elif selected_option == "Verbose":
        return ""

def get_command_rootless(selected_option):
    if selected_option == "Safe mode":
        return "palera1n -l -s"
    elif selected_option == "Boot":
        return "palera1n -l"
    elif selected_option == "Restore":
        return "palera1n -l --force-revert"
    elif selected_option == "Verbose":
        return ""

def check_command_completion():
    try:
        result = subprocess.run(["ps", "-C", "palera1n"], stdout=subprocess.PIPE)
        if result.returncode != 0:  # Il processo non è attivo
            messagebox.showinfo("Completed", "Operation completed.")
        else:
            root.after(1000, check_command_completion)
    except Exception as e:
        messagebox.showerror("Error", f"Error while checking the process state: {str(e)}")

# Creazione della finestra principale
root = tk.Tk()
root.title("Selection of the type")

verbose_var = tk.BooleanVar()

# Etichetta di istruzioni
label = tk.Label(root, text="Select an option:")
label.pack(pady=10)

# Opzione "rootful"
rootful_button = tk.Button(root, text="Rootful", command=show_additional_options)
rootful_button.pack()

# Opzione "rootless"
rootless_button = tk.Button(root, text="Rootless", command=show_additional_options_rootless)
rootless_button.pack()

# Opzione "Sistema USB"
usb_button = tk.Button(root, text="Sistema USB", command=show_usb_commands)
usb_button.pack()

# Avvio della loop principale
root.mainloop()

