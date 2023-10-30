import tkinter as tk
from tkinter import ttk
import serial
from PIL import Image, ImageTk  # Import Image and ImageTk from the PIL library
from serial_communication import send_to_arduino, read_from_arduino



def main():
    root = tk.Tk()
    root.title('MASTER')
    root.geometry('1000x800')
    root.resizable(False, False)

    MASTER_PORT = 'COM7'
    master_ser = serial.Serial(MASTER_PORT, 115200)

    # Load the background image and resize it to 700x400
    background_image = Image.open('C:/Users/chamod/OneDrive/Desktop/8th sem/task04/final/GUI/IMAGE/railway.png')
    background_image = background_image.resize((1000, 650), Image.LANCZOS)  # Use ANTIALIAS for resampling
    background_image = ImageTk.PhotoImage(background_image)

    # Create a label widget to display the background image
    background_label = tk.Label(root, image=background_image)
    background_label.place(relx=0.5, rely=0.5, anchor='center')  # Center the image

    key_var = tk.StringVar()
    gate_number = tk.StringVar()

    # Create a ttk Style object
    style = ttk.Style()
    # Set the background color (highlight background) to light blue
    style.configure("LightBlue.TLabel", background="light blue")

    title_label = ttk.Label(root, text='Welcome to the Sri Lanka Railway Passenger Registration', font=("Helvetica", 22, "bold"), style="LightBlue.TLabel")
    title_label.place(relx=0.8, rely=0.1, anchor='center')  # Center the label

    title_label.pack(side='top', pady='40')


    def copy_label_value():
        label_text = key_var.get()
        root.clipboard_clear()
        root.clipboard_append(label_text)
        root.update()
        key_var.set("Copied")
        root.after(1000, reset_func)

    def reset_func():
        key_var.set("")
        reg_btn.configure(state="active")
        
    token_var = tk.StringVar()
    token_var.set("")

    def generate_token():

        global newtoken
        if gate_number.get():
            send_to_arduino(gate_number.get(), master_ser)
            while master_ser.inWaiting() == 0:
                pass
            token = read_from_arduino(master_ser)
            print(token)
            newtoken = token
            key_var.set(token)
            token_var.set("Your Gate Key is :- " + newtoken)  # Update the label 
        

    ttk.Label(root).pack()
    style = ttk.Style()

    # Set the background color (highlight background) for the label to light green
    style.configure("LightGreen.TLabel", background="light green")

    # Set the background color (highlight background) for the entry to light pink
    style.configure("LightPink.TEntry", fieldbackground="light pink")

    # Create a frame to hold the "Name" label and entry
    name_frame = ttk.Frame(root)
    name_frame.pack(side='top', pady=10)

    # Apply a style to the "Name" frame to set its background color to light blue
    style.configure("LightBlue.TFrame", background="light blue")
    name_frame.configure(style="LightBlue.TFrame")

    name_label = ttk.Label(name_frame, text='Name :- ', font=("Helvetica", 20), style="LightGreen.TLabel")
    name_entry = ttk.Entry(name_frame, font=("Helvetica", 16), style="LightPink.TEntry")

    # Use pack to place the "Name" label and entry in the same horizontal line inside the "Name" frame
    name_label.pack(side='left', padx=10)
    name_entry.pack(side='left', padx=10)

    # Create a frame to hold the "NIC" label and entry, and add spacing
    nic_frame = ttk.Frame(root)
    nic_frame.pack(side='top', pady=50)  # Adjust the pady value for spacing

    # Apply a style to the "NIC" frame to set its background color to light blue
    nic_frame.configure(style="LightBlue.TFrame")

    nic_label = ttk.Label(nic_frame, text='NIC :- ', font=("Helvetica", 20), style="LightGreen.TLabel")
    nic_entry = ttk.Entry(nic_frame, font=("Helvetica", 16), style="LightPink.TEntry")

    # Use pack to place the "NIC" label and entry in the same horizontal line inside the "NIC" frame
    nic_label.pack(side='left', padx=10)
    nic_entry.pack(side='left', padx=10)

    # Create a frame for the "Select Stage" (gate) section
    gate_frame = ttk.Frame(root)
    gate_frame.pack(side='top', pady=50)

    gate_label = ttk.Label(gate_frame, text='Select Stage', font=("Helvetica", 20), style="LightGreen.TLabel")

    style = ttk.Style()
    style.configure("Large.TRadiobutton", padding=(10, 10))  # Increase padding to increase size
    style.configure("LightBlue.TRadiobutton", background="light blue")
    

    style.configure("Large.TRadiobutton", padding=(10, 10), foreground="dark red")

    gate1 = ttk.Radiobutton(gate_frame, text=' Stage 1 for Jaffna  ', value='1', variable=gate_number, style="Large.TRadiobutton")
    gate2 = ttk.Radiobutton(gate_frame, text='Stage 2 for Mannar', value='2', variable=gate_number, style="Large.TRadiobutton")

    gate_label.pack()
    ttk.Label(gate_frame).pack()
    gate1.pack()
    gate2.pack()

    style.configure("DarkBlue.TButton", background="dark blue", foreground="red")
    # Create and configure the "Register" button with the custom style
    reg_btn = ttk.Button(root, text="Register", command=generate_token, style="DarkBlue.TButton")
    reg_btn.pack(ipadx=20, ipady=10)

    ttk.Label(root).pack()
    # token_label = ttk.Label(root, textvariable=token_var, foreground="red")
    # token_label.pack()
    
    token_label = ttk.Label(root, textvariable=token_var, foreground="blue", font=("Helvetica", 14, "bold"), style="LightBlue.TLabel")
    token_label.pack()
   

    root.mainloop()

if __name__ == "__main__":
    main()