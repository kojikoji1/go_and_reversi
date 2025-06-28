import tkinter as tk
from go_types import Stone
from go_board import GoBoard
from bot import RandomBot, MonteCarloBot, MiniGoBot


class GoGameApp:
    def __init__(self, root):
        self.root = root
        self.stage = 1  # 現在のステージ
        self.board = None
        self.current_turn = None
        self.player1 = None
        self.player2 = None
        self.history = []  # 手の履歴を保存

        self.board_size_var = tk.IntVar(value=9)
        self.first_player_var = tk.StringVar(value="human")
        self.second_player_var = tk.StringVar(value="random")

        self.setup_stage1()

    def setup_stage1(self):
        """ステージ1: 設定画面"""
        self.clear_frame()

        self.setup_frame = tk.Frame(self.root)
        self.setup_frame.pack()

        tk.Label(self.setup_frame, text="碁盤サイズ:").pack()
        tk.Radiobutton(self.setup_frame, text="9路盤", variable=self.board_size_var, value=9).pack()
        tk.Radiobutton(self.setup_frame, text="19路盤", variable=self.board_size_var, value=19).pack()

        tk.Label(self.setup_frame, text="先手プレイヤー:").pack()
        tk.OptionMenu(self.setup_frame, self.first_player_var, "human", "random", "montecarlo", "minigo").pack()

        tk.Label(self.setup_frame, text="後手プレイヤー:").pack()
        tk.OptionMenu(self.setup_frame, self.second_player_var, "human", "random", "montecarlo", "minigo").pack()

        tk.Button(self.setup_frame, text="開始", command=self.start_stage2).pack()

    def start_stage2(self):
        """ステージ2: 対局画面"""
        self.clear_frame()

        self.board = GoBoard(size=self.board_size_var.get())
        self.current_turn = Stone.BLACK
        self.history = []  # 履歴を初期化

        # プレイヤーの設定
        self.player1 = self.get_player(self.first_player_var.get(), Stone.BLACK)
        self.player2 = self.get_player(self.second_player_var.get(), Stone.WHITE)

        canvas_width = self.board.size * 40 + 200
        canvas_height = self.board.size * 40 + 50
        self.canvas = tk.Canvas(self.root, width=canvas_width, height=canvas_height, bg="tan")
        self.canvas.pack()

        self.canvas.bind("<Button-1>", self.handle_click)
        self.draw_grid()
        self.redraw_board()

        tk.Button(self.root, text="終局", command=self.start_stage3).pack()
        tk.Button(self.root, text="待った", command=self.undo_move).pack()

        self.bot_play_if_needed()

    def get_player(self, player_type, color):
        """プレイヤー（人間またはボット）を設定"""
        if player_type == "human":
            return "human"
        elif player_type == "random":
            return RandomBot(color)
        elif player_type == "montecarlo":
            return MonteCarloBot(color)
        elif player_type == "minigo":
            return MiniGoBot(color)

    def undo_move(self):
        """「待った」を実行"""
        if len(self.history) >= 2:
            self.history.pop()  # 最後の手（白または黒）
            self.history.pop()  # その前の手

            if self.history:
                # 履歴から盤面とターンを復元
                last_state = self.history[-1]
                self.board.board = [row[:] for row in last_state['board']]
                self.current_turn = last_state['turn']  # 待った人から再開
            else:
                # 履歴が空の場合は初期状態に戻す
                self.board.board = [[Stone.EMPTY for _ in range(self.board.size)] for _ in range(self.board.size)]
                self.current_turn = Stone.BLACK

            self.redraw_board()
            self.bot_play_if_needed()  # ボットの手番が再開直後なら実行
        else:
            print("待ったできません：履歴がありません。")


    def save_to_history(self):
        """現在の状態を履歴に保存"""
        self.history.append({
            'board': [row[:] for row in self.board.board],
            'turn': self.current_turn
        })

    def handle_click(self, event):
        """クリック時の処理"""
        x = int((event.x - 20) // 40)
        y = int((event.y - 20) // 40)
        if 0 <= x < self.board.size and 0 <= y < self.board.size:
            if self.board.place_stone(x, y, self.current_turn):
                self.save_to_history()  # 手を履歴に保存
                self.redraw_board()
                self.switch_turn()
                self.bot_play_if_needed()

    def bot_play_if_needed(self):
        current_player = self.player1 if self.current_turn == Stone.BLACK else self.player2
        if isinstance(current_player, (RandomBot, MonteCarloBot, MiniGoBot)):
            bot_move = current_player.select_move(self.board)
            if bot_move:
                x, y = bot_move
                self.board.place_stone(x, y, self.current_turn)
                self.save_to_history()  # 手を履歴に保存
                self.redraw_board()
                self.switch_turn()
                self.bot_play_if_needed()

    def switch_turn(self):
        """ターンを切り替える"""
        self.current_turn = Stone.BLACK if self.current_turn == Stone.WHITE else Stone.WHITE

    def start_stage3(self):
        """ステージ3: ダメ整理"""
        self.clear_frame()

        tk.Label(self.root, text="ステージ3: ダメ整理").pack()
        tk.Label(self.root, text="ダメを手動で埋めてください。").pack()

        canvas_width = self.board.size * 40 + 200
        canvas_height = self.board.size * 40 + 50
        self.canvas = tk.Canvas(self.root, width=canvas_width, height=canvas_height, bg="tan")
        self.canvas.pack()

        self.canvas.bind("<Button-1>", self.handle_dame_click)
        self.draw_grid()
        self.redraw_board()

        tk.Button(self.root, text="黒地整理へ", command=self.start_stage4).pack()

    def start_stage4(self):
        """ステージ4: 黒地整理"""
        self.clear_frame()

        tk.Label(self.root, text="ステージ4: 黒地整理").pack()
        tk.Label(self.root, text="自陣にある死んだ白石を取り除いてください。").pack()

        canvas_width = self.board.size * 40 + 200
        canvas_height = self.board.size * 40 + 50
        self.canvas = tk.Canvas(self.root, width=canvas_width, height=canvas_height, bg="tan")
        self.canvas.pack()

        self.canvas.bind("<Button-1>", self.handle_black_cleanup_click)
        self.draw_grid()
        self.redraw_board()

        tk.Button(self.root, text="白地整理へ", command=self.start_stage5).pack()

    def start_stage5(self):
        """ステージ5: 白地整理"""
        self.clear_frame()

        tk.Label(self.root, text="ステージ5: 白地整理").pack()
        tk.Label(self.root, text="自陣にある死んだ黒石を取り除いてください。").pack()

        canvas_width = self.board.size * 40 + 200
        canvas_height = self.board.size * 40 + 50
        self.canvas = tk.Canvas(self.root, width=canvas_width, height=canvas_height, bg="tan")
        self.canvas.pack()

        self.canvas.bind("<Button-1>", self.handle_white_cleanup_click)
        self.draw_grid()
        self.redraw_board()

        tk.Button(self.root, text="勝敗決定", command=self.start_stage6).pack()

    def start_stage6(self):
        """ステージ6: 勝敗決定"""
        self.clear_frame()

        tk.Label(self.root, text="ステージ6: 勝敗決定").pack()

        black_territory, white_territory = self.board.count_territory()

        # 捕獲された石の数を地から引く
        black_score = black_territory - self.board.captured_stones[Stone.BLACK]
        white_score = white_territory - self.board.captured_stones[Stone.WHITE]

        result_text = f"黒の地: {black_territory} - 捕獲された石: {self.board.captured_stones[Stone.BLACK]} = {black_score}\n"
        result_text += f"白の地: {white_territory} - 捕獲された石: {self.board.captured_stones[Stone.WHITE]} = {white_score}\n"

        if black_score > white_score:
            result_text += "黒の勝ち！"
        elif white_score > black_score:
            result_text += "白の勝ち！"
        else:
            result_text += "引き分け！"

        tk.Label(self.root, text=result_text, font=("Arial", 14)).pack()

    def draw_grid(self):
        """碁盤の目を描画"""
        for i in range(self.board.size):
            self.canvas.create_line(40, (i + 1) * 40, self.board.size * 40, (i + 1) * 40)
            self.canvas.create_line((i + 1) * 40, 40, (i + 1) * 40, self.board.size * 40)

    def redraw_board(self):
        """碁盤を再描画"""
        self.canvas.delete("all")
        self.draw_grid()
        self.draw_goke()
        for y in range(self.board.size):
            for x in range(self.board.size):
                stone = self.board.board[y][x]
                if stone != Stone.EMPTY:
                    self.draw_stone(x, y, stone)

    def draw_stone(self, x, y, stone):
        """石を描画"""
        cx = (x + 1) * 40
        cy = (y + 1) * 40
        r = 15
        color = "black" if stone == Stone.BLACK else "white"
        self.canvas.create_oval(cx - r, cy - r, cx + r, cy + r, fill=color)

    def draw_goke(self):
        """捕獲石の表示"""
        offset_x = self.board.size * 40 + 20
        self.canvas.create_text(offset_x, 50, text="ごけ", font=("Arial", 14), anchor="w")
        self.canvas.create_text(offset_x, 100, text=f"黒: {self.board.captured_stones[Stone.WHITE]}", font=("Arial", 12), anchor="w")
        self.canvas.create_text(offset_x, 130, text=f"白: {self.board.captured_stones[Stone.BLACK]}", font=("Arial", 12), anchor="w")

    def handle_black_cleanup_click(self, event):
        """黒地整理中のクリック処理"""
        x = int((event.x - 20) // 40)
        y = int((event.y - 20) // 40)
        if 0 <= x < self.board.size and 0 <= y < self.board.size:
            if self.board.board[y][x] == Stone.WHITE:
                self.board.board[y][x] = Stone.EMPTY
                self.board.captured_stones[Stone.WHITE] += 1
                self.redraw_board()

    def handle_white_cleanup_click(self, event):
        """白地整理中のクリック処理"""
        x = int((event.x - 20) // 40)
        y = int((event.y - 20) // 40)
        if 0 <= x < self.board.size and 0 <= y < self.board.size:
            if self.board.board[y][x] == Stone.BLACK:
                self.board.board[y][x] = Stone.EMPTY
                self.board.captured_stones[Stone.BLACK] += 1
                self.redraw_board()

    def handle_dame_click(self, event):
        """ダメ整理中のクリック処理"""
        x = int((event.x - 20) // 40)
        y = int((event.y - 20) // 40)
        if 0 <= x < self.board.size and 0 <= y < self.board.size:
            if self.board.board[y][x] == Stone.EMPTY:
                self.board.place_stone(x, y, self.current_turn)
                self.redraw_board()

    def clear_frame(self):
        """現在のフレームを削除"""
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("囲碁ゲーム")
    app = GoGameApp(root)
    root.mainloop()
