"""
The Train Captain - Railway Ticket Booking Desktop Application
Entry point for the application
Software developed by Ashish Vishwakarma
"""

import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    from gui.main_window import TrainCaptainApp
    import tkinter as tk
    from tkinter import messagebox
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Please ensure all files are in correct structure")
    input("Press Enter to exit...")
    sys.exit(1)

def main():
    """Main entry point for the application"""
    try:
        # Create the main window
        root = tk.Tk()
        
        # Set application title with developer credit
        root.title("The Train Captain - Railway Ticket Booking System | Developed by Ashish Vishwakarma")
        
        # Set window icon (if you have an icon file)
        try:
            icon_path = Path(__file__).parent / 'assets' / 'icon.ico'
            if icon_path.exists():
                root.iconbitmap(icon_path)
        except:
            pass
        
        # Make it full screen
        root.state('zoomed')
        
        # Set minimum window size
        root.minsize(1366, 768)
        
        # Set window background
        root.configure(bg='#1a1a2e')
        
        # Create application instance
        app = TrainCaptainApp(root)
        
        # Center the window on screen
        root.update_idletasks()
        
        # Display startup message
        print("=" * 60)
        print("   The Train Captain - Railway Ticket Booking System")
        print("   Developed by Ashish Vishwakarma")
        print("=" * 60)
        print("Application started successfully!")
        print("Make sure train1.jpg and train2.jpg are in the assets folder for images.")
        print("=" * 60)
        
        # Run the application
        root.mainloop()
        
    except Exception as e:
        print(f"Error starting application: {e}")
        import traceback
        traceback.print_exc()
        messagebox.showerror("Startup Error", 
                           f"Failed to start application:\n{str(e)}\n\nPlease check the console for details.")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()