import tkinter as tk
from tkinter import messagebox
import time
import random

class TypingSpeedTestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Test")
        self.root.configure(bg='light blue')  # Set background color


        self.sentences = [
            " There was once a hare who was friends with a Tortoise. One day, He challenge the tortoise to race. Seeing how slow the tortoise was going, The hare thought he'd win this easily.",
            "Once there was a Dog who wandered the street night and day in search of food. One day, He found a big juicy Bone, and he immediately grabbed it in his mouth and took it home",
            " THE THIRSTY CROW, After flying long distance, a thristy crow wandered the forest searching for water. Finlly, He saw a pot half filled with water.",



        ]

        self.label_sentence = tk.Label(root, text="", font=("Arial", 16), wraplength=500, justify='center')
        self.label_sentence.pack(pady=40)

        self.user_input = tk.Entry(root, font=("Arial", 14), bd=3, relief=tk.GROOVE)
        self.user_input.pack(pady=10)

        self.start_button = tk.Button(root, text="Start Typing Test", command=self.start_typing_test, bg="#FF5252", fg="white", font=("Arial", 12), padx=20, pady=10)
        self.start_button.pack(pady=10)

        self.submit_button = tk.Button(root, text="Submit", command=self.submit_typing_test, state=tk.DISABLED, bg="#FFD740", fg="black", font=("Arial", 12), padx=20, pady=10)
        self.submit_button.pack(pady=30)

        self.start_time = 0


        

    def start_typing_test(self):
        self.label_sentence.config(text=random.choice(self.sentences))
        self.start_time = time.time()
        self.start_button.config(state=tk.DISABLED)
        self.submit_button.config(state=tk.NORMAL)

    def submit_typing_test(self):
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


if __name__ == "__main__":
    root = tk.Tk()
    app = TypingSpeedTestApp(root)
    root.mainloop()
