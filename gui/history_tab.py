"""
The Train Captain - Booking History Tab
Displays past bookings with search and filter options
Software developed by Ashish Vishwakarma
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import json
import calendar

class HistoryTab(tk.Frame):
    """Enhanced Booking History Tab with Professional GUI"""
    
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        
        # Configure frame
        self.configure(bg=self.app.colors['background'])
        
        # Initialize variables
        self.filter_var = tk.StringVar(value="All Time")
        self.search_var = tk.StringVar()
        self.sort_var = tk.StringVar(value="Newest First")
        self.bookings_container = None
        self.no_bookings_label = None
        self.stats_frame = None
        self.results_frame = None
        
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
        """Create all widgets for history display"""
        # Main container with consistent padding
        main_container = tk.Frame(self.scrollable_frame, bg=self.app.colors['background'])
        main_container.pack(fill='both', expand=True, padx=30, pady=30)
        
        # Title with developer credit
        title_frame = tk.Frame(main_container, bg=self.app.colors['background'])
        title_frame.pack(fill='x', pady=(0, 20))
        
        title_label = tk.Label(title_frame, text="📜 Booking History", 
                              font=('Segoe UI', 24, 'bold'),
                              fg=self.app.colors['primary'], bg=self.app.colors['background'])
        title_label.pack(side='left')
        
        # Developer badge
        dev_badge = tk.Label(title_frame, text="👨‍💻 Ashish Vishwakarma", 
                            font=('Segoe UI', 10),
                            fg=self.app.colors['text_light'], bg=self.app.colors['background'],
                            relief='solid', bd=1, padx=10, pady=2)
        dev_badge.pack(side='right')
        
        # Statistics Dashboard
        self.create_statistics_dashboard(main_container)
        
        # Filters Section
        self.create_enhanced_filters(main_container)
        
        # Bookings List Header
        self.create_bookings_header(main_container)
        
        # Bookings List Container
        self.create_bookings_list_container(main_container)
        
        # Populate bookings
        self.display_enhanced_bookings()
    
    def create_statistics_dashboard(self, parent):
        """Create enhanced statistics dashboard"""
        self.stats_frame = tk.Frame(parent, bg=self.app.colors['surface'],
                                   relief='solid', bd=1, highlightbackground=self.app.colors['border'])
        self.stats_frame.pack(fill='x', pady=(0, 20))
        
        # Header
        header_frame = tk.Frame(self.stats_frame, bg=self.app.colors['primary'], height=40)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="📊 Booking Statistics", 
                font=('Segoe UI', 12, 'bold'),
                fg='white', bg=self.app.colors['primary']).pack(side='left', padx=15)
        
        # Stats cards
        cards_frame = tk.Frame(self.stats_frame, bg=self.app.colors['surface'])
        cards_frame.pack(padx=20, pady=20, fill='x')
        
        # Configure grid for cards
        for i in range(4):
            cards_frame.columnconfigure(i, weight=1)
        
        # Calculate statistics
        total_bookings = len(self.app.bookings_history)
        total_spent = sum(b.get('total_fare', 0) for b in self.app.bookings_history)
        
        # Get current month bookings
        current_month = datetime.now().month
        current_year = datetime.now().year
        month_bookings = sum(1 for b in self.app.bookings_history 
                           if self.get_booking_month(b) == current_month 
                           and self.get_booking_year(b) == current_year)
        
        # Get average fare
        avg_fare = total_spent // total_bookings if total_bookings > 0 else 0
        
        stats = [
            ("🎫 Total Bookings", f"{total_bookings}", self.app.colors['primary']),
            ("💰 Total Spent", f"₹{total_spent:,}", self.app.colors['success']),
            ("📅 This Month", f"{month_bookings}", self.app.colors['accent']),
            ("📊 Average Fare", f"₹{avg_fare:,}", self.app.colors['secondary'])
        ]
        
        for i, (label, value, color) in enumerate(stats):
            card = tk.Frame(cards_frame, bg='white', relief='solid', bd=1,
                          highlightbackground=self.app.colors['border'])
            card.grid(row=0, column=i, padx=5, pady=5, sticky='nsew')
            
            tk.Label(card, text=label, font=('Segoe UI', 10),
                    fg=self.app.colors['text_light'], bg='white').pack(pady=(10, 0))
            
            tk.Label(card, text=value, font=('Segoe UI', 18, 'bold'),
                    fg=color, bg='white').pack(pady=(0, 10))
    
    def get_booking_month(self, booking):
        """Extract month from booking"""
        try:
            booking_time = booking.get('booking_time', '')
            if booking_time:
                return datetime.fromisoformat(booking_time).month
        except:
            pass
        return 0
    
    def get_booking_year(self, booking):
        """Extract year from booking"""
        try:
            booking_time = booking.get('booking_time', '')
            if booking_time:
                return datetime.fromisoformat(booking_time).year
        except:
            pass
        return 0
    
    def create_enhanced_filters(self, parent):
        """Create enhanced filter and search section"""
        filter_frame = tk.Frame(parent, bg=self.app.colors['surface'],
                               relief='solid', bd=1, highlightbackground=self.app.colors['border'])
        filter_frame.pack(fill='x', pady=(0, 20))
        
        # Header
        header_frame = tk.Frame(filter_frame, bg=self.app.colors['secondary'], height=40)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="🔍 Filter & Search", 
                font=('Segoe UI', 12, 'bold'),
                fg='white', bg=self.app.colors['secondary']).pack(side='left', padx=15)
        
        # Filter options
        options_frame = tk.Frame(filter_frame, bg=self.app.colors['surface'])
        options_frame.pack(padx=20, pady=20, fill='x')
        
        # Configure grid
        options_frame.columnconfigure(0, weight=1)
        options_frame.columnconfigure(1, weight=1)
        options_frame.columnconfigure(2, weight=1)
        options_frame.columnconfigure(3, weight=0)
        
        # Filter by time period
        period_frame = tk.Frame(options_frame, bg=self.app.colors['surface'])
        period_frame.grid(row=0, column=0, sticky='ew', padx=5)
        
        tk.Label(period_frame, text="📅 Time Period:", font=('Segoe UI', 10, 'bold'),
                fg=self.app.colors['text'], bg=self.app.colors['surface']).pack(anchor='w')
        
        periods = ["All Time", "Today", "This Week", "This Month", "This Year", "Last 30 Days"]
        
        period_combo = ttk.Combobox(period_frame, textvariable=self.filter_var,
                                   values=periods, state='readonly',
                                   font=('Segoe UI', 10), width=15)
        period_combo.pack(fill='x', pady=(5, 0))
        period_combo.bind('<<ComboboxSelected>>', lambda e: self.apply_filters())
        
        # Sort by
        sort_frame = tk.Frame(options_frame, bg=self.app.colors['surface'])
        sort_frame.grid(row=0, column=1, sticky='ew', padx=5)
        
        tk.Label(sort_frame, text="🔀 Sort By:", font=('Segoe UI', 10, 'bold'),
                fg=self.app.colors['text'], bg=self.app.colors['surface']).pack(anchor='w')
        
        sort_options = ["Newest First", "Oldest First", "Highest Fare", "Lowest Fare"]
        
        sort_combo = ttk.Combobox(sort_frame, textvariable=self.sort_var,
                                 values=sort_options, state='readonly',
                                 font=('Segoe UI', 10), width=15)
        sort_combo.pack(fill='x', pady=(5, 0))
        sort_combo.bind('<<ComboboxSelected>>', lambda e: self.apply_filters())
        
        # Search
        search_frame = tk.Frame(options_frame, bg=self.app.colors['surface'])
        search_frame.grid(row=0, column=2, sticky='ew', padx=5)
        
        tk.Label(search_frame, text="🔎 Search:", font=('Segoe UI', 10, 'bold'),
                fg=self.app.colors['text'], bg=self.app.colors['surface']).pack(anchor='w')
        
        # Search entry with icon
        search_entry_frame = tk.Frame(search_frame, bg='white', relief='solid', bd=1)
        search_entry_frame.pack(fill='x', pady=(5, 0))
        
        tk.Label(search_entry_frame, text="🔍", bg='white', 
                font=('Segoe UI', 10)).pack(side='left', padx=5)
        
        search_entry = tk.Entry(search_entry_frame, textvariable=self.search_var,
                               font=('Segoe UI', 10), bg='white',
                               relief='flat', highlightthickness=0)
        search_entry.pack(side='left', fill='x', expand=True, ipady=5)
        search_entry.bind('<KeyRelease>', lambda e: self.apply_filters())
        
        # Clear search button
        clear_btn = tk.Label(search_entry_frame, text="✕", bg='white',
                            font=('Segoe UI', 10), cursor='hand2')
        clear_btn.pack(side='right', padx=5)
        clear_btn.bind('<Button-1>', lambda e: [self.search_var.set(''), self.apply_filters()])
        
        # Refresh button
        refresh_btn = tk.Button(options_frame, text="⟳ Refresh",
                               command=self.refresh,
                               bg=self.app.colors['primary'], fg='white',
                               font=('Segoe UI', 10, 'bold'), 
                               padx=20, pady=8,
                               relief='flat', cursor='hand2')
        refresh_btn.grid(row=0, column=3, padx=5)
        self.add_hover_effect(refresh_btn, self.app.colors['primary'], self.app.colors['primary_dark'])
    
    def create_bookings_header(self, parent):
        """Create header for bookings list"""
        header_frame = tk.Frame(parent, bg=self.app.colors['surface'],
                               relief='solid', bd=1, highlightbackground=self.app.colors['border'])
        header_frame.pack(fill='x', pady=(0, 10))
        
        # Header content
        content_frame = tk.Frame(header_frame, bg=self.app.colors['surface'])
        content_frame.pack(padx=20, pady=15, fill='x')
        
        tk.Label(content_frame, text="📋 Your Bookings", 
                font=('Segoe UI', 14, 'bold'),
                fg=self.app.colors['primary'], bg=self.app.colors['surface']).pack(side='left')
        
        # Export button
        export_btn = tk.Button(content_frame, text="📥 Export",
                              command=self.export_bookings,
                              bg=self.app.colors['secondary'], fg='white',
                              font=('Segoe UI', 10), padx=15, pady=5,
                              relief='flat', cursor='hand2')
        export_btn.pack(side='right', padx=5)
        self.add_hover_effect(export_btn, self.app.colors['secondary'], self.app.colors['secondary_dark'])
    
    def create_bookings_list_container(self, parent):
        """Create container for bookings list"""
        self.bookings_container = tk.Frame(parent, bg=self.app.colors['background'])
        self.bookings_container.pack(fill='both', expand=True)
        
        # No bookings message
        self.no_bookings_label = tk.Label(self.bookings_container,
                                         text="✨ No booking history found",
                                         font=('Segoe UI', 14),
                                         fg=self.app.colors['text_light'],
                                         bg=self.app.colors['background'])
    
    def display_enhanced_bookings(self):
        """Display filtered bookings with enhanced layout"""
        # Clear existing widgets in container
        for widget in self.bookings_container.winfo_children():
            widget.destroy()
        
        # Get filtered and sorted bookings
        filtered_bookings = self.get_filtered_bookings()
        
        if not filtered_bookings:
            # Show no bookings message
            no_bookings = tk.Label(self.bookings_container,
                                  text="✨ No booking history found",
                                  font=('Segoe UI', 14),
                                  fg=self.app.colors['text_light'],
                                  bg=self.app.colors['background'])
            no_bookings.pack(expand=True, pady=50)
            return
        
        # Create header for list with gradient
        header_frame = tk.Frame(self.bookings_container, bg=self.app.colors['primary'], height=50)
        header_frame.pack(fill='x', pady=(0, 5))
        header_frame.pack_propagate(False)
        
        # Configure grid columns
        for i in range(8):
            header_frame.columnconfigure(i, weight=1)
        
        # Headers with icons
        headers = [
            ("🎫 PNR", 0),
            ("📅 Date", 1),
            ("🚂 Train", 2),
            ("📍 Route", 3),
            ("👥 Pax", 4),
            ("💰 Amount", 5),
            ("📊 Status", 6),
            ("⚡ Action", 7)
        ]
        
        for header, col in headers:
            tk.Label(header_frame, text=header, 
                    font=('Segoe UI', 11, 'bold'),
                    fg='white', bg=self.app.colors['primary']).grid(
                        row=0, column=col, padx=5, pady=15, sticky='w')
        
        # Create scrollable area for bookings
        canvas = tk.Canvas(self.bookings_container, bg=self.app.colors['background'],
                          highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.bookings_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.app.colors['background'])
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Add bookings
        for idx, booking in enumerate(filtered_bookings):
            self.create_enhanced_booking_row(scrollable_frame, booking, idx)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Add summary footer
        self.create_summary_footer(self.bookings_container, filtered_bookings)
    
    def create_enhanced_booking_row(self, parent, booking, index):
        """Create an enhanced booking row with card-like design"""
        # Alternate row colors with hover effect
        bg_color = '#f8f9fa' if index % 2 == 0 else 'white'
        
        row_frame = tk.Frame(parent, bg=bg_color, relief='solid', bd=1,
                            highlightbackground=self.app.colors['border'])
        row_frame.pack(fill='x', pady=2, padx=2)
        
        # Configure grid columns
        for i in range(8):
            row_frame.columnconfigure(i, weight=1)
        
        # Format date
        booking_time = booking.get('booking_time', '')
        if booking_time:
            try:
                dt = datetime.fromisoformat(booking_time)
                date_str = dt.strftime("%d %b %Y")
                time_str = dt.strftime("%H:%M")
            except:
                date_str = booking_time[:10]
                time_str = ""
        else:
            date_str = "N/A"
            time_str = ""
        
        # PNR with copy functionality
        pnr = booking.get('pnr', 'N/A')[:12]
        pnr_frame = tk.Frame(row_frame, bg=bg_color)
        pnr_frame.grid(row=0, column=0, padx=5, pady=10, sticky='w')
        
        pnr_label = tk.Label(pnr_frame, text=pnr,
                            font=('Segoe UI', 9, 'bold'), 
                            fg=self.app.colors['primary'],
                            bg=bg_color, cursor='hand2')
        pnr_label.pack()
        
        # Copy on click
        pnr_label.bind('<Button-1>', lambda e, p=pnr: self.copy_to_clipboard(p))
        
        # Date with time
        date_frame = tk.Frame(row_frame, bg=bg_color)
        date_frame.grid(row=0, column=1, padx=5, pady=10, sticky='w')
        
        tk.Label(date_frame, text=date_str, font=('Segoe UI', 9),
                fg=self.app.colors['text'], bg=bg_color).pack(anchor='w')
        
        if time_str:
            tk.Label(date_frame, text=time_str, font=('Segoe UI', 8),
                    fg=self.app.colors['text_light'], bg=bg_color).pack(anchor='w')
        
        # Train with number
        train_frame = tk.Frame(row_frame, bg=bg_color)
        train_frame.grid(row=0, column=2, padx=5, pady=10, sticky='w')
        
        train_name = booking.get('train_name', 'N/A')[:15]
        train_num = booking.get('train_number', '')
        
        tk.Label(train_frame, text=train_name, font=('Segoe UI', 9, 'bold'),
                fg=self.app.colors['text'], bg=bg_color).pack(anchor='w')
        
        if train_num:
            tk.Label(train_frame, text=train_num, font=('Segoe UI', 8),
                    fg=self.app.colors['text_light'], bg=bg_color).pack(anchor='w')
        
        # Route with icons
        route_frame = tk.Frame(row_frame, bg=bg_color)
        route_frame.grid(row=0, column=3, padx=5, pady=10, sticky='w')
        
        source = booking.get('source', 'N/A').split('(')[0].strip()[:10]
        dest = booking.get('destination', 'N/A').split('(')[0].strip()[:10]
        
        tk.Label(route_frame, text=source, font=('Segoe UI', 9),
                fg=self.app.colors['text'], bg=bg_color).pack(side='left')
        
        tk.Label(route_frame, text=" → ", font=('Segoe UI', 9, 'bold'),
                fg=self.app.colors['primary'], bg=bg_color).pack(side='left')
        
        tk.Label(route_frame, text=dest, font=('Segoe UI', 9),
                fg=self.app.colors['text'], bg=bg_color).pack(side='left')
        
        # Passengers
        passenger_count = booking.get('passenger_count', len(booking.get('passengers', [])))
        
        pax_frame = tk.Frame(row_frame, bg=bg_color)
        pax_frame.grid(row=0, column=4, padx=5, pady=10, sticky='w')
        
        tk.Label(pax_frame, text=str(passenger_count), font=('Segoe UI', 9, 'bold'),
                fg=self.app.colors['text'], bg=bg_color).pack(side='left')
        
        tk.Label(pax_frame, text=" pax", font=('Segoe UI', 9),
                fg=self.app.colors['text_light'], bg=bg_color).pack(side='left')
        
        # Amount with badge
        amount = booking.get('total_fare', 0)
        amount_color = self.app.colors['success'] if amount > 0 else self.app.colors['text']
        
        amount_frame = tk.Frame(row_frame, bg=bg_color)
        amount_frame.grid(row=0, column=5, padx=5, pady=10, sticky='w')
        
        tk.Label(amount_frame, text=f"₹{amount:,}", font=('Segoe UI', 9, 'bold'),
                fg=amount_color, bg=bg_color).pack()
        
        # Status with badge
        status = booking.get('status', 'Confirmed')
        status_colors = {
            'Confirmed': self.app.colors['success'],
            'Cancelled': self.app.colors['danger'],
            'Waiting': self.app.colors['warning'],
            'RAC': self.app.colors['accent']
        }
        status_color = status_colors.get(status, self.app.colors['success'])
        
        status_frame = tk.Frame(row_frame, bg=status_color, relief='flat')
        status_frame.grid(row=0, column=6, padx=5, pady=10, sticky='w')
        
        tk.Label(status_frame, text=f" {status} ", font=('Segoe UI', 8, 'bold'),
                fg='white', bg=status_color).pack(padx=5, pady=2)
        
        # Action buttons frame
        action_frame = tk.Frame(row_frame, bg=bg_color)
        action_frame.grid(row=0, column=7, padx=5, pady=10, sticky='w')
        
        # View button
        view_btn = tk.Button(action_frame, text="👁️",
                            command=lambda b=booking: self.view_enhanced_booking(b),
                            bg=self.app.colors['info'], fg='white',
                            font=('Segoe UI', 8), width=3, height=1,
                            relief='flat', cursor='hand2')
        view_btn.pack(side='left', padx=1)
        self.add_hover_effect(view_btn, self.app.colors['info'], self.app.colors['primary'])
        
        # Download button
        download_btn = tk.Button(action_frame, text="📥",
                               command=lambda b=booking: self.download_booking(b),
                               bg=self.app.colors['secondary'], fg='white',
                               font=('Segoe UI', 8), width=3, height=1,
                               relief='flat', cursor='hand2')
        download_btn.pack(side='left', padx=1)
        self.add_hover_effect(download_btn, self.app.colors['secondary'], 
                            self.app.colors['secondary_dark'])
        
        # Add hover effect to row
        self.add_row_hover_effect(row_frame, bg_color)
    
    def add_row_hover_effect(self, row, normal_color):
        """Add hover effect to booking row"""
        def on_enter(e):
            try:
                row.config(bg='#e3f2fd', relief='ridge', bd=2)
                for child in row.winfo_children():
                    if isinstance(child, tk.Frame):
                        child.config(bg='#e3f2fd')
                        for grandchild in child.winfo_children():
                            if isinstance(grandchild, (tk.Label, tk.Frame)):
                                try:
                                    grandchild.config(bg='#e3f2fd')
                                except:
                                    pass
            except:
                pass
        
        def on_leave(e):
            try:
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
            except:
                pass
        
        row.bind("<Enter>", on_enter)
        row.bind("<Leave>", on_leave)
    
    def create_summary_footer(self, parent, bookings):
        """Create summary footer with totals"""
        footer_frame = tk.Frame(parent, bg=self.app.colors['surface'],
                               relief='solid', bd=1, highlightbackground=self.app.colors['border'])
        footer_frame.pack(fill='x', pady=(10, 0))
        
        # Calculate totals
        total_bookings = len(bookings)
        total_amount = sum(b.get('total_fare', 0) for b in bookings)
        total_passengers = sum(b.get('passenger_count', len(b.get('passengers', []))) for b in bookings)
        
        # Footer content
        content_frame = tk.Frame(footer_frame, bg=self.app.colors['surface'])
        content_frame.pack(padx=20, pady=15, fill='x')
        
        tk.Label(content_frame, text=f"Showing {total_bookings} bookings", 
                font=('Segoe UI', 10, 'italic'),
                fg=self.app.colors['text_light'], bg=self.app.colors['surface']).pack(side='left')
        
        tk.Label(content_frame, text=f"Total Passengers: {total_passengers} | Total Amount: ₹{total_amount:,}",
                font=('Segoe UI', 10, 'bold'),
                fg=self.app.colors['primary'], bg=self.app.colors['surface']).pack(side='right')
    
    def copy_to_clipboard(self, text):
        """Copy text to clipboard"""
        self.clipboard_clear()
        self.append(text)
        messagebox.showinfo("Copied", f"PNR {text} copied to clipboard!")
    
    def download_booking(self, booking):
        """Download single booking as text file"""
        try:
            from tkinter import filedialog
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                initialfile=f"booking_{booking.get('pnr', 'unknown')}.txt"
            )
            
            if filename:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(self.format_booking_text(booking))
                messagebox.showinfo("Success", f"Booking saved as {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to download: {e}")
    
    def format_booking_text(self, booking):
        """Format booking as text"""
        lines = []
        lines.append("=" * 60)
        lines.append("                 THE TRAIN CAPTAIN")
        lines.append("                Booking Details")
        lines.append("=" * 60)
        lines.append("")
        lines.append(f"PNR: {booking.get('pnr', 'N/A')}")
        lines.append(f"Booking Date: {booking.get('booking_time', 'N/A')}")
        lines.append("")
        lines.append("-" * 60)
        lines.append("JOURNEY DETAILS")
        lines.append("-" * 60)
        lines.append(f"Train: {booking.get('train_name', 'N/A')} ({booking.get('train_number', 'N/A')})")
        lines.append(f"From: {booking.get('source', 'N/A')}")
        lines.append(f"To: {booking.get('destination', 'N/A')}")
        lines.append(f"Date: {booking.get('journey_date', 'N/A')}")
        lines.append(f"Class: {booking.get('class', 'N/A')}")
        lines.append(f"Quota: {booking.get('quota', 'N/A')}")
        lines.append("")
        lines.append("-" * 60)
        lines.append("PASSENGER DETAILS")
        lines.append("-" * 60)
        
        for i, p in enumerate(booking.get('passengers', []), 1):
            lines.append(f"{i}. {p.get('name', 'N/A')} - Age: {p.get('age', 'N/A')}, Gender: {p.get('gender', 'N/A')}")
        
        lines.append("")
        lines.append("-" * 60)
        lines.append(f"Total Fare: ₹{booking.get('total_fare', 0):,}")
        lines.append("=" * 60)
        lines.append("Software developed by Ashish Vishwakarma")
        
        return '\n'.join(lines)
    
    def export_bookings(self):
        """Export all bookings to CSV"""
        try:
            from tkinter import filedialog
            import csv
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                initialfile=f"bookings_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            )
            
            if filename:
                with open(filename, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    # Write header
                    writer.writerow(['PNR', 'Booking Date', 'Train', 'Train Number', 'From', 'To', 
                                   'Journey Date', 'Class', 'Quota', 'Passengers', 'Total Fare', 'Status'])
                    
                    # Write data
                    for booking in self.app.bookings_history:
                        writer.writerow([
                            booking.get('pnr', ''),
                            booking.get('booking_time', ''),
                            booking.get('train_name', ''),
                            booking.get('train_number', ''),
                            booking.get('source', ''),
                            booking.get('destination', ''),
                            booking.get('journey_date', ''),
                            booking.get('class', ''),
                            booking.get('quota', ''),
                            booking.get('passenger_count', len(booking.get('passengers', []))),
                            booking.get('total_fare', 0),
                            'Confirmed'
                        ])
                
                messagebox.showinfo("Success", f"Bookings exported to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export: {e}")
    
    def get_filtered_bookings(self):
        """Get filtered and sorted bookings based on criteria"""
        bookings = self.app.bookings_history.copy()
        
        if not bookings:
            return []
        
        # Apply time filter
        filter_value = self.filter_var.get()
        today = datetime.now().date()
        
        if filter_value == "Today":
            bookings = [b for b in bookings if self.is_today(b, today)]
        elif filter_value == "This Week":
            bookings = [b for b in bookings if self.is_this_week(b, today)]
        elif filter_value == "This Month":
            bookings = [b for b in bookings if self.is_this_month(b, today)]
        elif filter_value == "This Year":
            bookings = [b for b in bookings if self.is_this_year(b, today)]
        elif filter_value == "Last 30 Days":
            bookings = [b for b in bookings if self.is_last_30_days(b, today)]
        
        # Apply search filter
        search_term = self.search_var.get().lower().strip()
        if search_term:
            filtered = []
            for b in bookings:
                pnr = b.get('pnr', '').lower()
                train = b.get('train_name', '').lower()
                train_num = b.get('train_number', '').lower()
                source = b.get('source', '').lower()
                dest = b.get('destination', '').lower()
                
                if (search_term in pnr or 
                    search_term in train or 
                    search_term in train_num or
                    search_term in source or
                    search_term in dest):
                    filtered.append(b)
            bookings = filtered
        
        # Apply sorting
        sort_value = self.sort_var.get()
        
        if sort_value == "Newest First":
            bookings.sort(key=lambda x: x.get('booking_time', ''), reverse=True)
        elif sort_value == "Oldest First":
            bookings.sort(key=lambda x: x.get('booking_time', ''))
        elif sort_value == "Highest Fare":
            bookings.sort(key=lambda x: x.get('total_fare', 0), reverse=True)
        elif sort_value == "Lowest Fare":
            bookings.sort(key=lambda x: x.get('total_fare', 0))
        
        return bookings
    
    def is_today(self, booking, today):
        """Check if booking is from today"""
        booking_time = booking.get('booking_time', '')
        if booking_time:
            try:
                b_date = datetime.fromisoformat(booking_time).date()
                return b_date == today
            except:
                pass
        return False
    
    def is_this_week(self, booking, today):
        """Check if booking is from this week"""
        booking_time = booking.get('booking_time', '')
        if booking_time:
            try:
                b_date = datetime.fromisoformat(booking_time).date()
                week_ago = today - timedelta(days=7)
                return b_date >= week_ago
            except:
                pass
        return False
    
    def is_this_month(self, booking, today):
        """Check if booking is from this month"""
        booking_time = booking.get('booking_time', '')
        if booking_time:
            try:
                b_date = datetime.fromisoformat(booking_time).date()
                return b_date.month == today.month and b_date.year == today.year
            except:
                pass
        return False
    
    def is_this_year(self, booking, today):
        """Check if booking is from this year"""
        booking_time = booking.get('booking_time', '')
        if booking_time:
            try:
                b_date = datetime.fromisoformat(booking_time).date()
                return b_date.year == today.year
            except:
                pass
        return False
    
    def is_last_30_days(self, booking, today):
        """Check if booking is from last 30 days"""
        booking_time = booking.get('booking_time', '')
        if booking_time:
            try:
                b_date = datetime.fromisoformat(booking_time).date()
                days_ago = today - timedelta(days=30)
                return b_date >= days_ago
            except:
                pass
        return False
    
    def apply_filters(self):
        """Apply filters and refresh display"""
        self.display_enhanced_bookings()
    
    def view_enhanced_booking(self, booking):
        """View booking details in enhanced popup"""
        # Create popup window
        popup = tk.Toplevel(self)
        popup.title(f"Booking Details - {booking.get('pnr', 'N/A')}")
        popup.geometry("700x800")
        popup.configure(bg='white')
        
        # Make it modal
        popup.transient(self)
        popup.grab_set()
        
        # Center the popup
        popup.update_idletasks()
        x = (popup.winfo_screenwidth() // 2) - (700 // 2)
        y = (popup.winfo_screenheight() // 2) - (800 // 2)
        popup.geometry(f'700x800+{x}+{y}')
        
        # Create scrollable frame
        canvas = tk.Canvas(popup, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(popup, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='white')
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Header with gradient
        header = tk.Frame(scrollable_frame, bg=self.app.colors['primary'], height=80)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        tk.Label(header, text="🎫 Booking Details", 
                font=('Segoe UI', 18, 'bold'),
                fg='white', bg=self.app.colors['primary']).pack(pady=20)
        
        # Content with enhanced layout
        content = tk.Frame(scrollable_frame, bg='white')
        content.pack(fill='both', expand=True, padx=30, pady=30)
        
        # PNR Section
        pnr_section = tk.Frame(content, bg='white', relief='solid', bd=1,
                              highlightbackground=self.app.colors['border'])
        pnr_section.pack(fill='x', pady=(0, 20))
        
        pnr_header = tk.Frame(pnr_section, bg=self.app.colors['primary_light'], height=30)
        pnr_header.pack(fill='x')
        pnr_header.pack_propagate(False)
        
        tk.Label(pnr_header, text="📌 PNR Information", 
                font=('Segoe UI', 11, 'bold'),
                fg='white', bg=self.app.colors['primary_light']).pack(side='left', padx=10)
        
        pnr_content = tk.Frame(pnr_section, bg='white')
        pnr_content.pack(padx=20, pady=15, fill='x')
        
        # PNR with copy button
        pnr_row = tk.Frame(pnr_content, bg='white')
        pnr_row.pack(fill='x', pady=5)
        
        tk.Label(pnr_row, text="PNR:", font=('Segoe UI', 12, 'bold'),
                fg=self.app.colors['text'], bg='white').pack(side='left')
        
        pnr_label = tk.Label(pnr_row, text=booking.get('pnr', 'N/A'), 
                            font=('Segoe UI', 14, 'bold'),
                            fg=self.app.colors['primary'], bg='white')
        pnr_label.pack(side='left', padx=10)
        
        copy_btn = tk.Button(pnr_row, text="📋 Copy",
                            command=lambda: self.copy_to_clipboard(booking.get('pnr', '')),
                            bg=self.app.colors['info'], fg='white',
                            font=('Segoe UI', 9), padx=10, pady=2,
                            relief='flat', cursor='hand2')
        copy_btn.pack(side='left')
        self.add_hover_effect(copy_btn, self.app.colors['info'], self.app.colors['primary'])
        
        # Booking time
        booking_time = booking.get('booking_time', 'N/A')
        if booking_time != 'N/A':
            try:
                dt = datetime.fromisoformat(booking_time)
                booking_time = dt.strftime("%d %B %Y at %I:%M %p")
            except:
                pass
        
        tk.Label(pnr_content, text=f"Booked on: {booking_time}", 
                font=('Segoe UI', 10),
                fg=self.app.colors['text_light'], bg='white').pack(anchor='w', pady=5)
        
        # Journey Details Section
        self.create_detail_section(content, "🚂 Journey Details", [
            ("Train:", f"{booking.get('train_name', 'N/A')} ({booking.get('train_number', 'N/A')})"),
            ("From:", booking.get('source', 'N/A')),
            ("To:", booking.get('destination', 'N/A')),
            ("Journey Date:", booking.get('journey_date', 'N/A')),
            ("Class:", booking.get('class', 'N/A')),
            ("Quota:", booking.get('quota', 'N/A'))
        ])
        
        # Passenger Details Section
        passenger_section = self.create_detail_section(content, "👥 Passenger Details", [])
        
        passengers = booking.get('passengers', [])
        for i, p in enumerate(passengers, 1):
            p_frame = tk.Frame(passenger_section, bg='white', relief='solid', bd=1,
                              highlightbackground=self.app.colors['border'])
            p_frame.pack(fill='x', pady=5)
            
            # Passenger header
            p_header = tk.Frame(p_frame, bg=self.app.colors['background'])
            p_header.pack(fill='x')
            
            tk.Label(p_header, text=f"Passenger {i}", 
                    font=('Segoe UI', 10, 'bold'),
                    fg=self.app.colors['primary'], 
                    bg=self.app.colors['background']).pack(side='left', padx=10, pady=5)
            
            # Passenger details
            p_details = tk.Frame(p_frame, bg='white')
            p_details.pack(padx=20, pady=10, fill='x')
            
            details = [
                ("Name:", p.get('name', 'N/A')),
                ("Age:", str(p.get('age', 'N/A'))),
                ("Gender:", p.get('gender', 'N/A')),
                ("ID:", f"{p.get('id_type', 'N/A')} - {p.get('id_number', 'N/A')}")
            ]
            
            for label, value in details:
                row = tk.Frame(p_details, bg='white')
                row.pack(fill='x', pady=2)
                
                tk.Label(row, text=label, font=('Segoe UI', 9, 'bold'),
                        fg=self.app.colors['text'], bg='white', width=10, anchor='w').pack(side='left')
                
                tk.Label(row, text=value, font=('Segoe UI', 9),
                        fg=self.app.colors['text'], bg='white').pack(side='left', padx=5)
        
        # Fare Details Section
        self.create_detail_section(content, "💰 Fare Details", [
            ("Total Fare:", f"₹{booking.get('total_fare', 0):,}"),
            ("Payment Status:", "✅ Paid"),
            ("Booking Status:", "Confirmed")
        ])
        
        # Developer credit
        credit_frame = tk.Frame(content, bg='white')
        credit_frame.pack(fill='x', pady=20)
        
        tk.Label(credit_frame, 
                text="Software developed by Ashish Vishwakarma",
                font=('Segoe UI', 9, 'italic'),
                fg=self.app.colors['text_light'], bg='white').pack()
        
        # Close button
        close_btn = tk.Button(scrollable_frame, text="Close",
                             command=popup.destroy,
                             bg=self.app.colors['primary'], fg='white',
                             font=('Segoe UI', 11, 'bold'), 
                             padx=40, pady=10,
                             relief='flat', cursor='hand2')
        close_btn.pack(pady=20)
        self.add_hover_effect(close_btn, self.app.colors['primary'], self.app.colors['primary_dark'])
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def create_detail_section(self, parent, title, details):
        """Create a detail section with consistent styling"""
        section = tk.Frame(parent, bg='white', relief='solid', bd=1,
                          highlightbackground=self.app.colors['border'])
        section.pack(fill='x', pady=(0, 20))
        
        # Header
        header = tk.Frame(section, bg=self.app.colors['secondary'], height=30)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        tk.Label(header, text=title, font=('Segoe UI', 11, 'bold'),
                fg='white', bg=self.app.colors['secondary']).pack(side='left', padx=10)
        
        # Content
        content = tk.Frame(section, bg='white')
        content.pack(padx=20, pady=15, fill='x')
        
        for label, value in details:
            row = tk.Frame(content, bg='white')
            row.pack(fill='x', pady=2)
            
            tk.Label(row, text=label, font=('Segoe UI', 10, 'bold'),
                    fg=self.app.colors['text'], bg='white', width=15, anchor='w').pack(side='left')
            
            tk.Label(row, text=value, font=('Segoe UI', 10),
                    fg=self.app.colors['text'], bg='white').pack(side='left', padx=5)
        
        return content
    
    def refresh(self):
        """Refresh the history tab"""
        self.app.load_bookings()  # Reload from file
        self.display_enhanced_bookings()
    
    def add_hover_effect(self, button, normal_color, hover_color):
        """Add hover effect to button"""
        def on_enter(e):
            try:
                button['background'] = hover_color
                button.config(cursor='hand2')
            except:
                pass
        
        def on_leave(e):
            try:
                button['background'] = normal_color
            except:
                pass
        
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)