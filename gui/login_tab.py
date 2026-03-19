"""
The Train Captain - Login Tab
Handles user authentication and registration with enhanced UI
Software developed by Ashish Vishwakarma
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json
import os
import re
from pathlib import Path
import hashlib
import random

class LoginTab(tk.Frame):
    """Enhanced Login and Registration Tab with Professional GUI"""
    
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.parent = parent
        
        # Configure frame
        self.configure(bg=self.app.colors['background'])
        
        # Initialize variables
        self.is_login_mode = tk.BooleanVar(value=True)
        self.remember_me = tk.BooleanVar(value=False)
        self.show_password = tk.BooleanVar(value=False)
        
        # Entry widgets
        self.username_entry = None
        self.password_entry = None
        self.name_entry = None
        self.email_entry = None
        self.reg_username_entry = None
        self.reg_password_entry = None
        self.confirm_entry = None
        self.phone_entry = None
        self.action_button = None
        
        # Create scrollable frame with enhanced scrolling
        self.create_scrollable_frame()
        
        # Create UI
        self.create_widgets()
        
        # Load saved credentials if remember me was checked
        self.load_saved_credentials()
    
    def create_scrollable_frame(self):
        """Create an enhanced scrollable frame for content"""
        # Main container with border
        main_container = tk.Frame(self, bg=self.app.colors['surface'], 
                                 relief='solid', bd=1, highlightbackground=self.app.colors['border'])
        main_container.pack(fill='both', expand=True, padx=1, pady=1)
        
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
        
        def on_enter(event):
            self.canvas.bind_all("<MouseWheel>", on_mousewheel)
        
        def on_leave(event):
            self.canvas.unbind_all("<MouseWheel>")
        
        self.canvas.bind("<Enter>", on_enter)
        self.canvas.bind("<Leave>", on_leave)
    
    def create_widgets(self):
        """Create all widgets for login/register"""
        # Main container with gradient background
        main_container = tk.Frame(self.scrollable_frame, bg=self.app.colors['background'])
        main_container.pack(expand=True, fill='both', padx=30, pady=30)
        
        # Create left and right split
        split_frame = tk.Frame(main_container, bg=self.app.colors['background'])
        split_frame.pack(fill='both', expand=True)
        
        # Configure grid
        split_frame.columnconfigure(0, weight=1)
        split_frame.columnconfigure(1, weight=1)
        
        # Left side - Welcome/Branding
        self.create_branding_section(split_frame)
        
        # Right side - Login/Register Form
        self.create_form_section(split_frame)
    
    def create_branding_section(self, parent):
        """Create left side branding section"""
        branding_frame = tk.Frame(parent, bg=self.app.colors['primary'], 
                                  relief='solid', bd=1)
        branding_frame.grid(row=0, column=0, sticky='nsew', padx=(0, 10))
        
        # Center content
        center_frame = tk.Frame(branding_frame, bg=self.app.colors['primary'])
        center_frame.pack(expand=True, fill='both', padx=30, pady=50)
        
        # Train animation
        canvas = tk.Canvas(center_frame, width=200, height=100, 
                          bg=self.app.colors['primary'], highlightthickness=0)
        canvas.pack(pady=20)
        
        # Draw train
        self.animate_train(canvas)
        
        # Welcome text
        tk.Label(center_frame, text="Welcome to", 
                font=('Segoe UI', 16), fg='white', 
                bg=self.app.colors['primary']).pack()
        
        tk.Label(center_frame, text="THE TRAIN CAPTAIN", 
                font=('Segoe UI', 24, 'bold'), fg=self.app.colors['accent'], 
                bg=self.app.colors['primary']).pack(pady=10)
        
        tk.Label(center_frame, text="Your Trusted Railway Booking Partner", 
                font=('Segoe UI', 12), fg='white', 
                bg=self.app.colors['primary']).pack()
        
        # Features list
        features_frame = tk.Frame(center_frame, bg=self.app.colors['primary'])
        features_frame.pack(pady=30)
        
        features = [
            "✓ 8+ Million Happy Customers",
            "✓ 5000+ Trains Available",
            "✓ 24/7 Customer Support",
            "✓ Instant PNR Generation",
            "✓ Secure Payments"
        ]
        
        for feature in features:
            tk.Label(features_frame, text=feature, 
                    font=('Segoe UI', 11), fg='white', 
                    bg=self.app.colors['primary']).pack(pady=2)
        
        # Developer credit
        tk.Label(center_frame, text="Developed by Ashish Vishwakarma", 
                font=('Segoe UI', 10, 'italic'), fg=self.app.colors['accent'], 
                bg=self.app.colors['primary']).pack(side='bottom', pady=20)
    
    def animate_train(self, canvas):
        """Animate train on canvas"""
        x = 50
        # Draw train
        canvas.create_rectangle(x, 40, x+100, 70, 
                               fill=self.app.colors['secondary'], outline='white', width=2)
        canvas.create_rectangle(x+20, 30, x+40, 40, 
                               fill=self.app.colors['accent'], outline='white')
        canvas.create_oval(x+10, 70, x+30, 90, fill='black')
        canvas.create_oval(x+70, 70, x+90, 90, fill='black')
        
        # Animation loop
        def move():
            canvas.move(1, 2, 0)  # Move train
            canvas.move(2, 2, 0)  # Move windows
            canvas.move(3, 2, 0)  # Move wheels
            canvas.move(4, 2, 0)  # Move wheels
            if canvas.coords(1)[0] > 200:
                canvas.move(1, -200, 0)
                canvas.move(2, -200, 0)
                canvas.move(3, -200, 0)
                canvas.move(4, -200, 0)
            canvas.after(50, move)
        
        move()
    
    def create_form_section(self, parent):
        """Create right side form section"""
        form_container = tk.Frame(parent, bg=self.app.colors['surface'],
                                  relief='solid', bd=1, highlightbackground=self.app.colors['border'])
        form_container.grid(row=0, column=1, sticky='nsew', padx=(10, 0))
        
        # Form header with toggle
        header_frame = tk.Frame(form_container, bg=self.app.colors['primary'], height=60)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        # Mode toggle buttons
        toggle_frame = tk.Frame(header_frame, bg=self.app.colors['primary'])
        toggle_frame.pack(expand=True)
        
        login_btn = tk.Button(toggle_frame, text="LOGIN", 
                             command=lambda: self.set_mode(True),
                             bg=self.app.colors['primary'] if self.is_login_mode.get() else self.app.colors['primary_dark'],
                             fg='white', font=('Segoe UI', 12, 'bold'),
                             padx=30, pady=8, relief='flat', cursor='hand2',
                             width=10)
        login_btn.pack(side='left', padx=2)
        
        register_btn = tk.Button(toggle_frame, text="REGISTER", 
                                command=lambda: self.set_mode(False),
                                bg=self.app.colors['primary'] if not self.is_login_mode.get() else self.app.colors['primary_dark'],
                                fg='white', font=('Segoe UI', 12, 'bold'),
                                padx=30, pady=8, relief='flat', cursor='hand2',
                                width=10)
        register_btn.pack(side='left', padx=2)
        
        self.toggle_buttons = (login_btn, register_btn)
        
        # Form container
        self.form_container = tk.Frame(form_container, bg=self.app.colors['surface'])
        self.form_container.pack(expand=True, fill='both', padx=40, pady=40)
        
        # Create login form initially
        self.create_login_form()
    
    def set_mode(self, is_login):
        """Set login/register mode"""
        self.is_login_mode.set(is_login)
        
        # Update button colors
        login_btn, register_btn = self.toggle_buttons
        if is_login:
            login_btn.config(bg=self.app.colors['primary'])
            register_btn.config(bg=self.app.colors['primary_dark'])
        else:
            login_btn.config(bg=self.app.colors['primary_dark'])
            register_btn.config(bg=self.app.colors['primary'])
        
        self.toggle_mode()
    
    def create_login_form(self):
        """Create enhanced login form"""
        # Clear form container
        for widget in self.form_container.winfo_children():
            widget.destroy()
        
        # Form title
        tk.Label(self.form_container, text="Welcome Back!", 
                font=('Segoe UI', 20, 'bold'),
                fg=self.app.colors['primary'], bg=self.app.colors['surface']).pack(pady=(0, 30))
        
        # Username with icon
        username_frame = tk.Frame(self.form_container, bg='white', 
                                  relief='solid', bd=1, highlightbackground=self.app.colors['border'])
        username_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(username_frame, text="👤", bg='white', 
                font=('Segoe UI', 12)).pack(side='left', padx=10)
        
        self.username_entry = tk.Entry(username_frame, font=('Segoe UI', 11),
                                      bg='white', fg=self.app.colors['text'],
                                      relief='flat', highlightthickness=0)
        self.username_entry.pack(side='left', fill='x', expand=True, ipady=10)
        self.username_entry.insert(0, "Username")
        self.username_entry.bind('<FocusIn>', lambda e: self.on_entry_click(e, "Username"))
        self.username_entry.bind('<FocusOut>', lambda e: self.on_entry_leave(e, "Username"))
        
        # Password with icon
        password_frame = tk.Frame(self.form_container, bg='white',
                                  relief='solid', bd=1, highlightbackground=self.app.colors['border'])
        password_frame.pack(fill='x', pady=(0, 15))
        
        tk.Label(password_frame, text="🔒", bg='white', 
                font=('Segoe UI', 12)).pack(side='left', padx=10)
        
        self.password_entry = tk.Entry(password_frame, font=('Segoe UI', 11),
                                      show='•', bg='white', fg=self.app.colors['text'],
                                      relief='flat', highlightthickness=0)
        self.password_entry.pack(side='left', fill='x', expand=True, ipady=10)
        self.password_entry.insert(0, "Password")
        self.password_entry.bind('<FocusIn>', lambda e: self.on_entry_click(e, "Password", is_password=True))
        self.password_entry.bind('<FocusOut>', lambda e: self.on_entry_leave(e, "Password", is_password=True))
        
        # Show password checkbox
        show_frame = tk.Frame(self.form_container, bg=self.app.colors['surface'])
        show_frame.pack(fill='x', pady=(0, 15))
        
        show_check = tk.Checkbutton(show_frame, text="Show Password", 
                                    variable=self.show_password,
                                    command=self.toggle_password_visibility,
                                    bg=self.app.colors['surface'],
                                    fg=self.app.colors['text'],
                                    selectcolor=self.app.colors['surface'],
                                    activebackground=self.app.colors['surface'],
                                    font=('Segoe UI', 9))
        show_check.pack(side='left')
        
        # Remember me and Forgot password
        options_frame = tk.Frame(self.form_container, bg=self.app.colors['surface'])
        options_frame.pack(fill='x', pady=(0, 25))
        
        remember_check = tk.Checkbutton(options_frame, text="Remember Me",
                                        variable=self.remember_me,
                                        bg=self.app.colors['surface'],
                                        fg=self.app.colors['text'],
                                        selectcolor=self.app.colors['surface'],
                                        activebackground=self.app.colors['surface'],
                                        font=('Segoe UI', 9))
        remember_check.pack(side='left')
        
        forgot_btn = tk.Button(options_frame, text="Forgot Password?",
                              command=self.show_forgot_password,
                              bg=self.app.colors['surface'], fg=self.app.colors['primary'],
                              font=('Segoe UI', 9, 'bold'),
                              relief='flat', cursor='hand2')
        forgot_btn.pack(side='right')
        self.add_hover_effect(forgot_btn, self.app.colors['surface'], self.app.colors['background'])
        
        # Login button
        self.action_button = tk.Button(self.form_container, text="LOGIN", 
                                       command=self.handle_login,
                                       bg=self.app.colors['primary'], fg='white',
                                       font=('Segoe UI', 14, 'bold'),
                                       padx=30, pady=12, relief='flat', 
                                       cursor='hand2', width=20)
        self.action_button.pack(pady=(0, 15))
        self.add_hover_effect(self.action_button, self.app.colors['primary'], self.app.colors['primary_dark'])
        
        # Bind Enter key
        self.password_entry.bind('<Return>', lambda e: self.handle_login())
        self.username_entry.bind('<Return>', lambda e: self.password_entry.focus())
    
    def create_register_form(self):
        """Create enhanced registration form"""
        # Clear form container
        for widget in self.form_container.winfo_children():
            widget.destroy()
        
        # Form title
        tk.Label(self.form_container, text="Create Account", 
                font=('Segoe UI', 20, 'bold'),
                fg=self.app.colors['primary'], bg=self.app.colors['surface']).pack(pady=(0, 20))
        
        # Full Name
        self.create_registration_field("👤", "Full Name", "name")
        
        # Email
        self.create_registration_field("📧", "Email Address", "email")
        
        # Username
        self.create_registration_field("🔑", "Username", "reg_username")
        
        # Password
        self.create_registration_field("🔒", "Password", "reg_password", is_password=True)
        
        # Confirm Password
        self.create_registration_field("🔒", "Confirm Password", "confirm", is_password=True)
        
        # Phone (optional)
        self.create_registration_field("📱", "Phone Number (Optional)", "phone")
        
        # Terms and conditions
        terms_frame = tk.Frame(self.form_container, bg=self.app.colors['surface'])
        terms_frame.pack(fill='x', pady=(10, 20))
        
        self.terms_var = tk.BooleanVar(value=False)
        terms_check = tk.Checkbutton(terms_frame, text="I agree to the ", 
                                     variable=self.terms_var,
                                     bg=self.app.colors['surface'],
                                     fg=self.app.colors['text'],
                                     selectcolor=self.app.colors['surface'],
                                     activebackground=self.app.colors['surface'],
                                     font=('Segoe UI', 9))
        terms_check.pack(side='left')
        
        terms_link = tk.Button(terms_frame, text="Terms & Conditions",
                              command=self.show_terms,
                              bg=self.app.colors['surface'], fg=self.app.colors['primary'],
                              font=('Segoe UI', 9, 'bold'),
                              relief='flat', cursor='hand2')
        terms_link.pack(side='left')
        self.add_hover_effect(terms_link, self.app.colors['surface'], self.app.colors['background'])
        
        # Register button
        self.action_button = tk.Button(self.form_container, text="CREATE ACCOUNT", 
                                       command=self.handle_login,
                                       bg=self.app.colors['primary'], fg='white',
                                       font=('Segoe UI', 14, 'bold'),
                                       padx=30, pady=12, relief='flat', 
                                       cursor='hand2', width=20)
        self.action_button.pack()
        self.add_hover_effect(self.action_button, self.app.colors['primary'], self.app.colors['primary_dark'])
    
    def create_registration_field(self, icon, placeholder, attr_name, is_password=False):
        """Create a registration field with consistent styling"""
        frame = tk.Frame(self.form_container, bg='white',
                         relief='solid', bd=1, highlightbackground=self.app.colors['border'])
        frame.pack(fill='x', pady=(0, 15))
        
        tk.Label(frame, text=icon, bg='white', 
                font=('Segoe UI', 12)).pack(side='left', padx=10)
        
        entry = tk.Entry(frame, font=('Segoe UI', 11),
                        show='•' if is_password else '',
                        bg='white', fg=self.app.colors['text'],
                        relief='flat', highlightthickness=0)
        entry.pack(side='left', fill='x', expand=True, ipady=10)
        entry.insert(0, placeholder)
        
        # Store reference
        setattr(self, f"{attr_name}_entry", entry)
        
        # Bind events
        entry.bind('<FocusIn>', lambda e, p=placeholder: self.on_entry_click(e, p, is_password))
        entry.bind('<FocusOut>', lambda e, p=placeholder: self.on_entry_leave(e, p, is_password))
    
    def on_entry_click(self, event, placeholder, is_password=False):
        """Handle entry click to clear placeholder"""
        entry = event.widget
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            if is_password:
                entry.config(show='•')
            else:
                entry.config(show='')
    
    def on_entry_leave(self, event, placeholder, is_password=False):
        """Handle entry leave to restore placeholder if empty"""
        entry = event.widget
        if not entry.get():
            if is_password:
                entry.config(show='')
            entry.insert(0, placeholder)
    
    def toggle_password_visibility(self):
        """Toggle password visibility"""
        if hasattr(self, 'password_entry'):
            if self.show_password.get():
                self.password_entry.config(show='')
            else:
                self.password_entry.config(show='•')
    
    def toggle_mode(self):
        """Toggle between login and register modes"""
        if self.is_login_mode.get():
            self.create_login_form()
        else:
            self.create_register_form()
    
    def handle_login(self):
        """Handle login or registration"""
        if self.is_login_mode.get():
            self.login()
        else:
            self.register()
    
    def login(self):
        """Process login with enhanced validation"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        
        # Remove placeholder if present
        if username == "Username":
            username = ""
        if password == "Password":
            password = ""
        
        # Validate inputs
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return
        
        # Load users from file
        users = self.load_users()
        
        # Hash password for comparison
        hashed_password = self.hash_password(password)
        
        # Check credentials
        if username in users and users[username]['password'] == hashed_password:
            # Login successful
            self.app.logged_in = True
            self.app.user_data = {
                'user_id': username,
                'name': users[username]['name'],
                'email': users[username]['email'],
                'phone': users[username].get('phone', '')
            }
            
            # Save credentials if remember me is checked
            if self.remember_me.get():
                self.save_credentials(username, password)
            
            # Show welcome back message with animation
            self.show_welcome_message(users[username]['name'])
            
            # Update tab access
            self.app.update_tab_access()
            
            # Go to search tab
            self.app.notebook.select(1)
            
            # Clear form
            self.clear_form()
        else:
            messagebox.showerror("Error", "Invalid username or password")
    
    def register(self):
        """Process registration with enhanced validation"""
        # Get form data
        name = self.name_entry.get().strip() if hasattr(self, 'name_entry') else ""
        email = self.email_entry.get().strip() if hasattr(self, 'email_entry') else ""
        username = self.reg_username_entry.get().strip() if hasattr(self, 'reg_username_entry') else ""
        password = self.reg_password_entry.get() if hasattr(self, 'reg_password_entry') else ""
        confirm = self.confirm_entry.get() if hasattr(self, 'confirm_entry') else ""
        phone = self.phone_entry.get().strip() if hasattr(self, 'phone_entry') else ""
        
        # Remove placeholders
        if name == "Full Name":
            name = ""
        if email == "Email Address":
            email = ""
        if username == "Username":
            username = ""
        if password == "Password":
            password = ""
        if confirm == "Confirm Password":
            confirm = ""
        if phone == "Phone Number (Optional)":
            phone = ""
        
        # Validate inputs
        if not all([name, email, username, password, confirm]):
            messagebox.showerror("Error", "Please fill in all required fields")
            return
        
        if password != confirm:
            messagebox.showerror("Error", "Passwords do not match")
            return
        
        # Password strength check
        is_valid, message = self.check_password_strength(password)
        if not is_valid:
            messagebox.showerror("Error", message)
            return
        
        # Email validation
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            messagebox.showerror("Error", "Please enter a valid email address")
            return
        
        # Terms agreement
        if not hasattr(self, 'terms_var') or not self.terms_var.get():
            messagebox.showerror("Error", "Please agree to Terms & Conditions")
            return
        
        # Load existing users
        users = self.load_users()
        
        # Check if username already exists
        if username in users:
            messagebox.showerror("Error", "Username already exists. Please choose another.")
            return
        
        # Check if email already exists
        for user_data in users.values():
            if user_data.get('email') == email:
                messagebox.showerror("Error", "Email already registered. Please use another.")
                return
        
        # Hash password
        hashed_password = self.hash_password(password)
        
        # Save new user
        users[username] = {
            'name': name,
            'email': email,
            'password': hashed_password,
            'phone': phone,
            'registered_date': datetime.now().isoformat(),
            'last_login': None,
            'total_bookings': 0,
            'member_since': datetime.now().strftime("%B %Y")
        }
        
        if self.save_users(users):
            messagebox.showinfo("Success", 
                              "Registration successful! Please login.\n\n"
                              "You can now book tickets with your new account.")
            
            # Switch to login mode
            self.set_mode(True)
            
            # Pre-fill username
            if hasattr(self, 'username_entry'):
                self.username_entry.delete(0, tk.END)
                self.username_entry.insert(0, username)
        else:
            messagebox.showerror("Error", "Registration failed. Please try again.")
    
    def check_password_strength(self, password):
        """Check password strength"""
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"
        
        if not re.search(r'[A-Z]', password):
            return False, "Password must contain at least one uppercase letter"
        
        if not re.search(r'[a-z]', password):
            return False, "Password must contain at least one lowercase letter"
        
        if not re.search(r'[0-9]', password):
            return False, "Password must contain at least one number"
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return False, "Password must contain at least one special character"
        
        return True, "Strong"
    
    def show_welcome_message(self, name):
        """Show animated welcome message"""
        welcome = tk.Toplevel(self)
        welcome.title("")
        welcome.geometry("400x200")
        welcome.configure(bg=self.app.colors['success'])
        welcome.overrideredirect(True)
        
        # Center on screen
        welcome.update_idletasks()
        x = (welcome.winfo_screenwidth() // 2) - (400 // 2)
        y = (welcome.winfo_screenheight() // 2) - (200 // 2)
        welcome.geometry(f'400x200+{x}+{y}')
        
        tk.Label(welcome, text="✓ Login Successful!", 
                font=('Segoe UI', 18, 'bold'),
                fg='white', bg=self.app.colors['success']).pack(pady=30)
        
        tk.Label(welcome, text=f"Welcome back, {name}!", 
                font=('Segoe UI', 14),
                fg='white', bg=self.app.colors['success']).pack()
        
        tk.Label(welcome, text="Redirecting to search page...", 
                font=('Segoe UI', 11),
                fg='white', bg=self.app.colors['success']).pack(pady=20)
        
        # Auto close
        self.after(2000, welcome.destroy)
    
    def show_forgot_password(self):
        """Show forgot password dialog"""
        dialog = tk.Toplevel(self)
        dialog.title("Reset Password")
        dialog.geometry("400x300")
        dialog.configure(bg='white')
        dialog.transient(self)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (dialog.winfo_screenheight() // 2) - (300 // 2)
        dialog.geometry(f'400x300+{x}+{y}')
        
        tk.Label(dialog, text="Reset Password", 
                font=('Segoe UI', 16, 'bold'),
                fg=self.app.colors['primary'], bg='white').pack(pady=20)
        
        tk.Label(dialog, text="Enter your email address", 
                font=('Segoe UI', 11),
                fg=self.app.colors['text'], bg='white').pack()
        
        email_frame = tk.Frame(dialog, bg='white', relief='solid', bd=1)
        email_frame.pack(pady=20, padx=40, fill='x')
        
        tk.Label(email_frame, text="📧", bg='white', 
                font=('Segoe UI', 11)).pack(side='left', padx=10)
        
        email_entry = tk.Entry(email_frame, font=('Segoe UI', 11),
                              bg='white', relief='flat')
        email_entry.pack(side='left', fill='x', expand=True, ipady=8)
        
        def send_reset():
            email = email_entry.get().strip()
            if email:
                messagebox.showinfo("Reset Link Sent", 
                                   f"Password reset link has been sent to {email}")
                dialog.destroy()
            else:
                messagebox.showerror("Error", "Please enter your email")
        
        send_btn = tk.Button(dialog, text="Send Reset Link",
                            command=send_reset,
                            bg=self.app.colors['primary'], fg='white',
                            font=('Segoe UI', 11), padx=30, pady=8,
                            relief='flat', cursor='hand2')
        send_btn.pack(pady=10)
        
        cancel_btn = tk.Button(dialog, text="Cancel",
                              command=dialog.destroy,
                              bg=self.app.colors['text_light'], fg='white',
                              font=('Segoe UI', 11), padx=30, pady=8,
                              relief='flat', cursor='hand2')
        cancel_btn.pack()
    
    def show_terms(self):
        """Show terms and conditions"""
        terms = tk.Toplevel(self)
        terms.title("Terms & Conditions")
        terms.geometry("600x400")
        terms.configure(bg='white')
        terms.transient(self)
        
        # Center dialog
        terms.update_idletasks()
        x = (terms.winfo_screenwidth() // 2) - (600 // 2)
        y = (terms.winfo_screenheight() // 2) - (400 // 2)
        terms.geometry(f'600x400+{x}+{y}')
        
        # Terms text
        text_widget = tk.Text(terms, wrap='word', font=('Segoe UI', 11),
                             padx=20, pady=20, bg='white')
        text_widget.pack(fill='both', expand=True)
        
        terms_text = """
        TERMS AND CONDITIONS

        1. Acceptance of Terms
        By accessing and using The Train Captain application, you agree to be bound by these Terms and Conditions.

        2. User Registration
        You must provide accurate and complete information during registration. You are responsible for maintaining the confidentiality of your account.

        3. Booking and Payments
        All bookings are subject to availability. Payments are processed securely through our payment partners.

        4. Cancellation and Refunds
        Cancellation charges apply as per IRCTC rules. Refunds will be processed to the original payment method.

        5. User Conduct
        You agree to use the application only for lawful purposes and in accordance with these Terms.

        6. Privacy
        Your personal information is handled according to our Privacy Policy.

        7. Modifications
        We reserve the right to modify these terms at any time.

        8. Contact
        For any questions regarding these terms, please contact our support team.

        Last updated: March 2024
        """
        
        text_widget.insert('1.0', terms_text)
        text_widget.config(state='disabled')
        
        close_btn = tk.Button(terms, text="Close",
                             command=terms.destroy,
                             bg=self.app.colors['primary'], fg='white',
                             font=('Segoe UI', 11), padx=30, pady=8,
                             relief='flat', cursor='hand2')
        close_btn.pack(pady=10)
    
    def save_credentials(self, username, password):
        """Save credentials for remember me"""
        try:
            cred_path = Path(__file__).parent.parent / '.credentials'
            with open(cred_path, 'w') as f:
                json.dump({
                    'username': username,
                    'password': self.hash_password(password)  # Store hash for security
                }, f)
        except:
            pass
    
    def load_saved_credentials(self):
        """Load saved credentials"""
        try:
            cred_path = Path(__file__).parent.parent / '.credentials'
            if cred_path.exists():
                with open(cred_path, 'r') as f:
                    creds = json.load(f)
                    if creds.get('username') and creds.get('password'):
                        # Don't auto-fill for security, just set remember me
                        self.remember_me.set(True)
        except:
            pass
    
    def hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def load_users(self):
        """Load users from JSON file"""
        try:
            users_path = Path(__file__).parent.parent / 'users.json'
            if users_path.exists():
                with open(users_path, 'r') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            print(f"Error loading users: {e}")
            return {}
    
    def save_users(self, users):
        """Save users to JSON file"""
        try:
            users_path = Path(__file__).parent.parent / 'users.json'
            with open(users_path, 'w') as f:
                json.dump(users, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving users: {e}")
            return False
    
    def clear_form(self):
        """Clear all form fields"""
        if self.is_login_mode.get():
            if hasattr(self, 'username_entry'):
                self.username_entry.delete(0, tk.END)
                self.username_entry.insert(0, "Username")
                self.password_entry.delete(0, tk.END)
                self.password_entry.insert(0, "Password")
                self.password_entry.config(show='')
        else:
            if hasattr(self, 'name_entry'):
                for attr in ['name', 'email', 'reg_username', 'reg_password', 'confirm', 'phone']:
                    entry = getattr(self, f'{attr}_entry', None)
                    if entry:
                        entry.delete(0, tk.END)
                        placeholder = {
                            'name': 'Full Name',
                            'email': 'Email Address',
                            'reg_username': 'Username',
                            'reg_password': 'Password',
                            'confirm': 'Confirm Password',
                            'phone': 'Phone Number (Optional)'
                        }[attr]
                        entry.insert(0, placeholder)
                        if attr in ['reg_password', 'confirm']:
                            entry.config(show='')
    
    def add_hover_effect(self, button, normal_color, hover_color):
        """Add hover effect to button"""
        def on_enter(e):
            button['background'] = hover_color
            button.config(cursor='hand2')
        
        def on_leave(e):
            button['background'] = normal_color
        
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)