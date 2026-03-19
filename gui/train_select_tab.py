"""
The Train Captain - Train Selection Tab
Handles class selection, quota, and berth preference
Software developed by Ashish Vishwakarma
Version: 3.0 Professional Edition
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class TrainSelectTab(tk.Frame):
    """Professional Train Selection Tab with Modern GUI"""
    
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        
        # Configure frame
        self.configure(bg=self.app.colors['background'])
        
        # Variables
        self.class_var = tk.StringVar()
        self.quota_var = tk.StringVar()
        self.berth_var = tk.StringVar()
        self.fare_var = tk.StringVar(value="₹ 0")
        self.available_classes = []
        
        # Create scrollable frame with professional styling
        self.create_professional_scrollable_frame()
        
        # Create UI
        self.create_professional_widgets()
    
    def create_professional_scrollable_frame(self):
        """Create a professional scrollable frame for content"""
        # Main container with shadow effect
        main_container = tk.Frame(self, bg=self.app.colors['surface'], 
                                 relief='solid', bd=1, highlightbackground=self.app.colors['border'])
        main_container.pack(fill='both', expand=True, padx=2, pady=2)
        
        # Create canvas and scrollbar
        self.canvas = tk.Canvas(main_container, bg=self.app.colors['background'], 
                               highlightthickness=0, bd=0)
        self.scrollbar = ttk.Scrollbar(main_container, orient="vertical", 
                                       command=self.canvas.yview, 
                                       style='Vertical.TScrollbar')
        self.scrollable_frame = tk.Frame(self.canvas, bg=self.app.colors['background'])
        
        # Configure canvas
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Create window inside canvas
        self.canvas_window = self.canvas.create_window((0, 0), 
                                                       window=self.scrollable_frame, 
                                                       anchor="nw")
        
        # Pack canvas and scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Bind configure events
        self.scrollable_frame.bind('<Configure>', self.on_frame_configure)
        self.canvas.bind('<Configure>', self.on_canvas_configure)
        
        # Bind mousewheel
        self.bind_mousewheel()
    
    def on_frame_configure(self, event):
        """Update scroll region when frame changes"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def on_canvas_configure(self, event):
        """Update canvas window width when canvas resizes"""
        self.canvas.itemconfig(self.canvas_window, width=event.width - 5)
    
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
    
    def create_professional_widgets(self):
        """Create all widgets with professional layout"""
        # Main container with centered content
        main_container = tk.Frame(self.scrollable_frame, bg=self.app.colors['background'])
        main_container.pack(fill='both', expand=True, padx=50, pady=30)
        
        # Header with title and developer credit
        self.create_header_section(main_container)
        
        # Train Details Card
        self.create_train_details_card(main_container)
        
        # Class Selection Card
        self.create_class_selection_card(main_container)
        
        # Quota Selection Card
        self.create_quota_selection_card(main_container)
        
        # Berth Preference Card
        self.create_berth_preference_card(main_container)
        
        # Fare Summary Card
        self.create_fare_summary_card(main_container)
        
        # Navigation Buttons
        self.create_navigation_buttons(main_container)
    
    def create_header_section(self, parent):
        """Create header with title and developer credit"""
        header_frame = tk.Frame(parent, bg=self.app.colors['background'])
        header_frame.pack(fill='x', pady=(0, 25))
        
        # Title with icon
        title_label = tk.Label(header_frame, 
                              text="🚂 SELECT TRAIN CLASS", 
                              font=('Segoe UI', 24, 'bold'),
                              fg=self.app.colors['primary'], 
                              bg=self.app.colors['background'])
        title_label.pack(side='left')
        
        # Developer badge
        dev_badge = tk.Label(header_frame, 
                            text="👨‍💻 Ashish Vishwakarma", 
                            font=('Segoe UI', 10),
                            fg=self.app.colors['text_light'], 
                            bg=self.app.colors['background'],
                            relief='solid', bd=1, padx=12, pady=4)
        dev_badge.pack(side='right')
    
    def create_train_details_card(self, parent):
        """Create train details card with glass morphism effect"""
        # Card container
        card = tk.Frame(parent, bg='white', relief='solid', bd=1,
                       highlightbackground=self.app.colors['border'])
        card.pack(fill='x', pady=(0, 20))
        
        # Card header with gradient effect
        header = tk.Frame(card, bg=self.app.colors['primary'], height=45)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        tk.Label(header, text="📋 Selected Train Details", 
                font=('Segoe UI', 12, 'bold'),
                fg='white', bg=self.app.colors['primary']).pack(side='left', padx=20)
        
        # Card content with grid layout
        content = tk.Frame(card, bg='white')
        content.pack(padx=25, pady=20, fill='x')
        
        # Configure grid for 2 columns
        content.columnconfigure(0, weight=1)
        content.columnconfigure(1, weight=2)
        
        # Train details with icons
        if self.app.selected_train:
            train = self.app.selected_train
            
            details = [
                ("🚆 Train Name:", train['train_name']),
                ("🔢 Train Number:", train['train_number']),
                ("📍 From:", train['source']),
                ("🎯 To:", train['destination']),
                ("📅 Journey Date:", self.app.booking_details.get('journey_date', 'N/A')),
                ("⏰ Departure:", train['departure']),
                ("⌛ Arrival:", train['arrival']),
                ("⏱️ Duration:", train['duration'])
            ]
            
            for i, (label, value) in enumerate(details):
                # Label column
                tk.Label(content, text=label, 
                        font=('Segoe UI', 10, 'bold'),
                        fg=self.app.colors['text'], 
                        bg='white').grid(row=i, column=0, sticky='w', pady=3)
                
                # Value column
                tk.Label(content, text=value, 
                        font=('Segoe UI', 10),
                        fg=self.app.colors['primary'], 
                        bg='white').grid(row=i, column=1, sticky='w', pady=3, padx=(10, 0))
    
    def create_class_selection_card(self, parent):
        """Create class selection card with modern options"""
        card = tk.Frame(parent, bg='white', relief='solid', bd=1,
                       highlightbackground=self.app.colors['border'])
        card.pack(fill='x', pady=(0, 20))
        
        # Card header
        header = tk.Frame(card, bg=self.app.colors['secondary'], height=45)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        tk.Label(header, text="🪑 Select Class", 
                font=('Segoe UI', 12, 'bold'),
                fg='white', bg=self.app.colors['secondary']).pack(side='left', padx=20)
        
        # Card content
        content = tk.Frame(card, bg='white')
        content.pack(padx=25, pady=20, fill='x')
        
        # Class options with descriptions
        classes = [
            ("1A", "First AC", "Luxury AC coaches with private cabins", "₹2,500 - ₹4,500", "⭐ 5"),
            ("2A", "Second AC", "AC coaches with 2-tier berths", "₹1,500 - ₹2,500", "⭐ 4"),
            ("3A", "Third AC", "AC coaches with 3-tier berths", "₹1,000 - ₹1,800", "⭐ 3"),
            ("SL", "Sleeper", "Non-AC sleeper coaches", "₹400 - ₹800", "⭐ 3"),
            ("CC", "Chair Car", "AC chair car seating", "₹800 - ₹1,200", "⭐ 4"),
            ("2S", "Second Sitting", "Non-AC chair car", "₹200 - ₹400", "⭐ 2")
        ]
        
        # Create grid for class options (2 columns)
        row_frame = tk.Frame(content, bg='white')
        row_frame.pack(fill='x')
        
        for i, (code, name, desc, price, rating) in enumerate(classes):
            col = i % 2
            if i % 2 == 0 and i > 0:
                row_frame = tk.Frame(content, bg='white')
                row_frame.pack(fill='x', pady=5)
            
            # Class card
            class_card = tk.Frame(row_frame, bg='white', relief='solid', bd=1,
                                 highlightbackground=self.app.colors['border'])
            class_card.pack(side='left', fill='both', expand=True, padx=5)
            
            # Radio button with class code
            radio_frame = tk.Frame(class_card, bg='white')
            radio_frame.pack(anchor='w', padx=10, pady=(10, 5))
            
            radio = tk.Radiobutton(radio_frame, text=f"{code} - {name}",
                                  variable=self.class_var, value=code,
                                  bg='white', fg=self.app.colors['text'],
                                  selectcolor='white',
                                  activebackground='white',
                                  font=('Segoe UI', 11, 'bold'),
                                  command=self.update_fare)
            radio.pack(side='left')
            
            # Rating badge
            tk.Label(radio_frame, text=rating, 
                    font=('Segoe UI', 9),
                    fg=self.app.colors['accent'], 
                    bg='white').pack(side='left', padx=(10, 0))
            
            # Description
            tk.Label(class_card, text=desc, 
                    font=('Segoe UI', 9),
                    fg=self.app.colors['text_light'], 
                    bg='white', wraplength=200).pack(anchor='w', padx=10, pady=2)
            
            # Price range
            tk.Label(class_card, text=price, 
                    font=('Segoe UI', 9, 'bold'),
                    fg=self.app.colors['success'], 
                    bg='white').pack(anchor='w', padx=10, pady=(5, 10))
            
            # Hover effect
            self.add_card_hover_effect(class_card)
    
    def create_quota_selection_card(self, parent):
        """Create quota selection card"""
        card = tk.Frame(parent, bg='white', relief='solid', bd=1,
                       highlightbackground=self.app.colors['border'])
        card.pack(fill='x', pady=(0, 20))
        
        # Card header
        header = tk.Frame(card, bg=self.app.colors['accent'], height=45)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        tk.Label(header, text="🎫 Select Quota", 
                font=('Segoe UI', 12, 'bold'),
                fg='white', bg=self.app.colors['accent']).pack(side='left', padx=20)
        
        # Card content
        content = tk.Frame(card, bg='white')
        content.pack(padx=25, pady=20, fill='x')
        
        # Quota options with icons
        quotas = [
            ("GN", "General Quota", "Standard quota for all passengers", "🟢 Available"),
            ("TQ", "Tatkal Quota", "Emergency bookings (higher fare)", "🟡 Limited"),
            ("LD", "Ladies Quota", "Exclusively for women passengers", "🟢 Available"),
            ("SS", "Senior Citizen", "For senior citizens with concession", "🟢 Available"),
            ("FT", "Foreign Tourist", "For foreign tourists", "🟡 Limited"),
            ("PH", "Physically Handicapped", "Special quota for disabled", "🟢 Available")
        ]
        
        # Create grid for quota options (2 columns)
        row_frame = tk.Frame(content, bg='white')
        row_frame.pack(fill='x')
        
        for i, (code, name, desc, status) in enumerate(quotas):
            col = i % 2
            if i % 2 == 0 and i > 0:
                row_frame = tk.Frame(content, bg='white')
                row_frame.pack(fill='x', pady=5)
            
            # Quota card
            quota_card = tk.Frame(row_frame, bg='white', relief='solid', bd=1,
                                 highlightbackground=self.app.colors['border'])
            quota_card.pack(side='left', fill='both', expand=True, padx=5)
            
            # Radio button
            radio_frame = tk.Frame(quota_card, bg='white')
            radio_frame.pack(anchor='w', padx=10, pady=(10, 5))
            
            radio = tk.Radiobutton(radio_frame, text=f"{code} - {name}",
                                  variable=self.quota_var, value=code,
                                  bg='white', fg=self.app.colors['text'],
                                  selectcolor='white',
                                  activebackground='white',
                                  font=('Segoe UI', 10, 'bold'),
                                  command=self.update_fare)
            radio.pack(side='left')
            
            # Status badge
            tk.Label(radio_frame, text=status, 
                    font=('Segoe UI', 8),
                    fg=self.app.colors['success'] if "Available" in status else self.app.colors['warning'], 
                    bg='white').pack(side='left', padx=(10, 0))
            
            # Description
            tk.Label(quota_card, text=desc, 
                    font=('Segoe UI', 9),
                    fg=self.app.colors['text_light'], 
                    bg='white', wraplength=200).pack(anchor='w', padx=10, pady=(0, 10))
            
            # Hover effect
            self.add_card_hover_effect(quota_card)
    
    def create_berth_preference_card(self, parent):
        """Create berth preference card"""
        card = tk.Frame(parent, bg='white', relief='solid', bd=1,
                       highlightbackground=self.app.colors['border'])
        card.pack(fill='x', pady=(0, 20))
        
        # Card header
        header = tk.Frame(card, bg=self.app.colors['info'], height=45)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        tk.Label(header, text="🛏️ Berth Preference (Optional)", 
                font=('Segoe UI', 12, 'bold'),
                fg='white', bg=self.app.colors['info']).pack(side='left', padx=20)
        
        # Card content
        content = tk.Frame(card, bg='white')
        content.pack(padx=25, pady=20, fill='x')
        
        # Berth options with icons
        berths = [
            ("L", "Lower Berth", "Easy access, preferred by senior citizens"),
            ("M", "Middle Berth", "Standard comfort"),
            ("U", "Upper Berth", "More privacy, less disturbance"),
            ("SU", "Side Upper", "Compact, near window"),
            ("SL", "Side Lower", "Convenient for short journeys"),
            ("N", "No Preference", "Auto-allocated by system")
        ]
        
        # Create grid for berth options (2 columns)
        row_frame = tk.Frame(content, bg='white')
        row_frame.pack(fill='x')
        
        for i, (code, name, desc) in enumerate(berths):
            col = i % 2
            if i % 2 == 0 and i > 0:
                row_frame = tk.Frame(content, bg='white')
                row_frame.pack(fill='x', pady=5)
            
            # Berth card
            berth_card = tk.Frame(row_frame, bg='white', relief='solid', bd=1,
                                 highlightbackground=self.app.colors['border'])
            berth_card.pack(side='left', fill='both', expand=True, padx=5)
            
            # Radio button
            radio = tk.Radiobutton(berth_card, text=f"{code} - {name}",
                                  variable=self.berth_var, value=code,
                                  bg='white', fg=self.app.colors['text'],
                                  selectcolor='white',
                                  activebackground='white',
                                  font=('Segoe UI', 10, 'bold'))
            radio.pack(anchor='w', padx=10, pady=(10, 5))
            
            # Description
            tk.Label(berth_card, text=desc, 
                    font=('Segoe UI', 8),
                    fg=self.app.colors['text_light'], 
                    bg='white', wraplength=200).pack(anchor='w', padx=10, pady=(0, 10))
            
            # Hover effect
            self.add_card_hover_effect(berth_card)
    
    def create_fare_summary_card(self, parent):
        """Create fare summary card"""
        card = tk.Frame(parent, bg='white', relief='solid', bd=1,
                       highlightbackground=self.app.colors['border'])
        card.pack(fill='x', pady=(0, 20))
        
        # Card header
        header = tk.Frame(card, bg=self.app.colors['success'], height=45)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        tk.Label(header, text="💰 Fare Summary", 
                font=('Segoe UI', 12, 'bold'),
                fg='white', bg=self.app.colors['success']).pack(side='left', padx=20)
        
        # Card content
        content = tk.Frame(card, bg='white')
        content.pack(padx=25, pady=20, fill='x')
        
        # Configure grid
        content.columnconfigure(0, weight=1)
        content.columnconfigure(1, weight=1)
        
        # Fare display with modern styling
        fare_display = tk.Frame(content, bg='white')
        fare_display.pack(fill='x', pady=5)
        
        # Base fare
        base_frame = tk.Frame(fare_display, bg='white')
        base_frame.pack(fill='x', pady=2)
        
        tk.Label(base_frame, text="Base Fare (per passenger):",
                font=('Segoe UI', 11), fg=self.app.colors['text'],
                bg='white').pack(side='left')
        
        self.base_fare_label = tk.Label(base_frame, text="₹ 0",
                                       font=('Segoe UI', 11, 'bold'),
                                       fg=self.app.colors['primary'],
                                       bg='white')
        self.base_fare_label.pack(side='right')
        
        # Quota charges
        quota_frame = tk.Frame(fare_display, bg='white')
        quota_frame.pack(fill='x', pady=2)
        
        tk.Label(quota_frame, text="Quota Charges:",
                font=('Segoe UI', 11), fg=self.app.colors['text'],
                bg='white').pack(side='left')
        
        self.quota_charges_label = tk.Label(quota_frame, text="₹ 0",
                                           font=('Segoe UI', 11),
                                           fg=self.app.colors['text_light'],
                                           bg='white')
        self.quota_charges_label.pack(side='right')
        
        # GST
        gst_frame = tk.Frame(fare_display, bg='white')
        gst_frame.pack(fill='x', pady=2)
        
        tk.Label(gst_frame, text="GST (5%):",
                font=('Segoe UI', 11), fg=self.app.colors['text'],
                bg='white').pack(side='left')
        
        self.gst_label = tk.Label(gst_frame, text="₹ 0",
                                 font=('Segoe UI', 11),
                                 fg=self.app.colors['text_light'],
                                 bg='white')
        self.gst_label.pack(side='right')
        
        # Separator
        separator = ttk.Separator(fare_display, orient='horizontal')
        separator.pack(fill='x', pady=10)
        
        # Total fare
        total_frame = tk.Frame(fare_display, bg='white')
        total_frame.pack(fill='x', pady=5)
        
        tk.Label(total_frame, text="Total Fare (per passenger):",
                font=('Segoe UI', 12, 'bold'), fg=self.app.colors['text'],
                bg='white').pack(side='left')
        
        self.total_fare_label = tk.Label(total_frame, text="₹ 0",
                                        font=('Segoe UI', 16, 'bold'),
                                        fg=self.app.colors['success'],
                                        bg='white')
        self.total_fare_label.pack(side='right')
    
    def create_navigation_buttons(self, parent):
        """Create navigation buttons with professional styling"""
        nav_frame = tk.Frame(parent, bg=self.app.colors['background'])
        nav_frame.pack(fill='x', pady=20)
        
        # Configure grid for centered buttons
        nav_frame.columnconfigure(0, weight=1)
        nav_frame.columnconfigure(1, weight=1)
        nav_frame.columnconfigure(2, weight=1)
        
        # Back button
        back_btn = tk.Button(nav_frame, text="← BACK TO SEARCH",
                            command=self.go_back,
                            bg=self.app.colors['text_light'], fg='white',
                            font=('Segoe UI', 11, 'bold'), 
                            padx=30, pady=12, width=18,
                            relief='flat', cursor='hand2')
        back_btn.grid(row=0, column=0, padx=5)
        self.add_hover_effect(back_btn, self.app.colors['text_light'], self.app.colors['text'])
        
        # Continue button
        self.continue_btn = tk.Button(nav_frame, text="CONTINUE TO PASSENGERS →",
                                      command=self.go_to_passenger_tab,
                                      bg=self.app.colors['secondary'], fg='white',
                                      font=('Segoe UI', 12, 'bold'), 
                                      padx=40, pady=12, width=25,
                                      relief='flat', state='disabled', cursor='hand2')
        self.continue_btn.grid(row=0, column=2, padx=5)
        self.add_hover_effect(self.continue_btn, self.app.colors['secondary'],
                            self.app.colors['secondary_dark'])
    
    def add_card_hover_effect(self, card):
        """Add hover effect to cards"""
        def on_enter(e):
            card.config(relief='ridge', bd=2, highlightbackground=self.app.colors['primary'])
        
        def on_leave(e):
            card.config(relief='solid', bd=1, highlightbackground=self.app.colors['border'])
        
        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)
    
    def add_hover_effect(self, button, normal_color, hover_color):
        """Add hover effect to button"""
        def on_enter(e):
            button['background'] = hover_color
            button.config(cursor='hand2')
        
        def on_leave(e):
            button['background'] = normal_color
        
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
    
    def refresh(self):
        """Refresh the tab with current train data"""
        if self.app.selected_train:
            train = self.app.selected_train
            
            # Update train details will be handled by the card
            self.enable_available_classes(train.get('classes', []))
            
            # Clear previous selections
            self.class_var.set('')
            self.quota_var.set('')
            self.berth_var.set('')
            self.update_fare()
    
    def enable_available_classes(self, available_classes):
        """Enable only classes that are available for this train"""
        self.available_classes = available_classes
    
    def update_fare(self):
        """Update fare based on selected class and quota"""
        if not self.class_var.get() or not self.quota_var.get():
            if hasattr(self, 'continue_btn'):
                self.continue_btn.config(state='disabled')
            return
        
        # Get base fare from selected train
        train = self.app.selected_train
        if train and 'fare' in train:
            base_fare = train['fare'].get(self.class_var.get(), 500)
        else:
            base_fare = 500
        
        # Calculate quota charges
        quota_charges = 0
        if self.quota_var.get() == "TQ":  # Tatkal
            quota_charges = int(base_fare * 0.3)  # 30% extra
        elif self.quota_var.get() == "SS":  # Senior Citizen
            quota_charges = -int(base_fare * 0.4)  # 40% discount
        
        # Calculate GST
        subtotal = base_fare + quota_charges
        gst = int(subtotal * 0.05)
        total = subtotal + gst
        
        # Update labels
        self.base_fare_label.config(text=f"₹ {base_fare:,}")
        
        if quota_charges > 0:
            self.quota_charges_label.config(text=f"+ ₹ {quota_charges:,}", 
                                           fg=self.app.colors['danger'])
        elif quota_charges < 0:
            self.quota_charges_label.config(text=f"- ₹ {abs(quota_charges):,}", 
                                           fg=self.app.colors['success'])
        else:
            self.quota_charges_label.config(text="₹ 0", fg=self.app.colors['text_light'])
        
        self.gst_label.config(text=f"₹ {gst:,}")
        self.total_fare_label.config(text=f"₹ {total:,}")
        
        # Store fare details
        self.app.fare_details = {
            'base_fare': base_fare,
            'quota_charges': quota_charges,
            'gst': gst,
            'total': total
        }
        
        # Enable continue button
        self.continue_btn.config(state='normal')
    
    def go_back(self):
        """Go back to search tab"""
        self.app.notebook.select(1)
    
    def go_to_passenger_tab(self):
        """Save selections and go to passenger tab"""
        if not self.class_var.get():
            messagebox.showerror("Error", "Please select a class")
            return
        
        if not self.quota_var.get():
            messagebox.showerror("Error", "Please select a quota")
            return
        
        # Save selections to app state
        self.app.booking_details['class'] = self.class_var.get()
        self.app.booking_details['quota'] = self.quota_var.get()
        self.app.booking_details['berth_preference'] = self.berth_var.get() if self.berth_var.get() else None
        
        # Save fare details
        if self.app.fare_details:
            self.app.booking_details['fare_per_passenger'] = self.app.fare_details['total']
        
        # Go to passenger tab
        self.app.notebook.select(3)