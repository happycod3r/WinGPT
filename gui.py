import tkinter as tk

def process_input():
    user_input = input_text.get("1.0", tk.END).strip()
    output_text.insert(tk.END, f"User input: {user_input}\n")

# Create a new Tkinter window
window = tk.Tk()

output_text = tk.Text(window)
output_text.pack()

input_text = tk.Text(window)
input_text.pack()

process_button = tk.Button(window, text="Process", command=process_input)
process_button.pack()

# Start the Tkinter event loop
window.mainloop()
