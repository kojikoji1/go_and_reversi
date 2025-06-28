from go_types import Stone

class GoBoard:
    def __init__(self, size=19):
        self.size = size
        self.board = [[Stone.EMPTY for _ in range(size)] for _ in range(size)]
        self.previous_board = None  # コウ判定のために前の状態を保存
        self.captured_stones = {Stone.BLACK: 0, Stone.WHITE: 0}  # 取った石の数を管理
        self.pass_count = 0  # パスの回数を記録

    def place_stone(self, x, y, stone):
        if not (0 <= x < self.size and 0 <= y < self.size):
            return False  # 範囲外
        if self.board[y][x] != Stone.EMPTY:
            return False  # 既に石がある

        # 一時的に石を置いて呼吸点や自殺手を確認
        self.board[y][x] = stone
        if self.is_suicidal_move(x, y, stone):
            self.board[y][x] = Stone.EMPTY  # 無効な手なので戻す
            return False

        # 石を置いた後、相手の石を取り除く
        self.remove_dead_stones(Stone.BLACK if stone == Stone.WHITE else Stone.WHITE)

        # コウのチェック
        if self.is_ko_violation():
            self.board[y][x] = Stone.EMPTY  # 無効な手なので戻す
            return False

        # 前の状態を保存（コウ用）
        self.previous_board = [row[:] for row in self.board]
        self.pass_count = 0  # 石を置いたのでパス回数をリセット
        return True

    def pass_turn(self):
        """現在のプレイヤーがパスした場合の処理"""
        self.pass_count += 1

    def is_game_over(self):
        """ゲームが終了しているかを判定"""
        return self.pass_count >= 2  # 両者が連続でパスした場合、終了とする

    def get_legal_moves(self, color):
        """
        指定された色の合法手を取得。
        """
        legal_moves = []
        for y in range(self.size):
            for x in range(self.size):
                if self.board[y][x] == Stone.EMPTY:  # 空いている場所を確認
                    if self.is_legal_move(x, y, color):  # 合法手かを判定
                        legal_moves.append((x, y))
        return legal_moves

    def is_legal_move(self, x, y, color):
        """
        指定された位置に石を置けるか判定。
        """
        if self.board[y][x] != Stone.EMPTY:
            return False
        self.board[y][x] = color
        legal = not self.is_suicidal_move(x, y, color) and not self.is_ko_violation()
        self.board[y][x] = Stone.EMPTY
        return legal

    def get_liberties(self, x, y):
        """
        指定した石（またはグループ）の呼吸点を取得。
        """
        stone = self.board[y][x]
        visited = set()
        liberties = set()

        def dfs(cx, cy):
            if (cx, cy) in visited:
                return
            visited.add((cx, cy))

            for nx, ny in self.get_neighbors(cx, cy):
                if self.board[ny][nx] == Stone.EMPTY:
                    liberties.add((nx, ny))
                elif self.board[ny][nx] == stone:
                    dfs(nx, ny)

        dfs(x, y)
        return liberties

    def remove_dead_stones(self, stone):
        """
        囲まれた石を取り除き、取った石を「ごけ」に追加する。
        """
        to_remove = []
        for y in range(self.size):
            for x in range(self.size):
                if self.board[y][x] == stone and not self.get_liberties(x, y):
                    to_remove.append((x, y))

        for x, y in to_remove:
            self.board[y][x] = Stone.EMPTY
            self.captured_stones[stone] += 1

    def is_suicidal_move(self, x, y, stone):
        """
        自殺手かどうかを判定。
        """
        liberties = self.get_liberties(x, y)
        if liberties:
            return False  # 呼吸点があるなら自殺手ではない

        # 石を置いた後、敵の石を取れる場合も自殺手ではない
        opponent = Stone.BLACK if stone == Stone.WHITE else Stone.WHITE
        for nx, ny in self.get_neighbors(x, y):
            if self.board[ny][nx] == opponent and not self.get_liberties(nx, ny):
                return False

        return True

    def is_ko_violation(self):
        """
        コウの判定：現在の碁盤状態が前の状態と同じなら違反。
        """
        if not self.previous_board:
            return False
        return self.board == self.previous_board

    def get_neighbors(self, x, y):
        """
        指定座標の隣接点を取得。
        """
        neighbors = []
        if x > 0:
            neighbors.append((x - 1, y))
        if x < self.size - 1:
            neighbors.append((x + 1, y))
        if y > 0:
            neighbors.append((x, y - 1))
        if y < self.size - 1:
            neighbors.append((x, y + 1))
        return neighbors

    def count_territory(self):
        """
        碁盤上の地を数える。
        """
        visited = set()
        black_territory = 0
        white_territory = 0

        def dfs(x, y):
            stack = [(x, y)]
            territory = []
            surrounding_stones = set()

            while stack:
                cx, cy = stack.pop()
                if (cx, cy) in visited:
                    continue
                visited.add((cx, cy))
                territory.append((cx, cy))

                for nx, ny in self.get_neighbors(cx, cy):
                    if self.board[ny][nx] == Stone.EMPTY and (nx, ny) not in visited:
                        stack.append((nx, ny))
                    elif self.board[ny][nx] != Stone.EMPTY:
                        surrounding_stones.add(self.board[ny][nx])

            return territory, surrounding_stones

        for y in range(self.size):
            for x in range(self.size):
                if (x, y) not in visited and self.board[y][x] == Stone.EMPTY:
                    territory, surrounding_stones = dfs(x, y)
                    if len(surrounding_stones) == 1:
                        if Stone.BLACK in surrounding_stones:
                            black_territory += len(territory)
                        elif Stone.WHITE in surrounding_stones:
                            white_territory += len(territory)

        return black_territory, white_territory

    def copy(self):
        """
        現在の盤面をコピーして新しい GoBoard オブジェクトを返す。
        """
        new_board = GoBoard(size=self.size)
        new_board.board = [row[:] for row in self.board]
        new_board.previous_board = [row[:] for row in self.previous_board] if self.previous_board else None
        new_board.captured_stones = self.captured_stones.copy()
        new_board.pass_count = self.pass_count
        return new_board

    def display_board(self):
        """
        碁盤をコンソールに表示。
        """
        for row in self.board:
            print(" ".join(stone.name[0] for stone in row))
