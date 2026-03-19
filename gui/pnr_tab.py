"""
The Train Captain - PNR Display Tab
Shows the generated ticket/PNR details with complete booking information
Software developed by Ashish Vishwakarma
Version: 3.0 Professional Edition
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import random
from pathlib import Path

class PNRTab(tk.Frame):
    """Professional PNR Display Tab - Shows complete generated ticket"""
    
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        
        # Configure frame
        self.configure(bg=self.app.colors['background'])
        
        # Create scrollable frame
        self.create_professional_scrollable_frame()
        
        # Create UI
        self.create_professional_widgets()
    
    def create_professional_scrollable_frame(self):
        """Create professional scrollable frame"""
        # Main container
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
        
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Bind configure events
        self.scrollable_frame.bind('<Configure>', self.on_frame_configure)
        self.canvas.bind('<Configure>', self.on_canvas_configure)
        
        # Bind mousewheel
        self.bind_mousewheel()
    
    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width - 5)
    
    def bind_mousewheel(self):
        def on_mousewheel(event):
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        def on_enter(event):
            self.canvas.bind_all("<MouseWheel>", on_mousewheel)
        
        def on_leave(event):
            self.canvas.unbind_all("<MouseWheel>")
        
        self.canvas.bind("<Enter>", on_enter)
        self.canvas.bind("<Leave>", on_leave)
    
    def create_professional_widgets(self):
        """Create all widgets for PNR display"""
        # Main container
        self.main_container = tk.Frame(self.scrollable_frame, bg=self.app.colors['background'])
        self.main_container.pack(fill='both', expand=True, padx=80, pady=60)
        
        # Header
        self.create_header()
        
        # Show appropriate content
        self.refresh()
    
    def create_header(self):
        """Create header section"""
        header_frame = tk.Frame(self.main_container, bg=self.app.colors['background'])
        header_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(header_frame, text="🎫 VIEW PNR", 
                font=('Segoe UI', 24, 'bold'),
                fg=self.app.colors['primary'], bg=self.app.colors['background']).pack(side='left')
        
        # Developer badge
        dev_badge = tk.Label(header_frame, 
                            text="👨‍💻 Ashish Vishwakarma", 
                            font=('Segoe UI', 10),
                            fg=self.app.colors['text_light'], 
                            bg=self.app.colors['background'],
                            relief='solid', bd=1, padx=12, pady=4)
        dev_badge.pack(side='right')
    
    def show_no_ticket_message(self):
        """Show professional message when no ticket is selected"""
        # Clear container but keep header
        for widget in self.main_container.winfo_children():
            if widget != self.main_container.children.get('!frame'):
                widget.destroy()
        
        # Create message frame
        message_frame = tk.Frame(self.main_container, bg='white', 
                                 relief='solid', bd=2,
                                 highlightbackground=self.app.colors['primary'])
        message_frame.pack(expand=True, padx=100, pady=100, fill='both')
        
        # Icon
        tk.Label(message_frame, text="🎫", font=('Segoe UI', 72),
                fg=self.app.colors['text_light'], bg='white').pack(pady=40)
        
        # Message
        tk.Label(message_frame, text="No Ticket to Display",
                font=('Segoe UI', 20, 'bold'),
                fg=self.app.colors['text'], bg='white').pack()
        
        tk.Label(message_frame, text="Complete a booking to view your e-ticket here",
                font=('Segoe UI', 12),
                fg=self.app.colors['text_light'], bg='white').pack(pady=10)
        
        # Book now button
        book_btn = tk.Button(message_frame, text="🔍 BOOK A TICKET NOW",
                            command=lambda: self.app.notebook.select(1),
                            bg=self.app.colors['primary'], fg='white',
                            font=('Segoe UI', 12, 'bold'), 
                            padx=40, pady=12, relief='flat', cursor='hand2')
        book_btn.pack(pady=30)
        self.add_hover_effect(book_btn, self.app.colors['primary'], self.app.colors['primary_dark'])
    
    def show_professional_ticket(self):
        """Display the complete ticket with all booking details"""
        print("=" * 50)
        print("PNR TAB: Showing professional ticket")
        
        # Clear container but keep header
        for widget in self.main_container.winfo_children():
            if widget != self.main_container.children.get('!frame'):
                widget.destroy()
        
        booking = self.app.booking_details
        train = self.app.selected_train
        
        print(f"PNR TAB: Booking details: {booking}")
        print(f"PNR TAB: Train details: {train}")
        print(f"PNR TAB: PNR: {booking.get('pnr')}")
        print(f"PNR TAB: Passengers: {booking.get('passengers')}")
        
        if not booking or not booking.get('pnr'):
            print("PNR TAB: No PNR found")
            self.show_no_ticket_message()
            return
        
        # Create main ticket container with scrollable content
        ticket_container = tk.Frame(self.main_container, bg='white', 
                                   relief='solid', bd=2, 
                                   highlightbackground=self.app.colors['primary'])
        ticket_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Create canvas for ticket content
        canvas = tk.Canvas(ticket_container, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(ticket_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='white')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # ========== TICKET HEADER ==========
        header_frame = tk.Frame(scrollable_frame, bg=self.app.colors['primary'], height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        title_frame = tk.Frame(header_frame, bg=self.app.colors['primary'])
        title_frame.pack(expand=True)
        
        tk.Label(title_frame, text="🚂", font=('Segoe UI', 28),
                fg='white', bg=self.app.colors['primary']).pack(side='left', padx=10)
        
        tk.Label(title_frame, text="THE TRAIN CAPTAIN", 
                font=('Segoe UI', 20, 'bold'),
                fg='white', bg=self.app.colors['primary']).pack(side='left')
        
        tk.Label(title_frame, text="RAILWAY E-TICKET", 
                font=('Segoe UI', 14),
                fg=self.app.colors['accent'], bg=self.app.colors['primary']).pack(side='left', padx=20)
        
        # ========== PNR SECTION ==========
        pnr_section = tk.Frame(scrollable_frame, bg='white')
        pnr_section.pack(fill='x', padx=30, pady=20)
        
        # Create two columns
        pnr_section.columnconfigure(0, weight=1)
        pnr_section.columnconfigure(1, weight=1)
        
        # Left side - PNR
        left_pnr = tk.Frame(pnr_section, bg='white')
        left_pnr.grid(row=0, column=0, sticky='w')
        
        tk.Label(left_pnr, text="PNR NUMBER", font=('Segoe UI', 11, 'bold'),
                fg=self.app.colors['text_light'], bg='white').pack(anchor='w')
        
        pnr_label = tk.Label(left_pnr, text=booking.get('pnr', 'N/A'), 
                            font=('Courier', 22, 'bold'),
                            fg=self.app.colors['primary'], bg='white', cursor='hand2')
        pnr_label.pack(anchor='w')
        
        # Copy on click
        pnr_label.bind('<Button-1>', lambda e: self.copy_pnr(booking.get('pnr', '')))
        tk.Label(left_pnr, text="(Click to copy)", font=('Segoe UI', 8),
                fg=self.app.colors['text_light'], bg='white').pack(anchor='w')
        
        # Right side - Date
        right_date = tk.Frame(pnr_section, bg='white')
        right_date.grid(row=0, column=1, sticky='e')
        
        tk.Label(right_date, text="BOOKING DATE & TIME", font=('Segoe UI', 11, 'bold'),
                fg=self.app.colors['text_light'], bg='white').pack(anchor='e')
        
        booking_time = booking.get('booking_time', '')
        if booking_time:
            try:
                dt = datetime.fromisoformat(booking_time)
                date_str = dt.strftime("%d %B %Y")
                time_str = dt.strftime("%I:%M %p")
            except:
                date_str = booking_time[:10]
                time_str = ""
        else:
            date_str = datetime.now().strftime("%d %B %Y")
            time_str = datetime.now().strftime("%I:%M %p")
        
        tk.Label(right_date, text=date_str, font=('Segoe UI', 14, 'bold'),
                fg=self.app.colors['text'], bg='white').pack(anchor='e')
        
        tk.Label(right_date, text=time_str, font=('Segoe UI', 12),
                fg=self.app.colors['text_light'], bg='white').pack(anchor='e')
        
        # Separator
        ttk.Separator(scrollable_frame, orient='horizontal').pack(fill='x', padx=30, pady=10)
        
        # ========== JOURNEY DETAILS ==========
        journey_section = tk.Frame(scrollable_frame, bg='white')
        journey_section.pack(fill='x', padx=30, pady=15)
        
        tk.Label(journey_section, text="🚂 JOURNEY DETAILS", 
                font=('Segoe UI', 16, 'bold'),
                fg=self.app.colors['primary'], bg='white').pack(anchor='w', pady=(0, 15))
        
        # Create grid for journey details
        journey_grid = tk.Frame(journey_section, bg='white')
        journey_grid.pack(fill='x')
        
        # Configure columns
        journey_grid.columnconfigure(0, weight=1)
        journey_grid.columnconfigure(1, weight=2)
        
        # Get train details
        train_name = booking.get('train_name', 'N/A')
        train_num = booking.get('train_number', 'N/A')
        source = booking.get('source', 'N/A')
        destination = booking.get('destination', 'N/A')
        journey_date = booking.get('journey_date', 'N/A')
        travel_class = booking.get('class', 'N/A')
        quota = booking.get('quota', 'N/A')
        berth_pref = booking.get('berth_preference', 'No Preference')
        
        # Train details from selected_train if available
        if train:
            departure = train.get('departure', 'N/A')
            arrival = train.get('arrival', 'N/A')
            duration = train.get('duration', 'N/A')
        else:
            departure = 'N/A'
            arrival = 'N/A'
            duration = 'N/A'
        
        # Row 1: Train Name
        tk.Label(journey_grid, text="Train Name:", 
                font=('Segoe UI', 11, 'bold'),
                fg=self.app.colors['text'], bg='white').grid(row=0, column=0, sticky='w', pady=3)
        tk.Label(journey_grid, text=f"{train_name} ({train_num})", 
                font=('Segoe UI', 11),
                fg=self.app.colors['text'], bg='white').grid(row=0, column=1, sticky='w', pady=3, padx=(10, 0))
        
        # Row 2: From
        tk.Label(journey_grid, text="From:", 
                font=('Segoe UI', 11, 'bold'),
                fg=self.app.colors['text'], bg='white').grid(row=1, column=0, sticky='w', pady=3)
        tk.Label(journey_grid, text=source, 
                font=('Segoe UI', 11),
                fg=self.app.colors['text'], bg='white').grid(row=1, column=1, sticky='w', pady=3, padx=(10, 0))
        
        # Row 3: To
        tk.Label(journey_grid, text="To:", 
                font=('Segoe UI', 11, 'bold'),
                fg=self.app.colors['text'], bg='white').grid(row=2, column=0, sticky='w', pady=3)
        tk.Label(journey_grid, text=destination, 
                font=('Segoe UI', 11),
                fg=self.app.colors['text'], bg='white').grid(row=2, column=1, sticky='w', pady=3, padx=(10, 0))
        
        # Row 4: Journey Date
        tk.Label(journey_grid, text="Journey Date:", 
                font=('Segoe UI', 11, 'bold'),
                fg=self.app.colors['text'], bg='white').grid(row=3, column=0, sticky='w', pady=3)
        tk.Label(journey_grid, text=journey_date, 
                font=('Segoe UI', 11),
                fg=self.app.colors['text'], bg='white').grid(row=3, column=1, sticky='w', pady=3, padx=(10, 0))
        
        # Row 5: Class
        tk.Label(journey_grid, text="Class:", 
                font=('Segoe UI', 11, 'bold'),
                fg=self.app.colors['text'], bg='white').grid(row=4, column=0, sticky='w', pady=3)
        tk.Label(journey_grid, text=travel_class, 
                font=('Segoe UI', 11),
                fg=self.app.colors['text'], bg='white').grid(row=4, column=1, sticky='w', pady=3, padx=(10, 0))
        
        # Row 6: Quota
        tk.Label(journey_grid, text="Quota:", 
                font=('Segoe UI', 11, 'bold'),
                fg=self.app.colors['text'], bg='white').grid(row=5, column=0, sticky='w', pady=3)
        tk.Label(journey_grid, text=quota, 
                font=('Segoe UI', 11),
                fg=self.app.colors['text'], bg='white').grid(row=5, column=1, sticky='w', pady=3, padx=(10, 0))
        
        # Row 7: Berth Preference
        tk.Label(journey_grid, text="Berth Preference:", 
                font=('Segoe UI', 11, 'bold'),
                fg=self.app.colors['text'], bg='white').grid(row=6, column=0, sticky='w', pady=3)
        tk.Label(journey_grid, text=berth_pref, 
                font=('Segoe UI', 11),
                fg=self.app.colors['text'], bg='white').grid(row=6, column=1, sticky='w', pady=3, padx=(10, 0))
        
        # Row 8: Departure
        tk.Label(journey_grid, text="Departure:", 
                font=('Segoe UI', 11, 'bold'),
                fg=self.app.colors['text'], bg='white').grid(row=7, column=0, sticky='w', pady=3)
        tk.Label(journey_grid, text=departure, 
                font=('Segoe UI', 11),
                fg=self.app.colors['text'], bg='white').grid(row=7, column=1, sticky='w', pady=3, padx=(10, 0))
        
        # Row 9: Arrival
        tk.Label(journey_grid, text="Arrival:", 
                font=('Segoe UI', 11, 'bold'),
                fg=self.app.colors['text'], bg='white').grid(row=8, column=0, sticky='w', pady=3)
        tk.Label(journey_grid, text=arrival, 
                font=('Segoe UI', 11),
                fg=self.app.colors['text'], bg='white').grid(row=8, column=1, sticky='w', pady=3, padx=(10, 0))
        
        # Row 10: Duration
        tk.Label(journey_grid, text="Duration:", 
                font=('Segoe UI', 11, 'bold'),
                fg=self.app.colors['text'], bg='white').grid(row=9, column=0, sticky='w', pady=3)
        tk.Label(journey_grid, text=duration, 
                font=('Segoe UI', 11),
                fg=self.app.colors['text'], bg='white').grid(row=9, column=1, sticky='w', pady=3, padx=(10, 0))
        
        # Separator
        ttk.Separator(scrollable_frame, orient='horizontal').pack(fill='x', padx=30, pady=15)
        
        # ========== PASSENGER DETAILS ==========
        passenger_section = tk.Frame(scrollable_frame, bg='white')
        passenger_section.pack(fill='x', padx=30, pady=15)
        
        tk.Label(passenger_section, text="👥 PASSENGER DETAILS", 
                font=('Segoe UI', 16, 'bold'),
                fg=self.app.colors['primary'], bg='white').pack(anchor='w', pady=(0, 15))
        
        # Get passengers
        passengers = booking.get('passengers', [])
        print(f"PNR TAB: Passengers to display: {passengers}")
        
        if not passengers:
            tk.Label(passenger_section, text="No passenger details available", 
                    font=('Segoe UI', 12, 'italic'),
                    fg=self.app.colors['text_light'], bg='white').pack(pady=10)
        else:
            # Create table
            table_frame = tk.Frame(passenger_section, bg='white')
            table_frame.pack(fill='x')
            
            # Table headers
            headers = ["S.No", "Name", "Age", "Gender", "ID Type", "ID Number", "Status"]
            header_colors = [self.app.colors['primary'], self.app.colors['primary_light'], 
                           self.app.colors['secondary'], self.app.colors['info'], 
                           self.app.colors['accent'], self.app.colors['success'], 
                           self.app.colors['warning']]
            
            header_frame = tk.Frame(table_frame, bg=self.app.colors['primary'], height=35)
            header_frame.pack(fill='x')
            header_frame.pack_propagate(False)
            
            # Configure columns
            for i in range(7):
                header_frame.columnconfigure(i, weight=1)
            
            for i, (header, color) in enumerate(zip(headers, header_colors)):
                tk.Label(header_frame, text=header, 
                        font=('Segoe UI', 10, 'bold'),
                        fg='white', bg=self.app.colors['primary']).grid(
                            row=0, column=i, padx=5, pady=8, sticky='w')
            
            # Passenger rows
            for i, passenger in enumerate(passengers, 1):
                # Alternate row colors
                row_color = '#f0f7ff' if i % 2 == 0 else 'white'
                row_frame = tk.Frame(table_frame, bg=row_color)
                row_frame.pack(fill='x', pady=1)
                
                # Configure columns
                for j in range(7):
                    row_frame.columnconfigure(j, weight=1)
                
                # S.No
                tk.Label(row_frame, text=str(i), 
                        font=('Segoe UI', 9, 'bold'),
                        fg=self.app.colors['primary'], 
                        bg=row_color).grid(row=0, column=0, padx=5, pady=8, sticky='w')
                
                # Name
                name = passenger.get('name', 'N/A')
                tk.Label(row_frame, text=name[:20], 
                        font=('Segoe UI', 9),
                        fg=self.app.colors['text'], 
                        bg=row_color).grid(row=0, column=1, padx=5, pady=8, sticky='w')
                
                # Age
                age = str(passenger.get('age', 'N/A'))
                tk.Label(row_frame, text=age, 
                        font=('Segoe UI', 9),
                        fg=self.app.colors['text'], 
                        bg=row_color).grid(row=0, column=2, padx=5, pady=8, sticky='w')
                
                # Gender
                gender = passenger.get('gender', 'N/A')
                tk.Label(row_frame, text=gender, 
                        font=('Segoe UI', 9),
                        fg=self.app.colors['text'], 
                        bg=row_color).grid(row=0, column=3, padx=5, pady=8, sticky='w')
                
                # ID Type
                id_type = passenger.get('id_type', 'N/A')
                tk.Label(row_frame, text=id_type[:12], 
                        font=('Segoe UI', 9),
                        fg=self.app.colors['text'], 
                        bg=row_color).grid(row=0, column=4, padx=5, pady=8, sticky='w')
                
                # ID Number
                id_num = passenger.get('id_number', 'N/A')
                tk.Label(row_frame, text=id_num[:15], 
                        font=('Segoe UI', 9),
                        fg=self.app.colors['text'], 
                        bg=row_color).grid(row=0, column=5, padx=5, pady=8, sticky='w')
                
                # Status with badge
                status_frame = tk.Frame(row_frame, bg=self.app.colors['success'], relief='flat')
                status_frame.grid(row=0, column=6, padx=5, pady=5, sticky='w')
                
                tk.Label(status_frame, text=" CONFIRMED ", 
                        font=('Segoe UI', 8, 'bold'),
                        fg='white', bg=self.app.colors['success']).pack()
        
        # Separator
        ttk.Separator(scrollable_frame, orient='horizontal').pack(fill='x', padx=30, pady=15)
        
        # ========== FARE DETAILS ==========
        fare_section = tk.Frame(scrollable_frame, bg='white')
        fare_section.pack(fill='x', padx=30, pady=15)
        
        tk.Label(fare_section, text="💰 FARE DETAILS", 
                font=('Segoe UI', 16, 'bold'),
                fg=self.app.colors['primary'], bg='white').pack(anchor='w', pady=(0, 15))
        
        fare_grid = tk.Frame(fare_section, bg='white')
        fare_grid.pack(fill='x')
        
        fare_grid.columnconfigure(0, weight=1)
        fare_grid.columnconfigure(1, weight=1)
        
        total_fare = booking.get('total_fare', 0)
        
        # Total Fare
        tk.Label(fare_grid, text="Total Fare:", 
                font=('Segoe UI', 14, 'bold'),
                fg=self.app.colors['text'], 
                bg='white').grid(row=0, column=0, sticky='w', pady=5)
        
        tk.Label(fare_grid, text=f"₹ {total_fare:,}", 
                font=('Segoe UI', 20, 'bold'),
                fg=self.app.colors['success'], 
                bg='white').grid(row=0, column=1, sticky='e', pady=5)
        
        # Payment Status
        tk.Label(fare_grid, text="Payment Status:", 
                font=('Segoe UI', 12),
                fg=self.app.colors['text'], 
                bg='white').grid(row=1, column=0, sticky='w', pady=5)
        
        tk.Label(fare_grid, text="✅ PAID", 
                font=('Segoe UI', 12, 'bold'),
                fg=self.app.colors['success'], 
                bg='white').grid(row=1, column=1, sticky='e', pady=5)
        
        # Separator
        ttk.Separator(scrollable_frame, orient='horizontal').pack(fill='x', padx=30, pady=15)
        
        # ========== TERMS & CONDITIONS ==========
        terms_section = tk.Frame(scrollable_frame, bg='white')
        terms_section.pack(fill='x', padx=30, pady=15)
        
        tk.Label(terms_section, text="📋 TERMS & CONDITIONS", 
                font=('Segoe UI', 12, 'bold'),
                fg=self.app.colors['primary'], bg='white').pack(anchor='w', pady=(0, 10))
        
        terms_text = tk.Text(terms_section, height=3, wrap='word',
                            font=('Segoe UI', 9), bg='#f8f9fa',
                            fg=self.app.colors['text'], relief='flat')
        terms_text.pack(fill='x')
        terms_text.insert('1.0', """• This e-ticket is valid only with a valid ID proof (Aadhar/PAN/Passport)
