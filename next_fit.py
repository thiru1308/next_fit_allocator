import tkinter as tk
from tkinter import messagebox

class MemoryBlock:
    def __init__(self, size):
        self.size = size
        self.remaining = size
        self.allocated = False
        self.process_names = [] 

class NextFitAllocator:
    def __init__(self):
        self.initial_memory_blocks = [300, 200, 100, 250, 150, 50]
        self.reset_memory()

    def reset_memory(self):
        self.memory_blocks = [MemoryBlock(size) for size in self.initial_memory_blocks]
        self.last_allocated_index = 0

    def allocate(self, process_name, process_size):
        start_index = self.last_allocated_index
        
        while True:
            block = self.memory_blocks[self.last_allocated_index]
            if block.remaining >= process_size:
                block.remaining -= process_size
                block.allocated = True
                block.process_names.append(process_name)
                allocation_info = f"Allocated {process_size} KB to {process_name} in Block {self.last_allocated_index + 1}"
                self.last_allocated_index = (self.last_allocated_index + 1) % len(self.memory_blocks)
                return allocation_info
            
            self.last_allocated_index = (self.last_allocated_index + 1) % len(self.memory_blocks)
            if self.last_allocated_index == start_index:
                break

        return "No suitable block found for allocation."

    def get_memory_state(self):
        state = []
        for i, block in enumerate(self.memory_blocks):
            if block.allocated:
                processes = block.process_names
                display_processes = ", ".join(processes[:3])
                if len(processes) > 3:
                    display_processes += f", and {len(processes) - 3} more"
                state.append(f"Block {i + 1}: {block.size} KB (Allocated to {display_processes}, Remaining: {block.remaining} KB)")
            else:
                state.append(f"Block {i + 1}: {block.size} KB (Free)")
        return state

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Next Fit Memory Allocation")
        self.geometry("600x400")
        
        self.allocator = NextFitAllocator()
        
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Process Name:").pack(pady=10)
        self.process_name_entry = tk.Entry(self)
        self.process_name_entry.pack(pady=5)

        tk.Label(self, text="Process Size (KB):").pack(pady=10)
        self.process_size_entry = tk.Entry(self)
        self.process_size_entry.pack(pady=5)

        tk.Button(self, text="Allocate Memory", bg="lightGreen", fg="black", command=self.allocate_memory).pack(pady=10)
        tk.Button(self, text="Reset", bg="red", fg="white", command=self.reset_memory).pack(pady=10)
        
        frame = tk.Frame(self)
        frame.pack(pady=20)

        self.scrollbar = tk.Scrollbar(frame, orient=tk.HORIZONTAL)
        self.scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        self.memory_listbox = tk.Listbox(frame, width=80, height=10, xscrollcommand=self.scrollbar.set)
        self.memory_listbox.pack(side=tk.LEFT)

        self.scrollbar.config(command=self.memory_listbox.xview)

        self.memory_listbox.bind("<Double-1>", self.show_full_processes)

        self.update_memory_display()

    def allocate_memory(self):
        process_name = self.process_name_entry.get()
        try:
            process_size = int(self.process_size_entry.get())
            if process_size <= 0:
                raise ValueError("Size must be positive.")
            result = self.allocator.allocate(process_name, process_size)
            messagebox.showinfo("Allocation Result", result)
            self.update_memory_display()
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid process size.")

    def reset_memory(self):
        self.allocator.reset_memory()
        self.process_name_entry.delete(0, tk.END)
        self.process_size_entry.delete(0, tk.END)
        self.update_memory_display()
        messagebox.showinfo("Reset", "Memory has been reset to initial state.")

    def update_memory_display(self):
        self.memory_listbox.delete(0, tk.END)
        memory_state = self.allocator.get_memory_state()
        for state in memory_state:
            self.memory_listbox.insert(tk.END, state)

    def show_full_processes(self, event):
        selection = self.memory_listbox.curselection()
        if selection:
            index = selection[0]
            block = self.allocator.memory_blocks[index]
            processes = block.process_names
            full_processes = "\n".join(processes)
            messagebox.showinfo(f"Processes in Block {index + 1}", full_processes)

if __name__ == "__main__":
    app = Application()
    app.mainloop()