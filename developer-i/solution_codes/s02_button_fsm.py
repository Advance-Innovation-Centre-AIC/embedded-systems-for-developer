# s02_button_fsm.py — ปุ่ม + debounce + FSM (ไฟจราจร)
#
# วิธีรัน: เปิดไฟล์นี้ใน BENTO IDE แล้วกด "Program to Device"
#
# เป้าหมายของแล็บนี้: ฝึกแกนของ game loop จริง ๆ คือ
#   อ่าน input (ปุ่ม) -> กรองสัญญาณรบกวน (debounce) -> เปลี่ยน state (FSM) -> แสดงผล (LED)
# กดปุ่ม USER BTN1 หนึ่งครั้ง = เปลี่ยนสถานะไฟจราจรไปทีละขั้น: เขียว -> เหลือง -> แดง -> วนกลับ

import gpio
import time

# ขอใช้ปุ่มดวงแรก (index 0 = USER BTN1 บนบอร์ด) และไฟ LED 2 ดวงไว้บอกสถานะ
# ใช้ LED2 (เขียว) + RGB_RED — เลี่ยง LED1 (แดง, index 0) ที่ระบบหลักมักใช้เป็นไฟ status
btn = gpio.button(0)
led_a = gpio.led(1)   # LED2 (เขียว) — ใช้คู่กับ led_b เข้ารหัส 3 สถานะด้วย 2 ดวง
led_b = gpio.led(2)   # RGB_RED

# นิยาม state ของ FSM ให้อ่านง่าย แทนที่จะใช้ตัวเลขลอย ๆ
GREEN, YELLOW, RED = 0, 1, 2
state = GREEN

# ตารางว่าแต่ละ state ควรเปิด LED ดวงไหนบ้าง (led_a, led_b)
# เขียว = ดวง A, เหลือง = ทั้งคู่, แดง = ดวง B  (เลือกให้แยกกันได้ชัด)
LED_PATTERN = {
    GREEN:  (True,  False),
    YELLOW: (True,  True),
    RED:    (False, True),
}
NAME = {GREEN: "GREEN", YELLOW: "YELLOW", RED: "RED"}


def show(s):
    # สะท้อน state ปัจจุบันออก LED ตามตารางด้านบน
    a_on, b_on = LED_PATTERN[s]
    led_a.on() if a_on else led_a.off()
    led_b.on() if b_on else led_b.off()
    print("STATE =", NAME[s])


# ตัวแปรสำหรับ debounce: จำสถานะปุ่มรอบก่อน เพื่อจับ "ขอบขาลง" (กดลงครั้งเดียว)
prev_pressed = btn.is_pressed()
show(state)

print("กดปุ่ม USER BTN1 เพื่อเปลี่ยนไฟจราจร (Ctrl+C เพื่อหยุด)")
while True:
    pressed = btn.is_pressed()

    # debounce แบบง่าย: นับเป็น "กด" เฉพาะตอนที่เพิ่งเปลี่ยนจากปล่อย -> กด
    # (เป็น edge detection กันปุ่มเด้งซ้ำ ๆ จากการกดค้างหนึ่งครั้ง)
    if pressed and not prev_pressed:
        state = (state + 1) % 3   # เลื่อน FSM ไปสถานะถัดไปแบบวนรอบ
        show(state)
        time.sleep_ms(50)         # หน่วงสั้น ๆ ให้สัญญาณปุ่มนิ่งก่อนอ่านต่อ

    prev_pressed = pressed
    time.sleep_ms(10)             # คุมจังหวะ loop ~100 รอบ/วินาที ไม่ให้ busy เกินจำเป็น
