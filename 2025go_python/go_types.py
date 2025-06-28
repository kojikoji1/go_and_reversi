from enum import Enum

class Stone(Enum):
    """
    囲碁の石の状態を表すEnumクラス。
    - EMPTY: 空点
    - BLACK: 黒石
    - WHITE: 白石
    """
    EMPTY = 0
    BLACK = 1
    WHITE = 2

class Player(Enum):
    """
    プレイヤーを表すEnumクラス。
    - HUMAN: 人間プレイヤー
    - BOT: ボットプレイヤー（将来用）
    """
    HUMAN = "human"
    BOT = "bot"

class GameMode(Enum):
    """
    ゲームモードを表すEnumクラス。
    - HUMAN_VS_HUMAN: 人対人の対局
    - HUMAN_VS_BOT: 人対ボットの対局（将来用）
    """
    HUMAN_VS_HUMAN = "human_vs_human"
    HUMAN_VS_BOT = "human_vs_bot"