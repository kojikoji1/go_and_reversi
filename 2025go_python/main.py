import tkinter as tk
from go_types import Stone
from go_board import GoBoard

class GoGameGUI:
    def __init__(self, root, board_size=9):
        self.root = root
        self.board_size = board_size
        self.board = GoBoard(size=board_size)
        self.current_turn = Stone.BLACK
        self.cell_size = 30  # セルの大きさ（ピクセル）

        # キャンバスの設定
        canvas_width = board_size * self.cell_size + 100  # 右側に「ごけ」のスペースを追加
        canvas_height = board_size * self.cell_size
        self.canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="tan")
        self.canvas.pack()

        self.canvas.bind("<Button-1>", self.handle_click)
        self.draw_grid()
        self.draw_goke()  # 「ごけ」を描画

    def draw_grid(self):
        """碁盤の目を描画"""
        for i in range(self.board_size):
            self.canvas.create_line(self.cell_size // 2, (i + 0.5) * self.cell_size,
                                     self.board_size * self.cell_size - self.cell_size // 2, (i + 0.5) * self.cell_size)
            self.canvas.create_line((i + 0.5) * self.cell_size, self.cell_size // 2,
                                     (i + 0.5) * self.cell_size, self.board_size * self.cell_size - self.cell_size // 2)

    def handle_click(self, event):
        """クリック処理"""
        x = int(event.x // self.cell_size)
        y = int(event.y // self.cell_size)

        if self.board.place_stone(x, y, self.current_turn):
            self.redraw_board()  # 碁盤を再描画
            self.current_turn = Stone.BLACK if self.current_turn == Stone.WHITE else Stone.WHITE

    def redraw_board(self):
        """碁盤全体を再描画"""
        self.canvas.delete("all")  # 現在の描画をクリア
        self.draw_grid()  # 碁盤の目を再描画
        self.draw_goke()  # 「ごけ」を再描画

        for y in range(self.board_size):
            for x in range(self.board_size):
                stone = self.board.board[y][x]
                if stone != Stone.EMPTY:
                    self.draw_stone(x, y, stone)

    def draw_stone(self, x, y, stone):
        """石を描画"""
        x0 = x * self.cell_size + self.cell_size // 4
        y0 = y * self.cell_size + self.cell_size // 4
        x1 = (x + 1) * self.cell_size - self.cell_size // 4
        y1 = (y + 1) * self.cell_size - self.cell_size // 4

        color = "black" if stone == Stone.BLACK else "white"
        self.canvas.create_oval(x0, y0, x1, y1, fill=color)

    def draw_goke(self):
        """取った石（ごけ）を描画"""
        self.canvas.create_text(self.board_size * self.cell_size + 20, 50, text="ごけ", font=("Arial", 14), anchor="w")
        self.update_goke_display()

    def update_goke_display(self):
        """「ごけ」の石の数を更新"""
        # 黒のごけ
        self.canvas.create_text(self.board_size * self.cell_size + 20, 100,
                                 text=f"黒: {self.board.captured_stones[Stone.WHITE]}",
                                 font=("Arial", 12), anchor="w")
        # 白のごけ
        self.canvas.create_text(self.board_size * self.cell_size + 20, 130,
                                 text=f"白: {self.board.captured_stones[Stone.BLACK]}",
                                 font=("Arial", 12), anchor="w")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("囲碁ゲーム（人対人）")
    app = GoGameGUI(root)
    root.mainloop()