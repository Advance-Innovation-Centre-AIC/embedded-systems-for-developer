# bentogame.py — a tiny, beginner-friendly game framework for the
# BENTO Game Console, written in pure MicroPython on top of the existing
# `ui` (graphics) and `joystick` (input) modules. No firmware build needed.
#
# Design goal: a 2nd-year student who is weak at C can make a real,
# on-screen, joystick-controlled game by learning only ~6 ideas:
#   start(), Box, Text, keys(), hit(), run()
#
# The SAME concepts (sprite, move, input, collision, loop) map 1:1 onto the
# C game SDK later in the course — so Python is the on-ramp, not a dead end.

import ui
import joystick
import time

# Display size of the BENTO console canvas (matches ui.screen default).
WIDTH = 792
HEIGHT = 398

# A few friendly color names so beginners don't fight hex codes.
RED     = 0xFF5555
GREEN   = 0x50FA7B
BLUE    = 0x61AFEF
YELLOW  = 0xF1FA8C
CYAN    = 0x00E0FF
ORANGE  = 0xFFB86C
WHITE   = 0xFFFFFF
PINK    = 0xFF79C6
BLACK   = 0x101010

# Classic Game Boy 4-tone palette (same values as the on-board C games).
GB_DARKEST  = 0x0F380F
GB_DARK     = 0x306230
GB_LIGHT    = 0x8BAC0F
GB_LIGHTEST = 0x9BBC0F


# --- Sound -------------------------------------------------------------------
# Plays through the on-board C sound engine (bento_sfx) over IPC — no extra
# hardware, no firmware build. Needs sfx-capable firmware; older images stay
# silent so your game still runs.
_HAS_SOUND = hasattr(ui, "sfx")

if _HAS_SOUND:
    # Waveforms for tone()
    SINE, SQUARE, TRIANGLE, SAW = (ui.WAVE_SINE, ui.WAVE_SQUARE,
                                   ui.WAVE_TRIANGLE, ui.WAVE_SAW)
    # Friendly names -> the real firmware ids (always in sync with the C games).
    SFX = {
        "move": ui.SFX_UI_MOVE, "select": ui.SFX_UI_SELECT, "back": ui.SFX_UI_BACK,
        "deny": ui.SFX_UI_DENY, "start": ui.SFX_UI_START,
        "eat": ui.SFX_SNAKE_EAT, "turn": ui.SFX_SNAKE_TURN, "die": ui.SFX_SNAKE_DIE,
        "flap": ui.SFX_FLAPPY_FLAP, "point": ui.SFX_FLAPPY_SCORE,
        "wall": ui.SFX_PONG_WALL, "paddle": ui.SFX_PONG_PADDLE,
        "win": ui.SFX_PONG_WIN, "lose": ui.SFX_PONG_LOSE,
        "fire": ui.SFX_SHOOT_FIRE, "hit": ui.SFX_SHOOT_HIT,
        "explode": ui.SFX_SHOOT_EXPLODE, "gameover": ui.SFX_GAME_OVER,
    }
else:
    SINE = SQUARE = TRIANGLE = SAW = 0
    SFX = {}


def sfx(name):
    """Play a built-in sound effect — by name ("eat","die","gameover",...) or number."""
    if not _HAS_SOUND:
        return
    try:
        ui.sfx(SFX.get(name, name) if isinstance(name, str) else int(name))
    except Exception:
        pass


def tone(note, wave=None, velocity=100, ms=150):
    """Play your own note (MIDI note number, 60 = middle C). Invent your own sounds!"""
    if not _HAS_SOUND:
        return
    try:
        ui.tone(int(note), SQUARE if wave is None else wave, int(velocity), int(ms))
    except Exception:
        pass


# --- Real sprites (spike-b) -------------------------------------------------
# game.Sprite("snake_body", x, y) draws the SAME pixel-art the on-board C games
# use (the C side owns the pixels; only the name+position cross IPC). Needs
# sprite-capable firmware; on the desktop sim (or old firmware) it falls back to
# a small GB-green box so your game logic still runs (shapes, not pixel-art).
_HAS_SPRITE = hasattr(ui, "Sprite")

