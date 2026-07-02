# s09_tilt.py — เอียงเล่น: ขยับกล่องตามการเอียงบอร์ด
#
# วิธีรัน: เปิดไฟล์นี้ใน BENTO IDE แล้วกด "Program to Device"
#
# สิ่งที่จะได้ฝึก:
#   - อ่าน accelerometer (BMI270 ผ่าน I2C) ด้วยโมดูล sensors / bmi270
#   - แปลง (map) ค่า analog ความเอียง -> ความเร็วการเลื่อนของกล่อง
#   - ขยับ game.Box ตามการเอียงจริงของบอร์ด
#
# ลองเอียงบอร์ดซ้าย-ขวา-หน้า-หลัง แล้วดูกล่องวิ่งตามมือเราเลย

import bentogame as game
import sensors          # ชุดเซนเซอร์บนบอร์ด (ต้อง init ก่อนใช้)
# bmi270 อยู่ใต้ sensors แล้ว — เรียก sensors.bmi270.acceleration() ได้เลย
import time

game.start()            # เคลียร์จอ + เตรียมระบบ
sensors.init()          # ปลุกเซนเซอร์ทั้งชุด (รวม BMI270) ครั้งเดียวพอ

# สร้างกล่องไว้กลางจอ ขนาด 40x40
box = game.Box(game.WIDTH // 2, game.HEIGHT // 2, 40, 40, color=game.CYAN)
label = game.Text("เอียงบอร์ดเพื่อขยับกล่อง", 20, 20)

DEADZONE = 0.10   # ค่าเอียงเล็ก ๆ ถือว่ายังนิ่ง กันกล่องสั่น
SPEED = 120.0     # ตัวคูณ: ยิ่งเอียงมาก กล่องยิ่งวิ่งไว

while True:
    keys = game.keys()          # อ่านปุ่มระบบ (BACK = ออก)
    if keys.back:
        game.clear()
        break

    # อ่านความเร่ง 3 แกน เซนเซอร์คืน m/s²
    ax, ay, az = sensors.bmi270.acceleration()
    # แปลงเป็น g (วางราบ แกนหนึ่ง ≈ 1.0, ช่วงเอียงราว -1..1)
    ax, ay, az = ax/9.81, ay/9.81, az/9.81

    # ตัด noise ในช่วง deadzone ให้เป็น 0 (กล่องจะนิ่งเมื่อวางราบ)
    if abs(ax) < DEADZONE:
        ax = 0.0
    if abs(ay) < DEADZONE:
        ay = 0.0

    # map ค่าความเอียง -> ระยะเลื่อนต่อเฟรม (box.move คุมขอบจอให้แล้ว)
    box.move(ax * SPEED, ay * SPEED)

    time.sleep_ms(30)           # ~30 fps
