import random
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw
import os
import math

class DiceRollerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎲 Dice Rolling Simulator")
        self.root.geometry("500x600")
        self.root.resizable(False, False)
        self.root.configure(bg='#f0f0f0')
        
        # Style configuration
        self.style = ttk.Style()
        self.style.configure('TButton', font=('Arial', 12), padding=10)
        
        # Create main frame
        self.main_frame = ttk.Frame(root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(
            self.main_frame, 
            text="🎲 Dice Rolling Simulator", 
            font=('Arial', 20, 'bold'),
            foreground='#2c3e50'
        )
        title_label.pack(pady=(0, 20))
        
        # Dice frame
        self.dice_frame = ttk.Frame(self.main_frame)
        self.dice_frame.pack(pady=20)
        
        # Dice labels
        self.dice_images = {}
        self.dice_labels = []
        
        # Load dice images
        self.load_dice_images()
        
        # Create dice display with proper styling
        for i in range(2):
            frame = ttk.Frame(self.dice_frame, padding=10, relief='raised', borderwidth=2)
            frame.pack(side=tk.LEFT, padx=20, pady=10)
            
            # Add a subtle shadow effect
            style = ttk.Style()
            style.configure('Dice.TFrame', background='#e0e0e0')
            frame['style'] = 'Dice.TFrame'
            
            label = ttk.Label(frame, image=self.dice_images[1], background='white')
            label.pack(padx=5, pady=5)
            self.dice_labels.append(label)
        
        # Total label
        self.total_label = ttk.Label(
            self.main_frame, 
            text="Total: ", 
            font=('Arial', 18, 'bold'),
            foreground='#2c3e50'
        )
        self.total_label.pack(pady=10)
        
        # Roll button
        self.roll_button = ttk.Button(
            self.main_frame,
            text="Roll Dice",
            command=self.animate_roll,
            style='TButton'
        )
        self.roll_button.pack(pady=20)
        
        # Roll history
        self.history_label = ttk.Label(
            self.main_frame,
            text="Roll History:",
            font=('Arial', 12, 'bold'),
            foreground='#2c3e50'
        )
        self.history_label.pack()
        
        self.history_text = tk.Text(
            self.main_frame,
            height=6,
            width=30,
            font=('Arial', 10),
            state=tk.DISABLED
        )
        self.history_text.pack(pady=10)
        
        # Initialize history
        self.roll_history = []
    
    def load_dice_images(self):
        """Create dice images with proper dot patterns"""
        size = 100
        padding = 10
        dot_radius = 8
        
        # Dice face configurations (positions of dots for each face)
        face_configs = {
            1: [(0.5, 0.5)],
            2: [(0.25, 0.25), (0.75, 0.75)],
            3: [(0.25, 0.25), (0.5, 0.5), (0.75, 0.75)],
            4: [(0.25, 0.25), (0.75, 0.25), (0.25, 0.75), (0.75, 0.75)],
            5: [(0.25, 0.25), (0.75, 0.25), (0.5, 0.5), (0.25, 0.75), (0.75, 0.75)],
            6: [(0.25, 0.25), (0.25, 0.5), (0.25, 0.75), 
                (0.75, 0.25), (0.75, 0.5), (0.75, 0.75)]
        }
        
        for face_value, dots in face_configs.items():
            # Create a white square image
            image = Image.new('RGB', (size, size), 'white')
            draw = ImageDraw.Draw(image)
            
            # Draw dice border
            draw.rectangle([(padding, padding), (size-padding, size-padding)], 
                          outline='black', width=2, fill='white')
            
            # Draw rounded corners
            for x, y in [(padding, padding), (size-padding, padding), 
                         (padding, size-padding), (size-padding, size-padding)]:
                draw.ellipse([x-4, y-4, x+4, y+4], fill='white', outline='black')
            
            # Draw dots
            for dx, dy in dots:
                x = padding + (size - 2 * padding) * dx
                y = padding + (size - 2 * padding) * dy
                draw.ellipse([x-dot_radius, y-dot_radius, x+dot_radius, y+dot_radius], 
                            fill='black')
            
            # Save the image
            self.dice_images[face_value] = ImageTk.PhotoImage(image)
    
    def update_dice_faces(self, die1, die2):
        """Update the dice faces with new values"""
        # Update the first die
        self.dice_labels[0].config(image=self.dice_images[die1])
        self.dice_labels[0].image = self.dice_images[die1]  # Keep a reference
        
        # Update the second die
        self.dice_labels[1].config(image=self.dice_images[die2])
        self.dice_labels[1].image = self.dice_images[die2]  # Keep a reference
        
        # Update the window to show the changes immediately
        self.root.update()
    
    def animate_roll(self):
        """Animate the dice rolling"""
        self.roll_button.config(state=tk.DISABLED)
        self.animate_roll_step(0)
    
    def animate_roll_step(self, step):
        if step < 10:  # Number of animation steps
            # Show random faces during animation with increasing delay
            die1 = random.randint(1, 6)
            die2 = random.randint(1, 6)
            self.update_dice_faces(die1, die2)
            # Gradually slow down the animation
            delay = 50 + (step * 5)  # Start fast, get slower
            self.root.after(delay, lambda: self.animate_roll_step(step + 1))
        else:
            # Final roll
            self.roll_dice()
            self.roll_button.config(state=tk.NORMAL)
    
    def roll_dice(self):
        """Roll the dice and update the display"""
        die1 = random.randint(1, 6)
        die2 = random.randint(1, 6)
        total = die1 + die2
        
        # Update dice display
        self.update_dice_faces(die1, die2)
        
        # Update total
        self.total_label.config(text=f"Total: {total}")
        
        # Add to history
        self.add_to_history(die1, die2, total)
    
    def add_to_history(self, die1, die2, total):
        """Add the current roll to the history"""
        roll_text = f"🎲 {die1} + {die2} = {total}"
        self.roll_history.append(roll_text)
        
        # Update history display (show last 5 rolls)
        self.history_text.config(state=tk.NORMAL)
        self.history_text.delete(1.0, tk.END)
        
        # Show most recent 5 rolls
        for roll in self.roll_history[-5:]:
            self.history_text.insert(tk.END, roll + "\n")
        
        self.history_text.config(state=tk.DISABLED)

def main():
    root = tk.Tk()
    app = DiceRollerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