• Cancellation charges apply as per IRCTC rules
• Please arrive at least 2 hours before departure time""")
        terms_text.config(state='disabled')
        
        # ========== FOOTER ==========
        footer_frame = tk.Frame(scrollable_frame, bg=self.app.colors['background'], height=60)
        footer_frame.pack(fill='x', pady=20)
        footer_frame.pack_propagate(False)
        
        tk.Label(footer_frame, text="This is a computer generated e-ticket. No signature required.", 
                font=('Segoe UI', 10),
                fg=self.app.colors['text_light'], 
                bg=self.app.colors['background']).pack()
        
        tk.Label(footer_frame, text="Software developed by Ashish Vishwakarma", 
                font=('Segoe UI', 9, 'italic'),
                fg=self.app.colors['primary'], 
                bg=self.app.colors['background']).pack()
        
        # ========== ACTION BUTTONS ==========
        self.create_action_buttons(booking)
    
    def create_action_buttons(self, booking):
        """Create action buttons"""
        button_frame = tk.Frame(self.main_container, bg=self.app.colors['background'])
        button_frame.pack(fill='x', pady=20)
        
        # Configure grid for centered buttons
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        button_frame.columnconfigure(2, weight=1)
        button_frame.columnconfigure(3, weight=1)
        
        # Download button
        download_btn = tk.Button(button_frame, text="📥 DOWNLOAD",
                                command=lambda: self.download_ticket(booking),
                                bg=self.app.colors['primary'], fg='white',
                                font=('Segoe UI', 10, 'bold'), 
                                padx=20, pady=8, width=12,
                                relief='flat', cursor='hand2')
        download_btn.grid(row=0, column=0, padx=5)
        self.add_hover_effect(download_btn, self.app.colors['primary'], self.app.colors['primary_dark'])
        
        # Print button
        print_btn = tk.Button(button_frame, text="🖨️ PRINT",
                             command=self.print_ticket,
                             bg=self.app.colors['secondary'], fg='white',
                             font=('Segoe UI', 10, 'bold'), 
                             padx=20, pady=8, width=12,
                             relief='flat', cursor='hand2')
        print_btn.grid(row=0, column=1, padx=5)
        self.add_hover_effect(print_btn, self.app.colors['secondary'], self.app.colors['secondary_dark'])
        
        # Email button
        email_btn = tk.Button(button_frame, text="📧 EMAIL",
                             command=self.email_ticket,
                             bg=self.app.colors['info'], fg='white',
                             font=('Segoe UI', 10, 'bold'), 
                             padx=20, pady=8, width=12,
                             relief='flat', cursor='hand2')
        email_btn.grid(row=0, column=2, padx=5)
        self.add_hover_effect(email_btn, self.app.colors['info'], self.app.colors['primary'])
        
        # New booking button
        new_btn = tk.Button(button_frame, text="➕ NEW",
                           command=self.new_booking,
                           bg=self.app.colors['accent'], fg='white',
                           font=('Segoe UI', 10, 'bold'), 
                           padx=20, pady=8, width=12,
                           relief='flat', cursor='hand2')
        new_btn.grid(row=0, column=3, padx=5)
        self.add_hover_effect(new_btn, self.app.colors['accent'], self.app.colors['accent'])
    
    def copy_pnr(self, pnr):
        """Copy PNR to clipboard"""
        self.clipboard_clear()
        self.append(pnr)
        messagebox.showinfo("Copied", f"PNR {pnr} copied to clipboard!")
    
    def download_ticket(self, booking):
        """Download ticket as text file"""
        try:
            from tkinter import filedialog
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                initialfile=f"ticket_{booking.get('pnr', 'unknown')}.txt"
            )
            
            if filename:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(self.format_complete_ticket(booking))
                messagebox.showinfo("Success", f"Ticket downloaded as {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to download ticket: {e}")
    
    def format_complete_ticket(self, booking):
        """Format complete ticket with all details as text"""
        train = self.app.selected_train or {}
        passengers = booking.get('passengers', [])
        
        lines = []
        lines.append("=" * 100)
        lines.append("                                    THE TRAIN CAPTAIN")
        lines.append("                                   RAILWAY E-TICKET")
        lines.append("=" * 100)
        lines.append("")
        lines.append(f"PNR: {booking.get('pnr', 'N/A')}")
        lines.append(f"Booking Date: {booking.get('booking_time', 'N/A')}")
        lines.append("")
        lines.append("-" * 100)
        lines.append("JOURNEY DETAILS")
        lines.append("-" * 100)
        lines.append(f"Train: {booking.get('train_name', 'N/A')} ({booking.get('train_number', 'N/A')})")
        lines.append(f"From: {booking.get('source', 'N/A')}")
        lines.append(f"To: {booking.get('destination', 'N/A')}")
        lines.append(f"Journey Date: {booking.get('journey_date', 'N/A')}")
        lines.append(f"Class: {booking.get('class', 'N/A')}")
        lines.append(f"Quota: {booking.get('quota', 'N/A')}")
        lines.append(f"Berth Preference: {booking.get('berth_preference', 'No Preference')}")
        lines.append(f"Departure: {train.get('departure', 'N/A')}")
        lines.append(f"Arrival: {train.get('arrival', 'N/A')}")
        lines.append(f"Duration: {train.get('duration', 'N/A')}")
        lines.append("")
        lines.append("-" * 100)
        lines.append("PASSENGER DETAILS")
        lines.append("-" * 100)
        lines.append(f"{'S.No':<5} {'Name':<25} {'Age':<5} {'Gender':<8} {'ID Type':<15} {'ID Number':<20} {'Status':<10}")
        lines.append("-" * 100)
        
        for i, p in enumerate(passengers, 1):
            lines.append(f"{i:<5} {p.get('name', 'N/A'):<25} {p.get('age', 'N/A'):<5} "
                        f"{p.get('gender', 'N/A'):<8} {p.get('id_type', 'N/A'):<15} "
                        f"{p.get('id_number', 'N/A'):<20} {'CONFIRMED':<10}")
        
        lines.append("")
        lines.append("-" * 100)
        lines.append("FARE DETAILS")
        lines.append("-" * 100)
        lines.append(f"Total Fare: ₹ {booking.get('total_fare', 0):,}")
        lines.append("Payment Status: PAID")
        lines.append("")
        lines.append("-" * 100)
        lines.append("IMPORTANT INSTRUCTIONS:")
        lines.append("• This e-ticket is valid only with a valid ID proof")
        lines.append("• Cancellation charges apply as per IRCTC rules")
        lines.append("• Please arrive at least 2 hours before departure")
        lines.append("")
        lines.append("=" * 100)
        lines.append("                 Software developed by Ashish Vishwakarma")
        lines.append("=" * 100)
        
        return '\n'.join(lines)
    
    def print_ticket(self):
        """Print the ticket"""
        messagebox.showinfo("Print", "Print dialog will open.\nPlease check your printer settings.")
    
    def email_ticket(self):
        """Email the ticket"""
        email = self.app.user_data.get('email', '') if self.app.user_data else ''
        if email:
            messagebox.showinfo("Email", f"Ticket has been sent to {email}")
        else:
            messagebox.showwarning("Email", "No email address found in profile")
    
    def new_booking(self):
        """Start a new booking"""
        if messagebox.askyesno("New Booking", "Start a new booking? Current booking data will be cleared."):
            self.app.clear_booking_data()
            self.app.notebook.select(1)
            self.show_no_ticket_message()
    
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
        print("\n" + "="*50)
        print("PNR TAB REFRESH CALLED")
        print(f"Booking details: {self.app.booking_details}")
        print(f"PNR exists: {self.app.booking_details.get('pnr')}")
        print(f"Passengers: {self.app.booking_details.get('passengers')}")
        print("="*50 + "\n")
        
        if self.app.booking_details and self.app.booking_details.get('pnr'):
            print("PNR TAB: Showing ticket")
            self.show_professional_ticket()
        else:
            print("PNR TAB: No ticket, showing message")
            self.show_no_ticket_message()