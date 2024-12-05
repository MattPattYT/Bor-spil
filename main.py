from machine import Pin, PWM
from random import randint
from time import sleep_ms
import neopixel
import time


n = 24
neo_pin = Pin(45, Pin.OUT)
neopixels = neopixel.NeoPixel(neo_pin, n)
takki = Pin(13, Pin.IN, Pin.PULL_UP)
takki2 = Pin(12, Pin.IN, Pin.PULL_UP)
hljod = PWM(Pin(10),freq=1000)
hljod.duty(0)

current_led = None
last_button_state = 1
debounce_time = 200

def play_note(frequency, duration, duty=512):
    hljod.freq(frequency)
    hljod.duty(duty)
    time.sleep(duration)
    hljod.duty(0)

tune = [
    (262, 0.4),
    (294, 0.4),
    (330, 0.4),
    (349, 0.4),
    (392, 0.4),
    (440, 0.4),
    (494, 0.4),
    (523, 0.8),
]

tune2 = [
    (200, 0.4)
    ]

def fade_in():
    global current_led
    turns = randint(10, 20)
    last_led = None
    for i in range(turns):
        led_index = randint(0, n - 1)
        if i == turns - 1:
            last_led = led_index
        for brightness in range(0, 256, 10):
            neopixels[led_index] = (brightness, 0, 0)
            neopixels.write()
            sleep_ms(2)
        if i < turns - 1:
            neopixels[led_index] = (0, 0, 0)
            neopixels.write()
            sleep_ms(7)
    if last_led is not None:
        neopixels[last_led] = (255, 0, 0)
        neopixels.write()
        current_led = last_led


def wheel(pos):
    pos = pos % 256
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    else:
        pos -= 170
        return (pos * 3, 0, 255 - pos * 3)

def victory_animation():
    for _ in range(250):
        for i in range(n):
            color_index = (i * 256 // n + _ * 5) % 256
            neopixels[i] = wheel(color_index)
        neopixels.write()
        sleep_ms(1)
    for _ in range(20):
        for i in range(n):
            neopixels[i] = (100, 0, 200) if _ % 2 == 0 else (0, 0, 0)
        neopixels.write()
        sleep_ms(100)


def turn_off_current_led():
    global current_led
    if current_led is not None:
        neopixels[current_led] = (0, 0, 0)
        neopixels.write()
        current_led = None

while True:
    button_state = takki.value()
    if button_state == 0 and last_button_state == 1:
        if current_led is not None:
            turn_off_current_led()
        else:
            for note in tune2:
                play_note(note[0], note[1])
            fade_in()
        sleep_ms(debounce_time)
        last_button_state = 0
    
    elif button_state == 1 and last_button_state == 0:
        last_button_state = 1
    sleep_ms(10)
    
    if takki2.value() == 0:
        for note in tune:
            play_note(note[0], note[1])
        victory_animation()

        
