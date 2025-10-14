import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import whisper
import os
from pathlib import Path
import time
import torch
from datetime import datetime
import shutil

class SpeechToTextApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Speech to Text - Whisper")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        # Initialize Whisper model (will be loaded when needed)
        self.model = None
        self.model_loaded = False
        self.current_model_name = "base"  # Default model
        
        # Device detection
        self.device = self.detect_device()
        
        # Output folder setup
        self.output_folder = self.setup_output_folder()
        
        # Time tracking
        self.start_time = None
        self.end_time = None
        
        # Create GUI elements
        self.create_widgets()
        
    def detect_device(self):
        """Detect available device (GPU or CPU)"""
        if torch.cuda.is_available():
            device = "cuda"
            gpu_name = torch.cuda.get_device_name(0)
            print(f"GPU detected: {gpu_name}")
        elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
            device = "mps"  # Apple Silicon GPU
            print("Apple Silicon GPU detected")
        else:
            device = "cpu"
            print("Using CPU (no GPU detected)")
        return device
        
    def setup_output_folder(self):
        """Setup default output folder for transcriptions"""
        # Create output folder in the same directory as the script
        script_dir = Path(__file__).parent
        output_folder = script_dir / "transcriptions"
        output_folder.mkdir(exist_ok=True)
        return output_folder
        
    def get_device_status_text(self):
        """Get device status text for display"""
        if self.device == "cuda":
            gpu_name = torch.cuda.get_device_name(0)
            return f"🚀 GPU Acceleration: {gpu_name} (CUDA)"
        elif self.device == "mps":
            return "🚀 GPU Acceleration: Apple Silicon (MPS)"
        else:
            return "💻 Using CPU (GPU not available)"
        
    def create_widgets(self):
        # Title
        title_label = tk.Label(
            self.root, 
            text="Speech to Text Converter", 
            font=("Arial", 20, "bold"),
            bg='#f0f0f0',
            fg='#333333'
        )
        title_label.pack(pady=20)
        
        # File selection frame
        file_frame = tk.Frame(self.root, bg='#f0f0f0')
        file_frame.pack(pady=20, padx=20, fill='x')
        
        # File selection button
        self.select_button = tk.Button(
            file_frame,
            text="Select Audio/Video File",
            command=self.select_file,
            font=("Arial", 12),
            bg='#4CAF50',
            fg='white',
            padx=20,
            pady=10,
            relief='raised',
            bd=2
        )
        self.select_button.pack(side='left', padx=10)
        
        # Selected file label
        self.file_label = tk.Label(
            file_frame,
            text="No file selected",
            font=("Arial", 10),
            bg='#f0f0f0',
            fg='#666666'
        )
        self.file_label.pack(side='left', padx=20)
        
        # Model selection frame
        model_frame = tk.Frame(self.root, bg='#f0f0f0')
        model_frame.pack(pady=10, padx=20, fill='x')
        
        # Model selection label
        model_label = tk.Label(
            model_frame,
            text="Whisper Model:",
            font=("Arial", 11, "bold"),
            bg='#f0f0f0',
            fg='#333333'
        )
        model_label.pack(side='left', padx=5)
        
        # Model dropdown
        self.model_var = tk.StringVar(value="base")
        self.model_dropdown = ttk.Combobox(
            model_frame,
            textvariable=self.model_var,
            values=["tiny", "base", "small", "medium", "large"],
            state="readonly",
            width=15,
            font=("Arial", 10)
        )
        self.model_dropdown.pack(side='left', padx=10)
        self.model_dropdown.bind("<<ComboboxSelected>>", self.on_model_change)
        
        # Model info label
        self.model_info_label = tk.Label(
            model_frame,
            text="(Good balance of speed and accuracy)",
            font=("Arial", 9),
            bg='#f0f0f0',
            fg='#666666'
        )
        self.model_info_label.pack(side='left', padx=10)
        
        # Device status frame
        device_frame = tk.Frame(self.root, bg='#f0f0f0')
        device_frame.pack(pady=5, padx=20, fill='x')
        
        # Device status label
        device_text = self.get_device_status_text()
        self.device_label = tk.Label(
            device_frame,
            text=device_text,
            font=("Arial", 9),
            bg='#f0f0f0',
            fg='#0066CC' if self.device != "cpu" else '#666666'
        )
        self.device_label.pack()
        
        # Progress frame
        progress_frame = tk.Frame(self.root, bg='#f0f0f0')
        progress_frame.pack(pady=10, padx=20, fill='x')
        
        # Progress bar
        self.progress_var = tk.StringVar(value="Ready")
        self.progress_label = tk.Label(
            progress_frame,
            textvariable=self.progress_var,
            font=("Arial", 10),
            bg='#f0f0f0',
            fg='#333333'
        )
        self.progress_label.pack()
        
        # Time counter
        self.time_var = tk.StringVar(value="")
        self.time_label = tk.Label(
            progress_frame,
            textvariable=self.time_var,
            font=("Arial", 9),
            bg='#f0f0f0',
            fg='#666666'
        )
        self.time_label.pack()
        
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            mode='indeterminate',
            length=400
        )
        self.progress_bar.pack(pady=5)
        
        # Transcribe button
        self.transcribe_button = tk.Button(
            self.root,
            text="Start Transcription",
            command=self.start_transcription,
            font=("Arial", 12),
            bg='#2196F3',
            fg='white',
            padx=20,
            pady=10,
            relief='raised',
            bd=2,
            state='disabled'
        )
        self.transcribe_button.pack(pady=10)
        
        # Text output frame
        text_frame = tk.Frame(self.root, bg='#f0f0f0')
        text_frame.pack(pady=20, padx=20, fill='both', expand=True)
        
        # Output label
        output_label = tk.Label(
            text_frame,
            text="Transcribed Text:",
            font=("Arial", 12, "bold"),
            bg='#f0f0f0',
            fg='#333333'
        )
        output_label.pack(anchor='w')
        
        # Text output area
        self.text_output = scrolledtext.ScrolledText(
            text_frame,
            wrap=tk.WORD,
            font=("Arial", 11),
            bg='white',
            fg='#333333',
            relief='sunken',
            bd=2,
            padx=10,
            pady=10
        )
        self.text_output.pack(fill='both', expand=True, pady=5)
        
        # Button frame for copy and save
        button_frame = tk.Frame(text_frame, bg='#f0f0f0')
        button_frame.pack(pady=5)
        
        # Copy button
        self.copy_button = tk.Button(
            button_frame,
            text="📋 Copy to Clipboard",
            command=self.copy_text,
            font=("Arial", 10),
            bg='#2196F3',
            fg='white',
            padx=15,
            pady=5,
            relief='raised',
            bd=2,
            state='disabled'
        )
        self.copy_button.pack(side='left', padx=5)
        
        # Save button
        self.save_button = tk.Button(
            button_frame,
            text="💾 Save to Custom Location",
            command=self.save_text_custom,
            font=("Arial", 10),
            bg='#FF9800',
            fg='white',
            padx=15,
            pady=5,
            relief='raised',
            bd=2,
            state='disabled'
        )
        self.save_button.pack(side='left', padx=5)
        
    def select_file(self):
        """Open file dialog to select audio or video file"""
        file_types = [
            ("Audio & Video files", "*.mp3 *.wav *.m4a *.flac *.aac *.ogg *.wma *.mp4 *.avi *.mov *.mkv *.webm *.m4v *.3gp *.flv"),
            ("Audio files", "*.mp3 *.wav *.m4a *.flac *.aac *.ogg *.wma"),
            ("Video files", "*.mp4 *.avi *.mov *.mkv *.webm *.m4v *.3gp *.flv"),
            ("MP3 files", "*.mp3"),
            ("WAV files", "*.wav"),
            ("MP4 files", "*.mp4"),
            ("AVI files", "*.avi"),
            ("All files", "*.*")
        ]
        
        file_path = filedialog.askopenfilename(
            title="Select Audio or Video File",
            filetypes=file_types
        )
        
        if file_path:
            self.selected_file = file_path
            filename = os.path.basename(file_path)
            self.file_label.config(text=f"Selected: {filename}", fg='#333333')
            self.transcribe_button.config(state='normal')
            
    def on_model_change(self, event=None):
        """Handle model selection change"""
        selected_model = self.model_var.get()
        self.current_model_name = selected_model
        
        # Update model info text
        model_info = {
            "tiny": "(Fastest, least accurate - ~39MB)",
            "base": "(Good balance of speed and accuracy - ~142MB)",
            "small": "(Better accuracy, slower - ~461MB)",
            "medium": "(High accuracy, slower - ~1.5GB)",
            "large": "(Best accuracy, slowest - ~2.9GB)"
        }
        
        self.model_info_label.config(text=model_info[selected_model])
        
        # Reset model loaded flag if model changed
        if self.model_loaded and selected_model != self.current_model_name:
            self.model_loaded = False
            self.model = None
            
    def load_model(self):
        """Load Whisper model in a separate thread"""
        try:
            model_name = self.current_model_name
            device_text = "GPU" if self.device != "cpu" else "CPU"
            self.progress_var.set(f"Loading Whisper {model_name} model on {device_text}...")
            
            # Load model with device specification
            self.model = whisper.load_model(model_name, device=self.device)
            self.model_loaded = True
            
            device_status = f" on {device_text}" if self.device != "cpu" else ""
            self.progress_var.set(f"{model_name.title()} model loaded successfully{device_status}!")
            return True
        except Exception as e:
            error_msg = f"Failed to load Whisper {self.current_model_name} model: {str(e)}"
            messagebox.showerror("Error", error_msg)
            self.progress_var.set("Error loading model")
            return False
            
    def start_transcription(self):
        """Start transcription process in a separate thread"""
        if not hasattr(self, 'selected_file'):
            messagebox.showwarning("Warning", "Please select an audio or video file first!")
            return
            
        # Disable buttons during transcription
        self.transcribe_button.config(state='disabled')
        self.select_button.config(state='disabled')
        self.save_button.config(state='disabled')
        
        # Start timing
        self.start_time = time.time()
        self.time_var.set("Starting transcription...")
        
        # Start progress bar
        self.progress_bar.start()
        
        # Start transcription in separate thread
        transcription_thread = threading.Thread(target=self.transcribe_audio)
        transcription_thread.daemon = True
        transcription_thread.start()
        
    def transcribe_audio(self):
        """Transcribe the selected audio file"""
        try:
            # Load model if not already loaded
            if not self.model_loaded:
                if not self.load_model():
                    self.reset_ui()
                    return
                    
            device_text = "GPU" if self.device != "cpu" else "CPU"
            self.progress_var.set(f"Transcribing audio/video with {self.current_model_name} model on {device_text}... This may take a while for long files.")
            
            # Perform transcription
            result = self.model.transcribe(self.selected_file)
            
            # Update UI with results
            self.root.after(0, self.transcription_complete, result["text"])
            
        except Exception as e:
            error_msg = f"Transcription failed: {str(e)}"
            self.root.after(0, self.transcription_error, error_msg)
            
    def transcription_complete(self, text):
        """Handle successful transcription completion"""
        # Calculate processing time
        self.end_time = time.time()
        processing_time = self.end_time - self.start_time
        
        # Format time display
        if processing_time < 60:
            time_str = f"Processing completed in {processing_time:.1f} seconds"
        elif processing_time < 3600:
            minutes = int(processing_time // 60)
            seconds = processing_time % 60
            time_str = f"Processing completed in {minutes}m {seconds:.1f}s"
        else:
            hours = int(processing_time // 3600)
            minutes = int((processing_time % 3600) // 60)
            seconds = processing_time % 60
            time_str = f"Processing completed in {hours}h {minutes}m {seconds:.1f}s"
        
        # Stop progress bar
        self.progress_bar.stop()
        
        # Update UI
        self.text_output.delete(1.0, tk.END)
        self.text_output.insert(1.0, text)
        self.progress_var.set("Transcription completed successfully!")
        self.time_var.set(time_str)
        
        # Re-enable buttons
        self.transcribe_button.config(state='normal')
        self.select_button.config(state='normal')
        self.save_button.config(state='normal')
        self.copy_button.config(state='normal')
        
        # Automatically save to default folder
        self.auto_save_text(text)
        
        # Show completion message
        messagebox.showinfo("Success", f"Transcription completed successfully!\n\n{time_str}\n\nText automatically saved to:\n{self.output_folder}")
        
    def transcription_error(self, error_msg):
        """Handle transcription error"""
        # Stop progress bar
        self.progress_bar.stop()
        
        # Update UI
        self.progress_var.set("Transcription failed")
        
        # Re-enable buttons
        self.transcribe_button.config(state='normal')
        self.select_button.config(state='normal')
        
        # Show error message
        messagebox.showerror("Error", error_msg)
        
    def reset_ui(self):
        """Reset UI to initial state"""
        self.progress_bar.stop()
        self.progress_var.set("Ready")
        self.time_var.set("")
        self.transcribe_button.config(state='normal')
        self.select_button.config(state='normal')
        self.save_button.config(state='disabled')
        self.copy_button.config(state='disabled')
        
    def auto_save_text(self, text_content):
        """Automatically save transcribed text to default folder"""
        try:
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"transcription_{timestamp}.txt"
            file_path = self.output_folder / filename
            
            # Save the text
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(text_content)
            
            print(f"Text automatically saved to: {file_path}")
            return file_path
        except Exception as e:
            print(f"Failed to auto-save text: {str(e)}")
            return None
    
    def copy_text(self):
        """Copy transcribed text to clipboard"""
        text_content = self.text_output.get(1.0, tk.END).strip()
        
        if not text_content:
            messagebox.showwarning("Warning", "No text to copy!")
            return
            
        try:
            self.root.clipboard_clear()
            self.root.clipboard_append(text_content)
            messagebox.showinfo("Success", "Text copied to clipboard!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to copy text: {str(e)}")
    
    def save_text_custom(self):
        """Save transcribed text to a custom location"""
        text_content = self.text_output.get(1.0, tk.END).strip()
        
        if not text_content:
            messagebox.showwarning("Warning", "No text to save!")
            return
            
        # Get save location
        file_path = filedialog.asksaveasfilename(
            title="Save Transcribed Text",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(text_content)
                messagebox.showinfo("Success", f"Text saved to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {str(e)}")

def main():
    root = tk.Tk()
    app = SpeechToTextApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
