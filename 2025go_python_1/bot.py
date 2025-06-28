import random
from go_types import Stone

class RandomBot:
    """ランダムボット: 合法手の中からランダムに選ぶ。"""
    def __init__(self, color):
        self.color = color

    def select_move(self, board):
        legal_moves = board.get_legal_moves(self.color)
        return random.choice(legal_moves) if legal_moves else None


import random

import random

class MonteCarloBot:
    """モンテカルロボット: 終局まで進めるシミュレーションを実施"""
    def __init__(self, color, simulations=10):
        self.color = color
        self.simulations = simulations  # シミュレーション回数をデバッグ用に少なく設定

    def select_move(self, board):
        """次の一手を選択"""
        print(f"[MonteCarloBot] シミュレーションを開始 ({self.simulations} 回)")

        legal_moves = board.get_legal_moves(self.color)
        if not legal_moves:
            print("[MonteCarloBot] 合法手がないためパスします。")
            return None

        best_move = None
        best_score = -float('inf')

        for move in legal_moves:
            print(f"[MonteCarloBot] 手 {move} を評価中...")
            score = self.simulate_move(board, move)
            print(f"[MonteCarloBot] 手 {move} のスコア: {score}")
            if score > best_score:
                best_score = score
                best_move = move

        print(f"[MonteCarloBot] 選択した手: {best_move} (スコア: {best_score})")
        return best_move

    def simulate_move(self, board, move):
        """指定された手でシミュレーション"""
        print(f"[MonteCarloBot] シミュレーションを開始: 手 {move}")
        wins = 0
        for i in range(self.simulations):
            simulated_board = board.copy()
            simulated_board.place_stone(*move, self.color)
            print(f"[MonteCarloBot] シミュレーション {i + 1}/{self.simulations}: ランダムプレイアウト開始")
            if self.random_playout(simulated_board):
                wins += 1
            print(f"[MonteCarloBot] シミュレーション {i + 1}/{self.simulations}: 結果 = {'勝利' if wins > 0 else '敗北'}")
        return wins / self.simulations

    def random_playout(self, board):
       """終局までランダムに進め、勝敗を判定"""
       current_turn = self.color
       print("[MonteCarloBot] ランダムプレイアウト開始")
       turn_count = 0  # デバッグ用の手数カウンタ

       while not board.is_game_over():
        turn_count += 1
        if turn_count > 1000:  # 手数制限を設けて無限ループを防止
            print("[MonteCarloBot] 手数が1000手を超えたため、強制終了します。")
            break

        legal_moves = board.get_legal_moves(current_turn)
        if legal_moves:
            move = random.choice(legal_moves)
            print(f"[MonteCarloBot] ランダムプレイアウト: {current_turn} が {move} に置きます")
            board.place_stone(*move, current_turn)
        else:
            print(f"[MonteCarloBot] {current_turn} はパスします")
            board.pass_turn()
        current_turn = Stone.BLACK if current_turn == Stone.WHITE else Stone.WHITE

        print(f"[MonteCarloBot] ランダムプレイアウト終了: {turn_count} 手で終了しました。")
        black_territory, white_territory = board.count_territory()
        black_score = black_territory + board.captured_stones[Stone.BLACK]
        white_score = white_territory + board.captured_stones[Stone.WHITE]

        print(f"[MonteCarloBot] 黒: {black_score}, 白: {white_score}")
        if self.color == Stone.BLACK:
           return black_score > white_score
        else:
           return white_score > black_score

            
class MiniGoBot:
    """MiniGoベースのAI。"""
    def __init__(self, color, model_path="minigo_model.h5"):
        self.color = color
        self.model = self.load_model(model_path)

    def load_model(self, model_path):
        """MiniGo モデルをロード。"""
        from tensorflow.keras.models import load_model
        return load_model(model_path)

    def select_move(self, board):
        """MiniGo モデルを使って最善手を予測。"""
        legal_moves = board.get_legal_moves(self.color)
        if not legal_moves:
            return None

        # 入力データを準備
        board_state = self.prepare_input(board)
        predictions = self.model.predict(board_state)

        # 合法手の中から最もスコアが高い手を選ぶ
        best_move = max(legal_moves, key=lambda move: predictions[0][self.encode_move(move)])
        return best_move

    def prepare_input(self, board):
        """MiniGo に適した入力形式を準備。"""
        # 簡易例: 実際の MiniGo 入力形式に合わせて実装
        import numpy as np
        return np.array(board.board).reshape(1, board.size, board.size, 1)

    def encode_move(self, move):
        """座標 (x, y) をモデルの出力インデックスに変換。"""
        x, y = move
        return y * 19 + x  # 例: 19x19 の座標系