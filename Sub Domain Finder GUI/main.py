import requests
from typing import List
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

# Function to check if a subdomain is valid by its HTTP response status
def is_valid_subdomain(domain: str) -> bool:
    try:
        response = requests.get(f"http://{domain}", timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False

# Function to enumerate subdomains
def enumerate_subdomains(domain: str, subdomains: List[str]) -> List[str]:
    valid_subdomains = []
    
    for subdomain in subdomains:
        full_domain = f"{subdomain}.{domain}"
        if is_valid_subdomain(full_domain):
            valid_subdomains.append(full_domain)
            text_area.insert(tk.END, f"[+] Valid Subdomain Found: {full_domain}\n")
        # else:
        #     text_area.insert(tk.END, f"[-] Invalid Subdomain: {full_domain}\n")
    
    return valid_subdomains

# Function to read subdomains from a file
def read_subdomains_from_file(file_path: str) -> List[str]:
    try:
        with open(file_path, 'r') as file:
            subdomains = file.read().splitlines()
        return subdomains
    except FileNotFoundError:
        messagebox.showerror("Error", "File not found")
        return []

def start_enumeration():
    domain = entry_domain.get()
    subdomains_file = entry_file.get()
    
    if not domain:
        messagebox.showerror("Error", "Please enter a domain name")
        return
    
    if not subdomains_file:
        messagebox.showerror("Error", "Please select a subdomains file")
        return

    text_area.delete(1.0, tk.END)
    text_area.insert(tk.END, f"[*] Enumerating subdomains for: {domain}\n")

    subdomains = read_subdomains_from_file(subdomains_file)

    if subdomains:
        text_area.insert(tk.END, "[*] Checking subdomains from file:\n")
        valid_subdomains = enumerate_subdomains(domain, subdomains)
        
        text_area.insert(tk.END, "\n[*] All valid subdomains found:\n")
        for subdomain in valid_subdomains:
            text_area.insert(tk.END, subdomain + "\n")
    else:
        text_area.insert(tk.END, "[-] No subdomains to check\n")

def browse_file():
    file_path = filedialog.askopenfilename()
    entry_file.delete(0, tk.END)
    entry_file.insert(0, file_path)

# GUI Setup
root = tk.Tk()
root.title("Sub-Domain Finder")

frame = tk.Frame(root)
frame.pack(pady=10)

label_domain = tk.Label(frame, text="Domain Name:")
label_domain.grid(row=0, column=0, padx=5, pady=5)

entry_domain = tk.Entry(frame, width=50)
entry_domain.grid(row=0, column=1, padx=5, pady=5)

label_file = tk.Label(frame, text="Subdomains File:")
label_file.grid(row=1, column=0, padx=5, pady=5)

entry_file = tk.Entry(frame, width=50)
entry_file.grid(row=1, column=1, padx=5, pady=5)

button_browse = tk.Button(frame, text="Browse", command=browse_file)
button_browse.grid(row=1, column=2, padx=5, pady=5)

button_start = tk.Button(frame, text="Start Enumeration", command=start_enumeration)
button_start.grid(row=2, column=0, columnspan=3, pady=10)

text_area = scrolledtext.ScrolledText(root, width=80, height=20)
text_area.pack(pady=10)

root.mainloop()
