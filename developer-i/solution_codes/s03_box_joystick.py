# s03_box_joystick.py  (คาบ 3)
# Hello hardware: สี่เหลี่ยม (Box) ที่ขยับตามจอย และไม่หลุดจอ
#
# นี่คือ "win แรก" ของคอร์ส: เราคุมของบนจอได้ด้วยมือ
# ทักษะ 4 อย่างที่ใช้ซ้ำทุกเกม:  start() · Box · keys() · run()
#
# วิธีรัน: เปิดไฟล์นี้ใน BENTO IDE แล้วกดปุ่ม Program to Device
# หรือเซฟเป็น main.py แล้วรีเซ็ตบอร์ด
# กด Back บนจอยเพื่อออกกลับ Playground · กด Start เพื่อเริ่มเกมใหม่

import bentogame as game

game.title("MOVE BOX")                        # หน้าเริ่ม: Start=เล่น Back=ออก (ทำ start ให้ในตัว)

# สร้างสี่เหลี่ยมตัวแรก: x, y, กว้าง, สูง, สี
hero = game.Box(380, 180, 40, 40, game.CYAN)

BASE_SPEED = 6      # ความเร็วเริ่มต้น (พิกเซลต่อเฟรม) ตอนเพิ่งแตะจอย
MAX_SPEED  = 30     # ความเร็วสูงสุดเมื่อกดค้างนานพอ
hold_frames = 0     # กดค้างมากี่เฟรมแล้ว (ยิ่งมาก ยิ่งเร็ว)


def update():
    global hold_frames
    pressed = game.keys()                       # อ่านจอยเฟรมนี้

    moving = pressed.left or pressed.right or pressed.up or pressed.down
    if moving:
        hold_frames += 1                        # กดค้าง → สะสมขึ้นเรื่อย ๆ
    else:
        hold_frames = 0                         # ปล่อยจอย → รีเซ็ตกลับช้า

    # ยิ่งกดค้างนาน speed ยิ่งมากขึ้น แต่ไม่เกิน MAX_SPEED
    speed = min(BASE_SPEED + hold_frames, MAX_SPEED)

    if pressed.left:  hero.move(-speed, 0)      # ซ้าย
    if pressed.right: hero.move(speed, 0)       # ขวา
    if pressed.up:    hero.move(0, -speed)      # ขึ้น
    if pressed.down:  hero.move(0, speed)       # ลง
    # Back = ออกกลับ Playground · Start = เริ่มเกมใหม่ — game.run() จัดการให้ก่อนถึง update()
    # game.Box.move() กัน "หลุดจอ" ให้อัตโนมัติ (clamp ขอบ)


game.run(update)                    # วิ่งทุกเฟรมจนกว่าจะ return False
