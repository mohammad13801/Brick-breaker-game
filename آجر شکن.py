import tkinter as tk
import random

class BrickBreaker:
    def __init__(self, master):
        self.master = master
        self.master.title("بازی آجر شکن")

        # تنظیمات بازی
        self.canvas = tk.Canvas(master, width=600, height=400, bd=0, highlightthickness=0)
        self.canvas.pack()
        self.master.update()

        self.paddle = self.canvas.create_rectangle(0, 360, 100, 375, fill="blue")
        self.ball = self.canvas.create_oval(290, 240, 310, 260, fill="red")
        self.ball_x = 3
        self.ball_y = -3

        self.bricks = []
        self.create_bricks()

        self.canvas.bind_all("<KeyPress-Left>", self.move_paddle_left)
        self.canvas.bind_all("<KeyPress-Right>", self.move_paddle_right)

        self.update_game()

    def create_bricks(self):
        colors = ["green", "yellow", "orange", "purple", "pink"]
        for i in range(5):
            for j in range(10):
                x1 = j * 60 + 5
                y1 = i * 30 + 5
                x2 = x1 + 55
                y2 = y1 + 25
                brick = self.canvas.create_rectangle(x1, y1, x2, y2, fill=random.choice(colors))
                self.bricks.append(brick)

    def move_paddle_left(self, event):
        paddle_pos = self.canvas.coords(self.paddle)
        if paddle_pos[0] > 0:
            self.canvas.move(self.paddle, -20, 0)

    def move_paddle_right(self, event):
        paddle_pos = self.canvas.coords(self.paddle)
        if paddle_pos[2] < 600:
            self.canvas.move(self.paddle, 20, 0)

    def update_game(self):
        self.move_ball()
        self.check_collision()
        self.master.after(20, self.update_game)

    def move_ball(self):
        self.canvas.move(self.ball, self.ball_x, self.ball_y)
        ball_pos = self.canvas.coords(self.ball)

        # برخورد به دیوارهای کناری
        if ball_pos[0] <= 0 or ball_pos[2] >= 600:
            self.ball_x = -self.ball_x

        # برخورد به سقف
        if ball_pos[1] <= 0:
            self.ball_y = -self.ball_y

        # برخورد به پدال
        paddle_pos = self.canvas.coords(self.paddle)
        if ball_pos[3] >= paddle_pos[1] and ball_pos[2] >= paddle_pos[0] and ball_pos[0] <= paddle_pos[2]:
            self.ball_y = -self.ball_y

        # برخورد به کف (باخت)
        if ball_pos[3] >= 400:
            self.canvas.create_text(300, 200, text="Game Over", font=("Arial", 24), fill="red")
            self.canvas.unbind_all("<KeyPress-Left>")
            self.canvas.unbind_all("<KeyPress-Right>")
            return

    def check_collision(self):
        ball_pos = self.canvas.coords(self.ball)
        for brick in self.bricks:
            brick_pos = self.canvas.coords(brick)
            if ball_pos[2] >= brick_pos[0] and ball_pos[0] <= brick_pos[2]:
                if ball_pos[3] >= brick_pos[1] and ball_pos[1] <= brick_pos[3]:
                    self.canvas.delete(brick)
                    self.bricks.remove(brick)
                    self.ball_y = -self.ball_y
                    break

        if not self.bricks:
            self.canvas.create_text(300, 200, text="You Win!", font=("Arial", 24), fill="green")
            self.canvas.unbind_all("<KeyPress-Left>")
            self.canvas.unbind_all("<KeyPress-Right>")
            return

if __name__ == '__main__':
    root = tk.Tk()
    game = BrickBreaker(root)
    root.mainloop()