if _HAS_SPRITE:
    SPR = {
        "snake_head_r": ui.SPR_SNAKE_HEAD_R, "snake_head_d": ui.SPR_SNAKE_HEAD_D,
        "snake_head_l": ui.SPR_SNAKE_HEAD_L, "snake_head_u": ui.SPR_SNAKE_HEAD_U,
        "snake_body": ui.SPR_SNAKE_BODY, "snake_food": ui.SPR_SNAKE_FOOD,
        "bird": ui.SPR_FLAPPY_BIRD, "pipe_cap": ui.SPR_FLAPPY_PIPE_CAP,
        "ball": ui.SPR_PONG_BALL, "paddle": ui.SPR_PONG_PADDLE,
        "ship": ui.SPR_SHOOTER_SHIP, "enemy": ui.SPR_SHOOTER_ENEMY,
        "enemy2": ui.SPR_SHOOTER_ENEMY2, "enemy3": ui.SPR_SHOOTER_ENEMY3,
        "boom1": ui.SPR_SHOOTER_BOOM_P1, "boom2": ui.SPR_SHOOTER_BOOM_P2,
        "boom3": ui.SPR_SHOOTER_BOOM_C1, "boom4": ui.SPR_SHOOTER_BOOM_C2,
        "boom5": ui.SPR_SHOOTER_BOOM_F1, "boom6": ui.SPR_SHOOTER_BOOM_F2,
    }
else:
    SPR = {}


class Sprite:
    """A real pixel-art sprite from the on-board C games (e.g. "snake_body").
    Same moves as Box; .frame("snake_head_u") swaps which picture it shows."""

    def __init__(self, name, x=0, y=0):
        self.x, self.y, self.name = x, y, name
        if _HAS_SPRITE:
            self._w = ui.Sprite(SPR[name], int(x), int(y))
        else:
            # logic-only fallback so the desktop sim still runs (a 16px box)
            self._w = ui.Panel(x=int(x), y=int(y), w=16, h=16, color=GB_DARK)

    def move_to(self, x, y):
        self.x, self.y = x, y
        self._w.pos(int(x), int(y))

    def move(self, delta_x, delta_y):
        self.move_to(self.x + delta_x, self.y + delta_y)

    def frame(self, name):
        """Swap the picture (e.g. turn the snake head). No-op in the sim."""
        self.name = name
        if _HAS_SPRITE:
            self._w.frame(SPR[name])

    def hide(self):
        self._w.hide()

    def show(self):
        self._w.show()

    def center(self):
        return (self.x + 8, self.y + 8)


def pool(name, count):
    """Make `count` hidden sprites of one kind ONCE (e.g. snake body segments).
    Show/move the ones you need each frame, hide the rest — exactly like the C
    game. Keeps you under the 32-sprite limit and runs fast.
    NEVER create sprites inside your update() loop; size a pool here instead."""
    sprites = [Sprite(name, -100, -100) for _ in range(count)]
    for sprite in sprites:
        sprite.hide()
    return sprites


def start(width=WIDTH, height=HEIGHT):
    """Call once at the top of your game. Clears the screen and wakes the joystick."""
    global WIDTH, HEIGHT
    WIDTH, HEIGHT = width, height
    # Right after a soft-reset (Start = restart) CM33 can reach here before the
    # CM55 graphics core is ready — ui.screen() then raises "CM55 not ready
    # (retry shortly)". Retry for up to ~5s so restart never crashes.
    for _attempt in range(50):
        try:
            ui.screen(width, height)
            break
        except Exception:
            time.sleep_ms(100)
    try:
        joystick.init()
    except Exception:
        pass  # touch-only is fine; joystick is optional


def clear():
    """Erase everything on the screen."""
    ui.clear()


class Box:
    """A colored rectangle you can move around. The simplest 'sprite'."""

    def __init__(self, x, y, w, h, color=WHITE):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self._panel = ui.Panel(x=int(x), y=int(y), w=int(w), h=int(h), color=color)

    def move_to(self, x, y):
        """Put the box at an exact position."""
        self.x = x
        self.y = y
        self._panel.pos(int(x), int(y))

    def move(self, delta_x, delta_y):
        """Move the box by some amount, staying on screen."""
        next_x = self.x + delta_x
        next_y = self.y + delta_y
        if next_x < 0:
            next_x = 0
        if next_y < 0:
            next_y = 0
        if next_x > WIDTH - self.w:
            next_x = WIDTH - self.w
        if next_y > HEIGHT - self.h:
            next_y = HEIGHT - self.h
        self.move_to(next_x, next_y)

    def resize(self, w, h):
        """Change the box's width/height (e.g. Flappy pipes)."""
        self.w, self.h = w, h
        self._panel.size(int(w), int(h))

    def set_color(self, color):
        self._panel.color(color)

    def hide(self):
        self._panel.hide()

    def show(self):
        self._panel.show()

    def center(self):
        """Return (cx, cy) — the middle point of the box."""
        return (self.x + self.w / 2, self.y + self.h / 2)


class Text:
    """A line of text on screen (e.g. the score)."""

    def __init__(self, message, x, y, color=WHITE):
        self._label = ui.Label(str(message), x=int(x), y=int(y), color=color)

    def set(self, message):
        self._label.text(str(message))


