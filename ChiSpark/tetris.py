# テトリスもどき（Replitのコンソールで動作する）
# 左/右/下: 移動
# （半角）スペース: 回転

import curses
import random
import time


def main(stdscr):
    stdscr.clear()
    stdscr.nodelay(True)
    w = 12  # 幅
    h = 20  # 高さ
    b = []  # 落ちているブロック
    z = [0] * (w * h)  # 確定ブロック
    for i in range(w * h):
        if i % w == 0 or i % w == w - 1 or i // w == h - 1:
            z[i] = 1
    p = e = t = s = 0  # 落ちているブロックの位置、タイミング、テトロミノ番号、得点

    while True:
        t0 = time.time()

        # 落ちる処理
        e += 1
        if e == 4:
            e = 0
            p1 = p + w
            if b and not any(z[p1 + i] for i in b):
                p = p1

        # キー入力の処理
        k = stdscr.getch()
        while stdscr.getch() != -1:
            pass
        if k == ord(" ") and t != 0:
            # 時計回りに回転
            b1 = []
            for i in b:
                iy = round(i / w)
                ix = i - w * iy
                b1 += [-iy + ix * w]
            p1 = p
        elif k == curses.KEY_LEFT:
            b1 = b
            p1 = p - 1
        elif k == curses.KEY_RIGHT:
            b1 = b
            p1 = p + 1
        elif k == curses.KEY_DOWN:
            b1 = b
            p1 = p + w
        else:
            b1 = None
        if b1 and not any(z[p1 + i] for i in b1):
            b = b1
            p = p1

        # 確定ブロック+落ちているブロック
        x = z.copy()
        for i in b:
            x[p + i] = 1

        # 接地判定
        if b and any(z[p + i + w] for i in b):
            z = x
            b = []
            # 消去判定
            for j in range(h - 2, -1, -1):
                while True:
                    if all(z[i + j * w] for i in range(1, w - 1)):
                        z[w : (j + 1) * w] = z[0 : j * w]
                        z[1 : w - 1] = [0] * (w - 2)
                        s += 1
                    else:
                        break

        # 新しいブロック
        if not b:
            t = random.randint(0, 6)
            b = [
                [-w + 1, -w * 2, 2, w + 1, -w - 1, -1, -1][t],
                0,
                1,
                2 if t == 6 else -w,
            ]
            p = w + w // 2 - 1

        # 描画
        for j in range(h):
            for i in range(w):
                stdscr.addstr(j, i * 2, "[]" if x[i + j * w] else "  ")
        stdscr.addstr(h, 0, f"SCORE: {s}")

        # ゲームオーバー判定
        if z[w // 2 - 1]:
            stdscr.addstr(h // 2 - 2, w - 5, "GAME OVER")
            stdscr.refresh()
            time.sleep(2)
            break

        # スリープ処理
        dt = time.time() - t0
        time.sleep(max(0.1 - dt, 0.01))

    # 終了画面
    r = []
    for j in range(h):
        l = ""
        for i in range(w):
            l += "[]" if x[i + j * w] else "  "
        r += [l]
    r += [f"SCORE: {s}"]

    return "\n".join(r)


print(curses.wrapper(main))