import tkinter as tk
from tkinter import messagebox
import requests


# Function to check if a website is vulnerable to clickjacking
def check_clickjacking(url):
    try:
        # Add https:// schema if not present in the URL
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'https://' + url
        # Send a GET request to the URL
        response = requests.get(url)
        headers = response.headers

        # Check for X-Frame-Options header
        if 'X-Frame-Options' not in headers:
            return True

        # Get the value of X-Frame-Options and check it
        x_frame_options = headers['X-Frame-Options'].lower()
        if x_frame_options != 'deny' and x_frame_options != 'sameorigin':
            return True
        return False

    except requests.exceptions.RequestException as e:
        return None  # Error occurred


# Function to handle the checking process in the GUI
def on_check_click():
    url = url_entry.get()
    if url:
        result = check_clickjacking(url)
        if result is None:
            messagebox.showerror("Error", f"Could not check the website: {url}. Please check your connection or URL.")
        elif result:
            result_label.config(text=f"{url} may be vulnerable to clickjacking.")
        else:
            result_label.config(text=f"{url} is not vulnerable to clickjacking.")
    else:
        messagebox.showwarning("Input Error", "Please enter a valid URL.")


# Create the main window
root = tk.Tk()
root.title("Clickjacking Scanner")

# Create and place the widgets
tk.Label(root, text="Enter the website URL to check for Clickjacking:").pack(pady=10)

url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=10)

check_button = tk.Button(root, text="Check Clickjacking", command=on_check_click)
check_button.pack(pady=10)

result_label = tk.Label(root, text="", wraplength=400)
result_label.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()
