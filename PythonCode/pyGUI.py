import tkinter as tk
import serial
import time

#Global Variables
maroon = "#800000"  # maroon
gold = "#B8860B"    # rustic gold
background_color = "#FAF3E0"  # Light beige
entry_background_color = "#FFE4C4"  # Light gold
center_frame = None
error_labels = []
pwm_label = None
error_frame = None
global time_entry
global cycles_entry
global duty_entry
global square_entry
root = tk.Tk()



#Logic Methods
def main_loop():
    clear_error_labels()
    clear_pwm_label()

    time_at_peak_value = time_entry.get()
    num_cycles_value = cycles_entry.get()
    duty_cycle_value = duty_entry.get()
    square_type_value = check_square_type(square_entry.get())

    error_tap = check_time_at_peak_entry(time_at_peak_value)
    error_cycles = check_num_cycles_entry(num_cycles_value)
    error_duty = check_duty_cycle_entry(duty_cycle_value)

    if error_duty and error_tap and error_cycles:
        ser = None
        try:
            ser = serial.Serial('COM3', 9600, timeout=2)
            time.sleep(2)

            send_to_arduino(ser, time_at_peak_value, num_cycles_value, duty_cycle_value, square_type_value)
            set_pwm_label("Generated a " + square_type_value + " PWM wave with: \n" + time_at_peak_value + " ms time at peak\n" + num_cycles_value + " cycles\n" + duty_cycle_value + "% duty cycle on")

        except serial.SerialException as e:
            set_pwm_label("Unable to Connect to Arduino")
        finally:
            if ser is not None and ser.is_open:
                ser.close()
def send_to_arduino(ser, time_at_peak_value, num_cycles_value, duty_cycle_value, square_type_value):
    data = f"{time_at_peak_value},{num_cycles_value},{duty_cycle_value},{square_type_value}\n"
    ser.write(data.encode('utf-8'))
def is_number(number,canFloat):
    number = number.strip()
    if number.startswith('0') and number not in ['0', '0.0'] and not number.startswith('0.'):
        return False
    if canFloat:
        try:
            float(number)
        except ValueError:
            try:
                int(number)
            except ValueError:
                return False

    if not canFloat:
        try:
            int(number)
        except ValueError:
            return False

    return True
def check_time_at_peak_entry(time_at_peak_value):
    if not is_number(time_at_peak_value,True):
        set_error_label("time", "Non-integer/float input for time at peak entry.")
        return False
    elif float(time_at_peak_value) > 60000 or float(time_at_peak_value) < 1:
        set_error_label("time", "Integer input for time at peak is incorrect. Enter a number 1 - 60000.")
        return False
    return True
def check_num_cycles_entry(num_cycles_value,):
    if not is_number(num_cycles_value,False): #cant be a float
        set_error_label("cycle", "Non-integer input for number of cycles entry.")
        return False
    elif int(num_cycles_value) > 60000 or int(num_cycles_value) < 1:
        set_error_label("time", "Integer input for time at peak is incorrect. Enter a number 1 - 60000.")
        return False
    return True
def check_duty_cycle_entry(duty_cycle_value):
    if not is_number(duty_cycle_value,True):
        set_error_label("duty", "Non-integer input for duty cycle entry.")
        return False
    elif float(duty_cycle_value) > 100 or float(duty_cycle_value) < 0:
        set_error_label("duty", "Must input a percentage between 0 and 100 for duty cycle.")
        return False
    return True
def check_square_type(square_type):
    if square_type == 1 and isinstance(square_type,int):
        return "negative"
    elif square_type == 0 and isinstance(square_type,int):
        return "positive"
    else:
        return "unknown"



