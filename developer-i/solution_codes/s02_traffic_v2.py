# s02_traffic_v2.py — ไฟจราจรแบบ "ติดทีละดวง" (อ่านเสริม ไม่คิดคะแนน)
#
# วิธีรัน: เปิดไฟล์นี้ใน BENTO IDE แล้วกด "Program to Device"
#
# ไฟล์นี้เป็นเวอร์ชันอ่านเสริมของ s02_button_fsm.py
# แกน FSM (ปุ่ม -> debounce -> เปลี่ยน state) เหมือนเดิมทุกบรรทัด
# เปลี่ยนแค่วิธี "แสดงผล": จากเดิมใช้ LED 2 ดวงเข้ารหัส 3 สถานะ
# มาเป็น "ติดทีละดวง" ดวงเดียวต่อสถานะ เหมือนไฟจราจรจริง
#
# ประเด็นที่อยากให้เห็น: ตรรกะ (state) แยกออกจากการแสดงผล (display)
# เปลี่ยนหน้าตาได้โดยไม่ต้องแตะสมองของเกมเลย

import gpio
import time

# ปุ่มดวงแรก (index 0 = USER BTN1 บนบอร์ด)
btn = gpio.button(0)

# แต่ละสถานะ = LED หนึ่งดวง (ติดทีละดวง ดวงอื่นดับ)
# GREEN  -> LED2 (index 1)
# YELLOW -> LED1 (index 0)   <- เวอร์ชันหลักไม่ได้ใช้ ดวงนี้ คราวนี้ได้ใช้
# RED    -> RGB_RED (index 2)
lamp = {
    0: gpio.led(1),
    1: gpio.led(0),
    2: gpio.led(2),
}
NAME = {0: "GREEN", 1: "YELLOW", 2: "RED"}


def show(s):
    # ติดดวงที่ตรงกับ state ปัจจุบัน ดับดวงที่เหลือให้หมด
    for i, led in lamp.items():
        led.on() if i == s else led.off()
    print("STATE =", NAME[s])


# debounce: จำสถานะปุ่มรอบก่อน เพื่อจับ "ขอบขาลง" (กดลงครั้งเดียว)
state = 0
prev_pressed = btn.is_pressed()
show(state)

print("กดปุ่ม USER BTN1 เพื่อเปลี่ยนไฟจราจร (Ctrl+C เพื่อหยุด)")
while True:
    pressed = btn.is_pressed()

    # นับเป็น "กด" เฉพาะตอนเพิ่งเปลี่ยนจากปล่อย -> กด (edge detection เดิม)
    if pressed and not prev_pressed:
        state = (state + 1) % 3   # FSM เดิม: เขียว -> เหลือง -> แดง -> วนกลับ
        show(state)
        time.sleep_ms(50)

    prev_pressed = pressed
    time.sleep_ms(10)
