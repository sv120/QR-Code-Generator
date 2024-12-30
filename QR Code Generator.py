#This app is made by Sharad Verma using python language.
#Version of this app is 1.0(2024)

#This app generates QR code of any links. Useful to open any link in mobile phone.

from tkinter import Menu  # Add this import to fix the error
import qrcode
import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageTk
from datetime import datetime

# App setup
ctk.set_appearance_mode("Dark")  # Default to Dark mode
ctk.set_default_color_theme("blue")  # Use a consistent blue theme

app = ctk.CTk()
app.geometry("400x450")  # Increased window size to fit messages
app.title("QR Code Generator")
app.resizable(False, False)  # Prevent resizing

# Global variables
qr_image = None
theme_menu_open = False
theme_menu = None

# Function to generate QR code
def generate_qr():
    global qr_image
    link = entry.get()
    if link.strip() == "":
        display_message("Error: Please enter a valid link.", "red")
        return
    
    try:
        qr = qrcode.QRCode(box_size=10, border=2)
        qr.add_data(link)
        qr.make(fit=True)
        qr_image = qr.make_image(fill_color="black", back_color="white")
        
        # Display the QR code in the canvas
        img = qr_image.resize((180, 180))
        qr_photo = ImageTk.PhotoImage(img)
        canvas.create_image(90, 90, image=qr_photo)
        canvas.image = qr_photo
        
        # Enable save and clear buttons
        save_button.configure(state="normal")
        clear_button.configure(state="normal")
        display_message("QR Code generated successfully!", "green")
    except Exception as e:
        display_message(f"Error: {e}", "red")

# Function to save QR code
def save_qr():
    global qr_image
    if qr_image is None:
        display_message("Error: No QR Code to save. Generate one first.", "red")
        return
    
    try:
        default_name = f"QR_Code_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        file_path = filedialog.asksaveasfilename(initialfile=default_name,
                                                 defaultextension=".png",
                                                 filetypes=[("PNG files", "*.png")])
        if file_path:
            qr_image.save(file_path)
            display_message("QR Code saved successfully!", "green")
    except Exception as e:
        display_message(f"Error: {e}", "red")

# Function to clear the input and canvas
def clear_all():
    entry.delete(0, ctk.END)
    canvas.delete("all")
    save_button.configure(state="disabled")
    clear_button.configure(state="disabled")
    display_message("Cleared successfully!", "green")

# Function to display messages in the status bar
def display_message(message, color):
    status_label.configure(text=message, text_color=color)
    app.after(5000, lambda: status_label.configure(text=""))

# Function to toggle between light and dark mode
def toggle_theme(mode):
    ctk.set_appearance_mode(mode)

# Function to show/hide theme menu
def toggle_theme_menu(event):
    global theme_menu_open, theme_menu
    if theme_menu_open:
        theme_menu.destroy()
        theme_menu_open = False
    else:
        # Create menu and apply rounded corners
        theme_menu = Menu(app, tearoff=0, font=("Roboto", 12), relief="flat", bd=0)
        theme_menu.add_command(label="Light Mode", command=lambda: apply_theme("Light"))
        theme_menu.add_command(label="Dark Mode", command=lambda: apply_theme("Dark"))
        
        # Update background colors for light and dark modes
        if ctk.get_appearance_mode() == "Dark":
            theme_menu.config(bg="#2e2e2e", fg="white")
        else:
            theme_menu.config(bg="white", fg="black")
        
        # Add rounded corners effect
        theme_menu.config(borderwidth=2, relief="solid", bd=0)
        
        theme_menu.post(event.x_root, event.y_root)
        theme_menu_open = True

# Function to apply theme and close menu
def apply_theme(choice):
    global theme_menu, theme_menu_open
    toggle_theme(choice)
    if theme_menu_open:
        theme_menu.destroy()
        theme_menu_open = False

# Function for paste button action
def paste_text():
    try:
        clipboard_content = app.clipboard_get()  # Get text from clipboard
        entry.insert(ctk.END, clipboard_content)  # Insert into entry
    except Exception as e:
        display_message(f"Error: {e}", "red")

# UI Layout
# Header
header = ctk.CTkLabel(app, text="QR Code Generator", font=("Roboto", 20, "bold"))
header.pack(pady=10)

# Three-dot menu for theme selection
dots_button = ctk.CTkLabel(app, text="⋮", font=("Roboto", 20))
dots_button.place(relx=0.95, rely=0.05, anchor="ne")
dots_button.bind("<Button-1>", toggle_theme_menu)

# Frame for entry and paste button
entry_frame = ctk.CTkFrame(app, fg_color="transparent")
entry_frame.pack(pady=10)

# Entry Widget
entry = ctk.CTkEntry(entry_frame, width=200, placeholder_text="Enter Link Here")
entry.pack(side="left", padx=(0, 5))

# Bind the Enter key to generate the QR code
entry.bind("<Return>", lambda event: generate_qr())

# Paste Button
paste_button = ctk.CTkButton(entry_frame, text="Paste", width=50, command=paste_text)
paste_button.pack(side="right")

# Generate Button
generate_button = ctk.CTkButton(app, text="Generate QR Code", command=generate_qr)
generate_button.pack(pady=10)

# Canvas for QR Code
canvas_frame = ctk.CTkFrame(app, width=180, height=180, fg_color="white")
canvas_frame.pack(pady=10)
canvas = ctk.CTkCanvas(canvas_frame, width=180, height=180, bg="white", highlightthickness=0)
canvas.pack()

# Save Button
save_button = ctk.CTkButton(app, text="Save QR Code", state="disabled", command=save_qr)
save_button.pack(pady=5)

# Clear Button
clear_button = ctk.CTkButton(app, text="Clear", state="disabled", command=clear_all)
clear_button.pack(pady=5)

# Status Label
status_label = ctk.CTkLabel(app, text="", font=("Roboto", 12), height=40)  # Increased height
status_label.pack(pady=10)

# Footer - Using `place()` method for visibility and correct positioning
footer_frame = ctk.CTkFrame(app, fg_color="transparent", width=400, height=30)  # Increased width
footer_frame.place(relx=0.5, rely=1.0, anchor="s")

# Made by label
made_by_label = ctk.CTkLabel(footer_frame, text="Made by: Sharad Verma", font=("Consolas", 9), text_color="gray")
made_by_label.place(relx=0.02, rely=0.5, anchor="w")

# Version label
version_label = ctk.CTkLabel(footer_frame, text="Version: 1.0", font=("Consolas", 9), text_color="gray")
version_label.place(relx=0.98, rely=0.5, anchor="e")

app.mainloop()
