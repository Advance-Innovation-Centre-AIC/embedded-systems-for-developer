# mygame_skeleton.py — โครงเกมเปล่า ๆ ที่ "รันได้เลย" สำหรับคาบ MVP Clinic (คาบ 11)
#
# เป้าหมาย: เปิดมาแล้วมี "ผู้เล่น 1 ตัว" ขยับได้ด้วย joystick + มี score บนจอ +
#           กด Start เพื่อจบเกม. ยังไม่ต้องสนุก — แค่ "วิ่งได้" เป็นฐานให้กลุ่มไปต่อ.
#
# วิธีรันบนบอร์ด (REPL):
#     exec(open("mygame_skeleton.py").read())
#
# ทุก API ในไฟล์นี้มีจริงใน starter/bentogame.py (Box, Text, keys, hit, run, sfx,
# Sprite, tilt, connect, post_score). ก๊อปไฟล์นี้ตั้งชื่อใหม่ (เช่น our_game.py)
# แล้วเปลี่ยนสี/ความเร็ว/กติกาเป็นของกลุ่มคุณ.
#
# กฎทอง: เริ่มจากโครงนี้ก่อน → รันให้เห็นกล่องขยับ → แล้วค่อยเติมทีละ Issue.

import bentogame as game

# --- ตั้งค่าเกม (แก้ตรงนี้ก่อนเป็นอันดับแรก) --------------------------------
PLAYER_SPEED = 8          # ขยับทีละกี่พิกเซลต่อเฟรม
PLAYER_COLOR = game.GREEN # ลองเปลี่ยนเป็น game.CYAN / game.PINK ดู
FPS = 30                  # ความถี่ของ loop

# --- เริ่มเกม (ต้องเรียกก่อนสร้าง Box/Text/Sprite เสมอ) --------------------
game.start()

score = 0

# ผู้เล่น: เริ่มจาก Box ก่อน — คาบหน้าค่อยเปลี่ยนเป็น game.Sprite("ship", ...)
player = game.Box(380, 350, 30, 30, PLAYER_COLOR)

# ป้ายคะแนนมุมซ้ายบน
label = game.Text("Score: 0", 10, 10, game.WHITE)


def update():
    """ถูกเรียกทุกเฟรม. return False = จบเกม."""
    global score

    # 1) อ่าน input  (อยากคุมด้วยการเอียงบอร์ดแทน? เปลี่ยนเป็น game.tilt())
    k = game.keys()
    if k.left:
        player.move(-PLAYER_SPEED, 0)
    if k.right:
        player.move(PLAYER_SPEED, 0)
    if k.up:
        player.move(0, -PLAYER_SPEED)
    if k.down:
        player.move(0, PLAYER_SPEED)

    # 2) กด Start = จบเกม
    if k.start:
        return False

    # --- TODO (Issue #2) gameplay: สร้างศัตรู/ของ + game.hit() + คะแนน -------
    #     ตัวอย่าง (ลบคอมเมนต์ออกเมื่อพร้อม):
    #     if game.hit(player, food):
    #         score += 1
    #         label.set("Score: %d" % score)
    #         game.sfx("point")
    #         food.move_to(random_x(), random_y())

    # --- TODO (Issue #3) polish: เปลี่ยน Box -> game.Sprite + เสียงตอนจบ -----
    #     player = game.Sprite("ship", 380, 350)   # (สร้างครั้งเดียวตอนเริ่ม)
    #     game.sfx("gameover")                       # ตอน game over

    # --- TODO (เสริม) ส่งคะแนนขึ้น leaderboard ห้อง (เลือกสาย IoT เท่านั้น) --
    #     วาง game.connect(...) ครั้งเดียว "นอก" update() ตอนเริ่มเกม
    #     game.post_score(score, team="team1", game="ourgame")  # ตอน game over

    return True  # เล่นต่อ


# --- วน loop จนกว่าจะ return False -----------------------------------------
game.run(update, fps=FPS)
