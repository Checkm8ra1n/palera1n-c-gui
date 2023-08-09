import tkinter as tk
from tkinter import messagebox
import subprocess
import threading

def show_additional_options():
    additional_window = tk.Toplevel(root)
    additional_window.title("Opzioni Aggiuntive")

    sub_option_var = tk.StringVar(value="Boot")  # Impostato su "Boot" di default

    sub_options = ["Boot", "Create FakeFS", "Create BindFS", "Safe mode", "Verbose", "Sistema USB"]
    for sub_option in sub_options:
        sub_option_button = tk.Radiobutton(additional_window, text=sub_option, variable=sub_option_var, value=sub_option)
        sub_option_button.pack()

    confirm_button = tk.Button(additional_window, text="Conferma", command=lambda: start_command_thread(sub_option_var.get()))
    confirm_button.pack(pady=10)

def show_additional_options_rootless():
    additional_window = tk.Toplevel(root)
    additional_window.title("Opzioni Aggiuntive Rootless")

    sub_option_var = tk.StringVar(value="Safe mode")  # Impostato su "Safe mode" di default

    sub_options = ["Safe mode", "Verbose", "Boot", "Restore"]
    for sub_option in sub_options:
        sub_option_button = tk.Radiobutton(additional_window, text=sub_option, variable=sub_option_var, value=sub_option)
        sub_option_button.pack()

    confirm_button = tk.Button(additional_window, text="Conferma", command=lambda: start_command_thread_rootless(sub_option_var.get()))
    confirm_button.pack(pady=10)

def option_selected(selected_option):
    if selected_option == "Boot":
        messagebox.showinfo("Esecuzione Comando", "Comando 'palera1n -f' eseguito con successo.")
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
        command = "palera1n -l -s"
        if verbose_var.get():
            command += " -v"
        run_custom_command(command)
    elif selected_option == "Sistema USB":
        show_usb_commands()
    elif selected_option:
        messagebox.showinfo("Scelta", f"Hai selezionato 'rootful' con opzione '{selected_option}'")
    else:
        messagebox.showerror("Errore", "Seleziona una sottopzione")

def show_usb_commands():
    try:
        subprocess.Popen(["pkexec", "systemctl", "stop", "usbmuxd"])
        subprocess.Popen(["pkexec", "usbmuxd", "-f", "-p"])
    except Exception as e:
        messagebox.showerror("Errore", f"Errore nell'eseguire i comandi: {str(e)}")

def run_custom_command(command):
    try:
        if command:
            subprocess.run(command.split())
            root.after(1000, check_command_completion)  # Controlla lo stato ogni secondo
    except Exception as e:
        messagebox.showerror("Errore", f"Errore nell'avviare il comando: {str(e)}")

def start_command_thread(selected_option):
    if selected_option in ["Boot", "Create FakeFS", "Create BindFS", "Safe mode", "Sistema USB", "Verbose"]:
        messagebox.showinfo("Esecuzione in Corso", "Esecuzione in corso...")
        if selected_option in ["Create FakeFS", "Create BindFS", "Safe mode"]:
            run_command_with_verbose(selected_option)
        else:
            if selected_option == "Sistema USB":
                show_usb_commands()
            else:
                command = get_command(selected_option)
                run_custom_command(command)
    else:
        option_selected(selected_option)

def start_command_thread_rootless(selected_option):
    if selected_option in ["Safe mode", "Verbose", "Boot", "Restore"]:
        messagebox.showinfo("Esecuzione in Corso", "Esecuzione in corso...")
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
        return "palera1n -l -s"
    elif selected_option == "Sistema USB":
        return ""
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
            messagebox.showinfo("Completato", "Operazione completata.")
        else:
            root.after(1000, check_command_completion)
    except Exception as e:
        messagebox.showerror("Errore", f"Errore nel controllare lo stato del processo: {str(e)}")

# Creazione della finestra principale
root = tk.Tk()
root.title("Scelta del Tipo")

verbose_var = tk.BooleanVar()

# Etichetta di istruzioni
label = tk.Label(root, text="Seleziona una delle seguenti opzioni:")
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

