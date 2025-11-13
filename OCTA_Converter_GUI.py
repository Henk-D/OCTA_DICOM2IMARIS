#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Zeiss OCTA Converter - GUI Version
Graphical user interface for converting Zeiss Cirrus OCTA DICOM files.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import sys
from pathlib import Path
import subprocess
import os

class OCTAConverterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Zeiss OCTA Converter - GUI")
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        
        # Script directory
        self.script_dir = Path(__file__).parent
        
        # Variables
        self.folder_var = tk.StringVar()
        self.auto_detect_var = tk.BooleanVar(value=False)
        self.is_converting = False
        
        self.setup_ui()
        self.load_available_folders()
        
    def setup_ui(self):
        """Setup the user interface"""
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
        # Title
        title_label = ttk.Label(
            main_frame, 
            text="Zeiss Cirrus OCTA DICOM Converter",
            font=('Arial', 14, 'bold')
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        
        # Subtitle
        subtitle_label = ttk.Label(
            main_frame,
            text="Convert OCTA DICOM files to TIFF (Imaris) and NIfTI formats",
            font=('Arial', 9)
        )
        subtitle_label.grid(row=1, column=0, columnspan=3, pady=(0, 20))
        
        # Input section
        input_frame = ttk.LabelFrame(main_frame, text="Data Selection", padding="10")
        input_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame.columnconfigure(1, weight=1)
        
        # Folder selection
        ttk.Label(input_frame, text="Data Folder:").grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.folder_combo = ttk.Combobox(
            input_frame, 
            textvariable=self.folder_var,
            state='readonly',
            width=40
        )
        self.folder_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(5, 5), pady=5)
        
        browse_btn = ttk.Button(input_frame, text="Browse...", command=self.browse_folder)
        browse_btn.grid(row=0, column=2, padx=(0, 5), pady=5)
        
        refresh_btn = ttk.Button(input_frame, text="Refresh List", command=self.load_available_folders)
        refresh_btn.grid(row=0, column=3, pady=5)
        
        # Auto-detect checkbox
        auto_check = ttk.Checkbutton(
            input_frame,
            text="Auto-detect from DataFiles folder",
            variable=self.auto_detect_var,
            command=self.toggle_auto_detect
        )
        auto_check.grid(row=1, column=1, sticky=tk.W, padx=(5, 0), pady=5)
        
        # Output settings
        output_frame = ttk.LabelFrame(main_frame, text="Output Settings", padding="10")
        output_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        formats_text = "Output formats:\n" \
                      "  • TIFF (.tif) - For Imaris visualization\n" \
                      "  • NIfTI (.nii.gz) - For medical imaging software (ITK-SNAP, 3D Slicer, etc.)\n" \
                      "  • NumPy (.npy) - For Python analysis\n" \
                      "  • Preview (.png) - MIP projections\n" \
                      "  • Metadata (.json) - Scan parameters"
        
        ttk.Label(output_frame, text=formats_text, justify=tk.LEFT).grid(row=0, column=0, sticky=tk.W)
        
        output_path_text = f"Output location: Results\\[FolderName]\\"
        ttk.Label(output_frame, text=output_path_text, font=('Arial', 9, 'italic')).grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        
        # Control buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=3, pady=(0, 10))
        
        self.convert_btn = ttk.Button(
            button_frame,
            text="Start Conversion",
            command=self.start_conversion,
            style='Accent.TButton',
            width=20
        )
        self.convert_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = ttk.Button(
            button_frame,
            text="Stop",
            command=self.stop_conversion,
            state='disabled',
            width=15
        )
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        clear_btn = ttk.Button(
            button_frame,
            text="Clear Log",
            command=self.clear_log,
            width=15
        )
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Progress bar
        self.progress = ttk.Progressbar(
            main_frame,
            mode='indeterminate',
            length=300
        )
        self.progress.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Log output
        log_frame = ttk.LabelFrame(main_frame, text="Conversion Log", padding="5")
        log_frame.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            wrap=tk.WORD,
            width=80,
            height=15,
            font=('Courier', 9)
        )
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Status bar
        self.status_label = ttk.Label(
            main_frame,
            text="Ready",
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_label.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E))
        
    def load_available_folders(self):
        """Load available data folders from DataFiles directory"""
        datafiles_dir = self.script_dir / "DataFiles"
        folders = []
        
        if datafiles_dir.exists():
            for item in datafiles_dir.iterdir():
                if item.is_dir() and not item.name.startswith('.'):
                    folders.append(item.name)
        
        # Also check parent directory for HenkOCTA_DataFiles
        parent_datafiles = self.script_dir.parent / "HenkOCTA_DataFiles"
        if parent_datafiles.exists():
            for item in parent_datafiles.iterdir():
                if item.is_dir() and not item.name.startswith('.') and item.name not in folders:
                    folders.append(item.name)
        
        if folders:
            self.folder_combo['values'] = sorted(folders)
            if not self.folder_var.get():
                self.folder_combo.current(0)
            self.log_message(f"Found {len(folders)} data folders")
        else:
            self.folder_combo['values'] = []
            self.log_message("No data folders found in DataFiles/", "warning")
    
    def browse_folder(self):
        """Browse for a custom folder"""
        folder = filedialog.askdirectory(
            title="Select OCTA Data Folder",
            initialdir=self.script_dir / "DataFiles"
        )
        if folder:
            folder_name = Path(folder).name
            self.folder_var.set(folder_name)
            self.log_message(f"Selected folder: {folder_name}")
    
    def toggle_auto_detect(self):
        """Toggle auto-detect mode"""
        if self.auto_detect_var.get():
            self.folder_combo.config(state='disabled')
            self.log_message("Auto-detect mode enabled")
        else:
            self.folder_combo.config(state='readonly')
    
    def log_message(self, message, level="info"):
        """Add message to log"""
        timestamp = ""  # Could add timestamp if needed
        
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.log_text.update()
        
        # Update status bar
        if level == "error":
            self.status_label.config(foreground="red")
        elif level == "success":
            self.status_label.config(foreground="green")
        elif level == "warning":
            self.status_label.config(foreground="orange")
        else:
            self.status_label.config(foreground="black")
        
        self.status_label.config(text=message)
    
    def clear_log(self):
        """Clear the log text"""
        self.log_text.delete(1.0, tk.END)
        self.log_message("Log cleared")
    
    def start_conversion(self):
        """Start the conversion process"""
        if self.is_converting:
            return
        
        folder_name = self.folder_var.get()
        if not folder_name and not self.auto_detect_var.get():
            messagebox.showwarning(
                "No Folder Selected",
                "Please select a data folder or enable auto-detect."
            )
            return
        
        self.is_converting = True
        self.convert_btn.config(state='disabled')
        self.stop_btn.config(state='normal')
        self.progress.start()
        
        # Run conversion in separate thread
        thread = threading.Thread(target=self.run_conversion, args=(folder_name,))
        thread.daemon = True
        thread.start()
    
    def run_conversion(self, folder_name):
        """Run the conversion script"""
        try:
            self.log_message("="*80)
            self.log_message(f"Starting conversion for: {folder_name}")
            self.log_message("="*80)
            
            # Build command
            script_path = self.script_dir / "Zeiss_OCTA_Converter.py"
            cmd = [sys.executable, str(script_path), folder_name]
            
            # Run process
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # Read output line by line
            for line in process.stdout:
                line = line.rstrip()
                if line:
                    self.root.after(0, self.log_message, line)
            
            process.wait()
            
            if process.returncode == 0:
                self.root.after(0, self.log_message, "="*80)
                self.root.after(0, self.log_message, "✓ Conversion completed successfully!", "success")
                self.root.after(0, self.log_message, f"Output files saved to: Results\\{folder_name}\\", "success")
                self.root.after(0, self.log_message, "="*80)
                
                # Ask if user wants to open output folder
                self.root.after(0, self.ask_open_folder, folder_name)
            else:
                self.root.after(0, self.log_message, "✗ Conversion failed!", "error")
        
        except Exception as e:
            self.root.after(0, self.log_message, f"ERROR: {str(e)}", "error")
        
        finally:
            self.root.after(0, self.conversion_finished)
    
    def ask_open_folder(self, folder_name):
        """Ask user if they want to open the output folder"""
        result = messagebox.askyesno(
            "Conversion Complete",
            f"Conversion completed successfully!\n\n"
            f"Output saved to: Results\\{folder_name}\\\n\n"
            f"Would you like to open the output folder?"
        )
        if result:
            output_path = self.script_dir / "Results" / folder_name
            if output_path.exists():
                os.startfile(output_path)
    
    def stop_conversion(self):
        """Stop the conversion (placeholder)"""
        # This is a simplified version - full implementation would need process management
        self.log_message("Stop requested (conversion will finish current file)", "warning")
        self.stop_btn.config(state='disabled')
    
    def conversion_finished(self):
        """Cleanup after conversion finishes"""
        self.is_converting = False
        self.convert_btn.config(state='normal')
        self.stop_btn.config(state='disabled')
        self.progress.stop()
        self.status_label.config(text="Ready")


def main():
    """Main entry point"""
    root = tk.Tk()
    
    # Try to set a nice theme
    try:
        style = ttk.Style()
        available_themes = style.theme_names()
        if 'clam' in available_themes:
            style.theme_use('clam')
        elif 'vista' in available_themes:
            style.theme_use('vista')
    except:
        pass
    
    app = OCTAConverterGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
