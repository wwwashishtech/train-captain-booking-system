"""
The Train Captain - Settings Tab
Application settings and preferences
Software developed by Ashish Vishwakarma
Version: 3.0 Professional Edition
"""

import tkinter as tk
from tkinter import ttk, messagebox, colorchooser, font
import json
from pathlib import Path
from datetime import datetime

class SettingsTab(tk.Frame):
    """Professional Settings Tab - Application preferences"""
    
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        
        # Configure frame
        self.configure(bg=self.app.colors['background'])
        
        # Create scrollable frame
        self.create_professional_scrollable_frame()
        
        # Settings variables
        self.theme_var = tk.StringVar(value="Default Blue")
        self.notifications_var = tk.BooleanVar(value=True)
        self.auto_save_var = tk.BooleanVar(value=True)
        self.default_class_var = tk.StringVar(value="2A - Second AC")
        self.default_quota_var = tk.StringVar(value="GN - General")
        self.font_size_var = tk.StringVar(value="Medium")
        self.language_var = tk.StringVar(value="English")
        self.email_notify_var = tk.BooleanVar(value=True)
        self.sms_notify_var = tk.BooleanVar(value=False)
        self.autofill_var = tk.BooleanVar(value=False)
        self.timestamp_var = tk.BooleanVar(value=True)
        self.autosave_var = tk.BooleanVar(value=True)
        
        # Create UI
        self.create_professional_widgets()
        
        # Load saved settings
        self.load_settings()
    
    def create_professional_scrollable_frame(self):
        """Create a professional scrollable frame for content"""
        # Main container with border
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
        """Create all settings widgets with professional layout"""
        # Main container
        main_container = tk.Frame(self.scrollable_frame, bg=self.app.colors['background'])
        main_container.pack(fill='both', expand=True, padx=50, pady=30)
        
        # Header
        self.create_header(main_container)
        
        # Settings Grid (2 columns)
        settings_grid = tk.Frame(main_container, bg=self.app.colors['background'])
        settings_grid.pack(fill='both', expand=True)
        
        # Configure grid columns
        settings_grid.columnconfigure(0, weight=1, pad=10)
        settings_grid.columnconfigure(1, weight=1, pad=10)
        
        # Left Column Settings
        left_column = tk.Frame(settings_grid, bg=self.app.colors['background'])
        left_column.grid(row=0, column=0, sticky='nsew', padx=5)
        
        # Appearance Settings
        self.create_appearance_card(left_column)
        
        # Booking Preferences
        self.create_booking_preferences_card(left_column)
        
        # Display Settings
        self.create_display_card(left_column)
        
        # Right Column Settings
        right_column = tk.Frame(settings_grid, bg=self.app.colors['background'])
        right_column.grid(row=0, column=1, sticky='nsew', padx=5)
        
        # Notification Settings
        self.create_notification_card(right_column)
        
        # Data Management
        self.create_data_management_card(right_column)
        
        # About Section
        self.create_about_card(right_column)
        
        # Action Buttons
        self.create_action_buttons(main_container)
    
    def create_header(self, parent):
        """Create header section"""
        header_frame = tk.Frame(parent, bg=self.app.colors['background'])
        header_frame.pack(fill='x', pady=(0, 25))
        
        tk.Label(header_frame, text="⚙️ SETTINGS", 
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
        
        # Last sync
        sync_label = tk.Label(header_frame, 
                             text=f"Last synced: {datetime.now().strftime('%d %b %Y, %I:%M %p')}",
                             font=('Segoe UI', 9),
                             fg=self.app.colors['text_light'], 
                             bg=self.app.colors['background'])
        sync_label.pack(side='right', padx=20)
    
    def create_appearance_card(self, parent):
        """Create appearance settings card"""
        card = self.create_card(parent, "🎨 Appearance Settings")
        
        # Theme selection
        theme_frame = tk.Frame(card, bg='white')
        theme_frame.pack(fill='x', pady=10)
        
        tk.Label(theme_frame, text="Color Theme:", font=('Segoe UI', 11),
                fg=self.app.colors['text'], bg='white').pack(anchor='w')
        
        themes = ["Default Blue", "Dark Mode", "Light Mode", "Forest Green", "Royal Purple", "Sunset Orange"]
        
        theme_combo = ttk.Combobox(theme_frame, textvariable=self.theme_var,
                                  values=themes, state='readonly',
                                  font=('Segoe UI', 10), width=25)
        theme_combo.pack(fill='x', pady=(5, 15))
        
        # Custom colors
        tk.Label(theme_frame, text="Custom Colors:", font=('Segoe UI', 11, 'bold'),
                fg=self.app.colors['text'], bg='white').pack(anchor='w', pady=(10, 5))
        
        color_grid = tk.Frame(theme_frame, bg='white')
        color_grid.pack(fill='x')
        
        # Configure grid for color buttons
        color_grid.columnconfigure(0, weight=1)
        color_grid.columnconfigure(1, weight=1)
        color_grid.columnconfigure(2, weight=1)
        
        # Primary color
        primary_btn = tk.Button(color_grid, text="Primary",
                               command=lambda: self.choose_color('primary'),
                               bg=self.app.colors['primary'], fg='white',
                               font=('Segoe UI', 9, 'bold'), 
                               padx=15, pady=8, width=10,
                               relief='flat', cursor='hand2')
        primary_btn.grid(row=0, column=0, padx=2, pady=2)
        self.add_hover_effect(primary_btn, self.app.colors['primary'], self.app.colors['primary_light'])
        
        # Secondary color
        secondary_btn = tk.Button(color_grid, text="Secondary",
                                 command=lambda: self.choose_color('secondary'),
                                 bg=self.app.colors['secondary'], fg='white',
                                 font=('Segoe UI', 9, 'bold'), 
                                 padx=15, pady=8, width=10,
                                 relief='flat', cursor='hand2')
        secondary_btn.grid(row=0, column=1, padx=2, pady=2)
        self.add_hover_effect(secondary_btn, self.app.colors['secondary'], self.app.colors['secondary_light'])
        
        # Accent color
        accent_btn = tk.Button(color_grid, text="Accent",
                              command=lambda: self.choose_color('accent'),
                              bg=self.app.colors['accent'], fg='white',
                              font=('Segoe UI', 9, 'bold'), 
                              padx=15, pady=8, width=10,
                              relief='flat', cursor='hand2')
        accent_btn.grid(row=0, column=2, padx=2, pady=2)
        self.add_hover_effect(accent_btn, self.app.colors['accent'], self.app.colors['accent'])  # Fixed: removed accent_dark
        
        # Reset button
        reset_btn = tk.Button(theme_frame, text="Reset to Default Colors",
                             command=self.reset_colors,
                             bg=self.app.colors['text_light'], fg='white',
                             font=('Segoe UI', 9), 
                             padx=20, pady=8,
                             relief='flat', cursor='hand2')
        reset_btn.pack(pady=(15, 5))
        self.add_hover_effect(reset_btn, self.app.colors['text_light'], self.app.colors['text'])
    
    def create_booking_preferences_card(self, parent):
        """Create booking preferences card"""
        card = self.create_card(parent, "🎫 Booking Preferences")
        
        # Default class
        class_frame = tk.Frame(card, bg='white')
        class_frame.pack(fill='x', pady=5)
        
        tk.Label(class_frame, text="Default Class:", font=('Segoe UI', 11),
                fg=self.app.colors['text'], bg='white').pack(anchor='w')
        
        classes = ["1A - First AC", "2A - Second AC", "3A - Third AC", 
                   "SL - Sleeper", "CC - Chair Car", "2S - Second Sitting"]
        
        class_combo = ttk.Combobox(class_frame, textvariable=self.default_class_var,
                                  values=classes, state='readonly',
                                  font=('Segoe UI', 10), width=25)
        class_combo.pack(fill='x', pady=(5, 10))
        
        # Default quota
        quota_frame = tk.Frame(card, bg='white')
        quota_frame.pack(fill='x', pady=5)
        
        tk.Label(quota_frame, text="Default Quota:", font=('Segoe UI', 11),
                fg=self.app.colors['text'], bg='white').pack(anchor='w')
        
        quotas = ["GN - General", "TQ - Tatkal", "LD - Ladies", 
                  "SS - Senior Citizen", "FT - Foreign Tourist", "PH - Physically Handicapped"]
        
        quota_combo = ttk.Combobox(quota_frame, textvariable=self.default_quota_var,
                                  values=quotas, state='readonly',
                                  font=('Segoe UI', 10), width=25)
        quota_combo.pack(fill='x', pady=(5, 10))
        
        # Auto-fill passenger details
        autofill_frame = tk.Frame(card, bg='white')
        autofill_frame.pack(fill='x', pady=10)
        
        autofill_check = tk.Checkbutton(autofill_frame, 
                                       text="Auto-fill my details as first passenger",
                                       variable=self.autofill_var,
                                       bg='white', fg=self.app.colors['text'],
                                       selectcolor='white',
                                       activebackground='white',
                                       font=('Segoe UI', 10))
        autofill_check.pack(anchor='w')
    
    def create_display_card(self, parent):
        """Create display settings card"""
        card = self.create_card(parent, "📺 Display Settings")
        
        # Font size
        font_frame = tk.Frame(card, bg='white')
        font_frame.pack(fill='x', pady=5)
        
        tk.Label(font_frame, text="Font Size:", font=('Segoe UI', 11),
                fg=self.app.colors['text'], bg='white').pack(anchor='w')
        
        sizes = ["Small", "Medium", "Large", "Extra Large"]
        
        size_combo = ttk.Combobox(font_frame, textvariable=self.font_size_var,
                                  values=sizes, state='readonly',
                                  font=('Segoe UI', 10), width=15)
        size_combo.pack(fill='x', pady=(5, 10))
        
        # Language
        lang_frame = tk.Frame(card, bg='white')
        lang_frame.pack(fill='x', pady=5)
        
        tk.Label(lang_frame, text="Language:", font=('Segoe UI', 11),
                fg=self.app.colors['text'], bg='white').pack(anchor='w')
        
        languages = ["English", "हिन्दी (Hindi)", "தமிழ் (Tamil)", 
                     "తెలుగు (Telugu)", "বাংলা (Bengali)", "ગુજરાતી (Gujarati)"]
        
        lang_combo = ttk.Combobox(lang_frame, textvariable=self.language_var,
                                  values=languages, state='readonly',
                                  font=('Segoe UI', 10), width=20)
        lang_combo.pack(fill='x', pady=(5, 10))
        
        # Show timestamps
        timestamp_frame = tk.Frame(card, bg='white')
        timestamp_frame.pack(fill='x', pady=5)
        
        timestamp_check = tk.Checkbutton(timestamp_frame, 
                                        text="Show timestamps in history",
                                        variable=self.timestamp_var,
                                        bg='white', fg=self.app.colors['text'],
                                        selectcolor='white',
                                        activebackground='white',
                                        font=('Segoe UI', 10))
        timestamp_check.pack(anchor='w')
    
    def create_notification_card(self, parent):
        """Create notification settings card"""
        card = self.create_card(parent, "🔔 Notification Settings")
        
        # Email notifications
        email_frame = tk.Frame(card, bg='white')
        email_frame.pack(fill='x', pady=5)
        
        email_check = tk.Checkbutton(email_frame, 
                                    text="Email booking confirmation",
                                    variable=self.email_notify_var,
                                    bg='white', fg=self.app.colors['text'],
                                    selectcolor='white',
                                    activebackground='white',
                                    font=('Segoe UI', 10))
        email_check.pack(anchor='w')
        
        # SMS notifications
        sms_frame = tk.Frame(card, bg='white')
        sms_frame.pack(fill='x', pady=5)
        
        sms_check = tk.Checkbutton(sms_frame, 
                                  text="SMS booking updates",
                                  variable=self.sms_notify_var,
                                  bg='white', fg=self.app.colors['text'],
                                  selectcolor='white',
                                  activebackground='white',
                                  font=('Segoe UI', 10))
        sms_check.pack(anchor='w')
        
        # Email address
        email_addr_frame = tk.Frame(card, bg='white')
        email_addr_frame.pack(fill='x', pady=(15, 5))
        
        tk.Label(email_addr_frame, text="Email Address:", font=('Segoe UI', 11, 'bold'),
                fg=self.app.colors['text'], bg='white').pack(anchor='w')
        
        email_input_frame = tk.Frame(email_addr_frame, bg='white', relief='solid', bd=1)
        email_input_frame.pack(fill='x', pady=5)
        
        tk.Label(email_input_frame, text="📧", bg='white', 
                font=('Segoe UI', 11)).pack(side='left', padx=5)
        
        self.email_entry = tk.Entry(email_input_frame, font=('Segoe UI', 10),
                                   bg='white', relief='flat', highlightthickness=0)
        self.email_entry.pack(side='left', fill='x', expand=True, ipady=8)
        
        if self.app.user_data:
            self.email_entry.insert(0, self.app.user_data.get('email', ''))
    
    def create_data_management_card(self, parent):
        """Create data management card"""
        card = self.create_card(parent, "💾 Data Management")
        
        # Auto-save
        autosave_frame = tk.Frame(card, bg='white')
        autosave_frame.pack(fill='x', pady=5)
        
        autosave_check = tk.Checkbutton(autosave_frame, 
                                       text="Auto-save bookings",
                                       variable=self.autosave_var,
                                       bg='white', fg=self.app.colors['text'],
                                       selectcolor='white',
                                       activebackground='white',
                                       font=('Segoe UI', 10))
        autosave_check.pack(anchor='w')
        
        # Data management buttons grid
        button_grid = tk.Frame(card, bg='white')
        button_grid.pack(fill='x', pady=15)
        
        button_grid.columnconfigure(0, weight=1)
        button_grid.columnconfigure(1, weight=1)
        
        # Export data
        export_btn = tk.Button(button_grid, text="📤 Export Bookings",
                              command=self.export_data,
                              bg=self.app.colors['primary'], fg='white',
                              font=('Segoe UI', 10, 'bold'), 
                              padx=15, pady=10,
                              relief='flat', cursor='hand2')
        export_btn.grid(row=0, column=0, padx=2, pady=2, sticky='ew')
        self.add_hover_effect(export_btn, self.app.colors['primary'], self.app.colors['primary_light'])
        
        # Import data
        import_btn = tk.Button(button_grid, text="📥 Import Bookings",
                              command=self.import_data,
                              bg=self.app.colors['secondary'], fg='white',
                              font=('Segoe UI', 10, 'bold'), 
                              padx=15, pady=10,
                              relief='flat', cursor='hand2')
        import_btn.grid(row=0, column=1, padx=2, pady=2, sticky='ew')
        self.add_hover_effect(import_btn, self.app.colors['secondary'], self.app.colors['secondary_light'])
        
        # Clear history
        clear_btn = tk.Button(button_grid, text="🗑️ Clear History",
                             command=self.clear_history,
                             bg=self.app.colors['danger'], fg='white',
                             font=('Segoe UI', 10, 'bold'), 
                             padx=15, pady=10,
                             relief='flat', cursor='hand2')
        clear_btn.grid(row=1, column=0, columnspan=2, pady=5, sticky='ew')
        self.add_hover_effect(clear_btn, self.app.colors['danger'], '#d32f2f')
        
        # Storage info
        storage_frame = tk.Frame(card, bg='white')
        storage_frame.pack(fill='x', pady=10)
        
        total_bookings = len(self.app.bookings_history)
        storage_size = total_bookings * 2  # Approximate KB
        
        tk.Label(storage_frame, text="Storage Usage:", font=('Segoe UI', 10, 'bold'),
                fg=self.app.colors['text'], bg='white').pack(anchor='w')
        
        progress_frame = tk.Frame(storage_frame, height=6, bg=self.app.colors['border'])
        progress_frame.pack(fill='x', pady=5)
        progress_frame.pack_propagate(False)
        
        usage_percent = min(100, storage_size)
        progress = tk.Frame(progress_frame, bg=self.app.colors['success'],
                           width=int(200 * usage_percent / 100))
        progress.place(x=0, y=0, height=6)
        
        tk.Label(storage_frame, text=f"{total_bookings} bookings • {storage_size} KB used",
                font=('Segoe UI', 9), fg=self.app.colors['text_light'], bg='white').pack(anchor='w')
    
    def create_about_card(self, parent):
        """Create about section card"""
        card = self.create_card(parent, "ℹ️ About")
        
        # App info
        info_frame = tk.Frame(card, bg='white')
        info_frame.pack(fill='x', pady=10)
        
        # Logo
        tk.Label(info_frame, text="🚂", font=('Segoe UI', 32),
                fg=self.app.colors['primary'], bg='white').pack()
        
        tk.Label(info_frame, text="The Train Captain", 
                font=('Segoe UI', 16, 'bold'),
                fg=self.app.colors['primary'], bg='white').pack()
        
        tk.Label(info_frame, text="Version 3.0 Professional", 
                font=('Segoe UI', 11),
                fg=self.app.colors['text_light'], bg='white').pack()
        
        # Separator
        ttk.Separator(info_frame, orient='horizontal').pack(fill='x', pady=15)
        
        # Developer info
        dev_frame = tk.Frame(info_frame, bg='white')
        dev_frame.pack(fill='x')
        
        tk.Label(dev_frame, text="Developed by:", font=('Segoe UI', 10, 'bold'),
                fg=self.app.colors['text'], bg='white').pack()
        
        tk.Label(dev_frame, text="Ashish Vishwakarma", 
                font=('Segoe UI', 12, 'bold'),
                fg=self.app.colors['accent'], bg='white').pack()
        
        tk.Label(dev_frame, text="© 2024 All Rights Reserved", 
                font=('Segoe UI', 9),
                fg=self.app.colors['text_light'], bg='white').pack(pady=5)
        
        # Features
        features_frame = tk.Frame(info_frame, bg='white')
        features_frame.pack(fill='x', pady=10)
        
        features = [
            "✓ 8+ Million Happy Users",
            "✓ 5000+ Trains Covered",
            "✓ 24/7 Customer Support",
            "✓ Secure Payments",
            "✓ Instant PNR Generation"
        ]
        
        for feature in features:
            tk.Label(features_frame, text=feature, 
                    font=('Segoe UI', 9),
                    fg=self.app.colors['text'], bg='white').pack(anchor='w')
    
    def create_action_buttons(self, parent):
        """Create action buttons"""
        button_frame = tk.Frame(parent, bg=self.app.colors['background'])
        button_frame.pack(fill='x', pady=30)
        
        # Configure grid for centered buttons
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        button_frame.columnconfigure(2, weight=1)
        
        # Save button
        save_btn = tk.Button(button_frame, text="💾 SAVE SETTINGS",
                            command=self.save_settings,
                            bg=self.app.colors['success'], fg='white',
                            font=('Segoe UI', 12, 'bold'), 
                            padx=40, pady=12, width=20,
                            relief='flat', cursor='hand2')
        save_btn.grid(row=0, column=1, padx=10)
        self.add_hover_effect(save_btn, self.app.colors['success'], '#43a047')
        
        # Cancel button
        cancel_btn = tk.Button(button_frame, text="✕ CANCEL",
                              command=self.load_settings,
                              bg=self.app.colors['text_light'], fg='white',
                              font=('Segoe UI', 11), 
                              padx=30, pady=12, width=15,
                              relief='flat', cursor='hand2')
        cancel_btn.grid(row=0, column=0, padx=10)
        self.add_hover_effect(cancel_btn, self.app.colors['text_light'], self.app.colors['text'])
        
        # Reset all button
        reset_all_btn = tk.Button(button_frame, text="⟲ RESET ALL",
                                 command=self.reset_all_settings,
                                 bg=self.app.colors['warning'], fg='white',
                                 font=('Segoe UI', 11), 
                                 padx=30, pady=12, width=15,
                                 relief='flat', cursor='hand2')
        reset_all_btn.grid(row=0, column=2, padx=10)
        self.add_hover_effect(reset_all_btn, self.app.colors['warning'], self.app.colors['warning'])  # Fixed: removed warning_dark
    
    def create_card(self, parent, title):
        """Create a card with title"""
        card = tk.Frame(parent, bg='white', relief='solid', bd=1,
                       highlightbackground=self.app.colors['border'])
        card.pack(fill='x', pady=(0, 20))
        
        # Card header
        header = tk.Frame(card, bg=self.app.colors['primary_light'], height=40)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        tk.Label(header, text=title, font=('Segoe UI', 12, 'bold'),
                fg='white', bg=self.app.colors['primary_light']).pack(side='left', padx=15)
        
        # Card content
        content = tk.Frame(card, bg='white')
        content.pack(padx=20, pady=20, fill='x')
        
        return content
    
    def choose_color(self, color_key):
        """Open color chooser dialog"""
        color = colorchooser.askcolor(title=f"Choose {color_key} color",
                                     color=self.app.colors[color_key])
        if color[1]:
            self.app.colors[color_key] = color[1]
            messagebox.showinfo("Success", f"{color_key.title()} color updated!\nRestart to see changes.")
    
    def reset_colors(self):
        """Reset colors to default"""
        self.app.colors = {
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
            'gradient_end': '#3282b8',
            'shadow': '#d3d3d3'
        }
        messagebox.showinfo("Success", "Colors reset to default!\nRestart to see changes.")
    
    def save_settings(self):
        """Save all settings to file"""
        settings = {
            'theme': self.theme_var.get(),
            'notifications': self.notifications_var.get(),
            'auto_save': self.auto_save_var.get(),
            'default_class': self.default_class_var.get(),
            'default_quota': self.default_quota_var.get(),
            'font_size': self.font_size_var.get(),
            'language': self.language_var.get(),
            'email_notify': self.email_notify_var.get(),
            'sms_notify': self.sms_notify_var.get(),
            'autofill': self.autofill_var.get(),
            'email': self.email_entry.get() if hasattr(self, 'email_entry') else '',
            'show_timestamps': self.timestamp_var.get(),
            'autosave': self.autosave_var.get(),
            'last_saved': datetime.now().isoformat()
        }
        
        try:
            settings_path = Path(__file__).parent.parent / 'settings.json'
            with open(settings_path, 'w') as f:
                json.dump(settings, f, indent=2)
            
            messagebox.showinfo("Success", "Settings saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {e}")
    
    def load_settings(self):
        """Load settings from file"""
        try:
            settings_path = Path(__file__).parent.parent / 'settings.json'
            if settings_path.exists():
                with open(settings_path, 'r') as f:
                    settings = json.load(f)
                
                # Apply settings to variables
                self.theme_var.set(settings.get('theme', 'Default Blue'))
                self.notifications_var.set(settings.get('notifications', True))
                self.auto_save_var.set(settings.get('auto_save', True))
                self.default_class_var.set(settings.get('default_class', '2A - Second AC'))
                self.default_quota_var.set(settings.get('default_quota', 'GN - General'))
                self.font_size_var.set(settings.get('font_size', 'Medium'))
                self.language_var.set(settings.get('language', 'English'))
                self.email_notify_var.set(settings.get('email_notify', True))
                self.sms_notify_var.set(settings.get('sms_notify', False))
                self.autofill_var.set(settings.get('autofill', False))
                self.timestamp_var.set(settings.get('show_timestamps', True))
                self.autosave_var.set(settings.get('autosave', True))
                
                if hasattr(self, 'email_entry') and 'email' in settings:
                    self.email_entry.delete(0, tk.END)
                    self.email_entry.insert(0, settings['email'])
        except:
            pass  # Use defaults if file doesn't exist
    
    def reset_all_settings(self):
        """Reset all settings to defaults"""
        if messagebox.askyesno("Reset All", "Are you sure you want to reset all settings to defaults?"):
            self.theme_var.set("Default Blue")
            self.notifications_var.set(True)
            self.auto_save_var.set(True)
            self.default_class_var.set("2A - Second AC")
            self.default_quota_var.set("GN - General")
            self.font_size_var.set("Medium")
            self.language_var.set("English")
            self.email_notify_var.set(True)
            self.sms_notify_var.set(False)
            self.autofill_var.set(False)
            self.timestamp_var.set(True)
            self.autosave_var.set(True)
            
            if hasattr(self, 'email_entry'):
                self.email_entry.delete(0, tk.END)
                if self.app.user_data:
                    self.email_entry.insert(0, self.app.user_data.get('email', ''))
            
            messagebox.showinfo("Success", "All settings reset to defaults!")
    
    def export_data(self):
        """Export bookings to file"""
        try:
            from tkinter import filedialog
            filename = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                initialfile=f"bookings_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            )
            
            if filename:
                with open(filename, 'w') as f:
                    json.dump(self.app.bookings_history, f, indent=2, default=str)
                messagebox.showinfo("Success", f"Bookings exported to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export: {e}")
    
    def import_data(self):
        """Import bookings from file"""
        try:
            from tkinter import filedialog
            filename = filedialog.askopenfilename(
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                title="Import Bookings"
            )
            
            if filename:
                with open(filename, 'r') as f:
                    imported = json.load(f)
                
                # Merge with existing bookings
                self.app.bookings_history.extend(imported)
                self.app.save_bookings()
                
                messagebox.showinfo("Success", f"Imported {len(imported)} bookings")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to import: {e}")
    
    def clear_history(self):
        """Clear all booking history"""
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all booking history?\nThis action cannot be undone!"):
            self.app.bookings_history = []
            self.app.save_bookings()
            messagebox.showinfo("Success", "Booking history cleared")
    
    def add_hover_effect(self, button, normal_color, hover_color):
        """Add hover effect to button"""
        def on_enter(e):
            button['background'] = hover_color
            button.config(cursor='hand2')
        
        def on_leave(e):
            button['background'] = normal_color
        
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)