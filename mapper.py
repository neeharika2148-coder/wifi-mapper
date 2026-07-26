import tkinter as tk
from tkinter import ttk
import os

def create_gui():
    # 1. Main Window Setup
    root = tk.Tk()
    root.title("KITE Campus WiFi Strength Mapper")
    root.geometry("1100x700")
    root.configure(bg="#f4f4f9")

    # 2. Navigation Bar (Kept exactly as requested)
    nav_frame = tk.Frame(root, bg="#0056b3", height=50)
    nav_frame.pack(fill=tk.X)
    
    logo_label = tk.Label(nav_frame, text="KITE Dashboard", font=("Arial", 14, "bold"), bg="#0056b3", fg="white")
    logo_label.pack(side=tk.LEFT, padx=20, pady=10)

    # Dummy buttons for Nav
    nav_buttons = ["Settings", "Analytics", "Map", "Home"]
    for btn_text in nav_buttons:
        btn = tk.Button(nav_frame, text=btn_text, bg="#0056b3", fg="white", 
                        font=("Arial", 10, "bold"), bd=0, activebackground="#004494", activeforeground="white")
        btn.pack(side=tk.RIGHT, padx=10)

    # 3. Horizontal Project Details Bar (Based on your table)
    details_frame = tk.Frame(root, bg="#e9ecef", bd=1, relief=tk.RAISED)
    details_frame.pack(fill=tk.X)

    table_data = [
        ("Combined Subjects", "Engineering Physics +\nProgramming + IT Workshop"),
        ("Topics Integrated", "Sound waves, Signal\ngradient, Internet tools"),
        ("AI/LLM Layer", "AI suggests optimal\nrouter placement"),
        ("Coding Framework", "Python + os module\n+ simple GUI"),
        ("R23 Alignment", "Sem-I Physics +\nIT Workshop")
    ]

    # Dynamically create horizontal columns for the data
    for col_index, (header, content) in enumerate(table_data):
        col_frame = tk.Frame(details_frame, bg="#e9ecef")
        col_frame.grid(row=0, column=col_index, sticky="nsew", padx=10, pady=10)
        details_frame.grid_columnconfigure(col_index, weight=1) # Distribute space evenly

        lbl_header = tk.Label(col_frame, text=header, font=("Arial", 10, "bold"), bg="#e9ecef", fg="#0056b3")
        lbl_header.pack()

        lbl_content = tk.Label(col_frame, text=content, font=("Arial", 9), bg="#e9ecef", fg="#333", justify=tk.CENTER)
        lbl_content.pack()

    # 4. Main Title
    title_label = tk.Label(root, text="KITE Campus WiFi Strength Mapper", font=("Arial", 18, "bold"), bg="#f4f4f9", fg="#333")
    title_label.pack(pady=20)

    # 5. Main Content Area (Placeholder for your WiFi Heatmap/Logic)
    main_content_frame = tk.Frame(root, bg="white", bd=2, relief=tk.SUNKEN)
    main_content_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)
    
    placeholder_text = tk.Label(main_content_frame, 
                                text="(Your WiFi map, os module outputs, and heatmap visualizations go here)", 
                                font=("Arial", 12, "italic"), bg="white", fg="#666")
    placeholder_text.pack(expand=True)

    # 6. Footer (Specific team text)
    footer_frame = tk.Frame(root, bg="#222", height=40)
    footer_frame.pack(fill=tk.X, side=tk.BOTTOM)
    
    footer_label = tk.Label(footer_frame, 
                            text="Project is done by team three com- cse(ai &ml ) day scholars 2", 
                            font=("Arial", 10), bg="#222", fg="white")
    footer_label.pack(pady=10)

    # Start the GUI event loop
    root.mainloop()

if __name__ == "__main__":
    create_gui()