#GUI Methods
def setup_GUI():
    global error_frame
    global time_entry
    global cycles_entry
    global duty_entry
    global square_entry
    # Configure the root
    root.minsize(718, 500)
    root.title("PWM Generator")
    root.configure(bg=background_color)
    center_window(root, 718, 500)

    # Create a frame to hold entry boxes
    top_frame = tk.Frame(root, bg=background_color)
    top_frame.pack(pady=30)

    # Time at Peak Label
    tk.Label(top_frame, text="Time at Peak (ms)", font=("Arial", 14, "bold"), bg=background_color, fg=maroon).grid(row=0, column=0, padx=10, pady=10, sticky='e')
    time_entry = tk.Entry(top_frame, font=("Arial", 14), width=30, bg=entry_background_color, fg=maroon, bd=2,relief="groove")
    time_entry.grid(row=0, column=1, padx=10, pady=10)

    # Number of Cycles Label
    tk.Label(top_frame, text="Number of Cycles", font=("Arial", 14, "bold"), bg=background_color, fg=maroon).grid(row=1,column=0,padx=10,pady=10,sticky='e')
    cycles_entry = tk.Entry(top_frame, font=("Arial", 14), width=30, bg=entry_background_color, fg=maroon, bd=2,relief="groove")
    cycles_entry.grid(row=1, column=1, padx=10, pady=10)

    # Duty Cycle Label
    tk.Label(top_frame, text="Duty Cycle (% on)", font=("Arial", 14, "bold"), bg=background_color, fg=maroon).grid(row=2, column=0, padx=10, pady=10, sticky='e')
    duty_entry = tk.Entry(top_frame, font=("Arial", 14), width=30, bg=entry_background_color, fg=maroon, bd=2,relief="groove")
    duty_entry.grid(row=2, column=1, padx=10, pady=10)

    # Create a frame for the "Include Negative" Checkbox
    checkbox_frame = tk.Frame(root, bg=background_color)
    checkbox_frame.pack(pady=10)

    # "Include Negative" Checkbox
    square_entry = tk.IntVar(value=1)
    include_checkbox = tk.Checkbutton(checkbox_frame, text="Include Negative", variable=square_entry,
                                      font=("Arial", 14, "bold"), bg=background_color, fg=maroon,
                                      activebackground=entry_background_color, activeforeground=maroon,
                                      selectcolor=entry_background_color, onvalue=1, offvalue=0, padx=10, pady=0,
                                      bd=0)
    include_checkbox.pack()

    # Create a frame for "Generate PWM" button and "Close" button
    button_frame = tk.Frame(root, bg=background_color)
    button_frame.pack(pady=10)

    # "Generate PWM" Button
    pwm_button = tk.Button(button_frame, text="Generate PWM", command=main_loop, font=("Arial", 12, "bold"),
                           bg=maroon, fg="white", activebackground=gold, activeforeground=maroon, bd=2,
                           relief="raised", padx=10, pady=5)
    pwm_button.pack(side="left", padx=10)

    # "Close" Button
    close_button = tk.Button(button_frame, text="Close", font=("Arial", 12, "bold"), bg=maroon, fg="white",
                             activebackground=gold, activeforeground=maroon, bd=2, relief="raised", padx=10, pady=5,
                             command=root.destroy)  # Command to close the application
    close_button.pack(side="left", padx=10)

    # Create a frame to hold outputted text (pwm labels and error labels)
    error_frame = tk.Frame(root, bg=background_color)
    error_frame.pack(pady=10)

    root.mainloop()
def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')
def create_and_position_error_label(error_message, row):
    global error_frame
    error_label = tk.Label(error_frame, text=error_message, font=("Arial", 12, "bold"), fg="red", bg=background_color)
    error_label.grid(row=row, column=0, pady=5)
    return error_label
def set_error_label(error_type, error_message):
    global error_labels
    if error_type == "time":
        error_label = create_and_position_error_label(error_message, 0)
    elif error_type == "cycle":
        error_label = create_and_position_error_label(error_message, 1)
    elif error_type == "duty":
        error_label = create_and_position_error_label(error_message, 2)
    else:
        error_label = create_and_position_error_label("Unknown Error", 0)

    error_labels.append(error_label)
def set_pwm_label(text):
    global pwm_label
    global error_frame
    pwm_label = tk.Label(error_frame, text=text, font=("Helvetica", 16), fg=maroon, bg=entry_background_color)
    pwm_label.grid(row=0, column=0, pady=5)
    root.after(10000, pwm_label.destroy)
def clear_error_labels():
    global error_labels
    for label in error_labels:
        label.destroy()
    error_labels = []
def clear_pwm_label():
    global pwm_label
    if pwm_label:
        pwm_label.destroy()
        pwm_label = None
def close_application():
    root.destroy()



#Main
if __name__ == "__main__":
    setup_GUI()
