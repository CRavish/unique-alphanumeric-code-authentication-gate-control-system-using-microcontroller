import tkinter as tk
from tkinter import ttk
import serial
from serial_communication import send_to_arduino_slave, read_from_arduino
import time

root = tk.Tk()
root.title("SLAVE 2")
root.geometry('600x500')
root.configure(bg="#000055")
root.resizable(False, False)

SLAVE1_PORT = 'COM7'
slave_ser = serial.Serial(SLAVE1_PORT, 9600)

def get_response():
    start_time = time.time()

    while (slave_ser.inWaiting() == 0):
        if time.time() - start_time > 3:
            return "Your Gate Code is Wrong Try Again !!"

    result = read_from_arduino(slave_ser)

    return result

def submit_token():
    result_label.configure(text="")
    submit_button.configure(state="disabled")
    send_to_arduino_slave(token_entry.get(), slave_ser)

    token_entry.delete(0, tk.END)

    result = get_response()
    result_label.configure(text=result, font=("Helvetica", 16), foreground="red")
    
    submit_button.configure(state="active")

ttk.Label(root).pack()

style = ttk.Style()

# Configure a custom style with a light blue background
style.configure("LightBlue.TLabel", background="light blue")

# Create a Label widget with the custom style
heading_label = ttk.Label(root, text="Gate number 2 - Mannar", font=("Helvetica", 30), style="LightBlue.TLabel")
heading_label.pack(pady=20)

token_label = ttk.Label(root, text="Enter your gate Key",font=("Helvetica", 20),style="LightBlue.TLabel")
token_label.pack(pady=2)
style.configure("TEntry", padding=(20, 10))

token_entry = ttk.Entry(root, width=60)
token_entry.pack(pady=10)

# ttk.Label(root).pack()

# Increase the size of the "Submit" button and set color and font
style.configure("Custom.TButton", font=("Helvetica", 18), margin=(20, 0), padding=(20, 10), background="blue", foreground="red")

submit_button = ttk.Button(root, text='Submit', command=lambda:submit_token(), style="Custom.TButton")
submit_button.pack()

result_label = ttk.Label(root, text="")
result_label.pack(side='bottom', pady='15')

root.mainloop()
