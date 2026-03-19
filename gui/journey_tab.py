"""
The Train Captain - Journey/Search Tab
Handles train search and selection with enhanced UI
Software developed by Ashish Vishwakarma
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import random
import re

class JourneyTab(tk.Frame):
    """Enhanced Journey Search and Train Selection Tab with Professional GUI"""
    
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        
        # Configure frame
        self.configure(bg=self.app.colors['background'])
        
        # Initialize variables
        self.search_results = []
        self.selected_train_index = None
        self.train_var = tk.StringVar()
        self.continue_btn = None
        self.recent_searches = []
        
        # Create scrollable frame with enhanced scrolling
        self.create_scrollable_frame()
        
        # Create UI
        self.create_widgets()
    
    def create_scrollable_frame(self):
        """Create an enhanced scrollable frame for content"""
        # Main container with border
        main_container = tk.Frame(self, bg=self.app.colors['surface'], 
                                 relief='solid', bd=1, highlightbackground=self.app.colors['border'])
        main_container.pack(fill='both', expand=True, padx=1, pady=1)
        
        # Create canvas and scrollbar with modern styling
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
        
        # Enhanced mousewheel binding
        self.bind_mousewheel()
    
    def on_frame_configure(self, event):
        """Update scroll region when frame changes"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def on_canvas_configure(self, event):
        """Update canvas window width when canvas resizes"""
        self.canvas.itemconfig(self.canvas_window, width=event.width - 5)
    
    def bind_mousewheel(self):
        """Enhanced mousewheel binding with smooth scrolling"""
        def on_mousewheel(event):
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        def on_shift_mousewheel(event):
            self.canvas.xview_scroll(int(-1*(event.delta/120)), "units")
        
        def on_enter(event):
            self.canvas.bind_all("<MouseWheel>", on_mousewheel)
            self.canvas.bind_all("<Shift-MouseWheel>", on_shift_mousewheel)
        
        def on_leave(event):
            self.canvas.unbind_all("<MouseWheel>")
            self.canvas.unbind_all("<Shift-MouseWheel>")
        
        self.canvas.bind("<Enter>", on_enter)
        self.canvas.bind("<Leave>", on_leave)
    
    def create_widgets(self):
        """Create all widgets for journey search"""
        # Main container with consistent padding
        main_container = tk.Frame(self.scrollable_frame, bg=self.app.colors['background'])
        main_container.pack(fill='both', expand=True, padx=30, pady=30)
        
        # Title with developer credit
        title_frame = tk.Frame(main_container, bg=self.app.colors['background'])
        title_frame.pack(fill='x', pady=(0, 20))
        
        title_label = tk.Label(title_frame, text="🔍 Search Trains", 
                              font=('Segoe UI', 24, 'bold'),
                              fg=self.app.colors['primary'], bg=self.app.colors['background'])
        title_label.pack(side='left')
        
        # Developer badge
        dev_badge = tk.Label(title_frame, text="👨‍💻 Ashish Vishwakarma", 
                            font=('Segoe UI', 10),
                            fg=self.app.colors['text_light'], bg=self.app.colors['background'],
                            relief='solid', bd=1, padx=10, pady=2)
        dev_badge.pack(side='right')
        
        # Search Section
        self.create_enhanced_search_section(main_container)
        
        # Quick Links Section
        self.create_quick_links(main_container)
        
        # Results Section
        self.create_enhanced_results_section(main_container)
    
    def create_enhanced_search_section(self, parent):
        """Create enhanced search input section"""
        search_frame = tk.Frame(parent, bg=self.app.colors['surface'],
                               relief='solid', bd=1, highlightbackground=self.app.colors['border'])
        search_frame.pack(fill='x', pady=(0, 20))
        
        # Header with icon
        header_frame = tk.Frame(search_frame, bg=self.app.colors['primary'], height=50)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="🚂 Journey Details", 
                font=('Segoe UI', 14, 'bold'),
                fg='white', bg=self.app.colors['primary']).pack(side='left', padx=15)
        
        # Form frame with grid layout
        form_frame = tk.Frame(search_frame, bg=self.app.colors['surface'])
        form_frame.pack(padx=30, pady=25, fill='x')
        
        # Configure grid - use integer weights
        form_frame.columnconfigure(0, weight=1)
        form_frame.columnconfigure(1, weight=0)  # For swap button
        form_frame.columnconfigure(2, weight=1)
        
        # Source
        source_frame = tk.Frame(form_frame, bg=self.app.colors['surface'])
        source_frame.grid(row=0, column=0, sticky='ew', padx=5)
        
        tk.Label(source_frame, text="📍 From Station:", 
                font=('Segoe UI', 11, 'bold'),
                fg=self.app.colors['text'], bg=self.app.colors['surface']).pack(anchor='w')
        
        source_combo = ttk.Combobox(source_frame, textvariable=self.app.source_var,
                                   font=('Segoe UI', 11), state='readonly')
        source_combo['values'] = self.get_stations()
        source_combo.pack(fill='x', pady=(5, 0), ipady=8)
        
        # Swap button
        swap_btn = tk.Label(form_frame, text="⇄", font=('Segoe UI', 16, 'bold'),
                           fg=self.app.colors['primary'], bg=self.app.colors['surface'],
                           cursor='hand2')
        swap_btn.grid(row=0, column=1, padx=10)
        swap_btn.bind('<Button-1>', lambda e: self.swap_stations())
        
        # Destination
        dest_frame = tk.Frame(form_frame, bg=self.app.colors['surface'])
        dest_frame.grid(row=0, column=2, sticky='ew', padx=5)
        
        tk.Label(dest_frame, text="🎯 To Station:", 
                font=('Segoe UI', 11, 'bold'),
                fg=self.app.colors['text'], bg=self.app.colors['surface']).pack(anchor='w')
        
        dest_combo = ttk.Combobox(dest_frame, textvariable=self.app.destination_var,
                                 font=('Segoe UI', 11), state='readonly')
        dest_combo['values'] = self.get_stations()
        dest_combo.pack(fill='x', pady=(5, 0), ipady=8)
        
        # Journey Date (second row)
        date_frame = tk.Frame(form_frame, bg=self.app.colors['surface'])
        date_frame.grid(row=1, column=0, columnspan=3, sticky='ew', pady=15)
        
        tk.Label(date_frame, text="📅 Journey Date:", 
                font=('Segoe UI', 11, 'bold'),
                fg=self.app.colors['text'], bg=self.app.colors['surface']).pack(anchor='w')
        
        # Date input with calendar icon
        date_input_frame = tk.Frame(date_frame, bg='white', relief='solid', bd=1)
        date_input_frame.pack(fill='x', pady=(5, 0))
        
        tk.Label(date_input_frame, text="📅", bg='white', 
                font=('Segoe UI', 11)).pack(side='left', padx=5)
        
        date_entry = tk.Entry(date_input_frame, textvariable=self.app.journey_date_var,
                             font=('Segoe UI', 11), bg='white',
                             relief='flat', highlightthickness=0)
        date_entry.pack(side='left', fill='x', expand=True, ipady=8)
        
        # Quick date buttons
        quick_date_frame = tk.Frame(date_frame, bg=self.app.colors['surface'])
        quick_date_frame.pack(fill='x', pady=(10, 0))
        
        today = datetime.now()
        dates = [
            ("Today", today.strftime("%d-%m-%Y")),
            ("Tomorrow", (today + timedelta(days=1)).strftime("%d-%m-%Y")),
            ("Day After", (today + timedelta(days=2)).strftime("%d-%m-%Y"))
        ]
        
        for label, date_val in dates:
            btn = tk.Button(quick_date_frame, text=label,
                          command=lambda d=date_val: self.app.journey_date_var.set(d),
                          bg=self.app.colors['background'], fg=self.app.colors['primary'],
                          font=('Segoe UI', 9), padx=15, pady=3,
                          relief='flat', cursor='hand2')
            btn.pack(side='left', padx=2)
            self.add_hover_effect(btn, self.app.colors['background'], self.app.colors['primary_light'])
        
        # Date hint
        tk.Label(date_frame, text="Format: DD-MM-YYYY", 
                font=('Segoe UI', 9), fg=self.app.colors['text_light'],
                bg=self.app.colors['surface']).pack(anchor='w', pady=(5, 0))
        
        # Search button with icon
        button_frame = tk.Frame(form_frame, bg=self.app.colors['surface'])
        button_frame.grid(row=2, column=0, columnspan=3, pady=20)
        
        search_btn = tk.Button(button_frame, text="🔍 Search Trains", 
                              command=self.search_trains,
                              bg=self.app.colors['primary'], fg='white',
                              font=('Segoe UI', 14, 'bold'), 
                              padx=50, pady=12,
                              relief='flat', cursor='hand2')
        search_btn.pack()
        
        self.add_hover_effect(search_btn, self.app.colors['primary'], self.app.colors['primary_dark'])
    
    def create_quick_links(self, parent):
        """Create quick journey links section"""
        links_frame = tk.Frame(parent, bg=self.app.colors['surface'],
                              relief='solid', bd=1, highlightbackground=self.app.colors['border'])
        links_frame.pack(fill='x', pady=(0, 20))
        
        # Header
        header_frame = tk.Frame(links_frame, bg=self.app.colors['secondary'], height=40)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="⚡ Quick Journeys", 
                font=('Segoe UI', 12, 'bold'),
                fg='white', bg=self.app.colors['secondary']).pack(side='left', padx=15)
        
        # Quick links
        links_content = tk.Frame(links_frame, bg=self.app.colors['surface'])
        links_content.pack(padx=20, pady=15, fill='x')
        
        # Configure grid for quick links (3 columns)
        for i in range(3):
            links_content.columnconfigure(i, weight=1)
        
        popular_routes = [
            ("Mumbai (CST) → Delhi (NDLS)", "Mumbai (CST)", "Delhi (NDLS)"),
            ("Delhi (NDLS) → Mumbai (CST)", "Delhi (NDLS)", "Mumbai (CST)"),
            ("Chennai (MAS) → Bangalore (SBC)", "Chennai (MAS)", "Bangalore (SBC)"),
            ("Kolkata (HWH) → Delhi (NDLS)", "Kolkata (HWH)", "Delhi (NDLS)"),
            ("Pune (PUNE) → Mumbai (CST)", "Pune (PUNE)", "Mumbai (CST)"),
            ("Jaipur (JP) → Delhi (NDLS)", "Jaipur (JP)", "Delhi (NDLS)")
        ]
        
        for i, (route, source, dest) in enumerate(popular_routes):
            row = i // 3
            col = i % 3
            btn = tk.Button(links_content, text=route,
                          command=lambda s=source, d=dest: self.set_quick_route(s, d),
                          bg=self.app.colors['background'], fg=self.app.colors['text'],
                          font=('Segoe UI', 9), padx=10, pady=5,
                          relief='flat', cursor='hand2', wraplength=150)
            btn.grid(row=row, column=col, padx=3, pady=3, sticky='ew')
            self.add_hover_effect(btn, self.app.colors['background'], self.app.colors['primary_light'])
    
    def set_quick_route(self, source, destination):
        """Set source and destination from quick route"""
        self.app.source_var.set(source)
        self.app.destination_var.set(destination)
    
    def swap_stations(self):
        """Swap source and destination stations"""
        source = self.app.source_var.get()
        dest = self.app.destination_var.get()
        if source and dest:
            self.app.source_var.set(dest)
            self.app.destination_var.set(source)
    
    def create_enhanced_results_section(self, parent):
        """Create enhanced search results section"""
        # Results frame
        self.results_frame = tk.Frame(parent, bg=self.app.colors['surface'],
                                     relief='solid', bd=1, highlightbackground=self.app.colors['border'])
        self.results_frame.pack(fill='both', expand=True)
        
        # Results header with icon
        header_frame = tk.Frame(self.results_frame, bg=self.app.colors['primary'], height=50)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="🚆 Available Trains", 
                font=('Segoe UI', 14, 'bold'), 
                fg='white', bg=self.app.colors['primary']).pack(side='left', padx=15)
        
        # No results message
        self.no_results_frame = tk.Frame(self.results_frame, bg=self.app.colors['surface'])
        self.no_results_label = tk.Label(self.no_results_frame, 
                                        text="✨ No trains to display. Please search for trains.",
                                        font=('Segoe UI', 14), 
                                        fg=self.app.colors['text_light'],
                                        bg=self.app.colors['surface'])
        self.no_results_label.pack(pady=50)
        
        # Results container (will be populated dynamically)
        self.results_container = tk.Frame(self.results_frame, bg=self.app.colors['surface'])
        
        # Show no results initially
        self.no_results_frame.pack(fill='both', expand=True)
    
    def search_trains(self):
        """Enhanced search for trains based on criteria"""
        source = self.app.source_var.get()
        destination = self.app.destination_var.get()
        date = self.app.journey_date_var.get()
        
        # Validate inputs
        if not source or not destination or not date:
            messagebox.showerror("Error", "Please fill in all search fields")
            return
        
        if source == destination:
            messagebox.showerror("Error", "Source and destination cannot be the same")
            return
        
        # Validate date
        try:
            journey_date = datetime.strptime(date, "%d-%m-%Y")
            if journey_date.date() < datetime.now().date():
                if not messagebox.askyesno("Past Date", 
                    "Selected date is in the past. Do you want to continue?"):
                    return
        except ValueError:
            messagebox.showerror("Error", "Please enter date in DD-MM-YYYY format")
            return
        
        # Save to recent searches
        self.save_recent_search(source, destination, date)
        
        # Clear previous results
        for widget in self.results_container.winfo_children():
            widget.destroy()
        
        # Hide no results frame
        self.no_results_frame.pack_forget()
        
        # Show results container
        self.results_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Show loading indicator
        loading_label = tk.Label(self.results_container, text="🔍 Searching for trains...", 
                                font=('Segoe UI', 12), fg=self.app.colors['primary'],
                                bg=self.app.colors['surface'])
        loading_label.pack(pady=30)
        self.update()
        
        # Simulate search delay
        self.after(1000, lambda: self.display_search_results(source, destination, date, loading_label))
    
    def display_search_results(self, source, destination, date, loading_label):
        """Display search results after loading"""
        # Remove loading indicator
        loading_label.destroy()
        
        # Generate dummy train data
        self.search_results = self.generate_enhanced_trains(source, destination, date)
        
        if not self.search_results:
            # No results found
            self.results_container.pack_forget()
            self.no_results_label.config(text="🚫 No trains found for the selected route and date.")
            self.no_results_frame.pack(fill='both', expand=True)
            return
        
        # Display results count
        count_label = tk.Label(self.results_container, 
                              text=f"Found {len(self.search_results)} trains",
                              font=('Segoe UI', 11, 'italic'),
                              fg=self.app.colors['success'],
                              bg=self.app.colors['surface'])
        count_label.pack(anchor='w', pady=(0, 10))
        
        # Display enhanced results
        self.display_enhanced_train_results()
    
    def generate_enhanced_trains(self, source, destination, date):
        """Generate enhanced dummy train data"""
        trains = []
        
        # Extract station codes
        source_code = source.split('(')[-1].strip(')').split()[0]
        dest_code = destination.split('(')[-1].strip(')').split()[0]
        
        # Train types with icons
        train_types = [
            ("Shatabdi Express", 12000, ["1A", "2A", "CC"]),
            ("Rajdhani Express", 12300, ["1A", "2A", "3A"]),
            ("Duronto Express", 12200, ["1A", "2A", "3A", "SL"]),
            ("Superfast Express", 12800, ["2A", "3A", "SL", "CC"]),
            ("Express", 12600, ["2A", "3A", "SL", "CC"]),
            ("Mail Express", 13200, ["3A", "SL", "CC"]),
            ("Garib Rath", 12400, ["3A", "CC"]),
            ("Jan Shatabdi", 12050, ["CC", "2S"])
        ]
        
        # Generate 6-10 trains
        num_trains = random.randint(6, 10)
        selected_types = random.sample(train_types, min(num_trains, len(train_types)))
        
        for i, (train_name, base_num, available_classes) in enumerate(selected_types):
            train_num = base_num + i + random.randint(1, 99)
            
            # Generate realistic timings
            dep_hour = random.randint(5, 22)  # Trains between 5 AM and 10 PM
            dep_min = random.choice([0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55])
            dep_time = f"{dep_hour:02d}:{dep_min:02d}"
            
            # Journey duration (based on distance approximation)
            distance = random.randint(500, 2000)
            duration_hours = distance // 60
            duration_mins = random.choice([0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55])
            
            # Calculate arrival
            total_mins = dep_hour * 60 + dep_min + duration_hours * 60 + duration_mins
            total_mins = total_mins % (24 * 60)
            arr_hour = total_mins // 60
            arr_min = total_mins % 60
            arr_time = f"{arr_hour:02d}:{arr_min:02d}"
            
            # Days of operation
            all_days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
            num_days = random.randint(5, 7)
            days_run = random.sample(all_days, num_days)
            days_run.sort(key=lambda x: all_days.index(x))
            
            # Availability status
            avail_status = random.choices(
                ["Available", "Limited", "Waiting", "RAC"],
                weights=[60, 20, 15, 5]
            )[0]
            
            # Calculate fare based on distance
            base_fare_km = {
                '1A': 4.5, '2A': 2.8, '3A': 2.0, 'SL': 1.2, 'CC': 1.8, '2S': 0.8
            }
            
            fares = {}
            for cls in available_classes:
                fare = int(distance * base_fare_km.get(cls, 1.5))
                # Add randomness
                fare = fare + random.randint(-100, 100)
                fares[cls] = max(fare, 100)
            
            train = {
                'train_number': f"{train_num}",
                'train_name': f"{source_code}-{dest_code} {train_name}",
                'short_name': train_name,
                'source': source,
                'destination': destination,
                'departure': dep_time,
                'arrival': arr_time,
                'duration': f"{duration_hours}h {duration_mins}m",
                'distance': distance,
                'days_run': ", ".join(days_run),
                'classes': available_classes,
                'available': avail_status,
                'availability_percent': random.randint(40, 100),
                'fare': fares,
                'rating': round(random.uniform(3.5, 5.0), 1),
                'stops': random.randint(5, 20),
                'platform': random.randint(1, 8)
            }
            
            trains.append(train)
        
        # Sort by departure time and rating
        trains.sort(key=lambda x: (x['departure'], -x['rating']))
        
        return trains
    
    def display_enhanced_train_results(self):
        """Display enhanced search results with modern table"""
        # Clear results container
        for widget in self.results_container.winfo_children():
            if widget != self.results_container.children.get('!label'):  # Keep count label
                widget.destroy()
        
        # Create headers with icons - use integer weights (multiply by 2 to avoid floats)
        headers = [
            ("Select", 1), ("Train", 4), ("Departure", 2), ("Arrival", 2),
            ("Duration", 2), ("Classes", 3), ("Availability", 2), ("Fare", 2)
        ]
        
        header_frame = tk.Frame(self.results_container, bg=self.app.colors['primary'], height=50)
        header_frame.pack(fill='x', pady=(0, 10))
        header_frame.pack_propagate(False)
        
        # Configure grid columns with integer weights
        total_weight = sum(w for _, w in headers)
        for i, (_, weight) in enumerate(headers):
            # Convert weight to percentage of total for proportional sizing
            header_frame.columnconfigure(i, weight=weight)
        
        # Header labels with icons
        header_icons = ["🔘", "🚂", "⏰", "⌛", "⏱️", "🪑", "📊", "💰"]
        for i, ((text, _), icon) in enumerate(zip(headers, header_icons)):
            label = tk.Label(header_frame, text=f"{icon} {text}", 
                           font=('Segoe UI', 11, 'bold'),
                           fg='white', bg=self.app.colors['primary'])
            label.grid(row=0, column=i, padx=5, pady=15, sticky='w')
        
        # Create scrollable results area
        self.create_scrollable_results()
    
    def create_scrollable_results(self):
        """Create scrollable area for train results"""
        # Canvas and scrollbar for results
        results_canvas = tk.Canvas(self.results_container, bg=self.app.colors['surface'],
                                  highlightthickness=0, height=400)
        results_scrollbar = ttk.Scrollbar(self.results_container, orient="vertical",
                                         command=results_canvas.yview)
        results_inner = tk.Frame(results_canvas, bg=self.app.colors['surface'])
        
        results_canvas.configure(yscrollcommand=results_scrollbar.set)
        
        # Configure scrolling
        def on_inner_configure(e):
            results_canvas.configure(scrollregion=results_canvas.bbox("all"))
        
        results_inner.bind('<Configure>', on_inner_configure)
        
        # Create window
        results_canvas_window = results_canvas.create_window((0, 0), window=results_inner,
                                                            anchor="nw")
        
        def on_canvas_configure(e):
            results_canvas.itemconfig(results_canvas_window, width=e.width)
        
        results_canvas.bind('<Configure>', on_canvas_configure)
        
        # Bind mousewheel to results canvas
        def on_mousewheel(e):
            results_canvas.yview_scroll(int(-1*(e.delta/120)), "units")
        
        results_canvas.bind("<Enter>", lambda e: results_canvas.bind_all("<MouseWheel>", on_mousewheel))
        results_canvas.bind("<Leave>", lambda e: results_canvas.unbind_all("<MouseWheel>"))
        
        # Pack canvas and scrollbar
        results_canvas.pack(side="left", fill="both", expand=True)
        results_scrollbar.pack(side="right", fill="y")
        
        # Store radio variable
        self.train_var = tk.StringVar()
        
        # Display trains
        for idx, train in enumerate(self.search_results):
            self.create_enhanced_train_row(results_inner, train, idx)
        
        # Continue button
        self.create_continue_button(self.results_container)
    
    def create_enhanced_train_row(self, parent, train, index):
        """Create an enhanced train row with hover effects"""
        # Alternate row colors
        bg_color = '#f8f9fa' if index % 2 == 0 else 'white'
        
        row_frame = tk.Frame(parent, bg=bg_color, relief='solid', bd=1,
                            highlightbackground=self.app.colors['border'])
        row_frame.pack(fill='x', pady=2, padx=2)
        
        # Configure grid columns with integer weights (match header)
        weights = [1, 4, 2, 2, 2, 3, 2, 2]
        for i, w in enumerate(weights):
            row_frame.columnconfigure(i, weight=w)
        
        # Radio button for selection
        radio_frame = tk.Frame(row_frame, bg=bg_color)
        radio_frame.grid(row=0, column=0, padx=5, pady=10, sticky='w')
        
        radio = tk.Radiobutton(radio_frame, variable=self.train_var, value=str(index),
                              bg=bg_color, activebackground=bg_color,
                              command=lambda t=train: self.select_train(t),
                              selectcolor=self.app.colors['primary'])
        radio.pack()
        
        # Train info (with name and number)
        train_frame = tk.Frame(row_frame, bg=bg_color)
        train_frame.grid(row=0, column=1, padx=5, pady=10, sticky='w')
        
        # Train name with icon
        name_label = tk.Label(train_frame, text=train['train_name'], 
                            font=('Segoe UI', 10, 'bold'),
                            fg=self.app.colors['primary'], bg=bg_color)
        name_label.pack(anchor='w')
        
        # Train number and rating
        details_frame = tk.Frame(train_frame, bg=bg_color)
        details_frame.pack(anchor='w')
        
        tk.Label(details_frame, text=f"#{train['train_number']}", 
                font=('Segoe UI', 8), fg=self.app.colors['text_light'],
                bg=bg_color).pack(side='left')
        
        tk.Label(details_frame, text=f" ⭐ {train['rating']}", 
                font=('Segoe UI', 8), fg=self.app.colors['accent'],
                bg=bg_color).pack(side='left', padx=5)
        
        # Departure time
        dep_frame = tk.Frame(row_frame, bg=bg_color)
        dep_frame.grid(row=0, column=2, padx=5, pady=10, sticky='w')
        
        tk.Label(dep_frame, text=train['departure'], 
                font=('Segoe UI', 11, 'bold'),
                fg=self.app.colors['text'], bg=bg_color).pack(anchor='w')
        
        # Arrival time
        arr_frame = tk.Frame(row_frame, bg=bg_color)
        arr_frame.grid(row=0, column=3, padx=5, pady=10, sticky='w')
        
        tk.Label(arr_frame, text=train['arrival'], 
                font=('Segoe UI', 11, 'bold'),
                fg=self.app.colors['text'], bg=bg_color).pack(anchor='w')
        
        # Duration
        dur_frame = tk.Frame(row_frame, bg=bg_color)
        dur_frame.grid(row=0, column=4, padx=5, pady=10, sticky='w')
        
        tk.Label(dur_frame, text=train['duration'], 
                font=('Segoe UI', 10),
                fg=self.app.colors['text'], bg=bg_color).pack(anchor='w')
        
        tk.Label(dur_frame, text=f"{train['stops']} stops", 
                font=('Segoe UI', 8), fg=self.app.colors['text_light'],
                bg=bg_color).pack(anchor='w')
        
        # Classes
        classes_frame = tk.Frame(row_frame, bg=bg_color)
        classes_frame.grid(row=0, column=5, padx=5, pady=10, sticky='w')
        
        for cls in train['classes'][:3]:  # Show first 3 classes
            class_badge = tk.Frame(classes_frame, bg=self.app.colors['info'], relief='flat')
            class_badge.pack(side='left', padx=2)
            tk.Label(class_badge, text=cls, font=('Segoe UI', 8, 'bold'),
                    fg='white', bg=self.app.colors['info']).pack(padx=3, pady=1)
        
        if len(train['classes']) > 3:
            tk.Label(classes_frame, text=f"+{len(train['classes'])-3}", 
                    font=('Segoe UI', 8), fg=self.app.colors['text_light'],
                    bg=bg_color).pack(side='left')
        
        # Availability
        avail_frame = tk.Frame(row_frame, bg=bg_color)
        avail_frame.grid(row=0, column=6, padx=5, pady=10, sticky='w')
        
        # Availability status
        avail_colors = {
            'Available': self.app.colors['success'],
            'Limited': self.app.colors['warning'],
            'Waiting': self.app.colors['danger'],
            'RAC': self.app.colors['accent']
        }
        avail_color = avail_colors.get(train['available'], self.app.colors['info'])
        
        status_label = tk.Label(avail_frame, text=train['available'], 
                               font=('Segoe UI', 9, 'bold'),
                               fg=avail_color, bg=bg_color)
        status_label.pack(anchor='w')
        
        # Simple progress indicator
        if train['availability_percent']:
            progress_text = f"{train['availability_percent']}%"
            tk.Label(avail_frame, text=progress_text, 
                    font=('Segoe UI', 8),
                    fg=self.app.colors['text_light'], bg=bg_color).pack(anchor='w')
        
        # Fare
        fare_frame = tk.Frame(row_frame, bg=bg_color)
        fare_frame.grid(row=0, column=7, padx=5, pady=10, sticky='w')
        
        min_fare = min(train['fare'].values())
        tk.Label(fare_frame, text=f"₹{min_fare}", 
                font=('Segoe UI', 11, 'bold'),
                fg=self.app.colors['success'], bg=bg_color).pack(anchor='w')
        
        tk.Label(fare_frame, text="Starting from", 
                font=('Segoe UI', 8), fg=self.app.colors['text_light'],
                bg=bg_color).pack(anchor='w')
        
        # Add hover effect
        self.add_row_hover_effect(row_frame, bg_color, train)
    
    def add_row_hover_effect(self, row, normal_color, train):
        """Add hover effect to train row"""
        def on_enter(e):
            row.config(bg='#e8f4fd', relief='ridge', bd=2)
            for child in row.winfo_children():
                if isinstance(child, tk.Frame):
                    child.config(bg='#e8f4fd')
                    for grandchild in child.winfo_children():
                        if isinstance(grandchild, (tk.Label, tk.Frame)):
                            try:
                                grandchild.config(bg='#e8f4fd')
                            except:
                                pass
        
        def on_leave(e):
            row.config(bg=normal_color, relief='solid', bd=1)
            for child in row.winfo_children():
                if isinstance(child, tk.Frame):
                    child.config(bg=normal_color)
                    for grandchild in child.winfo_children():
                        if isinstance(grandchild, (tk.Label, tk.Frame)):
                            try:
                                grandchild.config(bg=normal_color)
                            except:
                                pass
        
        row.bind("<Enter>", on_enter)
        row.bind("<Leave>", on_leave)
        
        # Double click to select
        row.bind("<Double-Button-1>", lambda e: self.select_train(train))
    
    def create_continue_button(self, parent):
        """Create continue button with enhanced styling"""
        continue_frame = tk.Frame(parent, bg=self.app.colors['surface'])
        continue_frame.pack(fill='x', pady=20)
        
        self.continue_btn = tk.Button(continue_frame, 
                                     text="Continue to Select Train →",
                                     command=self.go_to_train_select,
                                     bg=self.app.colors['secondary'], fg='white',
                                     font=('Segoe UI', 12, 'bold'), 
                                     padx=40, pady=12,
                                     relief='flat', state='disabled', cursor='hand2')
        self.continue_btn.pack()
        
        self.add_hover_effect(self.continue_btn, self.app.colors['secondary'], 
                            self.app.colors['secondary_dark'])
    
    def select_train(self, train):
        """Handle train selection with animation"""
        self.app.selected_train = train
        self.app.booking_details['source'] = train['source']
        self.app.booking_details['destination'] = train['destination']
        self.app.booking_details['train_number'] = train['train_number']
        self.app.booking_details['train_name'] = train['train_name']
        
        # Enable continue button
        self.continue_btn.config(state='normal')
        
        # Show selection feedback
        self.show_selection_feedback(train)
    
    def show_selection_feedback(self, train):
        """Show brief feedback when train is selected"""
        feedback = tk.Toplevel(self)
        feedback.title("")
        feedback.geometry("300x100")
        feedback.configure(bg=self.app.colors['success'])
        feedback.overrideredirect(True)
        
        # Center on screen
        feedback.update_idletasks()
        x = (feedback.winfo_screenwidth() // 2) - (300 // 2)
        y = (feedback.winfo_screenheight() // 2) - (100 // 2)
        feedback.geometry(f'300x100+{x}+{y}')
        
        tk.Label(feedback, text="✓ Train Selected", 
                font=('Segoe UI', 14, 'bold'),
                fg='white', bg=self.app.colors['success']).pack(pady=20)
        
        tk.Label(feedback, text=train['train_name'][:30], 
                font=('Segoe UI', 10),
                fg='white', bg=self.app.colors['success']).pack()
        
        # Auto close
        self.after(1500, feedback.destroy)
    
    def go_to_train_select(self):
        """Navigate to train selection tab"""
        if self.app.selected_train:
            # Store journey date
            self.app.booking_details['journey_date'] = self.app.journey_date_var.get()
            
            # Go to train select tab
            self.app.notebook.select(2)
            
            # Refresh train select tab
            self.app.train_select_tab.refresh()
    
    def save_recent_search(self, source, destination, date):
        """Save search to recent searches"""
        search = f"{source} → {destination} ({date})"
        if search not in self.recent_searches:
            self.recent_searches.insert(0, search)
            if len(self.recent_searches) > 5:
                self.recent_searches.pop()
    
    def get_stations(self):
        """Get enhanced list of stations with codes"""
        return [
            "Mumbai (CST) - Chhatrapati Shivaji Terminus",
            "Delhi (NDLS) - New Delhi Railway Station",
            "Chennai (MAS) - Chennai Central",
            "Kolkata (HWH) - Howrah Junction",
            "Bangalore (SBC) - Krantivira Sangolli Rayanna",
            "Hyderabad (HYB) - Hyderabad Deccan",
            "Ahmedabad (ADI) - Ahmedabad Junction",
            "Pune (PUNE) - Pune Junction",
            "Jaipur (JP) - Jaipur Junction",
            "Lucknow (LKO) - Lucknow Charbagh",
            "Patna (PNBE) - Patna Junction",
            "Bhopal (BPL) - Bhopal Junction",
            "Chandigarh (CDG) - Chandigarh Junction",
            "Guwahati (GHY) - Guwahati Railway Station",
            "Thiruvananthapuram (TVC) - Trivandrum Central"
        ]
    
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
        """Refresh the tab when accessed"""
        # Clear previous selection
        self.train_var = tk.StringVar()
        if hasattr(self, 'continue_btn') and self.continue_btn:
            self.continue_btn.config(state='disabled')
        
        # Reset to no results view
        self.no_results_frame.pack(fill='both', expand=True)
        if hasattr(self, 'results_container'):
            self.results_container.pack_forget()