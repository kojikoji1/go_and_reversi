import tkinter

BLACK = 1
WHITE = 2
mx = 0
my = 0
mc = 0
turn = 0
msg = ""
board = [
 [0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 2, 1, 0, 0, 0],
 [0, 0, 0, 1, 2, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0]
]

def click(e):
    global mx, my, mc, turn
    mc = 1
    mx = int(e.x/80)
    my = int(e.y/80)
    if mx > 7: mx = 7
    if my > 7: my = 7
    if turn == 0 and kaeseru(mx, my, BLACK) > 0:
        ishi_utsu(mx, my, BLACK)
        turn = 1
    elif turn == 1 and kaeseru(mx, my, WHITE) > 0:
        ishi_utsu(mx, my, WHITE)
        turn = 0

def banmen():
    cvs.delete("all")
    cvs.create_text(320, 670, text=msg, fill="silver")
    for y in range(8):
        for x in range(8):
            X = x*80
            Y = y*80
            cvs.create_rectangle(X, Y, X+80, Y+80, outline="black")
            if board[y][x] == BLACK:
                cvs.create_oval(X+10, Y+10, X+70, Y+70, fill="black", width=0)
            if board[y][x] == WHITE:
                cvs.create_oval(X+10, Y+10, X+70, Y+70, fill="white", width=0)
    cvs.update()

def ishi_utsu(x, y, iro):
    board[y][x] = iro
    for dy in range(-1, 2):
        for dx in range(-1, 2):
            k = 0
            sx = x
            sy = y
            while True:
                sx += dx
                sy += dy
                if sx < 0 or sx > 7 or sy < 0 or sy > 7:
                    break
                if board[sy][sx] == 0:
                    break
                if board[sy][sx] == 3-iro:
                    k += 1
                if board[sy][sx] == iro:
                    for i in range(k):
                        sx -= dx
                        sy -= dy
                        board[sy][sx] = iro
                    break

def kaeseru(x, y, iro):
    if board[y][x] > 0:
        return -1
    total = 0
    for dy in range(-1, 2):
        for dx in range(-1, 2):
            k = 0
            sx = x
            sy = y
            while True:
                sx += dx
                sy += dy
                if sx < 0 or sx > 7 or sy < 0 or sy > 7:
                    break
                if board[sy][sx] == 0:
                    break
                if board[sy][sx] == 3-iro:
                    k += 1
                if board[sy][sx] == iro:
                    total += k
                    break
    return total

def uteru_masu(iro):
    for y in range(8):
        for x in range(8):
            if kaeseru(x, y, iro) > 0:
                return True
    return False

def main():
    global mc, turn, msg
    banmen()
    if mc == 1:
        mc = 0
        if uteru_masu(BLACK) == False and uteru_masu(WHITE) == False:
            msg = "どちらも打てないので終了です"
        elif turn == 0 and uteru_masu(BLACK) == False:
            msg = "プレイヤー1は打てないのでパス"
            turn = 1
        elif turn == 1 and uteru_masu(WHITE) == False:
            msg = "プレイヤー2は打てないのでパス"
            turn = 0
        else:
            msg = "プレイヤー{}の番です".format(turn+1)
    root.after(100, main)

root = tkinter.Tk()
root.title("リバーシ")
root.resizable(False, False)
root.bind("<Button>", click)
cvs = tkinter.Canvas(width=640, height=700, bg="green")
cvs.pack()
root.after(100, main)
root.mainloop()