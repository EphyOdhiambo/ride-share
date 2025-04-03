import tkinter as tk
from tkinter import messagebox

# FAQ Data (Corrected with commas)
faq_data = {
    "How do I book a ride?": "To book a ride, select your pickup and drop-off location, then confirm.",
    "How do I cancel a ride?": "Go to 'Ride History', select the ride, and click 'Cancel'.",
    "How do I contact support?": "You can contact support at support@rideshare.com or +254 17289262.",
    "How do I pay for a ride?": "You can pay using M-Pesa, PayPal, or bank card in the app.",
    "Is there a cancellation fee?": "Yes, if you cancel after a driver accepts, a small fee may apply.",
    "How do I change my pickup location?": "Tap 'Edit Pickup' before confirming your ride.",
    "How do I rate my driver?": "After your ride, you'll see an option to rate your driver in the app.",
    "How can I get a refund?": "Contact support within 24 hours for refund requests.",
    "Can I schedule a ride in advance?": "Yes! Select 'Schedule Ride' and choose your preferred time.",
    "What happens if my driver cancels?": "You will be automatically matched with another driver.",
    "Do you offer ride-sharing?": "Yes, we offer shared rides at a lower cost.",
    "What if I left something in the car?": "Use the 'Lost & Found' option in the app or contact support.",
    "How do I update my payment method?": "Go to 'Settings' > 'Payments' to update your payment details.",
    "Do you have a referral program?": "Yes! You can refer a friend and earn ride discounts.",
}

# Function to show the answer when a question is clicked
def show_answer(question):
    answer = faq_data.get(question, "Answer not found.")
    messagebox.showinfo(question, answer)

# Create Tkinter Window
root = tk.Tk()
root.title("FAQs")

# Create buttons for each FAQ question
for question in faq_data.keys():
    btn = tk.Button(root, text=question, command=lambda q=question: show_answer(q), width=50, anchor="w")
    btn.pack(pady=2, padx=10)

# Run the Tkinter main loop
root.mainloop()
