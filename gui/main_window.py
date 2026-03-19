"""
The Train Captain - Main Window
Contains the main application window with notebook tabs and shared state
Software developed by Ashish Vishwakarma
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json
import os
from pathlib import Path
from PIL import Image, ImageTk
import hashlib
import random

# Import all tabs
from gui.login_tab import LoginTab
from gui.journey_tab import JourneyTab
from gui.train_select_tab import TrainSelectTab
from gui.passenger_tab import PassengerTab
from gui.booking_tab import BookingTab
from gui.pnr_tab import PNRTab
from gui.history_tab import HistoryTab
from gui.settings_tab import SettingsTab

class TrainCaptainApp:
    """Main Application Class"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("The Train Captain - Railway Ticket Booking System")
        
        # Define enhanced color scheme
        self.colors = {
            'primary': '#0f4c75', 
            'primary_light': '#3282b8', 
            'primary_dark': '#1b262c',
            'secondary': '#00b7c2', 
            'secondary_light': '#6ef3d6', 
            'secondary_dark': '#0a7e8c',
            'accent': '#fdcb9e', 
            'danger': '#f05454', 
            'warning': '#ffb26b',
            'success': '#6ecb63', 
            'info': '#5aa9e6',
            'background': '#f9f9f9', 
            'surface': '#ffffff',
            'text': '#222831', 
            'text_light': '#6b7280', 
            'border': '#e1e5ea',
            'gradient_start': '#0f4c75',
            'gradient_end': '#3282b8'
        }
        
        # Configure root window
        self.root.configure(bg=self.colors['primary_dark'])
        
        # Initialize shared application state
        self.logged_in = False
        self.user_data = None
        self.selected_train = None
        self.booking_details = {
            'source': None,
            'destination': None,
            'journey_date': None,
            'train_number': None,
            'train_name': None,
            'class': None,
            'quota': None,
            'berth_preference': None,
            'passengers': [],
            'passenger_count': 0,
            'total_fare': 0,
            'pnr': None,
            'booking_time': None
        }
        self.fare_details = None
        self.bookings_history = []
        
        # Variables for journey tab
        self.source_var = tk.StringVar()
        self.destination_var = tk.StringVar()
        self.journey_date_var = tk.StringVar(value=datetime.now().strftime("%d-%m-%Y"))
        
        # Load saved bookings
        self.load_bookings()
        
        # Create main container
        self.main_container = tk.Frame(self.root, bg=self.colors['primary_dark'])
        self.main_container.pack(fill='both', expand=True)
        
        # Create header with images and clock
        self.create_header()
        
        # Create notebook (tabbed interface)
        self.create_notebook()
        
        # Create footer
        self.create_footer()
        
        # Bind to tab change event
        self.notebook.bind('<<NotebookTabChanged>>', self.on_tab_change)
        
        # Start real-time clock update
        self.update_clock()
        
        # Apply custom styling
        self.apply_custom_styling()
    
    def apply_custom_styling(self):
        """Apply custom ttk styling"""
        style = ttk.Style()
        
        # Configure notebook style
        style.theme_use('clam')
        
        # Configure colors
        style.configure('TNotebook', background=self.colors['primary_dark'], borderwidth=0)
        style.configure('TNotebook.Tab', 
                       padding=[20, 10],
                       font=('Segoe UI', 10),
                       background=self.colors['primary'],
                       foreground='white',
                       borderwidth=0)
        
        style.map('TNotebook.Tab',
                 background=[('selected', self.colors['secondary']),
                           ('active', self.colors['primary_light'])],
                 foreground=[('selected', 'white'),
                           ('active', 'white')],
                 expand=[('selected', [1, 1, 1, 0])])
        
        # Configure combobox style
        style.configure('TCombobox', 
                       fieldbackground='white',
                       background='white',
                       foreground=self.colors['text'],
                       arrowcolor=self.colors['primary'])
        
        # Configure scrollbar style
        style.configure('Vertical.TScrollbar',
                       background=self.colors['primary'],
                       troughcolor=self.colors['background'],
                       arrowcolor='white')
    
    def create_header(self):
        """Create enhanced header with train images and clock"""
        header_frame = tk.Frame(self.main_container, bg=self.colors['primary'], height=120)
        header_frame.pack(fill='x', padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # Create gradient effect
        for i in range(120):
            color = self.fade_color(self.colors['gradient_start'], 
                                   self.colors['gradient_end'], i/120)
            line = tk.Frame(header_frame, bg=color, height=1)
            line.place(x=0, y=i, width=header_frame.winfo_width())
        
        # Left image (train1.jpg)
        left_frame = tk.Frame(header_frame, bg=self.colors['primary'], width=180)
        left_frame.pack(side='left', fill='y', padx=20)
        left_frame.pack_propagate(False)
        
        try:
            assets_path = Path(__file__).parent.parent / 'assets' / 'train.jpg'
            if assets_path.exists():
                img = Image.open(assets_path)
                img = img.resize((160, 90), Image.Resampling.LANCZOS)
                self.train1_img = ImageTk.PhotoImage(img)
                img_label = tk.Label(left_frame, image=self.train1_img, bg=self.colors['primary'])
                img_label.pack(expand=True)
                
                # Add border effect
                img_label.bind('<Enter>', lambda e: img_label.config(relief='ridge', bd=2))
                img_label.bind('<Leave>', lambda e: img_label.config(relief='flat', bd=0))
            else:
                # Enhanced fallback with animation
                self.create_train_animation(left_frame)
        except Exception as e:
            self.create_train_animation(left_frame)
        
        # Center title with animation
        center_frame = tk.Frame(header_frame, bg=self.colors['primary'])
        center_frame.pack(side='left', expand=True, fill='both')
        
        # Main title with shadow effect
        title_shadow = tk.Label(center_frame, text="THE TRAIN CAPTAIN", 
                               font=('Segoe UI', 32, 'bold'), 
                               fg=self.colors['primary_dark'], bg=self.colors['primary'])
        title_shadow.place(relx=0.5, rely=0.45, anchor='center')
        
        title_label = tk.Label(center_frame, text="THE TRAIN CAPTAIN", 
                              font=('Segoe UI', 32, 'bold'), 
                              fg='white', bg=self.colors['primary'])
        title_label.place(relx=0.5, rely=0.4, anchor='center')
        
        # Subtitle with typing effect
        self.subtitle_text = "Railway Ticket Booking System"
        self.subtitle_index = 0
        subtitle_label = tk.Label(center_frame, text="", 
                                 font=('Segoe UI', 14), 
                                 fg=self.colors['accent'], bg=self.colors['primary'])
        subtitle_label.place(relx=0.5, rely=0.65, anchor='center')
        
        def type_effect():
            if self.subtitle_index < len(self.subtitle_text):
                current_text = self.subtitle_text[:self.subtitle_index + 1]
                subtitle_label.config(text=current_text)
                self.subtitle_index += 1
                self.root.after(100, type_effect)
        
        # Start typing effect after a delay
        self.root.after(1000, type_effect)
        
        # Right frame with clock and train image
        right_frame = tk.Frame(header_frame, bg=self.colors['primary'], width=250)
        right_frame.pack(side='right', fill='y', padx=20)
        right_frame.pack_propagate(False)
        
        # Digital clock with modern design
        clock_container = tk.Frame(right_frame, bg=self.colors['primary_dark'], 
                                  relief='ridge', bd=2)
        clock_container.pack(pady=(10, 5), padx=5, fill='x')
        
        self.clock_label = tk.Label(clock_container, text="00:00:00", 
                                   font=('Digital-7', 20, 'bold'),
                                   fg=self.colors['accent'], 
                                   bg=self.colors['primary_dark'])
        self.clock_label.pack(pady=5)
        
        self.date_label = tk.Label(clock_container, text="", 
                                  font=('Segoe UI', 10),
                                  fg='white', bg=self.colors['primary_dark'])
        self.date_label.pack(pady=(0, 5))
        
        # Right image (train2.jpg)
        try:
            assets_path = Path(__file__).parent.parent / 'assets' / 'train5.jpg'
            if assets_path.exists():
                img = Image.open(assets_path)
                img = img.resize((160, 60), Image.Resampling.LANCZOS)
                self.train2_img = ImageTk.PhotoImage(img)
                tk.Label(right_frame, image=self.train2_img, 
                        bg=self.colors['primary']).pack(expand=True)
        except:
            tk.Label(right_frame, text="🚂", font=('Segoe UI', 24), 
                    fg='white', bg=self.colors['primary']).pack(expand=True)
    
    def fade_color(self, color1, color2, ratio):
        """Fade between two colors"""
        r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
        r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)
        
        r = int(r1 + (r2 - r1) * ratio)
        g = int(g1 + (g2 - g1) * ratio)
        b = int(b1 + (b2 - b1) * ratio)
        
        return f'#{r:02x}{g:02x}{b:02x}'
    
    def create_train_animation(self, parent):
        """Create animated train placeholder"""
        canvas = tk.Canvas(parent, width=160, height=90, 
                          bg=self.colors['primary'], highlightthickness=0)
        canvas.pack(expand=True)
        
        # Draw train
        def animate():
            canvas.delete("all")
            # Moving train animation
            x = random.randint(0, 10)
            # Draw train body
            canvas.create_rectangle(20-x, 30, 140-x, 70, 
                                   fill=self.colors['secondary'], outline='white', width=2)
            # Draw windows
            for i in range(4):
                canvas.create_rectangle(30-x + i*25, 40, 45-x + i*25, 55,
                                       fill=self.colors['accent'], outline='white')
            # Draw wheels
            canvas.create_oval(30-x, 70, 50-x, 90, fill='black', outline='white')
            canvas.create_oval(100-x, 70, 120-x, 90, fill='black', outline='white')
            
            parent.after(100, animate)
        
        animate()
    
    def create_notebook(self):
        """Create enhanced notebook with tabs"""
        # Notebook frame with border
        notebook_frame = tk.Frame(self.main_container, bg='white', 
                                 relief='solid', bd=1)
        notebook_frame.pack(fill='both', expand=True, padx=20, pady=(0, 10))
        
        self.notebook = ttk.Notebook(notebook_frame)
        self.notebook.pack(fill='both', expand=True, padx=1, pady=1)
        
        # Create all tabs
        self.create_tabs()
    
    def create_footer(self):
        """Create enhanced footer with status and developer credit"""
        footer_frame = tk.Frame(self.main_container, bg=self.colors['primary_dark'], height=40)
        footer_frame.pack(fill='x', side='bottom')
        footer_frame.pack_propagate(False)
        
        # Left side - Clock
        self.footer_clock = tk.Label(footer_frame, text="", font=('Segoe UI', 9),
                                    fg=self.colors['accent'], bg=self.colors['primary_dark'])
        self.footer_clock.pack(side='left', padx=15)
        
        # Center - Status
        self.status_label = tk.Label(footer_frame, text="Ready", font=('Segoe UI', 9),
                                    fg='white', bg=self.colors['primary_dark'])
        self.status_label.pack(side='left', padx=20)
        
        # Center - Developer Credit
        credit_label = tk.Label(footer_frame, 
                               text="Software developed by Ashish Vishwakarma",
                               font=('Segoe UI', 9, 'bold'),
                               fg=self.colors['accent'], bg=self.colors['primary_dark'])
        credit_label.pack(side='left', expand=True)
        
        # Right side - Version
        version_label = tk.Label(footer_frame, text="Version 2.0 | © 2024",
                                font=('Segoe UI', 9), fg='white', 
                                bg=self.colors['primary_dark'])
        version_label.pack(side='right', padx=15)
    
    def create_tabs(self):
        """Create all application tabs with icons"""
        # Define tab icons (text-based for simplicity)
        tab_icons = {
            'Login': '🔐',
            'Search': '🔍',
            'Train': '🚂',
            'Passengers': '👥',
            'Payment': '💰',
            'PNR': '🎫',
            'History': '📜',
            'Settings': '⚙️'
        }
        
        # Login Tab (index 0)
        self.login_tab = LoginTab(self.notebook, self)
        self.notebook.add(self.login_tab, text=f" {tab_icons['Login']} Login")
        
        # Search/Journey Tab (index 1)
        self.journey_tab = JourneyTab(self.notebook, self)
        self.notebook.add(self.journey_tab, text=f" {tab_icons['Search']} Search Trains")
        
        # Train Select Tab (index 2)
        self.train_select_tab = TrainSelectTab(self.notebook, self)
        self.notebook.add(self.train_select_tab, text=f" {tab_icons['Train']} Select Train")
        
        # Passengers Tab (index 3)
        self.passenger_tab = PassengerTab(self.notebook, self)
        self.notebook.add(self.passenger_tab, text=f" {tab_icons['Passengers']} Add Passengers")
        
        # Payment/Booking Tab (index 4)
        self.booking_tab = BookingTab(self.notebook, self)
        self.notebook.add(self.booking_tab, text=f" {tab_icons['Payment']} Payment")
        
        # PNR Tab (index 5)
        self.pnr_tab = PNRTab(self.notebook, self)
        self.notebook.add(self.pnr_tab, text=f" {tab_icons['PNR']} View PNR")
        
        # History Tab (index 6)
        self.history_tab = HistoryTab(self.notebook, self)
        self.notebook.add(self.history_tab, text=f" {tab_icons['History']} Booking History")
        
        # Settings Tab (index 7)
        self.settings_tab = SettingsTab(self.notebook, self)
        self.notebook.add(self.settings_tab, text=f" {tab_icons['Settings']} Settings")
        
        # Disable tabs that require login initially
        self.update_tab_access()
    
    def update_tab_access(self):
        """Enable/disable tabs based on login status"""
        for i in range(1, 8):  # Skip login tab (index 0)
            self.notebook.tab(i, state='normal' if self.logged_in else 'disabled')
    
    def on_tab_change(self, event):
        """Handle tab change events"""
        current_tab = self.notebook.index(self.notebook.select())
        
        # Update status based on current tab
        tab_names = ["Login", "Search Trains", "Select Train", "Add Passengers", 
                    "Payment", "View PNR", "Booking History", "Settings"]
        
        if current_tab < len(tab_names):
            status_text = f"📍 Current: {tab_names[current_tab]}"
            
            # Add contextual tips
            tips = {
                0: " | ℹ️ Login to access booking features",
                1: " | ℹ️ Select source, destination and date",
                2: " | ℹ️ Choose class and quota",
                3: f" | ℹ️ Add passenger details (max 6)",
                4: " | ℹ️ Select payment method",
                5: " | ℹ️ Your ticket will appear here",
                6: " | ℹ️ View past bookings",
                7: " | ℹ️ Customize application settings"
            }
            
            if current_tab in tips:
                status_text += tips[current_tab]
            
            self.status_label.config(text=status_text)
        
        # Refresh specific tabs when accessed
        if current_tab == 5:  # PNR Tab
            self.pnr_tab.refresh()
        elif current_tab == 6:  # History Tab
            self.history_tab.refresh()
    
    def update_clock(self):
        """Update real-time clock in header and footer"""
        now = datetime.now()
        time_str = now.strftime("%H:%M:%S")
        date_str = now.strftime("%A, %d %B %Y")
        
        # Update header clock
        self.clock_label.config(text=time_str)
        self.date_label.config(text=date_str)
        
        # Update footer clock
        self.footer_clock.config(text=f"🕒 {time_str} | {date_str}")
        
        # Schedule next update after 1000ms (1 second)
        self.root.after(1000, self.update_clock)
    
    def generate_pnr(self):
        """Generate 11-digit PNR number with checksum"""
        # Get current timestamp
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        
        # Get user ID if available
        user_id = self.user_data.get('user_id', '0000') if self.user_data else '0000'
        
        # Create base string
        base = f"{timestamp}{user_id}{len(self.booking_details.get('passengers', []))}"
        
        # Generate hash
        hash_obj = hashlib.md5(base.encode())
        hash_hex = hash_obj.hexdigest()
        
        # Take first 10 digits and add checksum
        pnr_digits = ''.join(filter(str.isdigit, hash_hex))[:10]
        
        # Calculate checksum (last digit)
        checksum = sum(int(d) for d in pnr_digits) % 10
        
        # Return 11-digit PNR
        return f"{pnr_digits}{checksum}"
    
    def save_booking(self):
        """Save current booking to history"""
        if self.booking_details and self.booking_details.get('pnr'):
            # Add to history
            booking_copy = self.booking_details.copy()
            booking_copy['booking_time'] = datetime.now().isoformat()
            self.bookings_history.append(booking_copy)
            
            # Save to file
            self.save_bookings()
            
            return True
        return False
    
    def save_bookings(self):
        """Save bookings to JSON file"""
        try:
            data_path = Path(__file__).parent.parent / 'bookings.json'
            with open(data_path, 'w') as f:
                json.dump(self.bookings_history, f, indent=2)
        except Exception as e:
            print(f"Error saving bookings: {e}")
    
    def load_bookings(self):
        """Load bookings from JSON file"""
        try:
            data_path = Path(__file__).parent.parent / 'bookings.json'
            if data_path.exists():
                with open(data_path, 'r') as f:
                    self.bookings_history = json.load(f)
        except Exception as e:
            print(f"Error loading bookings: {e}")
            self.bookings_history = []
    
    def clear_booking_data(self):
        """Clear current booking data"""
        self.selected_train = None
        self.booking_details = {
            'source': None,
            'destination': None,
            'journey_date': None,
            'train_number': None,
            'train_name': None,
            'class': None,
            'quota': None,
            'berth_preference': None,
            'passengers': [],
            'passenger_count': 0,
            'total_fare': 0,
            'pnr': None,
            'booking_time': None
        }
        self.fare_details = None
    
    def logout(self):
        """Log out current user"""
        self.logged_in = False
        self.user_data = None
        self.clear_booking_data()
        self.update_tab_access()
        self.notebook.select(0)  # Go to login tab
        messagebox.showinfo("Logout", "You have been logged out successfully!")
    
    def show_notification(self, title, message, type='info'):
        """Show modern notification"""
        colors = {
            'info': self.colors['info'],
            'success': self.colors['success'],
            'warning': self.colors['warning'],
            'error': self.colors['danger']
        }
        
        # Create top-level window
        notif = tk.Toplevel(self.root)
        notif.title("")
        notif.configure(bg=colors[type])
        notif.overrideredirect(True)
        
        # Position at top right
        notif.update_idletasks()
        x = self.root.winfo_x() + self.root.winfo_width() - 350
        y = self.root.winfo_y() + 100
        notif.geometry(f'300x100+{x}+{y}')
        
        # Content
        tk.Label(notif, text=title, font=('Segoe UI', 12, 'bold'),
                fg='white', bg=colors[type]).pack(pady=(10, 5))
        
        tk.Label(notif, text=message, font=('Segoe UI', 10),
                fg='white', bg=colors[type], wraplength=280).pack()
        
        # Auto close after 3 seconds
        self.root.after(3000, notif.destroy)