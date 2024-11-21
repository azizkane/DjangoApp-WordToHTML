import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import requests
from .gui_style import STYLES, COLORS

class WordToHtmlGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Word to HTML Converter")
        self.window.geometry(STYLES['main_window']['size'])
        self.window.configure(bg=STYLES['main_window']['bg'])
        
        self.file_path = None
        self.api_base_url = 'http://localhost:8000/api'
        self.setup_ui()
        
    def setup_ui(self):
        # Main container with padding
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.pack(fill='both', expand=True)
        
        # Title with modern styling
        title_label = tk.Label(
            main_frame,
            text="Word to HTML Converter",
            font=('Segoe UI', 24, 'bold'),
            bg=COLORS['background'],
            fg=COLORS['primary']
        )
        title_label.pack(pady=(0, 20))
        
        # File selection frame
        file_frame = ttk.Frame(main_frame)
        file_frame.pack(fill='x', pady=10)
        
        # Select file button
        select_btn = tk.Button(
            file_frame,
            text="Select Word File",
            bg=COLORS['primary'],
            fg='white',
            font=STYLES['button']['font'],
            relief='flat',
            cursor='hand2',
            command=self.select_file,
            padx=20,
            pady=10
        )
        select_btn.pack(side='left', padx=5)
        
        # File label
        self.file_label = tk.Label(
            file_frame,
            text="No file selected",
            bg=COLORS['background'],
            fg=COLORS['text'],
            font=STYLES['label']['font']
        )
        self.file_label.pack(side='left', padx=10)
        
        # Convert button
        convert_btn = tk.Button(
            main_frame,
            text="Convert to HTML",
            bg=COLORS['accent'],
            fg='white',
            font=STYLES['button']['font'],
            relief='flat',
            cursor='hand2',
            command=self.convert_file,
            padx=20,
            pady=10
        )
        convert_btn.pack(pady=20)
        
        # Status label
        self.status_label = tk.Label(
            main_frame,
            text="",
            bg=COLORS['background'],
            fg=COLORS['text'],
            font=STYLES['label']['font']
        )
        self.status_label.pack(pady=10)
    
    def select_file(self):
        self.file_path = filedialog.askopenfilename(
            filetypes=[("Word files", "*.docx"), ("All files", "*.*")]
        )
        if self.file_path:
            self.file_label.config(text=f"Selected: {self.file_path}")
            self.status_label.config(text="")
    
    def convert_file(self):
        if not self.file_path:
            messagebox.showerror("Error", "Please select a file first.")
            return
        
        try:
            url = f'{self.api_base_url}/convert/'
            with open(self.file_path, 'rb') as f:
                files = {'document': f}
                response = requests.post(url, files=files)
                # Set the encoding to UTF-8
                response.encoding = 'utf-8'
            
            if response.status_code == 200:
                self.status_label.config(text="Conversion successful!", fg=COLORS['success'])
                self.show_html_content(response.text)
            else:
                self.status_label.config(text="Conversion failed.", fg=COLORS['error'])
                messagebox.showerror("Error", f"Failed to convert document: {response.text}")
        except Exception as e:
            self.status_label.config(text="Error occurred during conversion.", fg=COLORS['error'])
            messagebox.showerror("Error", str(e))
    
    def show_html_content(self, html_content):
        html_window = tk.Toplevel(self.window)
        html_window.title("Converted HTML")
        html_window.geometry("800x600")
        
        # Toolbar
        toolbar = ttk.Frame(html_window)
        toolbar.pack(fill='x', padx=5, pady=5)
        
        # Save button in toolbar
        save_btn = tk.Button(
            toolbar,
            text="Save HTML",
            bg=COLORS['primary'],
            fg='white',
            font=('Segoe UI', 10),
            relief='flat',
            cursor='hand2',
            command=lambda: self.save_html(html_content),
            padx=15,
            pady=5
        )
        save_btn.pack(side='left', padx=5)
        
        # HTML content display
        text_frame = ttk.Frame(html_window)
        text_frame.pack(expand=True, fill='both', padx=10, pady=5)
        
        # Text widget with scrollbar
        text_widget = tk.Text(text_frame, wrap='word', font=('Consolas', 11))
        scrollbar = ttk.Scrollbar(text_frame, orient='vertical', command=text_widget.yview)
        
        text_widget.pack(side='left', expand=True, fill='both')
        scrollbar.pack(side='right', fill='y')
        
        text_widget.configure(yscrollcommand=scrollbar.set)
        text_widget.insert('1.0', html_content)
    
    def save_html(self, html_content):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".html",
            filetypes=[("HTML files", "*.html"), ("All files", "*.*")]
        )
        if file_path:
            # Add UTF-8 meta tag if not present
            if '<meta charset="utf-8">' not in html_content:
                html_content = '<meta charset="utf-8">\n' + html_content
                
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            messagebox.showinfo("Success", "HTML file saved successfully!")
    
    def run(self):
        self.window.mainloop()
