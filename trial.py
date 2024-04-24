import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class PatientManagementSystem(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Aprima Eye Care Patient Management System")
        
        self.create_database()
        
        self.create_widgets()
        
    def create_database(self):
        self.conn = sqlite3.connect('patient_data.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS patient_records
                            (id INTEGER PRIMARY KEY,
                             role TEXT,
                             identity TEXT,
                             order_number TEXT,
                             duration TEXT,
                             tasks TEXT,
                             comments TEXT)''')
        self.conn.commit()
        
    def create_widgets(self):
        self.role_label = ttk.Label(self, text="Role:")
        self.role_label.grid(row=0, column=0, padx=5, pady=5)
        
        self.role_entry = ttk.Entry(self)
        self.role_entry.grid(row=0, column=1, padx=5, pady=5)
        
        self.identity_label = ttk.Label(self, text="Identity:")
        self.identity_label.grid(row=1, column=0, padx=5, pady=5)
        
        self.identity_entry = ttk.Entry(self)
        self.identity_entry.grid(row=1, column=1, padx=5, pady=5)
        
        self.order_label = ttk.Label(self, text="Order Number:")
        self.order_label.grid(row=2, column=0, padx=5, pady=5)
        
        self.order_entry = ttk.Entry(self)
        self.order_entry.grid(row=2, column=1, padx=5, pady=5)
        
        self.duration_label = ttk.Label(self, text="Duration:")
        self.duration_label.grid(row=3, column=0, padx=5, pady=5)
        
        self.duration_entry = ttk.Entry(self)
        self.duration_entry.grid(row=3, column=1, padx=5, pady=5)
        
        self.tasks_label = ttk.Label(self, text="Tasks:")
        self.tasks_label.grid(row=4, column=0, padx=5, pady=5)
        
        self.tasks_entry = ttk.Entry(self)
        self.tasks_entry.grid(row=4, column=1, padx=5, pady=5)
        
        self.comments_label = ttk.Label(self, text="Comments:")
        self.comments_label.grid(row=5, column=0, padx=5, pady=5)
        
        self.comments_entry = ttk.Entry(self)
        self.comments_entry.grid(row=5, column=1, padx=5, pady=5)
        
        self.submit_button = ttk.Button(self, text="Submit", command=self.submit_data)
        self.submit_button.grid(row=6, column=0, columnspan=2, padx=5, pady=5)
        
        self.analyze_button = ttk.Button(self, text="Analyze Data", command=self.analyze_data)
        self.analyze_button.grid(row=7, column=0, columnspan=2, padx=5, pady=5)
        
    def submit_data(self):
        role = self.role_entry.get()
        identity = self.identity_entry.get()
        order_number = self.order_entry.get()
        duration = self.duration_entry.get()
        tasks = self.tasks_entry.get()
        comments = self.comments_entry.get()
        
        self.c.execute("INSERT INTO patient_records (role, identity, order_number, duration, tasks, comments) VALUES (?, ?, ?, ?, ?, ?)",
                       (role, identity, order_number, duration, tasks, comments))
        
        self.conn.commit()
        
        self.clear_entries()
        
    def clear_entries(self):
        self.role_entry.delete(0, 'end')
        self.identity_entry.delete(0, 'end')
        self.order_entry.delete(0, 'end')
        self.duration_entry.delete(0, 'end')
        self.tasks_entry.delete(0, 'end')
        self.comments_entry.delete(0, 'end')
        
    def analyze_data(self):
        self.c.execute("SELECT * FROM patient_records")
        data = self.c.fetchall()
        
        num_entries = len(data)
        
        durations = [float(entry[4].split()[0]) for entry in data if entry[4] and entry[4].split()[0].isdigit()]
        if durations:
            average_duration = sum(durations) / len(durations)
        else:
            average_duration = 0
            
        unique_roles = len(set([entry[1] for entry in data]))
        
        analysis_result = f"Number of Entries: {num_entries}\nAverage Duration: {average_duration:.2f}\nNumber of Unique Roles: {unique_roles}"
        
        messagebox.showinfo("Data Analysis Result", analysis_result)
        
if __name__ == "__main__":
    app = PatientManagementSystem()
    app.mainloop()
