import tkinter as tk
from tkinter import messagebox
import pygame
from PIL import Image, ImageTk


class GridOfSecretsGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Grid of Secrets")
        self.root.configure(bg="black")
        self.root.attributes('-fullscreen', True)  # Fullscreen mode

        # Initialize Pygame for sound
        pygame.mixer.init()

        # Load background music and sound effects
        pygame.mixer.music.load("background_music.wav")  # Replace with your file path
        pygame.mixer.music.play(-1)  # Loop the background music
        self.correct_sound = pygame.mixer.Sound("correct_guess.wav")  # Replace with your file path
        self.incorrect_sound = pygame.mixer.Sound("incorrect_guess.wav")  # Replace with your file path

        # Load and set background image
        self.background_image = Image.open("background_image.jpg")  # Replace with your file path
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.background_image = self.background_image.resize((screen_width, screen_height), Image.LANCZOS)
        self.background_photo = ImageTk.PhotoImage(self.background_image)
        self.background_label = tk.Label(root, image=self.background_photo)
        self.background_label.place(relwidth=1, relheight=1)

        # Clue instructions and answers
        self.clues = [
            ("Some Two Little Ducks", 4),
            ("I speak in numbers, but my words are letters. Decode me to proceed: 5 9 7 8 20", 8),
            ("Middle East  Chetan Sharma  1986 ", 6),
            ("npwf pof tufq epxo (Shift <--)", 9),  # Shifting one step backward reveals "move one step down"
            (
            "Th7s m1ght s33m l1k3 n0ns3ns3, but 1f y0u r34d cl0sely, y0u’ll f1nd y0ur cl3w. Twogether we can make it work.",
            2),
            ("C1E4N5T7E9R", 5),
            ("I resemble a vowel you see in the mirror. Reflect me onto myself. Rotate to get your answer.", 3)
        ]

        self.step = 0
        self.pin_input = []  # Store pin input

        # Create a frame for buttons
        self.button_frame = tk.Frame(root, bg="black")
        self.button_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Create a 3x3 grid of buttons
        self.buttons = []
        for row in range(3):
            button_row = []
            for col in range(3):
                button = tk.Button(
                    self.button_frame, text=str(row * 3 + col + 1), width=7, height=3, fg="lime",
                    bg="black", font=("Courier", 24, "bold"),
                    command=lambda r=row, c=col: self.check_answer(r, c)
                )
                button.grid(row=row, column=col, padx=10, pady=10)
                button_row.append(button)
            self.buttons.append(button_row)

        # Instruction label
        self.label_frame = tk.Frame(root, bg="black")
        self.label_frame.place(relx=0.5, rely=0.85, anchor=tk.CENTER)
        self.label = tk.Label(
            self.label_frame, text=self.clues[self.step][0], fg="lime", bg="black",
            font=("Courier", 14, "bold"), wraplength=1200
        )
        self.label.pack()

        # Prompt message to tap each number
        self.prompt = tk.Label(
            root, text="Tap the block to start unlocking the grid's secrets. (Numbers do not REPEAT)", fg="lime",
            bg="black", font=("Courier", 16)
        )
        self.prompt.pack(pady=20)

        # Pin display label
        self.pin_label = tk.Label(root, text="PIN: ", fg="lime", bg="black", font=("Courier", 22, "bold"))
        self.pin_label.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

    def update_pin_display(self):
        # Display the current PIN
        self.pin_label.config(text="PIN: " + "".join(map(str, self.pin_input)))

    def check_answer(self, row, col):
        # Define the correct answer grid
        answer_grid = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        answer = answer_grid[row * 3 + col]

        # Store the answer in pin input
        self.pin_input.append(answer)  # Store pin input
        self.update_pin_display()  # Update the displayed PIN

        # Move to next step if not completed
        if len(self.pin_input) < len(self.clues):
            self.label.config(text=self.clues[len(self.pin_input)][0])
        else:
            self.validate_pin()

    def validate_pin(self):
        correct_sequence = [clue[1] for clue in self.clues]  # Extract correct sequence

        if self.pin_input == correct_sequence:
            self.label.config(text="You've cracked the code! The grid's secrets are revealed.")
            messagebox.showinfo("Success", "The screen unlocks. No more to fear.")
            self.root.destroy()
        else:
            self.incorrect_sound.play()  # Play incorrect sound
            messagebox.showerror("Incorrect", "Incorrect sequence. Try again.")
            self.pin_input.clear()  # Reset input
            self.update_pin_display()
            self.label.config(text=self.clues[0][0])  # Reset first clue
            self.step = 0  # Reset step


if __name__ == "__main__":
    root = tk.Tk()
    app = GridOfSecretsGame(root)
    root.mainloop()
