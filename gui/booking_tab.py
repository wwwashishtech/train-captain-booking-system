"""
The Train Captain - Payment/Booking Tab
Handles payment processing and final booking confirmation
Software developed by Ashish Vishwakarma
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import random
import re

class BookingTab(tk.Frame):
    """Enhanced Payment and Booking Tab with Professional GUI"""
    
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        
        # Configure frame with gradient background
        self.configure(bg=self.app.colors['background'])
        
        # Initialize variables
        self.payment_method = tk.StringVar(value="card")
        self.card_number = None
        self.card_holder = None
        self.card_expiry = None
        self.card_cvv = None
        self.upi_id = None
        self.bank_combo = None
        self.wallet_combo = None
        self.terms_var = tk.BooleanVar()
        self.pay_btn = None
        
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
        
        # Create window inside canvas with proper anchoring
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
        """Enhanced mousewheel binding with better scrolling"""
        def on_mousewheel(event):
            # Smooth scrolling
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        def on_shift_mousewheel(event):
            # Horizontal scrolling with Shift key
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
        """Create all widgets for payment processing"""
        # Main container with consistent padding
        main_container = tk.Frame(self.scrollable_frame, bg=self.app.colors['background'])
        main_container.pack(fill='both', expand=True, padx=30, pady=30)
        
        # Title with developer credit
        title_frame = tk.Frame(main_container, bg=self.app.colors['background'])
        title_frame.pack(fill='x', pady=(0, 20))
        
        title_label = tk.Label(title_frame, text="Payment & Booking", 
                              font=('Segoe UI', 24, 'bold'),
                              fg=self.app.colors['primary'], bg=self.app.colors['background'])
        title_label.pack(side='left')
        
        # Developer badge
        dev_badge = tk.Label(title_frame, text="👨‍💻 Ashish Vishwakarma", 
                            font=('Segoe UI', 10),
                            fg=self.app.colors['text_light'], bg=self.app.colors['background'],
                            relief='solid', bd=1, padx=10, pady=2)
        dev_badge.pack(side='right')
        
        # Progress indicator
        self.create_progress_indicator(main_container)
        
        # Booking Summary Section
        self.create_booking_summary(main_container)
        
        # Fare Breakdown Section
        self.create_fare_breakdown(main_container)
        
        # Payment Methods Section
        self.create_payment_methods(main_container)
        
        # Payment Form Section (dynamic based on method)
        self.create_payment_form_section(main_container)
        
        # Terms and Conditions
        self.create_terms_section(main_container)
        
        # Action Buttons
        self.create_action_buttons(main_container)
        
        # Security badge
        self.create_security_badge(main_container)
    
    def create_progress_indicator(self, parent):
        """Create booking progress indicator"""
        progress_frame = tk.Frame(parent, bg=self.app.colors['surface'],
                                 relief='solid', bd=1, highlightbackground=self.app.colors['border'])
        progress_frame.pack(fill='x', pady=(0, 20))
        
        # Progress steps
        steps = [
            ("1", "Journey", "✓"),
            ("2", "Train", "✓"),
            ("3", "Passengers", "✓"),
            ("4", "Payment", "●"),
            ("5", "Ticket", "○")
        ]
        
        progress_canvas = tk.Canvas(progress_frame, height=60, 
                                   bg=self.app.colors['surface'], highlightthickness=0)
        progress_canvas.pack(fill='x', padx=20, pady=10)
        
        # Draw progress line
        width = progress_canvas.winfo_reqwidth() or 800
        step_width = width // (len(steps) - 1)
        
        for i, (num, label, status) in enumerate(steps):
            x = 50 + i * step_width
            y = 30
            
            # Draw connecting lines
            if i < len(steps) - 1:
                next_x = 50 + (i + 1) * step_width
                line_color = self.app.colors['success'] if status in ['✓', '●'] else self.app.colors['border']
                progress_canvas.create_line(x + 15, y, next_x - 15, y, 
                                           fill=line_color, width=3)
            
            # Draw circle
            circle_color = self.app.colors['success'] if status == '✓' else \
                          self.app.colors['primary'] if status == '●' else \
                          self.app.colors['border']
            
            progress_canvas.create_oval(x-8, y-8, x+8, y+8, 
                                       fill=circle_color, outline='white', width=2)
            
            # Draw status icon
            text_color = 'white'
            progress_canvas.create_text(x, y, text=status, 
                                       fill=text_color, font=('Segoe UI', 10, 'bold'))
            
            # Draw label
            progress_canvas.create_text(x, y + 20, text=label, 
                                       fill=self.app.colors['text'], 
                                       font=('Segoe UI', 9))
    
    def create_booking_summary(self, parent):
        """Create enhanced booking summary section"""
        summary_frame = tk.Frame(parent, bg=self.app.colors['surface'],
                                relief='solid', bd=1, highlightbackground=self.app.colors['border'])
        summary_frame.pack(fill='x', pady=(0, 20))
        
        # Header with icon
        header_frame = tk.Frame(summary_frame, bg=self.app.colors['primary'], height=40)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="📋 Booking Summary", 
                font=('Segoe UI', 12, 'bold'),
                fg='white', bg=self.app.colors['primary']).pack(side='left', padx=15)
        
        # Create notebook for summary views with custom styling
        style = ttk.Style()
        style.configure('Summary.TNotebook', background=self.app.colors['surface'])
        style.configure('Summary.TNotebook.Tab', 
                       padding=[15, 5],
                       font=('Segoe UI', 10))
        
        summary_notebook = ttk.Notebook(summary_frame, style='Summary.TNotebook')
        summary_notebook.pack(fill='x', padx=20, pady=15)
        
        # Journey Details Tab
        journey_frame = tk.Frame(summary_notebook, bg=self.app.colors['surface'])
        summary_notebook.add(journey_frame, text="🚂 Journey Details")
        self.create_journey_details(journey_frame)
        
        # Passenger Details Tab
        passenger_frame = tk.Frame(summary_notebook, bg=self.app.colors['surface'])
        summary_notebook.add(passenger_frame, text="👥 Passenger Details")
        self.create_passenger_details(passenger_frame)
    
    def create_journey_details(self, parent):
        """Create enhanced journey details"""
        if self.app.selected_train:
            train = self.app.selected_train
            
            # Create grid layout for better alignment
            info_frame = tk.Frame(parent, bg=self.app.colors['surface'])
            info_frame.pack(padx=20, pady=15, fill='x')
            
            # Configure grid columns
            info_frame.columnconfigure(0, weight=1)
            info_frame.columnconfigure(1, weight=2)
            
            # Journey details with icons
            details = [
                ("🚂 Train:", f"{train['train_name']} ({train['train_number']})"),
                ("📍 From:", train['source']),
                ("🎯 To:", train['destination']),
                ("📅 Date:", self.app.booking_details.get('journey_date', 'N/A')),
                ("⏰ Departure:", train['departure']),
                ("⏱️ Arrival:", train['arrival']),
                ("🪑 Class:", self.app.booking_details.get('class', 'N/A')),
                ("🎫 Quota:", self.app.booking_details.get('quota', 'N/A'))
            ]
            
            for i, (label, value) in enumerate(details):
                # Label
                tk.Label(info_frame, text=label, 
                        font=('Segoe UI', 10, 'bold'),
                        fg=self.app.colors['text'], 
                        bg=self.app.colors['surface']).grid(row=i, column=0, 
                                                            sticky='w', pady=3)
                
                # Value
                tk.Label(info_frame, text=value, 
                        font=('Segoe UI', 10),
                        fg=self.app.colors['primary'], 
                        bg=self.app.colors['surface']).grid(row=i, column=1, 
                                                            sticky='w', pady=3, padx=(10, 0))
    
    def create_passenger_details(self, parent):
        """Create enhanced passenger details with table layout"""
        passengers = self.app.booking_details.get('passengers', [])
        
        if not passengers:
            tk.Label(parent, text="No passengers added", 
                    font=('Segoe UI', 11, 'italic'),
                    fg=self.app.colors['text_light'],
                    bg=self.app.colors['surface']).pack(pady=20)
            return
        
        # Create frame for passenger list
        list_frame = tk.Frame(parent, bg=self.app.colors['surface'])
        list_frame.pack(fill='both', expand=True, padx=20, pady=15)
        
        # Headers
        headers = ["#", "Name", "Age", "Gender", "Berth", "Status"]
        for col, header in enumerate(headers):
            tk.Label(list_frame, text=header, 
                    font=('Segoe UI', 10, 'bold'),
                    fg=self.app.colors['primary'], 
                    bg=self.app.colors['surface']).grid(row=0, column=col, 
                                                         sticky='w', pady=(0, 10))
        
        # Passenger rows
        for i, passenger in enumerate(passengers, 1):
            # Alternate row colors
            bg_color = self.app.colors['background'] if i % 2 == 0 else self.app.colors['surface']
            
            # Row number
            tk.Label(list_frame, text=str(i), 
                    font=('Segoe UI', 9),
                    fg=self.app.colors['text'], 
                    bg=bg_color).grid(row=i, column=0, sticky='w', pady=2, padx=2)
            
            # Name
            tk.Label(list_frame, text=passenger['name'][:20], 
                    font=('Segoe UI', 9),
                    fg=self.app.colors['text'], 
                    bg=bg_color).grid(row=i, column=1, sticky='w', pady=2, padx=10)
            
            # Age
            tk.Label(list_frame, text=str(passenger['age']), 
                    font=('Segoe UI', 9),
                    fg=self.app.colors['text'], 
                    bg=bg_color).grid(row=i, column=2, sticky='w', pady=2, padx=10)
            
            # Gender
            tk.Label(list_frame, text=passenger['gender'], 
                    font=('Segoe UI', 9),
                    fg=self.app.colors['text'], 
                    bg=bg_color).grid(row=i, column=3, sticky='w', pady=2, padx=10)
            
            # Berth (random for demo)
            berths = ['L', 'M', 'U', 'SL', 'SU']
            berth = random.choice(berths)
            tk.Label(list_frame, text=berth, 
                    font=('Segoe UI', 9, 'bold'),
                    fg=self.app.colors['primary'], 
                    bg=bg_color).grid(row=i, column=4, sticky='w', pady=2, padx=10)
            
            # Status
            tk.Label(list_frame, text="✅ Confirmed", 
                    font=('Segoe UI', 9),
                    fg=self.app.colors['success'], 
                    bg=bg_color).grid(row=i, column=5, sticky='w', pady=2, padx=10)
    
    def create_fare_breakdown(self, parent):
        """Create enhanced fare breakdown section"""
        fare_frame = tk.Frame(parent, bg=self.app.colors['surface'],
                             relief='solid', bd=1, highlightbackground=self.app.colors['border'])
        fare_frame.pack(fill='x', pady=(0, 20))
        
        # Header with icon
        header_frame = tk.Frame(fare_frame, bg=self.app.colors['secondary'], height=40)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="💰 Fare Breakdown", 
                font=('Segoe UI', 12, 'bold'),
                fg='white', bg=self.app.colors['secondary']).pack(side='left', padx=15)
        
        # Fare details with better alignment
        details_frame = tk.Frame(fare_frame, bg=self.app.colors['surface'])
        details_frame.pack(padx=30, pady=20, fill='x')
        
        # Configure grid
        details_frame.columnconfigure(0, weight=2)
        details_frame.columnconfigure(1, weight=1)
        details_frame.columnconfigure(2, weight=1)
        
        # Get fare details
        passengers = self.app.booking_details.get('passengers', [])
        passenger_count = len(passengers)
        
        if passenger_count > 0 and self.app.fare_details:
            base_fare = self.app.fare_details.get('total', 0)
            subtotal = base_fare * passenger_count
            
            # Calculate concessions
            concession_count = sum(1 for p in passengers if p.get('concession', False))
            concession_amount = 0
            if concession_count > 0 and self.app.booking_details.get('quota') == "SS":
                concession_amount = int(base_fare * 0.4 * concession_count)
            
            # Calculate GST
            gst = self.app.fare_details.get('gst', 0) * passenger_count
            
            # Total
            total = subtotal - concession_amount
            
            # Display rows
            rows = [
                ("Base Fare", f"₹ {base_fare:,} × {passenger_count}", f"₹ {subtotal:,}"),
                ("GST (5%)", "", f"₹ {gst:,}")
            ]
            
            if concession_amount > 0:
                rows.append(("Senior Citizen Concession", f"-40% × {concession_count}", f"- ₹ {concession_amount:,}"))
            
            for i, (label, detail, amount) in enumerate(rows):
                # Label
                tk.Label(details_frame, text=label, 
                        font=('Segoe UI', 11),
                        fg=self.app.colors['text'], 
                        bg=self.app.colors['surface']).grid(row=i*2, column=0, 
                                                            sticky='w', pady=2)
                
                # Detail (if any)
                if detail:
                    tk.Label(details_frame, text=detail, 
                            font=('Segoe UI', 10, 'italic'),
                            fg=self.app.colors['text_light'], 
                            bg=self.app.colors['surface']).grid(row=i*2+1, column=0, 
                                                                sticky='w', pady=(0, 5))
                
                # Amount
                tk.Label(details_frame, text=amount, 
                        font=('Segoe UI', 11, 'bold'),
                        fg=self.app.colors['primary'], 
                        bg=self.app.colors['surface']).grid(row=i*2, column=2, 
                                                            sticky='e', pady=2)
            
            # Separator
            ttk.Separator(details_frame, orient='horizontal').grid(row=len(rows)*2, 
                                                                   column=0, columnspan=3, 
                                                                   sticky='ew', pady=10)
            
            # Total
            total_row = len(rows)*2 + 1
            tk.Label(details_frame, text="Total Amount", 
                    font=('Segoe UI', 14, 'bold'),
                    fg=self.app.colors['text'], 
                    bg=self.app.colors['surface']).grid(row=total_row, column=0, 
                                                        sticky='w', pady=5)
            
            tk.Label(details_frame, text=f"₹ {total:,}", 
                    font=('Segoe UI', 18, 'bold'),
                    fg=self.app.colors['success'], 
                    bg=self.app.colors['surface']).grid(row=total_row, column=2, 
                                                        sticky='e', pady=5)
    
    def create_payment_methods(self, parent):
        """Create enhanced payment method selection"""
        method_frame = tk.Frame(parent, bg=self.app.colors['surface'],
                               relief='solid', bd=1, highlightbackground=self.app.colors['border'])
        method_frame.pack(fill='x', pady=(0, 20))
        
        # Header with icon
        header_frame = tk.Frame(method_frame, bg=self.app.colors['accent'], height=40)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="💳 Select Payment Method", 
                font=('Segoe UI', 12, 'bold'),
                fg='white', bg=self.app.colors['accent']).pack(side='left', padx=15)
        
        # Method options with cards
        options_frame = tk.Frame(method_frame, bg=self.app.colors['surface'])
        options_frame.pack(pady=20)
        
        methods = [
            ("card", "💳", "Credit/Debit Card", "Pay with Visa, MasterCard, RuPay"),
            ("upi", "📱", "UPI", "Google Pay, PhonePe, Paytm"),
            ("netbanking", "🏦", "Net Banking", "All major banks"),
            ("wallet", "💰", "Wallet", "Paytm, Amazon Pay, Mobikwik")
        ]
        
        for i, (value, icon, title, desc) in enumerate(methods):
            # Create card-like button
            card_frame = tk.Frame(options_frame, bg=self.app.colors['surface'],
                                 relief='solid', bd=1, highlightbackground=self.app.colors['border'])
            card_frame.grid(row=0, column=i, padx=10, pady=5, ipadx=10, ipady=10)
            
            # Radio button
            radio = tk.Radiobutton(card_frame, variable=self.payment_method, value=value,
                                  command=self.switch_payment_form,
                                  bg=self.app.colors['surface'],
                                  activebackground=self.app.colors['surface'],
                                  selectcolor=self.app.colors['surface'])
            radio.pack(anchor='ne')
            
            # Icon
            tk.Label(card_frame, text=icon, font=('Segoe UI', 24),
                    fg=self.app.colors['primary'], bg=self.app.colors['surface']).pack(pady=5)
            
            # Title
            tk.Label(card_frame, text=title, font=('Segoe UI', 11, 'bold'),
                    fg=self.app.colors['text'], bg=self.app.colors['surface']).pack()
            
            # Description
            tk.Label(card_frame, text=desc, font=('Segoe UI', 8),
                    fg=self.app.colors['text_light'], bg=self.app.colors['surface'],
                    wraplength=120).pack(pady=5)
            
            # Add hover effect
            self.add_card_hover_effect(card_frame)
    
    def add_card_hover_effect(self, card):
        """Add hover effect to payment method cards"""
        def on_enter(e):
            card.config(relief='ridge', bd=2, highlightbackground=self.app.colors['primary'])
        
        def on_leave(e):
            card.config(relief='solid', bd=1, highlightbackground=self.app.colors['border'])
        
        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)
    
    def create_payment_form_section(self, parent):
        """Create payment form section container"""
        form_container = tk.Frame(parent, bg=self.app.colors['surface'],
                                 relief='solid', bd=1, highlightbackground=self.app.colors['border'])
        form_container.pack(fill='x', pady=(0, 20))
        
        # Header
        header_frame = tk.Frame(form_container, bg=self.app.colors['primary_light'], height=40)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        self.form_header = tk.Label(header_frame, text="💳 Card Payment Details", 
                                   font=('Segoe UI', 12, 'bold'),
                                   fg='white', bg=self.app.colors['primary_light'])
        self.form_header.pack(side='left', padx=15)
        
        # Form container (will be populated dynamically)
        self.payment_form_container = tk.Frame(form_container, bg=self.app.colors['surface'])
        self.payment_form_container.pack(fill='x', padx=20, pady=20)
        
        # Create default card form
        self.create_card_payment_form()
    
    def switch_payment_form(self):
        """Switch payment form based on selected method with animation"""
        method = self.payment_method.get()
        
        # Update header
        headers = {
            "card": "💳 Card Payment Details",
            "upi": "📱 UPI Payment Details",
            "netbanking": "🏦 Net Banking Details",
            "wallet": "💰 Wallet Payment Details"
        }
        self.form_header.config(text=headers.get(method, "Payment Details"))
        
        # Clear current form with fade effect (simulated)
        for widget in self.payment_form_container.winfo_children():
            widget.destroy()
        
        # Create new form based on method
        if method == "card":
            self.create_card_payment_form()
        elif method == "upi":
            self.create_upi_payment_form()
        elif method == "netbanking":
            self.create_netbanking_form()
        elif method == "wallet":
            self.create_wallet_form()
    
    def create_card_payment_form(self):
        """Create enhanced credit/debit card payment form"""
        form_frame = tk.Frame(self.payment_form_container, bg=self.app.colors['surface'])
        form_frame.pack(fill='x')
        
        # Configure grid for better alignment
        form_frame.columnconfigure(0, weight=1)
        form_frame.columnconfigure(1, weight=3)
        
        # Card Number
        tk.Label(form_frame, text="Card Number:", font=('Segoe UI', 11),
                fg=self.app.colors['text'], bg=self.app.colors['surface']).grid(
                    row=0, column=0, sticky='w', pady=(0, 10))
        
        card_frame = tk.Frame(form_frame, bg=self.app.colors['surface'])
        card_frame.grid(row=0, column=1, sticky='ew', pady=(0, 10), padx=(10, 0))
        
        self.card_number = tk.Entry(card_frame, font=('Segoe UI', 11), 
                                   bg='white', relief='solid', bd=1,
                                   highlightthickness=1, highlightcolor=self.app.colors['primary'])
        self.card_number.pack(fill='x', ipady=8)
        
        # Card number format hint
        tk.Label(form_frame, text="(16 digits)", font=('Segoe UI', 9),
                fg=self.app.colors['text_light'], bg=self.app.colors['surface']).grid(
                    row=1, column=1, sticky='w', padx=(10, 0), pady=(0, 15))
        
        # Card Holder Name
        tk.Label(form_frame, text="Card Holder:", font=('Segoe UI', 11),
                fg=self.app.colors['text'], bg=self.app.colors['surface']).grid(
                    row=2, column=0, sticky='w', pady=(0, 10))
        
        name_frame = tk.Frame(form_frame, bg=self.app.colors['surface'])
        name_frame.grid(row=2, column=1, sticky='ew', pady=(0, 10), padx=(10, 0))
        
        self.card_holder = tk.Entry(name_frame, font=('Segoe UI', 11), 
                                   bg='white', relief='solid', bd=1,
                                   highlightthickness=1, highlightcolor=self.app.colors['primary'])
        self.card_holder.pack(fill='x', ipady=8)
        
        tk.Label(form_frame, text="(as printed on card)", font=('Segoe UI', 9),
                fg=self.app.colors['text_light'], bg=self.app.colors['surface']).grid(
                    row=3, column=1, sticky='w', padx=(10, 0), pady=(0, 15))
        
        # Expiry and CVV in same row
        row_frame = tk.Frame(form_frame, bg=self.app.colors['surface'])
        row_frame.grid(row=4, column=1, sticky='ew', pady=(0, 10), padx=(10, 0))
        
        # Expiry
        expiry_frame = tk.Frame(row_frame, bg=self.app.colors['surface'])
        expiry_frame.pack(side='left', fill='x', expand=True, padx=(0, 10))
        
        tk.Label(expiry_frame, text="Expiry (MM/YY):", font=('Segoe UI', 11),
                fg=self.app.colors['text'], bg=self.app.colors['surface']).pack(anchor='w')
        
        self.card_expiry = tk.Entry(expiry_frame, font=('Segoe UI', 11), 
                                   bg='white', relief='solid', bd=1,
                                   highlightthickness=1, highlightcolor=self.app.colors['primary'])
        self.card_expiry.pack(fill='x', ipady=8, pady=(5, 0))
        
        # CVV
        cvv_frame = tk.Frame(row_frame, bg=self.app.colors['surface'])
        cvv_frame.pack(side='left', fill='x', expand=True, padx=(10, 0))
        
        tk.Label(cvv_frame, text="CVV:", font=('Segoe UI', 11),
                fg=self.app.colors['text'], bg=self.app.colors['surface']).pack(anchor='w')
        
        cvv_input_frame = tk.Frame(cvv_frame, bg=self.app.colors['surface'])
        cvv_input_frame.pack(fill='x', pady=(5, 0))
        
        self.card_cvv = tk.Entry(cvv_input_frame, font=('Segoe UI', 11), 
                                bg='white', show='•', relief='solid', bd=1,
                                highlightthickness=1, highlightcolor=self.app.colors['primary'],
                                width=10)
        self.card_cvv.pack(side='left', ipady=8)
        
        # CVV hint
        tk.Label(cvv_frame, text="3-4 digits", font=('Segoe UI', 9),
                fg=self.app.colors['text_light'], bg=self.app.colors['surface']).pack(anchor='w')
    
    def create_upi_payment_form(self):
        """Create enhanced UPI payment form"""
        form_frame = tk.Frame(self.payment_form_container, bg=self.app.colors['surface'])
        form_frame.pack(fill='x')
        
        # UPI ID
        tk.Label(form_frame, text="UPI ID:", font=('Segoe UI', 11),
                fg=self.app.colors['text'], bg=self.app.colors['surface']).pack(anchor='w')
        
        upi_frame = tk.Frame(form_frame, bg=self.app.colors['surface'])
        upi_frame.pack(fill='x', pady=(5, 5))
        
        self.upi_id = tk.Entry(upi_frame, font=('Segoe UI', 11), 
                              bg='white', relief='solid', bd=1,
                              highlightthickness=1, highlightcolor=self.app.colors['primary'])
        self.upi_id.pack(fill='x', ipady=8)
        
        tk.Label(form_frame, text="e.g., name@okhdfcbank, phone@paytm", 
                font=('Segoe UI', 9), fg=self.app.colors['text_light'],
                bg=self.app.colors['surface']).pack(anchor='w')
        
        # Quick select apps
        apps_frame = tk.Frame(form_frame, bg=self.app.colors['surface'])
        apps_frame.pack(fill='x', pady=15)
        
        tk.Label(apps_frame, text="Popular UPI Apps:", font=('Segoe UI', 10, 'bold'),
                fg=self.app.colors['text'], bg=self.app.colors['surface']).pack(anchor='w', pady=(0, 5))
        
        apps = [
            ("📱 Google Pay", "okhdfcbank"),
            ("📱 PhonePe", "ybl"),
            ("📱 Paytm", "paytm"),
            ("📱 BHIM", "okbizaxis")
        ]
        
        apps_row = tk.Frame(apps_frame, bg=self.app.colors['surface'])
        apps_row.pack(fill='x')
        
        for app, handle in apps:
            btn = tk.Button(apps_row, text=app,
                          command=lambda h=handle: self.upi_id.delete(0, tk.END) or 
                                                  self.upi_id.insert(0, f"username@{h}"),
                          bg=self.app.colors['background'], fg=self.app.colors['primary'],
                          font=('Segoe UI', 9), padx=10, pady=5,
                          relief='flat', cursor='hand2')
            btn.pack(side='left', padx=2)
            self.add_hover_effect(btn, self.app.colors['background'], self.app.colors['primary_light'])
    
    def create_netbanking_form(self):
        """Create enhanced net banking form"""
        form_frame = tk.Frame(self.payment_form_container, bg=self.app.colors['surface'])
        form_frame.pack(fill='x')
        
        # Bank Selection
        tk.Label(form_frame, text="Select Bank:", font=('Segoe UI', 11),
                fg=self.app.colors['text'], bg=self.app.colors['surface']).pack(anchor='w')
        
        banks = [
            "🏦 State Bank of India",
            "🏦 HDFC Bank",
            "🏦 ICICI Bank",
            "🏦 Axis Bank",
            "🏦 Kotak Mahindra Bank",
            "🏦 Yes Bank",
            "🏦 Punjab National Bank",
            "🏦 Bank of Baroda"
        ]
        
        self.bank_combo = ttk.Combobox(form_frame, font=('Segoe UI', 11),
                                      values=banks, state='readonly')
        self.bank_combo.pack(fill='x', pady=(5, 10), ipady=5)
        self.bank_combo.set("Select your bank")
        
        # Popular banks quick select
        popular_frame = tk.Frame(form_frame, bg=self.app.colors['surface'])
        popular_frame.pack(fill='x', pady=10)
        
        tk.Label(popular_frame, text="Popular Banks:", font=('Segoe UI', 10, 'bold'),
                fg=self.app.colors['text'], bg=self.app.colors['surface']).pack(anchor='w', pady=(0, 5))
        
        popular_banks = ["SBI", "HDFC", "ICICI", "Axis"]
        banks_row = tk.Frame(popular_frame, bg=self.app.colors['surface'])
        banks_row.pack(fill='x')
        
        for bank in popular_banks:
            btn = tk.Button(banks_row, text=bank,
                          command=lambda b=bank: self.bank_combo.set(f"🏦 {b} Bank"),
                          bg=self.app.colors['background'], fg=self.app.colors['primary'],
                          font=('Segoe UI', 9), padx=15, pady=5,
                          relief='flat', cursor='hand2')
            btn.pack(side='left', padx=2)
            self.add_hover_effect(btn, self.app.colors['background'], self.app.colors['primary_light'])
    
    def create_wallet_form(self):
        """Create enhanced wallet payment form"""
        form_frame = tk.Frame(self.payment_form_container, bg=self.app.colors['surface'])
        form_frame.pack(fill='x')
        
        # Wallet Selection
        tk.Label(form_frame, text="Select Wallet:", font=('Segoe UI', 11),
                fg=self.app.colors['text'], bg=self.app.colors['surface']).pack(anchor='w')
        
        wallets = [
            "💰 Paytm Wallet",
            "💰 Amazon Pay",
            "💰 Mobikwik",
            "💰 Freecharge",
            "💰 PhonePe Wallet"
        ]
        
        self.wallet_combo = ttk.Combobox(form_frame, font=('Segoe UI', 11),
                                        values=wallets, state='readonly')
        self.wallet_combo.pack(fill='x', pady=(5, 15), ipady=5)
        self.wallet_combo.set("Select wallet")
        
        # Balance info with progress bar
        balance_frame = tk.Frame(form_frame, bg=self.app.colors['surface'])
        balance_frame.pack(fill='x', pady=10)
        
        tk.Label(balance_frame, text="Available Balance:", font=('Segoe UI', 10),
                fg=self.app.colors['text'], bg=self.app.colors['surface']).pack(anchor='w')
        
        balance_amount = tk.Label(balance_frame, text="₹ 2,500", 
                                 font=('Segoe UI', 14, 'bold'),
                                 fg=self.app.colors['success'], 
                                 bg=self.app.colors['surface'])
        balance_amount.pack(anchor='w')
        
        # Simulated balance bar
        progress_canvas = tk.Canvas(balance_frame, height=5, bg=self.app.colors['border'],
                                   highlightthickness=0)
        progress_canvas.pack(fill='x', pady=(5, 0))
        progress_canvas.create_rectangle(0, 0, 200, 5, 
                                        fill=self.app.colors['success'], width=0)
    
    def create_terms_section(self, parent):
        """Create enhanced terms and conditions section"""
        terms_frame = tk.Frame(parent, bg=self.app.colors['surface'],
                              relief='solid', bd=1, highlightbackground=self.app.colors['border'])
        terms_frame.pack(fill='x', pady=(0, 20))
        
        # Terms header
        header_frame = tk.Frame(terms_frame, bg=self.app.colors['primary_dark'], height=30)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="📜 Terms & Conditions", 
                font=('Segoe UI', 10, 'bold'),
                fg='white', bg=self.app.colors['primary_dark']).pack(side='left', padx=10)
        
        # Terms content
        content_frame = tk.Frame(terms_frame, bg=self.app.colors['surface'])
        content_frame.pack(padx=20, pady=15, fill='x')
        
        # Checkbox
        terms_check = tk.Checkbutton(content_frame, text="I agree to the Terms and Conditions",
                                     variable=self.terms_var,
                                     bg=self.app.colors['surface'],
                                     fg=self.app.colors['text'],
                                     selectcolor=self.app.colors['surface'],
                                     activebackground=self.app.colors['surface'],
                                     font=('Segoe UI', 10, 'bold'))
        terms_check.pack(anchor='w')
        
        # Terms summary with better formatting
        terms_text = tk.Text(content_frame, height=4, 
                           font=('Segoe UI', 9), wrap='word',
                           bg=self.app.colors['background'],
                           fg=self.app.colors['text'],
                           relief='solid', bd=1, padx=10, pady=10)
        terms_text.pack(fill='x', pady=(10, 0))
        
        terms_text.insert('1.0', """• Tickets are non-refundable once booked
