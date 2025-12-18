import tkinter as tk
from tkinter import messagebox, ttk
import time

BOARD_SIZE = 8
CELL_SIZE = 60
BOARD_MARGIN = 50

class KnightsTour:
    def __init__(self):
        self.n = BOARD_SIZE
        self.board = [[0 for _ in range(self.n)] for _ in range(self.n)]
        self.moves = [(2, 1), (1, 2), (-1, 2), (-2, 1),
                      (-2, -1), (-1, -2), (1, -2), (2, -1)]
        self.path = []
        
    def is_valid(self, x, y):
        """Cek apakah posisi valid dan belum dikunjungi"""
        return 0 <= x < self.n and 0 <= y < self.n and self.board[x][y] == 0
    
    def get_accessibility(self, x, y):
        """Hitung jumlah kotak yang bisa dikunjungi dari posisi (x, y)"""
        count = 0
        for dx, dy in self.moves:
            nx, ny = x + dx, y + dy
            if self.is_valid(nx, ny):
                count += 1
        return count
    
    def solve_warnsdorff(self, start_x, start_y, closed=False):
        """Selesaikan Knight's Tour menggunakan Warnsdorff's Algorithm"""
        self.board = [[0 for _ in range(self.n)] for _ in range(self.n)]
        self.path = [(start_x, start_y)]
        self.board[start_x][start_y] = 1
        
        current_x, current_y = start_x, start_y
        move_count = 2
        
        while move_count <= self.n * self.n:
            next_moves = []
            for dx, dy in self.moves:
                nx, ny = current_x + dx, current_y + dy
                if self.is_valid(nx, ny):
                    accessibility = self.get_accessibility(nx, ny)
                    next_moves.append((accessibility, nx, ny))
            
            if not next_moves:
                break
            
            next_moves.sort()
            _, current_x, current_y = next_moves[0]
            
            self.board[current_x][current_y] = move_count
            self.path.append((current_x, current_y))
            move_count += 1
        
        success = move_count > self.n * self.n
        
        is_closed = False
        if success and closed:
            last_x, last_y = self.path[-1]
            for dx, dy in self.moves:
                if last_x + dx == start_x and last_y + dy == start_y:
                    is_closed = True
                    break
        
        return success, is_closed

class KnightTourGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("The Knight's Tour Visualizer")
        self.root.geometry("800x750")
        self.root.resizable(False, False)
        
        self.knight = KnightsTour()
        self.animation_running = False
        self.animation_speed = 200
        
        self.setup_ui()
        
    def setup_ui(self):        
        control_frame = tk.Frame(self.root, bg="#ecf0f1", pady=15)
        control_frame.pack(fill="x")
        
        pos_frame = tk.Frame(control_frame, bg="#ecf0f1")
        pos_frame.pack(pady=5)
        
        tk.Label(pos_frame, text="Posisi Awal Kuda:", font=("Arial", 11, "bold"), 
                bg="#ecf0f1").pack(side="left", padx=5)
        
        tk.Label(pos_frame, text="Baris:", font=("Arial", 10), 
                bg="#ecf0f1").pack(side="left", padx=5)
        self.row_entry = tk.Spinbox(pos_frame, from_=0, to=7, width=5, 
                                    font=("Arial", 10))
        self.row_entry.delete(0, "end")
        self.row_entry.insert(0, "0")
        self.row_entry.pack(side="left", padx=5)
        
        tk.Label(pos_frame, text="Kolom:", font=("Arial", 10), 
                bg="#ecf0f1").pack(side="left", padx=5)
        self.col_entry = tk.Spinbox(pos_frame, from_=0, to=7, width=5, 
                                    font=("Arial", 10))
        self.col_entry.delete(0, "end")
        self.col_entry.insert(0, "0")
        self.col_entry.pack(side="left", padx=5)
        
        mode_frame = tk.Frame(control_frame, bg="#ecf0f1")
        mode_frame.pack(pady=10)
        
        tk.Label(mode_frame, text="Mode Tour:", font=("Arial", 11, "bold"), 
                bg="#ecf0f1").pack(side="left", padx=10)
        
        self.mode_var = tk.StringVar(value="open")
        tk.Radiobutton(mode_frame, text="Open Tour", variable=self.mode_var, 
                      value="open", font=("Arial", 10), bg="#ecf0f1").pack(side="left", padx=10)
        tk.Radiobutton(mode_frame, text="Closed Tour", variable=self.mode_var, 
                      value="closed", font=("Arial", 10), bg="#ecf0f1").pack(side="left", padx=10)
        
        button_frame = tk.Frame(control_frame, bg="#ecf0f1")
        button_frame.pack(pady=5)
        
        tk.Button(button_frame, text="Solve Tour", command=self.solve_tour,
                 fg="black", font=("Arial", 11, "bold"), 
                 width=15, height=1, relief="raised", bd=2).pack(side="left", padx=5)
        
        tk.Button(button_frame, text="Animate", command=self.animate_tour,
                 fg="black", font=("Arial", 11, "bold"), 
                 width=15, height=1, relief="raised", bd=2).pack(side="left", padx=5)
        
        tk.Button(button_frame, text="Reset", command=self.reset_board,
                 fg="black", font=("Arial", 11, "bold"), 
                 width=15, height=1, relief="raised", bd=2).pack(side="left", padx=5)
        
        canvas_frame = tk.Frame(self.root, bg="white")
        canvas_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        canvas_width = BOARD_SIZE * CELL_SIZE + 2 * BOARD_MARGIN
        canvas_height = BOARD_SIZE * CELL_SIZE + 2 * BOARD_MARGIN
        
        self.canvas = tk.Canvas(canvas_frame, width=canvas_width, 
                               height=canvas_height, bg="white")
        self.canvas.pack()
        
        # Info panel
        info_frame = tk.Frame(self.root, bg="#ecf0f1", height=60)
        info_frame.pack(fill="x")
        info_frame.pack_propagate(False)
        
        self.info_label = tk.Label(info_frame, text="Klik 'Solve Tour' untuk memulai", 
                                   font=("Arial", 11), bg="#ecf0f1", fg="#2c3e50")
        self.info_label.pack(pady=5)
        
        self.status_label = tk.Label(info_frame, text="Status: Ready", 
                                     font=("Arial", 10, "bold"), bg="#ecf0f1", fg="#16a085")
        self.status_label.pack(pady=2)
        
        self.draw_board()
        
    def draw_board(self, show_numbers=False, animate_step=-1):
        """Gambar papan catur"""
        self.canvas.delete("all")
        
        for i in range(BOARD_SIZE):
            # Row numbers (left side)
            self.canvas.create_text(BOARD_MARGIN - 20, 
                                   BOARD_MARGIN + i * CELL_SIZE + CELL_SIZE // 2,
                                   text=str(i), font=("Arial", 10, "bold"))
            self.canvas.create_text(BOARD_MARGIN + i * CELL_SIZE + CELL_SIZE // 2,
                                   BOARD_MARGIN - 20,
                                   text=str(i), font=("Arial", 10, "bold"))
        
        # Draw chessboard squares
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                x1 = BOARD_MARGIN + col * CELL_SIZE
                y1 = BOARD_MARGIN + row * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE
                
                color = "#f0d9b5" if (row + col) % 2 == 0 else "#b58863"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, 
                                            outline="#8b6f47", width=2)
                
                # Show numbers if solved
                if show_numbers and self.knight.board[row][col] > 0:
                    num = self.knight.board[row][col]
                    
                    # Highlight current step during animation
                    if animate_step > 0 and num == animate_step:
                        self.canvas.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5,
                                               fill="#e74c3c", outline="#c0392b", width=3)
                    
                    text_color = "#2c3e50" if num != 1 else "#27ae60"
                    if num == len(self.knight.path):
                        text_color = "#e74c3c"
                    
                    self.canvas.create_text(x1 + CELL_SIZE // 2, 
                                          y1 + CELL_SIZE // 2,
                                          text=str(num), 
                                          font=("Arial", 14, "bold"),
                                          fill=text_color)
        
        if show_numbers and len(self.knight.path) > 1:
            max_step = animate_step if animate_step > 0 else len(self.knight.path)
            
            for i in range(min(max_step - 1, len(self.knight.path) - 1)):
                row1, col1 = self.knight.path[i]
                row2, col2 = self.knight.path[i + 1]
                
                x1 = BOARD_MARGIN + col1 * CELL_SIZE + CELL_SIZE // 2
                y1 = BOARD_MARGIN + row1 * CELL_SIZE + CELL_SIZE // 2
                x2 = BOARD_MARGIN + col2 * CELL_SIZE + CELL_SIZE // 2
                y2 = BOARD_MARGIN + row2 * CELL_SIZE + CELL_SIZE // 2
                
                self.canvas.create_line(x1, y1, x2, y2, fill="#3498db", 
                                       width=3, arrow=tk.LAST, arrowshape=(10, 12, 5))
        
        if show_numbers and self.knight.path:
            start_row, start_col = self.knight.path[0]
            x = BOARD_MARGIN + start_col * CELL_SIZE + CELL_SIZE // 2
            y = BOARD_MARGIN + start_row * CELL_SIZE + CELL_SIZE // 2
            self.canvas.create_text(x, y - CELL_SIZE // 2 - 15, 
                                   text="START", font=("Arial", 9, "bold"), 
                                   fill="#27ae60")
            
            if animate_step < 0 or animate_step >= len(self.knight.path):
                end_row, end_col = self.knight.path[-1]
                x = BOARD_MARGIN + end_col * CELL_SIZE + CELL_SIZE // 2
                y = BOARD_MARGIN + end_row * CELL_SIZE + CELL_SIZE // 2
                self.canvas.create_text(x, y + CELL_SIZE // 2 + 15, 
                                       text="END", font=("Arial", 9, "bold"), 
                                       fill="#e74c3c")
    
    def solve_tour(self):
        """Solve the knight's tour"""
        try:
            start_row = int(self.row_entry.get())
            start_col = int(self.col_entry.get())
            
            if not (0 <= start_row < 8 and 0 <= start_col < 8):
                messagebox.showerror("Error", "Posisi harus antara 0-7!")
                return
            
            self.status_label.config(text="Status: Processing...", fg="#f39c12")
            self.root.update()
            
            closed = self.mode_var.get() == "closed"
            
            if closed:
                max_attempts = 100
                found = False
                for attempt in range(max_attempts):
                    success, is_closed = self.knight.solve_warnsdorff(start_row, start_col, True)
                    if success and is_closed:
                        found = True
                        break
                
                if not found:
                    messagebox.showwarning("Warning", 
                        "Closed tour tidak ditemukan setelah 100 percobaan.\n"
                        "Menampilkan Open Tour sebagai gantinya.")
                    self.knight.solve_warnsdorff(start_row, start_col, False)
                    is_closed = False
            else:
                success, is_closed = self.knight.solve_warnsdorff(start_row, start_col, False)
            
            self.draw_board(show_numbers=True)
            
            visited = len(self.knight.path)
            tour_type = "CLOSED TOUR" if (closed and is_closed) else "OPEN TOUR"
            
            self.info_label.config(
                text=f"Start: ({start_row}, {start_col}) | "
                     f"Visited: {visited}/64 | "
                     f"End: {self.knight.path[-1]} | "
                     f"Type: {tour_type}"
            )
            
            if visited == 64:
                self.status_label.config(text="Status: SUCCESS", fg="#27ae60")
            else:
                self.status_label.config(text="Status: Incomplete", fg="#e74c3c")
                
        except ValueError:
            messagebox.showerror("Error", "Input tidak valid!")
    
    def animate_tour(self):
        """Animate the tour step by step"""
        if not self.knight.path:
            messagebox.showwarning("Warning", "Solve tour terlebih dahulu!")
            return
        
        if self.animation_running:
            return
        
        self.animation_running = True
        self.animate_step(1)
    
    def animate_step(self, step):
        """Animate one step"""
        if step > len(self.knight.path):
            self.animation_running = False
            self.draw_board(show_numbers=True)
            return
        
        self.draw_board(show_numbers=True, animate_step=step)
        self.status_label.config(text=f"Status: Animating... Step {step}/{len(self.knight.path)}", 
                                fg="#3498db")
        
        self.root.after(self.animation_speed, lambda: self.animate_step(step + 1))
    
    def reset_board(self):
        """Reset the board"""
        self.knight = KnightsTour()
        self.animation_running = False
        self.draw_board()
        self.info_label.config(text="Klik 'Solve Tour' untuk memulai")
        self.status_label.config(text="Status: Ready", fg="#16a085")

def main():
    root = tk.Tk()
    app = KnightTourGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()