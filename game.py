import curses
import time
import random
import subprocess
import os
import tempfile
from datetime import datetime, timedelta

class VimPracticeGame:
    def __init__(self):
        self.challenges = [
            # Each tuple contains (original_text, modified_text, difficulty_score)
            (
                "def quicksort(arr):\n    if len(arr) <= 1:\n        return arr\n    pivot = arr[len(arr) // 2]\n    left = [x for x in arr if x < pivot]\n    middle = [x for x in arr if x == pivot]\n    right = [x for x in arr if x > pivot]\n    return quicksort(left) + middle + quicksort(right)",
                "def quicksort(arr):\n    if len(arr) <= 1:\n        return arr\n    pivot = arr[len(arr) // 2]\n    left = [x for x in arr if x < povit]\n    middle = [x for x in arr if x = pivot]\n    right = [x for x in arr if x > pivot]\n    return quicksort(left) + middle + quciksort(right)",
                3
            ),
            (
                "class Node:\n    def __init__(self, value):\n        self.value = value\n        self.next = None\n        self.prev = None",
                "class Node:\n    def __init__(self, value)\n        self.value = value\n        self.next = None\n        prev = None",
                2
            ),
            (
                "@decorator\ndef complex_function(a, b):\n    result = []\n    for i in range(len(a)):\n        if a[i] > b[i]:\n            result.append(a[i])\n    return result",
                "@decorator\ndef complex_function(a, b)\n    result = []\n    for i in range(len(a))\n        if a[i] > b[i]\n            result.append(a[i])\n    return result",
                4
            )
        ]
        self.current_score = 0
        self.total_time = 60  # 1 minute timer

    def calculate_score(self, time_taken, difficulty):
        base_score = difficulty * 100
        time_penalty = (time_taken / self.total_time) * 50
        return max(0, int(base_score - time_penalty))

    def run_challenge(self, challenge_idx):
        original_text, modified_text, difficulty = self.challenges[challenge_idx]
        
        # Create temporary files
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(modified_text)
            temp_filename = f.name

        # Display original text
        print("\nTarget Text (memorize this):")
        print("-" * 50)
        print(original_text)
        print("-" * 50)
        input("Press Enter to start editing (you'll have 60 seconds)...")
        
        # Clear screen
        os.system('clear' if os.name == 'posix' else 'cls')
        
        # Start timer
        start_time = datetime.now()
        
        # Open vim
        subprocess.call(['vim', temp_filename])
        
        # Calculate time taken
        time_taken = (datetime.now() - start_time).total_seconds()
        
        # Read result
        with open(temp_filename, 'r') as f:
            result = f.read()
        
        # Clean up
        os.unlink(temp_filename)
        
        # Check result
        is_correct = result.strip() == original_text.strip()
        score = self.calculate_score(time_taken, difficulty) if is_correct else 0
        
        # Update total score
        self.current_score += score
        
        return {
            'time_taken': time_taken,
            'is_correct': is_correct,
            'score': score
        }

    def display_results(self, result):
        print("\nResults:")
        print("-" * 50)
        print(f"Time taken: {result['time_taken']:.2f} seconds")
        print(f"Correct: {'Yes' if result['is_correct'] else 'No'}")
        print(f"Score for this round: {result['score']}")
        print(f"Total score: {self.current_score}")
        print("-" * 50)

    def play(self):
        print("Welcome to Vim Practice Game!")
        print("You'll be given text samples with errors.")
        print("Your task is to edit them to match the target text exactly.")
        print("You have 60 seconds for each challenge.")
        
        for i in range(len(self.challenges)):
            print(f"\nChallenge {i + 1}/{len(self.challenges)}")
            result = self.run_challenge(i)
            self.display_results(result)
            
            if i < len(self.challenges) - 1:
                input("\nPress Enter for next challenge...")
            
        print("\nGame Over!")
        print(f"Final Score: {self.current_score}")

if __name__ == "__main__":
    game = VimPracticeGame()
    game.play()
