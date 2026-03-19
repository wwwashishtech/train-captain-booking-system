"""
The Train Captain - Passenger Details Tab
Handles adding/removing passenger information
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class PassengerTab(tk.Frame):
    """Passenger Details Tab - Add up to 6 passengers"""
    
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        
        # Configure frame
        self.configure(bg=self.app.colors['background'])
        
        # Create scrollable frame
        self.create_scrollable_frame()
        
        # Passenger list
        self.passengers = []
        self.passenger_frames = []
        
        # Initialize variables
        self.add_btn = None
        self.fare_frame = None
        self.fare_details_frame = None
        self.continue_btn = None
        
        # Create UI
        self.create_widgets()
    
    def create_scrollable_frame(self):
        """Create a scrollable frame for content"""
        # Create canvas and scrollbar
        self.canvas = tk.Canvas(self, bg=self.app.colors['background'], highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=self.app.colors['background'])
        
        # Configure canvas
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Create window inside canvas
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        # Pack canvas and scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Bind configure event to update scroll region
        self.scrollable_frame.bind('<Configure>', self.on_frame_configure)
        self.canvas.bind('<Configure>', self.on_canvas_configure)
        
        # Bind mousewheel for scrolling
        self.bind_mousewheel()
    
    def on_frame_configure(self, event):
        """Update scroll region when frame changes"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def on_canvas_configure(self, event):
        """Update canvas window width when canvas resizes"""
        self.canvas.itemconfig(self.canvas_window, width=event.width)
    
    def bind_mousewheel(self):
        """Bind mousewheel for scrolling"""
        def on_mousewheel(event):
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        def on_enter(event):
            self.canvas.bind_all("<MouseWheel>", on_mousewheel)
        
        def on_leave(event):
            self.canvas.unbind_all("<MouseWheel>")
        
        self.canvas.bind("<Enter>", on_enter)
        self.canvas.bind("<Leave>", on_leave)
    
    def create_widgets(self):
        """Create all widgets for passenger details"""
        # Main container
        main_container = tk.Frame(self.scrollable_frame, bg=self.app.colors['background'])
        main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Header with journey summary
        self.create_journey_summary(main_container)
        
        # Passenger limit info
        self.create_limit_info(main_container)
        
        # Passenger forms container
        self.forms_container = tk.Frame(main_container, bg=self.app.colors['background'])
        self.forms_container.pack(fill='both', expand=True, pady=10)
        
        # Add passenger button (create BEFORE adding forms)
        self.create_add_button(main_container)
        
        # Fare summary
        self.create_fare_summary(main_container)
        
        # Navigation buttons
        self.create_navigation_buttons(main_container)
        
        # Add first passenger by default (AFTER all widgets are created)
        self.add_passenger_form()
    
    def create_journey_summary(self, parent):
        """Create journey summary section"""
        summary_frame = tk.Frame(parent, bg=self.app.colors['surface'],
                                relief='solid', bd=1, highlightbackground=self.app.colors['border'])
        summary_frame.pack(fill='x', pady=(0, 10))
        
        # Title
        title_label = tk.Label(summary_frame, text="Journey Summary",
                              font=('Arial', 14, 'bold'),
                              fg=self.app.colors['primary'], bg=self.app.colors['surface'])
        title_label.pack(pady=5)
        
        # Details
        details_frame = tk.Frame(summary_frame, bg=self.app.colors['surface'])
        details_frame.pack(padx=20, pady=10, fill='x')
        
        if self.app.selected_train:
            train = self.app.selected_train
            details = [
                f"Train: {train['train_name']} ({train['train_number']})",
                f"From: {train['source']} → To: {train['destination']}",
                f"Date: {self.app.booking_details.get('journey_date', 'N/A')}",
                f"Class: {self.app.booking_details.get('class', 'N/A')}",
                f"Quota: {self.app.booking_details.get('quota', 'N/A')}"
            ]
            
            for detail in details:
                label = tk.Label(details_frame, text=detail,
                               font=('Arial', 10),
                               fg=self.app.colors['text'], bg=self.app.colors['surface'])
                label.pack(anchor='w', pady=1)
    
    def create_limit_info(self, parent):
        """Show passenger limit information"""
        limit_frame = tk.Frame(parent, bg=self.app.colors['info'], height=30)
        limit_frame.pack(fill='x', pady=(0, 10))
        limit_frame.pack_propagate(False)
        
        limit_label = tk.Label(limit_frame,
                              text="📋 Maximum 6 passengers per booking • All fields are mandatory",
                              font=('Arial', 10, 'bold'),
                              fg='white', bg=self.app.colors['info'])
        limit_label.pack(expand=True)
    
    def create_add_button(self, parent):
        """Create the add passenger button"""
        self.add_button_frame = tk.Frame(parent, bg=self.app.colors['background'])
        self.add_button_frame.pack(fill='x', pady=10)
        
        self.add_btn = tk.Button(self.add_button_frame, text="+ Add Another Passenger",
                                 command=self.add_passenger_form,
                                 bg=self.app.colors['primary'], fg='white',
                                 font=('Arial', 11), padx=20, pady=8,
                                 relief='flat', cursor='hand2')
        self.add_btn.pack()
        self.add_hover_effect(self.add_btn, self.app.colors['primary'], self.app.colors['primary_dark'])
    
    def add_passenger_form(self):
        """Add a new passenger form"""
        if len(self.passenger_frames) >= 6:
            messagebox.showwarning("Limit Reached", "Maximum 6 passengers allowed per booking")
            return
        
        passenger_num = len(self.passenger_frames) + 1
        
        # Create frame for this passenger
        frame = tk.Frame(self.forms_container, bg=self.app.colors['surface'],
                        relief='solid', bd=1, highlightbackground=self.app.colors['border'])
        frame.pack(fill='x', pady=5)
        
        # Header with passenger number and remove button
        header_frame = tk.Frame(frame, bg=self.app.colors['primary'])
        header_frame.pack(fill='x')
        
        tk.Label(header_frame, text=f"Passenger {passenger_num}",
                font=('Arial', 11, 'bold'), fg='white',
                bg=self.app.colors['primary']).pack(side='left', padx=10, pady=5)
        
        if passenger_num > 1:  # Can't remove first passenger
            remove_btn = tk.Button(header_frame, text="✖ Remove",
                                  command=lambda: self.remove_passenger_form(frame),
                                  bg=self.app.colors['danger'], fg='white',
                                  font=('Arial', 9), padx=10, pady=2,
                                  relief='flat', cursor='hand2')
            remove_btn.pack(side='right', padx=10, pady=5)
            self.add_hover_effect(remove_btn, self.app.colors['danger'], '#b91c1c')
        
        # Form fields
        form_frame = tk.Frame(frame, bg=self.app.colors['surface'])
        form_frame.pack(padx=20, pady=15, fill='x')
        
        # Name
        name_frame = tk.Frame(form_frame, bg=self.app.colors['surface'])
        name_frame.pack(fill='x', pady=5)
        
        tk.Label(name_frame, text="Full Name:", font=('Arial', 10),
                fg=self.app.colors['text'], bg=self.app.colors['surface']).pack(anchor='w')
        
        name_entry = tk.Entry(name_frame, font=('Arial', 10), bg='white',
                             relief='solid', bd=1, highlightthickness=1)
        name_entry.pack(fill='x', pady=(2, 0), ipady=3)
        
        # Age and Gender in same row
        row_frame = tk.Frame(form_frame, bg=self.app.colors['surface'])
        row_frame.pack(fill='x', pady=5)
        
        # Age
        age_frame = tk.Frame(row_frame, bg=self.app.colors['surface'])
        age_frame.pack(side='left', fill='x', expand=True, padx=(0, 5))
        
        tk.Label(age_frame, text="Age:", font=('Arial', 10),
                fg=self.app.colors['text'], bg=self.app.colors['surface']).pack(anchor='w')
        
        age_entry = tk.Entry(age_frame, font=('Arial', 10), bg='white', width=10,
                            relief='solid', bd=1, highlightthickness=1)
        age_entry.pack(fill='x', pady=(2, 0), ipady=3)
        
        # Gender
        gender_frame = tk.Frame(row_frame, bg=self.app.colors['surface'])
        gender_frame.pack(side='left', fill='x', expand=True, padx=(5, 0))
        
        tk.Label(gender_frame, text="Gender:", font=('Arial', 10),
                fg=self.app.colors['text'], bg=self.app.colors['surface']).pack(anchor='w')
        
        gender_combo = ttk.Combobox(gender_frame, font=('Arial', 10),
                                   values=["Male", "Female", "Other"], state='readonly')
        gender_combo.pack(fill='x', pady=(2, 0), ipady=2)
        gender_combo.set("Male")
        
        # ID Proof
        id_frame = tk.Frame(form_frame, bg=self.app.colors['surface'])
        id_frame.pack(fill='x', pady=5)
        
        tk.Label(id_frame, text="ID Proof Type:", font=('Arial', 10),
                fg=self.app.colors['text'], bg=self.app.colors['surface']).pack(anchor='w')
        
        id_type_combo = ttk.Combobox(id_frame, font=('Arial', 10),
                                     values=["Aadhar Card", "PAN Card", "Voter ID", 
                                            "Passport", "Driving License"], state='readonly')
        id_type_combo.pack(fill='x', pady=(2, 0), ipady=2)
        id_type_combo.set("Aadhar Card")
        
        # ID Number
        id_number_frame = tk.Frame(id_frame, bg=self.app.colors['surface'])
        id_number_frame.pack(fill='x', pady=(5, 0))
        
        tk.Label(id_number_frame, text="ID Number:", font=('Arial', 10),
                fg=self.app.colors['text'], bg=self.app.colors['surface']).pack(anchor='w')
        
        id_number_entry = tk.Entry(id_number_frame, font=('Arial', 10), bg='white',
                                  relief='solid', bd=1, highlightthickness=1)
        id_number_entry.pack(fill='x', pady=(2, 0), ipady=3)
        
        # Concession (for senior citizens)
        concession_frame = tk.Frame(form_frame, bg=self.app.colors['surface'])
        concession_frame.pack(fill='x', pady=5)
        
        concession_var = tk.BooleanVar()
        concession_check = tk.Checkbutton(concession_frame, text="Senior Citizen Concession",
                                         variable=concession_var,
                                         bg=self.app.colors['surface'],
                                         fg=self.app.colors['text'],
                                         selectcolor=self.app.colors['surface'],
                                         activebackground=self.app.colors['surface'])
        concession_check.pack(anchor='w')
        
        # Store references to entry widgets
        passenger_data = {
            'frame': frame,
            'name': name_entry,
            'age': age_entry,
            'gender': gender_combo,
            'id_type': id_type_combo,
            'id_number': id_number_entry,
            'concession': concession_var
        }
        
        self.passenger_frames.append(passenger_data)
        self.update_passenger_numbers()
        self.update_fare_summary()
        
        # Force canvas to update scroll region
        self.scrollable_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def remove_passenger_form(self, frame):
        """Remove a passenger form"""
        for i, passenger in enumerate(self.passenger_frames):
            if passenger['frame'] == frame:
                frame.destroy()
                self.passenger_frames.pop(i)
                break
        
        self.update_passenger_numbers()
        self.update_fare_summary()
        
        # Force canvas to update scroll region
        self.scrollable_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def update_passenger_numbers(self):
        """Update passenger numbers in headers"""
        for i, passenger in enumerate(self.passenger_frames):
            # Find header label and update
            for child in passenger['frame'].winfo_children():
                if isinstance(child, tk.Frame) and child['bg'] == self.app.colors['primary']:
                    for grandchild in child.winfo_children():
                        if isinstance(grandchild, tk.Label) and grandchild['bg'] == self.app.colors['primary']:
                            grandchild.config(text=f"Passenger {i+1}")
                            break
                    break
        
        # Update add button state if it exists
        if self.add_btn:
            if len(self.passenger_frames) >= 6:
                self.add_btn.config(state='disabled', bg=self.app.colors['text_light'])
            else:
                self.add_btn.config(state='normal', bg=self.app.colors['primary'])
    
    def create_fare_summary(self, parent):
        """Create fare summary section"""
        self.fare_frame = tk.Frame(parent, bg=self.app.colors['surface'],
                                   relief='solid', bd=1, highlightbackground=self.app.colors['border'])
        self.fare_frame.pack(fill='x', pady=10)
        
        # Title
        title_label = tk.Label(self.fare_frame, text="Fare Summary",
                              font=('Arial', 14, 'bold'),
                              fg=self.app.colors['primary'], bg=self.app.colors['surface'])
        title_label.pack(pady=5)
        
        # Details
        self.fare_details_frame = tk.Frame(self.fare_frame, bg=self.app.colors['surface'])
        self.fare_details_frame.pack(padx=20, pady=10, fill='x')
        
        self.update_fare_summary()
    
    def update_fare_summary(self):
        """Update fare summary based on passengers"""
        # Clear existing widgets
        if self.fare_details_frame:
            for widget in self.fare_details_frame.winfo_children():
                widget.destroy()
        
        if not self.app.fare_details or len(self.passenger_frames) == 0:
            # Show placeholder
            if self.fare_details_frame:
                placeholder = tk.Label(self.fare_details_frame, 
                                      text="Add passengers to see fare details",
                                      font=('Arial', 10, 'italic'),
                                      fg=self.app.colors['text_light'],
                                      bg=self.app.colors['surface'])
                placeholder.pack(pady=10)
            return
        
        base_fare = self.app.fare_details.get('total', 0)
        passenger_count = len(self.passenger_frames)
        
        # Calculate totals
        subtotal = base_fare * passenger_count
        
        # Senior citizen concession (if applicable)
        concession_count = 0
        for passenger in self.passenger_frames:
            if passenger['concession'].get():
                concession_count += 1
        
        concession_amount = 0
        if concession_count > 0 and self.app.booking_details.get('quota') == "SS":
            concession_amount = int(base_fare * 0.4 * concession_count)
        
        total = subtotal - concession_amount
        
        # Display
        details = [
            (f"Base Fare (per passenger)", f"₹ {base_fare}"),
            (f"Number of Passengers", f"{passenger_count}"),
            (f"Subtotal", f"₹ {subtotal}"),
        ]
        
        for label, value in details:
            row = tk.Frame(self.fare_details_frame, bg=self.app.colors['surface'])
            row.pack(fill='x', pady=2)
            
            tk.Label(row, text=label, font=('Arial', 10),
                    fg=self.app.colors['text'], bg=self.app.colors['surface']).pack(side='left')
            
            tk.Label(row, text=value, font=('Arial', 10, 'bold'),
                    fg=self.app.colors['primary'], bg=self.app.colors['surface']).pack(side='right')
        
        if concession_amount > 0:
            row = tk.Frame(self.fare_details_frame, bg=self.app.colors['surface'])
            row.pack(fill='x', pady=2)
            
            tk.Label(row, text="Senior Citizen Concession (-40%)", font=('Arial', 10),
                    fg=self.app.colors['text'], bg=self.app.colors['surface']).pack(side='left')
            
            tk.Label(row, text=f"- ₹ {concession_amount}", font=('Arial', 10, 'bold'),
                    fg=self.app.colors['success'], bg=self.app.colors['surface']).pack(side='right')
        
        # Separator
        separator = ttk.Separator(self.fare_details_frame, orient='horizontal')
        separator.pack(fill='x', pady=5)
        
        # Total
        total_row = tk.Frame(self.fare_details_frame, bg=self.app.colors['surface'])
        total_row.pack(fill='x', pady=5)
        
        tk.Label(total_row, text="Total Fare", font=('Arial', 12, 'bold'),
                fg=self.app.colors['text'], bg=self.app.colors['surface']).pack(side='left')
        
        tk.Label(total_row, text=f"₹ {total}", font=('Arial', 14, 'bold'),
                fg=self.app.colors['success'], bg=self.app.colors['surface']).pack(side='right')
        
        # Store total in booking details
        self.app.booking_details['total_fare'] = total
        self.app.booking_details['passenger_count'] = passenger_count
    
    def create_navigation_buttons(self, parent):
        """Create navigation buttons"""
        nav_frame = tk.Frame(parent, bg=self.app.colors['background'])
        nav_frame.pack(fill='x', pady=20)
        
        # Back button
        back_btn = tk.Button(nav_frame, text="← Back to Train Selection",
                            command=self.go_back,
                            bg=self.app.colors['text_light'], fg='white',
                            font=('Arial', 11), padx=20, pady=10,
                            relief='flat', cursor='hand2')
        back_btn.pack(side='left', padx=5)
        self.add_hover_effect(back_btn, self.app.colors['text_light'], self.app.colors['text'])
        
        # Continue button
        self.continue_btn = tk.Button(nav_frame, text="Continue to Payment →",
                                      command=self.go_to_payment,
                                      bg=self.app.colors['secondary'], fg='white',
                                      font=('Arial', 12, 'bold'), padx=30, pady=10,
                                      relief='flat', cursor='hand2')
        self.continue_btn.pack(side='right', padx=5)
        self.add_hover_effect(self.continue_btn, self.app.colors['secondary'],
                            self.app.colors['secondary_dark'])
    
    def validate_passengers(self):
        """Validate all passenger forms"""
        for i, passenger in enumerate(self.passenger_frames):
            # Get values
            name = passenger['name'].get().strip()
            age = passenger['age'].get().strip()
            gender = passenger['gender'].get()
            id_number = passenger['id_number'].get().strip()
            
            # Validate
            if not name:
                messagebox.showerror("Error", f"Please enter name for Passenger {i+1}")
                return False
            
            if not age:
                messagebox.showerror("Error", f"Please enter age for Passenger {i+1}")
                return False
            
            try:
                age_int = int(age)
                if age_int < 1 or age_int > 120:
                    messagebox.showerror("Error", f"Please enter valid age (1-120) for Passenger {i+1}")
                    return False
            except ValueError:
                messagebox.showerror("Error", f"Please enter valid age for Passenger {i+1}")
                return False
            
            if not id_number:
                messagebox.showerror("Error", f"Please enter ID number for Passenger {i+1}")
                return False
            
            # Check senior citizen concession
            if passenger['concession'].get():
                if age_int < 60:
                    if not messagebox.askyesno("Confirm", 
                        f"Passenger {i+1} is under 60. Senior citizen concession may not apply. Continue?"):
                        return False
        
        return True
    
    def save_passengers(self):
        """Save passenger data to app state"""
        passengers = []
        
        for passenger in self.passenger_frames:
            passenger_data = {
                'name': passenger['name'].get().strip(),
                'age': int(passenger['age'].get().strip()),
                'gender': passenger['gender'].get(),
                'id_type': passenger['id_type'].get(),
                'id_number': passenger['id_number'].get().strip(),
                'concession': passenger['concession'].get()
            }
            passengers.append(passenger_data)
        
        self.app.booking_details['passengers'] = passengers
        self.app.booking_details['passenger_count'] = len(passengers)
    
    def go_back(self):
        """Go back to train selection tab"""
        self.app.notebook.select(2)
    
    def go_to_payment(self):
        """Validate and go to payment tab"""
        if len(self.passenger_frames) == 0:
            messagebox.showerror("Error", "Please add at least one passenger")
            return
        
        if self.validate_passengers():
            self.save_passengers()
            self.update_fare_summary()
            self.app.notebook.select(4)
    
    def add_hover_effect(self, button, normal_color, hover_color):
        """Add hover effect to button"""
        def on_enter(e):
            button['background'] = hover_color
        
        def on_leave(e):
            button['background'] = normal_color
        
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
    
    def refresh(self):
        """Refresh the tab when accessed"""
        # Clear existing forms
        for passenger in self.passenger_frames:
            passenger['frame'].destroy()
        self.passenger_frames.clear()
        
        # Add first passenger
        self.add_passenger_form()
        
        # Update fare summary
        self.update_fare_summary()