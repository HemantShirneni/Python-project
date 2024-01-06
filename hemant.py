import tkinter as tk
from tkinter import messagebox
import time
import random

class TypingSpeedTestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Test")
        self.root.configure(bg='Salmon')  # Set background color

        self.sentences = [
            " There was once a hare who was friends with a Tortoise. One day, He challenged the tortoise to race. Seeing how slow the tortoise was going, The hare thought he'd win this easily.",
            "Once there was a Dog who wandered the street night and day in search of food. One day, He found a big juicy Bone, and he immediately grabbed it in his mouth and took it home",
            " THE THIRSTY CROW, After flying a long distance, a thirsty crow wandered the forest searching for water. Finally, He saw a pot half-filled with water.",
            "Peafowl is a common name for two bird species in the genera Pavo and Afropavo within the tribe Pavonini of the family Phasianidae (the pheasants and their allies). Male peafowl are referred to as peacocks",
            "In 2013, Kohli was ranked number one in the ICC rankings for ODI batsmen. In 2018, he was ranked top Test batsman, making him the only Indian cricketer to hold the number one spot in all three formats of the game. ",
        ]

        self.headline_label = tk.Label(root, text="Test Your Typing Skills", font=("Algerian", 32, "bold"), fg="black", bg='Salmon')
        self.headline_label.pack(pady=20)

        self.label_sentence = tk.Label(root, text="", font=("Arial", 26), wraplength=500, justify='center')
        self.label_sentence.pack(pady=20)

        self.user_input = tk.Entry(root, font=("Arial", 26), bd=3, relief=tk.GROOVE)
        self.user_input.pack(pady=10)

        self.timer_label = tk.Label(root, text="Time: 0:00", font=("Arial", 24), fg="black", bg='Salmon')
        self.timer_label.pack()

        self.start_button = tk.Button(root, text="Start Typing Test", command=self.start_typing_test, bg="black", fg="red", font=("Arial", 18), padx=20, pady=10)
        self.start_button.pack(pady=10)

        self.submit_button = tk.Button(root, text="Submit", command=self.submit_typing_test, state=tk.DISABLED, bg="black", fg="red", font=("Arial", 18), padx=20, pady=10)
        self.submit_button.pack(pady=30)

        self.start_time = 0
        self.timer_running = False

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

            self.label_sentence.config(text=random.choice(self.sentences))
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

        messagebox.showinfo(
            "Typing Test Result",
            f"Your typing speed: {words_per_minute:.2f} words per minute\nYour typing accuracy: {accuracy:.2f}%"
        )

        self.user_input.delete(0, tk.END)
        self.start_button.config(state=tk.NORMAL)
        self.submit_button.config(state=tk.DISABLED)
        self.timer_label.config(text="Time: 0:00")

if __name__ == "__main__":
    root = tk.Tk()
    app = TypingSpeedTestApp(root)
    root.mainloop()
