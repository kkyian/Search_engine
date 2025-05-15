import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

from search_web import search_web

class SearchApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Search-Enabled Chatbot GUI")
        self.geometry("600x400")

        # Query frame
        query_frame = ttk.Frame(self)
        query_frame.pack(padx=10, pady=10, fill='x')

        self.query_var = tk.StringVar()
        query_entry = ttk.Entry(query_frame, textvariable=self.query_var)
        query_entry.pack(side='left', fill='x', expand=True)
        query_entry.focus()

        search_button = ttk.Button(query_frame, text="Search", command=self.perform_search)
        search_button.pack(side='left', padx=(5, 0))

        # Results display
        results_frame = ttk.Frame(self)
        results_frame.pack(padx=10, pady=(0, 10), fill='both', expand=True)

        self.results_box = scrolledtext.ScrolledText(results_frame, wrap='word')
        self.results_box.pack(fill='both', expand=True)

    def perform_search(self):
        query = self.query_var.get().strip()
        if not query:
            messagebox.showwarning("Input error", "Please enter a search query.")
            return

        self.results_box.delete('1.0', tk.END)
        self.results_box.insert(tk.END, f"Searching for: {query}\n\n")
        try:
            hits = search_web(query)
            if not hits:
                self.results_box.insert(tk.END, "No results found.")
            else:
                for url, snippet in hits:
                    self.results_box.insert(tk.END, f"URL: {url}\n")
                    self.results_box.insert(tk.END, f"Snippet: {snippet}\n\n")
        except Exception as e:
            messagebox.showerror("Search error", str(e))

if __name__ == "__main__":
    app = SearchApp()
    app.mainloop()
