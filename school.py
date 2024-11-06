import tkinter as tk
import random

class SnakeGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Snake Game")
        
        self.width = 400
        self.height = 400
        
        self.canvas = tk.Canvas(master, width=self.width, height=self.height, bg="black")
        self.canvas.pack()
        
        self.score = 0
        self.reset_game()
        
        self.master.bind("<KeyPress>", self.change_direction)
        self.game_loop()
        
    def reset_game(self):
        self.snake = [(20, 20), (20, 30), (20, 40)]
        self.snake_direction = "Down"
        self.food_position = self.place_food()
        
    def place_food(self):
        x = random.randint(0, (self.width // 10) - 1) * 10
        y = random.randint(0, (self.height // 10) - 1) * 10
        return (x, y)

    def change_direction(self, event):
        if event.keysym in ["Up", "Down", "Left", "Right"]:
            # Prevent reversing direction
            if (self.snake_direction == "Up" and event.keysym != "Down") or \
               (self.snake_direction == "Down" and event.keysym != "Up") or \
               (self.snake_direction == "Left" and event.keysym != "Right") or \
               (self.snake_direction == "Right" and event.keysym != "Left"):
                self.snake_direction = event.keysym

    def game_loop(self):
        self.update_snake()
        self.check_collisions()
        self.draw_elements()
        self.master.after(100, self.game_loop)

    def update_snake(self):
        head_x, head_y = self.snake[0]

        if self.snake_direction == "Up":
            head_y -= 10
        elif self.snake_direction == "Down":
            head_y += 10
        elif self.snake_direction == "Left":
            head_x -= 10
        elif self.snake_direction == "Right":
            head_x += 10

        self.snake.insert(0, (head_x, head_y))

        if (head_x, head_y) == self.food_position:
            self.food_position = self.place_food()
            self.score += 1
        else:
            self.snake.pop()

    def check_collisions(self):
        head_x, head_y = self.snake[0]

        # Check wall collisions
        if (head_x < 0 or head_x >= self.width or 
            head_y < 0 or head_y >= self.height):
            self.game_over()

        # Check self collisions
        if (head_x, head_y) in self.snake[1:]:
            self.game_over()

    def game_over(self):
        self.canvas.create_text(self.width // 2, self.height // 2, text="Game Over", fill="red", font=("Arial", 24))
        self.canvas.create_text(self.width // 2, self.height // 2 + 30, text=f"Score: {self.score}", fill="white", font=("Arial", 16))
        self.master.unbind("<KeyPress>")
        self.master.after(2000, self.reset_and_restart)  # Restart after 2 seconds

    def reset_and_restart(self):
        self.reset_game()
        self.canvas.delete(tk.ALL)
        self.score = 0
        self.master.bind("<KeyPress>", self.change_direction)
        self.game_loop()

    def draw_elements(self):
        self.canvas.delete(tk.ALL)
        
        # Draw snake
        for segment in self.snake:
            x, y = segment
            self.canvas.create_rectangle(x, y, x + 10, y + 10, fill="green")

        # Draw food
        food_x, food_y = self.food_position
        self.canvas.create_rectangle(food_x, food_y, food_x + 10, food_y + 10, fill="red")

        # Draw score
        self.canvas.create_text(50, 10, text=f"Score: {self.score}", fill="white", font=("Arial", 12))

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()

