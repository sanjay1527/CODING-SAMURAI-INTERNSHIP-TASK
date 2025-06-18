import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
import threading
import math

class UltraImmersiveNumberGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🔥 ULTIMATE NUMBER HUNTER 🔥")
        self.root.geometry("800x600")
        self.root.configure(bg='#1a1a1a')
        self.root.resizable(True, True)
        
        # Game Variables
        self.target_number = 0
        self.attempts_left = 0
        self.max_attempts = 7
        self.current_level = 1
        self.score = 0
        self.streak = 0
        self.game_active = False
        self.min_range = 1
        self.max_range = 100
        
        # Animation Variables
        self.pulse_active = False
        self.current_bg_color = '#1a1a1a'
        self.animation_thread = None
        
        # Create the stunning UI
        self.setup_ui()
        self.start_new_game()
        
    def setup_ui(self):
        """Create the immersive game interface"""
        # Main container with gradient-like effect
        main_frame = tk.Frame(self.root, bg='#1a1a1a')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Animated Title with glow effect
        self.title_label = tk.Label(main_frame, 
                                   text="🔥 ULTIMATE NUMBER HUNTER 🔥",
                                   bg='#1a1a1a', 
                                   fg='#ff6600',
                                   font=('Arial', 28, 'bold'))
        self.title_label.pack(pady=(0, 20))
        
        # Game Stats Panel
        stats_frame = tk.Frame(main_frame, bg='#2a2a2a', relief='raised', bd=4)
        stats_frame.pack(fill='x', pady=(0, 20))
        
        stats_inner = tk.Frame(stats_frame, bg='#2a2a2a')
        stats_inner.pack(pady=15)
        
        # Stats Labels
        self.level_label = tk.Label(stats_inner, text="LEVEL: 1", 
                                   bg='#2a2a2a', fg='#00ff00', 
                                   font=('Arial', 14, 'bold'))
        self.level_label.grid(row=0, column=0, padx=20)
        
        self.score_label = tk.Label(stats_inner, text="SCORE: 0", 
                                   bg='#2a2a2a', fg='#ffff00', 
                                   font=('Arial', 14, 'bold'))
        self.score_label.grid(row=0, column=1, padx=20)
        
        self.streak_label = tk.Label(stats_inner, text="STREAK: 0", 
                                    bg='#2a2a2a', fg='#ff00ff', 
                                    font=('Arial', 14, 'bold'))
        self.streak_label.grid(row=0, column=2, padx=20)
        
        # Game Info Panel - This will change colors based on proximity!
        self.info_frame = tk.Frame(main_frame, bg='#333333', relief='sunken', bd=4)
        self.info_frame.pack(fill='x', pady=(0, 20))
        
        self.game_info = tk.Label(self.info_frame, 
                                 text="🎯 Ready to hunt some numbers? 🎯",
                                 bg='#333333', fg='#ffffff', 
                                 font=('Arial', 16, 'bold'))
        self.game_info.pack(pady=20)
        
        self.range_label = tk.Label(self.info_frame, 
                                   text="",
                                   bg='#333333', fg='#00ffff', 
                                   font=('Arial', 14))
        self.range_label.pack()
        
        self.attempts_label = tk.Label(self.info_frame, 
                                      text="",
                                      bg='#333333', fg='#ffffff', 
                                      font=('Arial', 14, 'bold'))
        self.attempts_label.pack(pady=(5, 15))
        
        # Input Section
        input_frame = tk.Frame(main_frame, bg='#1a1a1a')
        input_frame.pack(pady=20)
        
        tk.Label(input_frame, text="🔮 Enter Your Guess:", 
                bg='#1a1a1a', fg='#00ffff', 
                font=('Arial', 16, 'bold')).pack(pady=(0, 10))
        
        self.guess_entry = tk.Entry(input_frame, 
                                   font=('Arial', 20, 'bold'),
                                   bg='#2a2a2a', fg='#ffffff',
                                   insertbackground='#00ffff',
                                   justify='center',
                                   width=12,
                                   relief='solid',
                                   bd=3)
        self.guess_entry.pack(pady=10)
        self.guess_entry.bind('<Return>', self.on_enter_pressed)
        self.guess_entry.bind('<KeyRelease>', self.validate_input)
        
        # Action Buttons
        button_frame = tk.Frame(main_frame, bg='#1a1a1a')
        button_frame.pack(pady=20)
        
        self.guess_button = tk.Button(button_frame, 
                                     text="🚀 FIRE GUESS!", 
                                     command=self.make_guess,
                                     bg='#ff6600', fg='#ffffff',
                                     font=('Arial', 16, 'bold'),
                                     relief='raised', bd=4,
                                     padx=30, pady=10,
                                     activebackground='#ff8800')
        self.guess_button.pack(side='left', padx=15)
        
        self.hint_button = tk.Button(button_frame, 
                                    text="💡 HINT", 
                                    command=self.give_hint,
                                    bg='#0066cc', fg='#ffffff',
                                    font=('Arial', 16, 'bold'),
                                    relief='raised', bd=4,
                                    padx=30, pady=10,
                                    activebackground='#0088ff')
        self.hint_button.pack(side='left', padx=15)
        
        self.new_game_button = tk.Button(button_frame, 
                                        text="🔄 NEW GAME", 
                                        command=self.start_new_game,
                                        bg='#cc0066', fg='#ffffff',
                                        font=('Arial', 16, 'bold'),
                                        relief='raised', bd=4,
                                        padx=30, pady=10,
                                        activebackground='#ee0088')
        self.new_game_button.pack(side='left', padx=15)
        
        # Dynamic Feedback Display
        self.feedback_frame = tk.Frame(main_frame, bg='#2a2a2a', relief='sunken', bd=4)
        self.feedback_frame.pack(fill='both', expand=True, pady=(20, 0))
        
        tk.Label(self.feedback_frame, text="🌟 QUANTUM FEEDBACK 🌟", 
                bg='#2a2a2a', fg='#ffff00', 
                font=('Arial', 16, 'bold')).pack(pady=(15, 10))
        
        # Scrollable feedback area
        feedback_container = tk.Frame(self.feedback_frame, bg='#2a2a2a')
        feedback_container.pack(fill='both', expand=True, padx=15, pady=(0, 15))
        
        self.feedback_text = tk.Text(feedback_container, 
                                    bg='#1a1a1a', fg='#ffffff',
                                    font=('Arial', 12),
                                    wrap='word',
                                    height=8,
                                    relief='flat',
                                    bd=0,
                                    state='disabled')
        
        scrollbar = tk.Scrollbar(feedback_container, command=self.feedback_text.yview)
        self.feedback_text.configure(yscrollcommand=scrollbar.set)
        
        self.feedback_text.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Configure text styling tags
        self.setup_text_tags()
        
        # Keyboard shortcuts
        self.root.bind('<Control-n>', lambda e: self.start_new_game())
        self.root.bind('<Escape>', lambda e: self.root.quit())
        
        # Focus on entry
        self.guess_entry.focus()
        
    def setup_text_tags(self):
        """Setup colored text tags for feedback"""
        tags = {
            'burning': {'foreground': '#ff0000', 'font': ('Arial', 14, 'bold')},
            'hot': {'foreground': '#ff6600', 'font': ('Arial', 13, 'bold')},
            'warm': {'foreground': '#ff9900', 'font': ('Arial', 12, 'bold')},
            'cool': {'foreground': '#0099ff', 'font': ('Arial', 12)},
            'cold': {'foreground': '#0066cc', 'font': ('Arial', 12)},
            'frozen': {'foreground': '#003399', 'font': ('Arial', 12)},
            'win': {'foreground': '#00ff00', 'font': ('Arial', 16, 'bold')},
            'lose': {'foreground': '#ff0000', 'font': ('Arial', 14, 'bold')},
            'hint': {'foreground': '#ffff00', 'font': ('Arial', 12, 'italic')},
            'system': {'foreground': '#ff00ff', 'font': ('Arial', 12, 'bold')},
            'normal': {'foreground': '#ffffff', 'font': ('Arial', 12)}
        }
        
        for tag, config in tags.items():
            self.feedback_text.tag_config(tag, **config)
    
    def start_new_game(self):
        """Initialize a new game"""
        # Level progression
        self.max_range = min(1000, 50 + (self.current_level * 50))
        self.max_attempts = max(5, 10 - (self.current_level // 2))
        
        self.target_number = random.randint(self.min_range, self.max_range)
        self.attempts_left = self.max_attempts
        self.game_active = True
        
        # Reset UI colors
        self.reset_colors()
        
        # Update display
        self.update_display()
        self.add_feedback(f"🎮 NEW GAME STARTED! Level {self.current_level} 🎮\n", 'system')
        self.add_feedback(f"🎯 I'm thinking of a number between {self.min_range} and {self.max_range}\n", 'normal')
        self.add_feedback(f"⚡ You have {self.max_attempts} attempts to find it!\n\n", 'normal')
        
        # Clear and focus entry
        self.guess_entry.delete(0, tk.END)
        self.guess_entry.focus()
    
    def validate_input(self, event=None):
        """Real-time input validation with visual feedback"""
        try:
            value = self.guess_entry.get()
            if not value:
                self.guess_entry.configure(bg='#2a2a2a')
                return
                
            num = int(value)
            if self.min_range <= num <= self.max_range:
                self.guess_entry.configure(bg='#002200')  # Valid - green tint
            else:
                self.guess_entry.configure(bg='#330000')  # Invalid - red tint
        except ValueError:
            self.guess_entry.configure(bg='#330000')  # Invalid - red tint
    
    def on_enter_pressed(self, event):
        """Handle Enter key press"""
        self.make_guess()
    
    def make_guess(self):
        """Process the player's guess with immersive feedback!"""
        if not self.game_active:
            return
            
        try:
            guess = int(self.guess_entry.get())
        except ValueError:
            self.add_feedback("❌ Please enter a valid number!\n", 'lose')
            return
        
        if not (self.min_range <= guess <= self.max_range):
            self.add_feedback(f"❌ Number must be between {self.min_range} and {self.max_range}!\n", 'lose')
            return
        
        self.attempts_left -= 1
        
        # Calculate proximity for color effects
        distance = abs(guess - self.target_number)
        max_distance = self.max_range - self.min_range
        proximity = 1 - (distance / max_distance)  # 1 = perfect, 0 = furthest
        
        # WINNING!
        if guess == self.target_number:
            self.handle_win()
            return
        
        # Generate immersive feedback based on proximity
        self.generate_proximity_feedback(guess, distance, proximity)
        
        # Change background colors based on proximity (HOT/COLD effect!)
        self.animate_proximity_colors(proximity)
        
        # Check for game over
        if self.attempts_left <= 0:
            self.handle_lose()
        else:
            self.update_display()
        
        # Clear entry for next guess
        self.guess_entry.delete(0, tk.END)
    
    def generate_proximity_feedback(self, guess, distance, proximity):
        """Generate dynamic feedback based on how close the guess is"""
        feedback_messages = []
        
        # Proximity-based feedback
        if proximity > 0.9:  # Very close!
            feedback_messages.append(("🔥🔥🔥 BURNING HOT! You're almost there! 🔥🔥🔥\n", 'burning'))
        elif proximity > 0.7:  # Close
            feedback_messages.append(("🔥🔥 HOT! Getting very close! 🔥🔥\n", 'hot'))
        elif proximity > 0.5:  # Warm
            feedback_messages.append(("🔥 Warm! You're on the right track! 🔥\n", 'warm'))
        elif proximity > 0.3:  # Cool
            feedback_messages.append(("❄️ Cool. You're getting somewhere... ❄️\n", 'cool'))
        elif proximity > 0.1:  # Cold
            feedback_messages.append(("🧊 Cold! Pretty far off... 🧊\n", 'cold'))
        else:  # Very cold
            feedback_messages.append(("🧊🧊🧊 FROZEN! Way off target! 🧊🧊🧊\n", 'frozen'))
        
        # Direction hint
        if guess < self.target_number:
            feedback_messages.append(("📈 Think HIGHER!\n", 'normal'))
        else:
            feedback_messages.append(("📉 Think LOWER!\n", 'normal'))
        
        # Add attempt info
        feedback_messages.append((f"🎯 Guess #{self.max_attempts - self.attempts_left}: {guess}\n", 'normal'))
        feedback_messages.append((f"⚡ {self.attempts_left} attempts remaining\n\n", 'system'))
        
        # Display all feedback
        for message, tag in feedback_messages:
            self.add_feedback(message, tag)
    
    def animate_proximity_colors(self, proximity):
        """Animate background colors based on proximity - HOT/COLD effect!"""
        if self.pulse_active:
            return  # Don't start new animation if one is running
            
        self.pulse_active = True
        
        # Determine colors based on proximity
        if proximity > 0.8:  # Very hot - red shades
            colors = ['#ff0000', '#ff3333', '#ff6666', '#ff3333', '#ff0000']
        elif proximity > 0.6:  # Hot - orange/red
            colors = ['#ff6600', '#ff8833', '#ffaa66', '#ff8833', '#ff6600']
        elif proximity > 0.4:  # Warm - orange/yellow
            colors = ['#ff9900', '#ffbb33', '#ffdd66', '#ffbb33', '#ff9900']
        elif proximity > 0.2:  # Cool - light blue
            colors = ['#0099ff', '#33aaff', '#66bbff', '#33aaff', '#0099ff']
        else:  # Cold - dark blue
            colors = ['#0066cc', '#3388dd', '#66aaee', '#3388dd', '#0066cc']
        
        # Animate the color changes
        def animate():
            for color in colors:
                if not self.pulse_active:
                    break
                self.info_frame.configure(bg=color)
                self.game_info.configure(bg=color)
                self.range_label.configure(bg=color)
                self.attempts_label.configure(bg=color)
                self.root.update()
                time.sleep(0.15)
            
            # Return to normal
            self.reset_colors()
            self.pulse_active = False
        
        # Run animation in thread to avoid blocking
        if self.animation_thread and self.animation_thread.is_alive():
            self.pulse_active = False
            self.animation_thread.join(timeout=0.1)
        
        self.animation_thread = threading.Thread(target=animate, daemon=True)
        self.animation_thread.start()
    
    def reset_colors(self):
        """Reset UI to default colors"""
        self.info_frame.configure(bg='#333333')
        self.game_info.configure(bg='#333333')
        self.range_label.configure(bg='#333333')
        self.attempts_label.configure(bg='#333333')
    
    def handle_win(self):
        """Handle winning the game with celebration!"""
        self.game_active = False
        self.streak += 1
        
        # Calculate score
        efficiency_bonus = self.attempts_left * 10
        speed_bonus = max(0, 50 - (self.max_attempts - self.attempts_left) * 5)
        level_bonus = self.current_level * 20
        total_points = 100 + efficiency_bonus + speed_bonus + level_bonus
        self.score += total_points
        
        # Victory animation
        self.victory_animation()
        
        # Victory message
        self.add_feedback("🎉🎉🎉 VICTORY! YOU'VE FOUND THE NUMBER! 🎉🎉🎉\n", 'win')
        self.add_feedback(f"🎯 The number was: {self.target_number}\n", 'win')
        self.add_feedback(f"⭐ Points earned: {total_points}\n", 'system')
        self.add_feedback(f"🔥 Streak: {self.streak} wins!\n", 'system')
        
        # Level up
        if self.streak % 3 == 0:  # Level up every 3 wins
            self.current_level += 1
            self.add_feedback(f"🚀 LEVEL UP! Now at Level {self.current_level}!\n", 'win')
        
        self.update_display()
        
        # Auto-start next game after celebration
        self.root.after(3000, self.start_new_game)
    
    def victory_animation(self):
        """Epic victory animation!"""
        victory_colors = ['#00ff00', '#ffff00', '#ff00ff', '#00ffff', '#ff6600']
        
        def animate_victory():
            for _ in range(10):  # 10 cycles of color changes
                for color in victory_colors:
                    self.root.configure(bg=color)
                    self.root.update()
                    time.sleep(0.1)
            self.root.configure(bg='#1a1a1a')  # Back to normal
        
        threading.Thread(target=animate_victory, daemon=True).start()
    
    def handle_lose(self):
        """Handle losing the game"""
        self.game_active = False
        self.streak = 0  # Reset streak
        
        self.add_feedback("💥💥💥 GAME OVER! 💥💥💥\n", 'lose')
        self.add_feedback(f"😔 The number was: {self.target_number}\n", 'lose')
        self.add_feedback("🔄 Starting new game...\n\n", 'system')
        
        self.update_display()
        
        # Auto-start new game
        self.root.after(3000, self.start_new_game)
    
    def give_hint(self):
        """Provide a strategic hint (costs points!)"""
        if not self.game_active:
            return
        
        # Hint costs points
        self.score = max(0, self.score - 25)
        
        hints = []
        
        # Range hint
        quarter = (self.max_range - self.min_range) // 4
        if self.target_number <= self.min_range + quarter:
            hints.append(f"🔍 The number is in the LOWER quarter ({self.min_range}-{self.min_range + quarter})")
        elif self.target_number <= self.min_range + 2 * quarter:
            hints.append(f"🔍 The number is in the LOWER-MIDDLE quarter")
        elif self.target_number <= self.min_range + 3 * quarter:
            hints.append(f"🔍 The number is in the UPPER-MIDDLE quarter")
        else:
            hints.append(f"🔍 The number is in the UPPER quarter")
        
        # Even/odd hint
        if self.target_number % 2 == 0:
            hints.append("🔍 The number is EVEN")
        else:
            hints.append("🔍 The number is ODD")
        
        # Divisibility hint
        for divisor in [3, 5, 7]:
            if self.target_number % divisor == 0:
                hints.append(f"🔍 The number is divisible by {divisor}")
                break
        
        # Choose random hint
        chosen_hint = random.choice(hints)
        self.add_feedback(f"💡 HINT: {chosen_hint} (Cost: 25 points)\n", 'hint')
        
        self.update_display()
    
    def add_feedback(self, message, tag='normal'):
        """Add colored feedback to the display"""
        self.feedback_text.configure(state='normal')
        self.feedback_text.insert(tk.END, message, tag)
        self.feedback_text.configure(state='disabled')
        self.feedback_text.see(tk.END)  # Auto-scroll to bottom
    
    def update_display(self):
        """Update all display elements"""
        self.level_label.configure(text=f"LEVEL: {self.current_level}")
        self.score_label.configure(text=f"SCORE: {self.score}")
        self.streak_label.configure(text=f"STREAK: {self.streak}")
        
        self.range_label.configure(text=f"Range: {self.min_range} - {self.max_range}")
        self.attempts_label.configure(text=f"Attempts Left: {self.attempts_left}")
        
        if self.game_active:
            self.game_info.configure(text="🎯 Make your guess! Feel the heat! 🎯")
        else:
            self.game_info.configure(text="🎮 Game Over - New game starting... 🎮")
    
    def run(self):
        """Start the game"""
        self.root.mainloop()

# Create and run the game
if __name__ == "__main__":
    print("🚀 Starting Ultra-Immersive Number Guessing Game!")
    print("💡 Tips:")
    print("   • Watch the colors change as you get closer!")
    print("   • Use hints strategically (they cost points)")
    print("   • Build streaks to level up!")
    print("   • Press Ctrl+N for new game, Esc to quit")
    print("\n🎮 Let the hunt begin!\n")
    
    game = UltraImmersiveNumberGame()
    game.run()