• Valid ID proof must be shown during travel
• Cancellation charges apply as per IRCTC rules
• E-ticket will be sent to registered email
• Passengers must carry original ID proof""")
        terms_text.config(state='disabled')
    
    def create_action_buttons(self, parent):
        """Create enhanced action buttons"""
        button_frame = tk.Frame(parent, bg=self.app.colors['background'])
        button_frame.pack(fill='x', pady=10)
        
        # Back button with icon
        back_btn = tk.Button(button_frame, text="← Back to Passengers",
                            command=self.go_back,
                            bg=self.app.colors['text_light'], fg='white',
                            font=('Segoe UI', 11), padx=25, pady=12,
                            relief='flat', cursor='hand2')
        back_btn.pack(side='left')
        self.add_hover_effect(back_btn, self.app.colors['text_light'], self.app.colors['text'])
        
        # Pay Now button with amount
        total = self.app.booking_details.get('total_fare', 0)
        self.pay_btn = tk.Button(button_frame, 
                                 text=f"💳 Pay ₹ {total:,}",
                                 command=self.process_payment,
                                 bg=self.app.colors['success'], fg='white',
                                 font=('Segoe UI', 14, 'bold'), 
                                 padx=40, pady=12,
                                 relief='flat', cursor='hand2')
        self.pay_btn.pack(side='right')
        self.add_hover_effect(self.pay_btn, self.app.colors['success'], '#16a34a')
        
        # Add secure payment badge
        secure_badge = tk.Label(button_frame, text="🔒 Secure Payment",
                                font=('Segoe UI', 10),
                                fg=self.app.colors['primary'], 
                                bg=self.app.colors['background'])
        secure_badge.pack(side='right', padx=20)
    
    def create_security_badge(self, parent):
        """Create security badges"""
        badge_frame = tk.Frame(parent, bg=self.app.colors['background'])
        badge_frame.pack(fill='x', pady=10)
        
        badges = [
            "🔒 256-bit SSL Encryption",
            "💳 PCI DSS Compliant",
            "🛡️ 100% Secure Payment",
            "✓ Verified by Visa",
            "🔐 MasterCard SecureCode"
        ]
        
        for badge in badges:
            tk.Label(badge_frame, text=badge, 
                    font=('Segoe UI', 9),
                    fg=self.app.colors['text_light'], 
                    bg=self.app.colors['background']).pack(side='left', padx=10)
    
    def validate_payment_details(self):
        """Enhanced payment validation"""
        method = self.payment_method.get()
        
        if method == "card":
            if not self.card_number or not self.card_number.get().strip():
                messagebox.showerror("Error", "Please enter card number")
                return False
            
            card_num = self.card_number.get().strip().replace(' ', '')
            if not card_num.isdigit() or len(card_num) != 16:
                messagebox.showerror("Error", "Please enter valid 16-digit card number")
                return False
            
            # Luhn algorithm check (basic)
            if not self.luhn_check(card_num):
                messagebox.showerror("Error", "Invalid card number")
                return False
            
            if not self.card_holder or not self.card_holder.get().strip():
                messagebox.showerror("Error", "Please enter card holder name")
                return False
            
            if not self.card_expiry or not self.card_expiry.get().strip():
                messagebox.showerror("Error", "Please enter card expiry date")
                return False
            
            expiry = self.card_expiry.get().strip()
            if not re.match(r'^(0[1-9]|1[0-2])/[0-9]{2}$', expiry):
                messagebox.showerror("Error", "Please enter expiry in MM/YY format")
                return False
            
            # Check if card is not expired
            try:
                exp_month, exp_year = map(int, expiry.split('/'))
                current_year = datetime.now().year % 100
                current_month = datetime.now().month
                
                if exp_year < current_year or (exp_year == current_year and exp_month < current_month):
                    messagebox.showerror("Error", "Card has expired")
                    return False
            except:
                pass
            
            if not self.card_cvv or not self.card_cvv.get().strip():
                messagebox.showerror("Error", "Please enter CVV")
                return False
            
            cvv = self.card_cvv.get().strip()
            if not cvv.isdigit() or len(cvv) not in [3, 4]:
                messagebox.showerror("Error", "Please enter valid CVV")
                return False
        
        elif method == "upi":
            if not self.upi_id or not self.upi_id.get().strip():
                messagebox.showerror("Error", "Please enter UPI ID")
                return False
            
            upi = self.upi_id.get().strip()
            if not re.match(r'^[a-zA-Z0-9.\-_]{2,}@[a-zA-Z]{2,}$', upi):
                messagebox.showerror("Error", "Please enter valid UPI ID (e.g., name@bank)")
                return False
        
        elif method == "netbanking":
            if not self.bank_combo or self.bank_combo.get() == "Select your bank":
                messagebox.showerror("Error", "Please select a bank")
                return False
        
        elif method == "wallet":
            if not self.wallet_combo or self.wallet_combo.get() == "Select wallet":
                messagebox.showerror("Error", "Please select a wallet")
                return False
        
        return True
    
    def luhn_check(self, card_number):
        """Luhn algorithm for card validation"""
        digits = [int(d) for d in card_number]
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        total = sum(odd_digits)
        for d in even_digits:
            total += sum(divmod(d * 2, 10))
        return total % 10 == 0
    
    def process_payment(self):
        """Process the payment with animation"""
        # Check terms agreement
        if not self.terms_var.get():
            messagebox.showerror("Error", "Please agree to Terms and Conditions")
            return
        
        # Validate payment details
        if not self.validate_payment_details():
            return
        
        # Show processing animation
        self.pay_btn.config(text="⏳ Processing...", state='disabled')
        self.update()
        
        # Simulate payment processing with progress
        self.after(100, self.update_progress, 0)
    
    def update_progress(self, step):
        """Update payment progress"""
        steps = ["🔍 Validating", "💳 Processing", "✅ Confirming"]
        if step < len(steps):
            self.pay_btn.config(text=steps[step] + "...")
            self.update()
            self.after(700, self.update_progress, step + 1)
        else:
            self.complete_booking()
    
    def complete_booking(self):
        """Complete the booking process"""
        # Generate PNR
        pnr = self.app.generate_pnr()
        self.app.booking_details['pnr'] = pnr
        self.app.booking_details['booking_time'] = datetime.now().isoformat()
        
        # Save booking to history
        self.app.save_booking()
        
        # Show enhanced success message
        self.show_success_notification(pnr)
        
        # Enable pay button
        total = self.app.booking_details.get('total_fare', 0)
        self.pay_btn.config(text=f"💳 Pay ₹ {total:,}", state='normal')
        
        # Go to PNR tab
        self.app.notebook.select(5)
        
        # Refresh PNR tab
        self.app.pnr_tab.refresh()
    
    def show_success_notification(self, pnr):
        """Show enhanced success notification"""
        # Create custom success dialog
        success_dialog = tk.Toplevel(self)
        success_dialog.title("Booking Confirmed")
        success_dialog.geometry("400x300")
        success_dialog.configure(bg='white')
        
        # Center the dialog
        success_dialog.update_idletasks()
        x = (success_dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (success_dialog.winfo_screenheight() // 2) - (300 // 2)
        success_dialog.geometry(f'400x300+{x}+{y}')
        
        # Success icon
        tk.Label(success_dialog, text="✅", font=('Segoe UI', 48),
                fg=self.app.colors['success'], bg='white').pack(pady=20)
        
        # Message
        tk.Label(success_dialog, text="Payment Successful!",
                font=('Segoe UI', 16, 'bold'),
                fg=self.app.colors['primary'], bg='white').pack()
        
        tk.Label(success_dialog, text=f"PNR: {pnr}",
                font=('Segoe UI', 14),
                fg=self.app.colors['text'], bg='white').pack(pady=10)
        
        tk.Label(success_dialog, text="Your ticket has been generated",
                font=('Segoe UI', 11),
                fg=self.app.colors['text_light'], bg='white').pack()
        
        # OK button
        ok_btn = tk.Button(success_dialog, text="View Ticket",
                          command=lambda: [success_dialog.destroy(), 
                                         self.app.notebook.select(5)],
                          bg=self.app.colors['primary'], fg='white',
                          font=('Segoe UI', 11), padx=30, pady=8,
                          relief='flat', cursor='hand2')
        ok_btn.pack(pady=20)
        self.add_hover_effect(ok_btn, self.app.colors['primary'], self.app.colors['primary_dark'])
    
    def go_back(self):
        """Go back to passenger tab"""
        self.app.notebook.select(3)
    
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
        # Update pay button with current total
        total = self.app.booking_details.get('total_fare', 0)
        if self.pay_btn:
            self.pay_btn.config(text=f"💳 Pay ₹ {total:,}")
        
        # Reset payment method to default
        self.payment_method.set("card")
        self.switch_payment_form()
        
        # Reset terms checkbox
        self.terms_var.set(False)