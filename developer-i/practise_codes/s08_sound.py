# s08_sound.py (ฉบับฝึก) — เสียงเกมบน PSoC Edge (คาบ 8)
# เราจะทำ 2 เรื่อง: (1) เล่น sfx สำเร็จรูปตาม id, (2) ต่อโน้ตเป็นทำนองสั้น ๆ ด้วย tone
#
# วิธีรัน: เปิดไฟล์นี้ใน BENTO IDE แล้วกด Program to Device
#
# แนวคิดที่อยากให้เห็น:
#  - บอร์ดสร้างเสียงด้วย PWM (เปิด-ปิดขาเร็ว ๆ) แล้วเลือก "รูปคลื่น" (waveform)
#    SQUARE = สี่เหลี่ยม เสียงกระด้างแบบเกม 8-bit, SINE = นุ่ม, TRIANGLE/SAW = ก้ำกึ่ง
#  - โน้ตใช้เลข MIDI: 60 = โดกลาง (C4), ขึ้นทีละ 1 = ครึ่งเสียง, +12 = สูงขึ้น 1 ออกเทฟ
#  - velocity = ความดัง (0-127), ms = ความยาวเสียงเป็นมิลลิวินาที

import ui
import time

# --- ส่วนที่ 1: เสียงสำเร็จรูป (sfx) เรียกด้วย id ที่บอร์ดเตรียมไว้ให้ ---
print("เล่น sfx: เริ่มเกม")
# เติม (1): เล่นเสียงเริ่มเกม ด้วย ui.sfx(ui.SFX_UI_START)
pass
time.sleep_ms(600)

print("เล่น sfx: กินอาหาร (snake)")
# เติม (2): เล่นเสียงกินอาหารของ snake ด้วย ui.sfx(ui.SFX_SNAKE_EAT)
pass
time.sleep_ms(400)

print("เล่น sfx: เกมจบ")
ui.sfx(ui.SFX_GAME_OVER)            # ตัวอย่างที่ทำให้ดู: เสียงเกมจบ
time.sleep_ms(900)

# --- ส่วนที่ 2: แต่งทำนองเองด้วย tone ---
# ui.tone(note, wave, velocity, ms) — เล่นทีละโน้ต เราหน่วงเวลาเองให้โน้ตไม่ทับกัน
melody = [60, 62, 64, 65, 67]      # เลข MIDI ของแต่ละโน้ต (โด เร มี ฟา ซอล)
NOTE_MS = 200                      # โน้ตละ 200 ms

print("เล่นทำนองด้วย WAVE_SQUARE (เสียงเกมคลาสสิก)")
for note in melody:
    # เติม (3): เล่นโน้ตปัจจุบันด้วย ui.tone(note, ui.WAVE_SQUARE, 100, NOTE_MS)
    pass
    time.sleep_ms(NOTE_MS + 20)    # +20 ms กันโน้ตเกยกัน ฟังเป็นจังหวะ

time.sleep_ms(300)

# ลองเปลี่ยน "รูปคลื่น" แล้วฟังว่าน้ำเสียงต่างกันอย่างไร (โน้ตเดิมทั้งหมด)
print("เล่นทำนองเดิมด้วย WAVE_SINE (เสียงนุ่มขึ้น)")
for note in melody:
    # เติม (4): เล่นโน้ตเดิมแต่เปลี่ยนรูปคลื่นเป็น ui.WAVE_SINE
    #          ด้วย ui.tone(note, ui.WAVE_SINE, 100, NOTE_MS)
    pass
    time.sleep_ms(NOTE_MS + 20)

print("จบแล็บเสียง — ลองแก้ melody / wave / NOTE_MS ดูว่าผลลัพธ์เปลี่ยนยังไง")

# --- เมนูเสียงสำเร็จรูปทั้งหมด 21 เสียง (หยิบไปใส่เกมได้เลย) ---
# วิธีง่ายสุด: import bentogame as game  แล้ว  game.sfx("ชื่อ")
#   Snake : "eat"  "turn"  "die"
#   Flappy: "flap"  "point"  "fall"
#   Pong  : "wall"  "paddle"  "pong_score"  "win"  "lose"
#   Shoot : "fire"  "hit"  "explode"  "lose_life"
#   UI    : "start"  "select"  "back"  "deny"  "move"  "gameover"
# (หรือเรียกตรง ๆ แบบส่วนที่ 1: ui.sfx(ui.SFX_SNAKE_EAT) ก็ได้เหมือนกัน)
