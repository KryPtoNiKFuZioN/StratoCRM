import os
import json
import customtkinter as ctk
from tkinter import messagebox
from tkinter import filedialog
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Initialize the application window
ctk.set_appearance_mode("System")  # Options: "System", "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue", "green", "dark-blue"

app = ctk.CTk()
app.geometry("800x600")
app.title("StratoCRM")

# Folder to store customer files
CUSTOMER_FOLDER = "customers"
os.makedirs(CUSTOMER_FOLDER, exist_ok=True)

# Utility Functions
def generate_account_number():
    """Generate a unique account number for each customer."""
    return str(len(os.listdir(CUSTOMER_FOLDER)) + 1).zfill(6)

def save_customer_data(data):
    """Save customer data to a JSON file."""
    account_number = data["account_number"]
    file_path = os.path.join(CUSTOMER_FOLDER, f"{account_number}.json")
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

def load_customer_data(account_number):
    """Load customer data from a JSON file."""
    file_path = os.path.join(CUSTOMER_FOLDER, f"{account_number}.json")
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
    else:
        return None

# GUI Functionality
def create_customer():
    """Create a new customer and save their details."""
    name = name_entry.get()
    email = email_entry.get()
    phone = phone_entry.get()

    if not name or not email or not phone:
        messagebox.showerror("Error", "All fields are required!")
        return

    account_number = generate_account_number()
    customer_data = {
        "account_number": account_number,
        "name": name,
        "email": email,
        "phone": phone,
        "notes": []
    }

    save_customer_data(customer_data)
    messagebox.showinfo("Success", f"Customer created successfully!\nAccount Number: {account_number}")
    name_entry.delete(0, ctk.END)
    email_entry.delete(0, ctk.END)
    phone_entry.delete(0, ctk.END)

def lookup_customer():
    """Look up a customer by account number."""
    account_number = lookup_entry.get()

    if not account_number:
        messagebox.showerror("Error", "Please enter an account number!")
        return

    customer_data = load_customer_data(account_number)

    if customer_data:
        customer_details_label.configure(
            text=(
                f"Account Number: {customer_data['account_number']}\n"
                f"Name: {customer_data['name']}\n"
                f"Email: {customer_data['email']}\n"
                f"Phone: {customer_data['phone']}\n"
                f"Notes: {', '.join(customer_data['notes']) if customer_data['notes'] else 'No notes'}"
            )
        )
    else:
        messagebox.showerror("Error", "Customer not found!")

def add_note():
    """Add a note to an existing customer account."""
    account_number = note_account_entry.get()
    note = note_entry.get()

    if not account_number or not note:
        messagebox.showerror("Error", "Both fields are required!")
        return

    customer_data = load_customer_data(account_number)

    if customer_data:
        customer_data["notes"].append(note)
        save_customer_data(customer_data)
        messagebox.showinfo("Success", "Note added successfully!")
        note_account_entry.delete(0, ctk.END)
        note_entry.delete(0, ctk.END)
    else:
        messagebox.showerror("Error", "Customer not found!")

def send_email():
    """Send an email to a customer."""
    recipient = email_recipient_entry.get()
    subject = email_subject_entry.get()
    body = email_body_entry.get("1.0", ctk.END)

    if not recipient or not subject or not body.strip():
        messagebox.showerror("Error", "All fields are required!")
        return

    try:
        # Email configuration (replace with your SMTP server details)
        sender_email = "youremail@example.com"
        sender_password = "yourpassword"
        
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = recipient
        msg["Subject"] = subject
        
        msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient, msg.as_string())
        server.quit()

        messagebox.showinfo("Success", "Email sent successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to send email: {e}")

# GUI Layout
# Tabs
tabview = ctk.CTkTabview(app)
tabview.pack(fill="both", expand=True)

# Tab 1: Create Customer
tab1 = tabview.add("Create Customer")
name_label = ctk.CTkLabel(tab1, text="Name:")
name_label.pack(pady=5)
name_entry = ctk.CTkEntry(tab1)
name_entry.pack(pady=5)
email_label = ctk.CTkLabel(tab1, text="Email:")
email_label.pack(pady=5)
email_entry = ctk.CTkEntry(tab1)
email_entry.pack(pady=5)
phone_label = ctk.CTkLabel(tab1, text="Phone:")
phone_label.pack(pady=5)
phone_entry = ctk.CTkEntry(tab1)
phone_entry.pack(pady=5)
create_button = ctk.CTkButton(tab1, text="Create Customer", command=create_customer)
create_button.pack(pady=10)

# Tab 2: Lookup Customer
tab2 = tabview.add("Lookup Customer")
lookup_label = ctk.CTkLabel(tab2, text="Enter Account Number:")
lookup_label.pack(pady=5)
lookup_entry = ctk.CTkEntry(tab2)
lookup_entry.pack(pady=5)
lookup_button = ctk.CTkButton(tab2, text="Lookup", command=lookup_customer)
lookup_button.pack(pady=10)
customer_details_label = ctk.CTkLabel(tab2, text="", justify="left")
customer_details_label.pack(pady=10)

# Tab 3: Add Note
tab3 = tabview.add("Add Note")
note_account_label = ctk.CTkLabel(tab3, text="Enter Account Number:")
note_account_label.pack(pady=5)
note_account_entry = ctk.CTkEntry(tab3)
note_account_entry.pack(pady=5)
note_label = ctk.CTkLabel(tab3, text="Enter Note:")
note_label.pack(pady=5)
note_entry = ctk.CTkEntry(tab3)
note_entry.pack(pady=5)
note_button = ctk.CTkButton(tab3, text="Add Note", command=add_note)
note_button.pack(pady=10)

# Tab 4: Send Email
tab4 = tabview.add("Send Email")
email_recipient_label = ctk.CTkLabel(tab4, text="Recipient Email:")
email_recipient_label.pack(pady=5)
email_recipient_entry = ctk.CTkEntry(tab4)
email_recipient_entry.pack(pady=5)
email_subject_label = ctk.CTkLabel(tab4, text="Subject:")
email_subject_label.pack(pady=5)
email_subject_entry = ctk.CTkEntry(tab4)
email_subject_entry.pack(pady=5)
email_body_label = ctk.CTkLabel(tab4, text="Body:")
email_body_label.pack(pady=5)
email_body_entry = ctk.CTkTextbox(tab4, height=150)
email_body_entry.pack(pady=5)
email_button = ctk.CTkButton(tab4, text="Send Email", command=send_email)
email_button.pack(pady=10)

# Run the app
app.mainloop
