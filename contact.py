import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk

# Initialize main window
root = ctk.CTk()
root.title("Contact Us - Ride-Share App")
root.geometry("600x700")
root.configure(bg="#f5f5f5")  # Light gray background

# Styling
font_style = ("Arial", 14, "bold")
entry_style = {"width": 400, "height": 40, "corner_radius": 10, "fg_color": "white", "border_width": 2, "border_color": "#800080"}
btn_style = {"fg_color": "#800080", "text_color": "white", "font": ("Arial", 14, "bold"), "corner_radius": 10, "height": 50, "width": 250}

# Function to Submit Contact Form
def submit_contact():
    name = name_entry.get()
    email = email_entry.get()
    comment = comment_entry.get("1.0", "end").strip()
    rating = rating_var.get()
    
    if not name or not email or not comment or rating == 0:
        messagebox.showerror("Error", "Please fill out all fields and provide a rating.")
        return
    
    messagebox.showinfo("Success", "Thank you for your feedback!")
    root.destroy()

# Title
title_label = ctk.CTkLabel(root, text="Contact Us", font=("Arial", 24, "bold"), text_color="#800080")
title_label.pack(pady=20)

# Name Entry
ctk.CTkLabel(root, text="Full Name:", font=font_style, text_color="#800080").pack(anchor="w", padx=100)
name_entry = ctk.CTkEntry(root, **entry_style)
name_entry.pack(pady=10)

# Email Entry
ctk.CTkLabel(root, text="Email Address:", font=font_style, text_color="#800080").pack(anchor="w", padx=100)
email_entry = ctk.CTkEntry(root, **entry_style)
email_entry.pack(pady=10)

# Comment Entry
ctk.CTkLabel(root, text="Comment:", font=font_style, text_color="#800080").pack(anchor="w", padx=100)
comment_entry = ctk.CTkTextbox(root, width=400, height=100, corner_radius=10, border_width=2, border_color="#800080")
comment_entry.pack(pady=10)

# Star Rating
ctk.CTkLabel(root, text="Rate Us:", font=font_style, text_color="#800080").pack(anchor="w", padx=100)
rating_var = tk.IntVar()
rating_frame = tk.Frame(root, bg="#f5f5f5")
rating_frame.pack(pady=10)

for i in range(1, 6):
    tk.Radiobutton(rating_frame, text=f"{i}★", variable=rating_var, value=i, font=("Arial", 14), bg="#f5f5f5", fg="#800080").pack(side="left", padx=5)

# Submit Button
submit_btn = ctk.CTkButton(root, text="Submit", command=submit_contact, **btn_style)
submit_btn.pack(pady=20)

# Run the Tkinter main loop
root.mainloop()