class Keys:
    """A friendly snapshot of the controller this frame.

    .left .right .up .down  -> True/False  (D-pad OR left stick)
    .a .b .x .y             -> face buttons
    .start .back            -> system buttons
    """

    def __init__(self, raw):
        self.raw = raw or {}
        threshold = 60  # stick threshold around center (128)
        stick_x = self.raw.get("left_x", 128)
        stick_y = self.raw.get("left_y", 127)
        self.left  = bool(self.raw.get("dpad_left"))  or (stick_x < 128 - threshold)
        self.right = bool(self.raw.get("dpad_right")) or (stick_x > 128 + threshold)
        self.up    = bool(self.raw.get("dpad_up"))    or (stick_y < 127 - threshold)
        self.down  = bool(self.raw.get("dpad_down"))  or (stick_y > 127 + threshold)
        self.a = bool(self.raw.get("a"))
        self.b = bool(self.raw.get("b"))
        self.x = bool(self.raw.get("x"))
        self.y = bool(self.raw.get("y"))
        self.start = bool(self.raw.get("start"))
        self.back  = bool(self.raw.get("back"))


def keys():
    """Read the controller right now. Returns a Keys object."""
    try:
        return Keys(joystick.read())
    except Exception:
        return Keys({})


# --- Sensors & IoT (Option C) ------------------------------------------------
# Tilt control reads the on-board BMI270; online ranking publishes over MQTT.
# Both are forgiving: if the hardware/network isn't there they no-op so your
# game still runs (e.g. in the desktop sim).
_tilt_inited = False


def tilt(deadzone=0.18):
    """Tilt the board to steer — reads the BMI270 and returns a Keys object
    (.left/.right/.up/.down). First call wakes the sensor. All-False if missing."""
    global _tilt_inited
    steering = Keys({})
    try:
        import sensors, bmi270
        if not _tilt_inited:
            sensors.init()
            _tilt_inited = True
        accel_x, accel_y, accel_z = bmi270.acceleration()
    except Exception:
        return steering
    steering.right = accel_x > deadzone
    steering.left = accel_x < -deadzone
    steering.down = accel_y > deadzone
    steering.up = accel_y < -deadzone
    return steering


_net_ready = False


def connect(ssid, password, broker, port=1883):
    """Connect WiFi + MQTT once (for the online ranking). Call near game start;
    safe to call again. Returns True when ready, False if it can't connect."""
    global _net_ready
    try:
        import wifi, mqtt
        if not wifi.is_connected():
            wifi.connect(ssid, password)
        if not _net_ready:
            mqtt.connect(broker, port=port)
            _net_ready = True
        return True
    except Exception:
        return False


def post_score(score, team="team1", game="snake"):
    """Publish a score to the class ranking over MQTT (call connect() first).
    Topic: game/<game>/<team>/score. Returns True if it was sent."""
    try:
        import mqtt
        if not mqtt.is_connected():
            return False
        topic = "game/%s/%s/score" % (game, team)
        mqtt.publish(topic, '{"team":"%s","game":"%s","score":%d}' % (team, game, score))
        return True
    except Exception:
        return False


def send(state, topic="game/multiplayer/state"):
    """Publish your game state to other players over MQTT (call connect() first).
    `state` is any string. No-op (returns False) when the network is absent."""
    try:
        import mqtt
        if not mqtt.is_connected():
            return False
        mqtt.publish(topic, state)
        return True
    except Exception:
        return False


def recv():
    """Return the latest message from other players, or None if nothing arrived.
    Safe to call every frame; no-op (returns None) when the network is absent."""
    try:
        import mqtt
        if not mqtt.is_connected():
            return None
        return mqtt.get_message()
    except Exception:
        return None


def hit(a, b):
    """True if Box a overlaps Box b (axis-aligned bounding-box test)."""
    return (a.x < b.x + b.w and a.x + a.w > b.x and
            a.y < b.y + b.h and a.y + a.h > b.y)


def _restart():
    """Re-run MicroPython from the top = start the game over (Start button)."""
    try:
        import machine
        machine.soft_reset()
    except Exception:
        pass


def run(update, fps=30):
    """Run your game. `update` is a function called every frame.

    System buttons are handled for you on every Bento game:
      BACK  = ออกจากเกม กลับหน้า Bento Playground
      START = เริ่มเกมใหม่ (รัน MicroPython ใหม่)
    update() may also return False to stop on its own (e.g. GAME OVER).
    """
    delay = int(1000 / fps)
    while True:
        pressed = keys()
        if pressed.back:            # BACK = ออกกลับ Playground
            clear()
            return
        if pressed.start:           # START = เริ่มเกมใหม่
            _restart()
            return
        if update() is False:
            break
        time.sleep_ms(delay)
