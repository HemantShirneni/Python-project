import tkinter as tk
from tkinter import messagebox
import time
import random
import sqlite3

class TypingSpeedTestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Test")
        self.root.configure(bg='Salmon')  # Set background color

        self.name = ""  # Initialize name variable

        self.easy_sentences = [
            "The quick brown fox jumps over the lazy dog.",
            "A journey of a thousand miles begins with a single step.",
            "All that glitters is not gold.",
            "Actions speak louder than words.",
            "Haste makes waste.",
        ]

        self.hard_sentences = [
            "In the beginning God created the heavens and the earth.",
            "To be or not to be, that is the question.",
            "All the world's a stage, and all the men and women merely players.",
            "To thine own self be true.",
            "The only limit to our realization of tomorrow will be our doubts of today.",
        ]

        self.history = []  # Store typing test results

        self.headline_label = tk.Label(root, text="Test Your Typing Skills", font=("Algerian", 30, "bold"), fg="black", bg='Salmon')
        self.headline_label.pack(pady=20)

        # Add label and entry for user's name
        self.name_label = tk.Label(root, text="Enter your name:", font=("Arial", 18), fg="black", bg='Salmon')
        self.name_label.pack(pady=10)
        self.name_entry = tk.Entry(root, font=("Arial", 18), bd=3, relief=tk.GROOVE, textvariable=self.name)
        self.name_entry.pack(pady=10)

        self.label_sentence = tk.Label(root, text="", font=("Arial", 22), wraplength=500, justify='center')
        self.label_sentence.pack(pady=20)

        self.user_input = tk.Entry(root, font=("Arial", 22), bd=3, relief=tk.GROOVE)
        self.user_input.pack(pady=10)

        self.timer_label = tk.Label(root, text="Time: 0:00", font=("Arial", 18), fg="black", bg='Salmon')
        self.timer_label.pack()

        self.level_var = tk.StringVar()
        self.level_var.set("easy")  # Default level is set to easy

        self.level_radio_frame = tk.Frame(root, bg='Salmon')
        self.easy_radio = tk.Radiobutton(self.level_radio_frame, text="Easy", variable=self.level_var, value="easy", font=("Arial", 16), bg='Salmon')
        self.easy_radio.pack(side=tk.LEFT, padx=20)
        self.hard_radio = tk.Radiobutton(self.level_radio_frame, text="Hard", variable=self.level_var, value="hard", font=("Arial", 16), bg='Salmon')
        self.hard_radio.pack(side=tk.LEFT)
        self.level_radio_frame.pack(pady=10)

        self.start_button = tk.Button(root, text="Start Typing Test", command=self.start_typing_test, bg="black", fg="red", font=("Arial", 16), padx=20, pady=10)
        self.start_button.pack(pady=10)

        self.submit_button = tk.Button(root, text="Submit", command=self.submit_typing_test, state=tk.DISABLED, bg="black", fg="red", font=("Arial", 16), padx=20, pady=10)
        self.submit_button.pack(pady=30)

        self.show_leaderboard_button = tk.Button(root, text="Show Leaderboard", command=self.show_leaderboard, bg="black", fg="red", font=("Arial", 16), padx=20, pady=10)
        self.show_leaderboard_button.pack(pady=10)

        self.show_history_button = tk.Button(root, text="Show History", command=self.show_history, bg="black", fg="red", font=("Arial", 16), padx=20, pady=10)
        self.show_history_button.pack(pady=10)

        

        self.start_time = 0
        self.timer_running = False

        # Initialize database connection and create table if not exists
        self.conn = sqlite3.connect("typing_test.db")
        self.cur = self.conn.cursor()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS leaderboard
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                             name TEXT,
                             speed REAL,
                             accuracy REAL)''')

    def start_typing_test(self):
        if not self.timer_running:
            self.start_button.config(state=tk.DISABLED)
            self.submit_button.config(state=tk.NORMAL)
            self.timer_running = True
            self.update_timer()
            self.start_time = time.time()
            # Countdown timer
            countdown_time = 3  # Set the countdown time in seconds
            for i in range(countdown_time, 0, -1):
                self.label_sentence.config(text=f"Get ready! Starting in {i} seconds...")
                self.root.update()
                time.sleep(1)

            level = self.level_var.get()
            sentences = self.easy_sentences if level == "easy" else self.hard_sentences
            self.label_sentence.config(text=random.choice(sentences))
            self.start_time = time.time()

    def update_timer(self):
        if self.timer_running:
            elapsed_time = int(time.time() - self.start_time)
            minutes = elapsed_time // 60
            seconds = elapsed_time % 60
            timer_text = f"Time: {minutes:02d}:{seconds:02d}"
            self.timer_label.config(text=timer_text)
            self.root.after(1000, self.update_timer)

    def submit_typing_test(self):
        self.timer_running = False
        user_input = self.user_input.get()
        sentence = self.label_sentence.cget("text")
        elapsed_time = time.time() - self.start_time
        words_per_minute = len(user_input.split()) / (elapsed_time / 60)
        correct_chars = sum([1 for c1, c2 in zip(sentence, user_input) if c1 == c2])
        accuracy = (correct_chars / len(sentence)) * 100

        # Get the name from the name_entry widget and store it
        self.name = self.name_entry.get()

        result_text = f"{self.name}, your typing speed: {words_per_minute:.2f} words per minute\nYour typing accuracy: {accuracy:.2f}%"
        messagebox.showinfo("Typing Test Result", result_text)

        # Store typing test result in history
        self.history.append(result_text)

        # Store typing test result in database
        self.cur.execute("INSERT INTO leaderboard (name, speed, accuracy) VALUES (?, ?, ?)",
                         (self.name, words_per_minute, accuracy))
        self.conn.commit()

        self.user_input.delete(0, tk.END)
        # Clear the name entry
        self.name_entry.delete(0, tk.END)
        self.start_button.config(state=tk.NORMAL)
        self.submit_button.config(state=tk.DISABLED)
        self.timer_label.config(text="Time: 0:00")

    def show_history(self):
        history_window = tk.Toplevel(self.root)
        history_window.title("Typing Test History")
        history_window.configure(bg='light blue')

        history_label = tk.Label(history_window, text="Typing Test History", font=("Algerian", 24, "bold"), fg="black", bg='yellow')
        history_label.pack(pady=20)

        for idx, entry in enumerate(self.history, start=1):
            history_entry_label = tk.Label(history_window, text=f"{idx}. {entry}", font=("Arial", 18), fg="black", bg='yellow')
            history_entry_label.pack()

    def show_leaderboard(self):
        leaderboard_window = tk.Toplevel(self.root)
        leaderboard_window.title("Typing Speed Leaderboard")
        leaderboard_window.configure(bg='light green')

        leaderboard_label = tk.Label(leaderboard_window, text="Typing Speed Leaderboard", font=("Algerian", 24, "bold"), fg="black", bg='yellow')
        leaderboard_label.pack(pady=20)

        # Retrieve leaderboard data from database
        self.cur.execute("SELECT name, speed, accuracy FROM leaderboard ORDER BY speed DESC")
        leaderboard_data = self.cur.fetchall()

        for idx, (name, speed, accuracy) in enumerate(leaderboard_data, start=1):
            leaderboard_entry_label = tk.Label(leaderboard_window, text=f"{idx}. {name}: {speed:.2f} words per minute, Accuracy: {accuracy:.2f}%", font=("Arial", 18), fg="black", bg='yellow')
            leaderboard_entry_label.pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = TypingSpeedTestApp(root)
    root.mainloop()
