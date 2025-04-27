import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import threading
from zip_manager import ZipManager

class ZipToolGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ZIP Tools Pro")
        self.zip_path = None
        self.password = None
        self.manager = None

        self.select_button = tk.Button(root, text="Select ZIP", command=self.select_zip)
        self.select_button.pack(pady=5)

        self.password_button = tk.Button(root, text="Set Password", command=self.set_password)
        self.password_button.pack(pady=5)

        self.list_button = tk.Button(root, text="List Files", command=self.list_files)
        self.list_button.pack(pady=5)

        self.extract_button = tk.Button(root, text="Extract All", command=self.extract_all)
        self.extract_button.pack(pady=5)

        self.add_button = tk.Button(root, text="Add File", command=self.add_file)
        self.add_button.pack(pady=5)

        self.delete_button = tk.Button(root, text="Delete File", command=self.delete_file)
        self.delete_button.pack(pady=5)

    def run_in_thread(self, func):
        threading.Thread(target=func).start()

    def select_zip(self):
        self.zip_path = filedialog.askopenfilename(filetypes=[("ZIP files", "*.zip")])
        if self.zip_path:
            self.manager = ZipManager(self.zip_path, password=self.password)
            messagebox.showinfo("Selected", f"Selected: {self.zip_path}")

    def set_password(self):
        password = simpledialog.askstring("Password", "Enter Password:", show='*')
        if password:
            self.password = password
            if self.zip_path:
                self.manager = ZipManager(self.zip_path, password=self.password)
            messagebox.showinfo("Password", "Password set.")

    def list_files(self):
        if not self.manager:
            messagebox.showwarning("Warning", "No ZIP selected")
            return
        self.run_in_thread(self._list_files)

    def _list_files(self):
        try:
            files = self.manager.list_files()
            messagebox.showinfo("Files", "\n".join(files))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def extract_all(self):
        if not self.manager:
            messagebox.showwarning("Warning", "No ZIP selected")
            return
        output_dir = filedialog.askdirectory()
        self.run_in_thread(lambda: self._extract_all(output_dir))

    def _extract_all(self, output_dir):
        try:
            self.manager.extract_all(output_dir)
            messagebox.showinfo("Done", f"Extracted to {output_dir}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def add_file(self):
        if not self.manager:
            messagebox.showwarning("Warning", "No ZIP selected")
            return
        file_path = filedialog.askopenfilename()
        self.run_in_thread(lambda: self._add_file(file_path))

    def _add_file(self, file_path):
        try:
            self.manager.add_file(file_path)
            messagebox.showinfo("Done", f"Added {file_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_file(self):
        if not self.manager:
            messagebox.showwarning("Warning", "No ZIP selected")
            return
        filename = simpledialog.askstring("Delete File", "Enter filename to delete")
        self.run_in_thread(lambda: self._delete_file(filename))

    def _delete_file(self, filename):
        try:
            self.manager.delete_file(filename)
            messagebox.showinfo("Done", f"Deleted {filename}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

def start_gui():
    root = tk.Tk()
    app = ZipToolGUI(root)
    root.mainloop()

if __name__ == "__main__":
    start_gui()
