# Pimoroni PicoPlasma Multi-Effects - by Glenn Jones
# Shooting star, Halloween, Rainbow disco and Christmas lights
#
# purchase a pimoroni plasma 2040 form here:-
# https://shop.pimoroni.com/products/plasma-2040?variant=39410354847827
#
# attach an addressable led strip to your plasma 2040
#
# I chose - 10m Addressable RGB LED Star Wire (AKA NeoPixel, WS2812B, SK6812) 
# https://shop.pimoroni.com/products/10m-addressable-rgb-led-star-wire?variant=41375620530259
#
# flash the pimoroni pico firmware to the plasma2040 - pico-v1.23.0-1-pimoroni-micropython.uf2
# 
# copy to your plasma 2040 as main.py
# set the NUM_LEDS to the amount or leds your led strip has 
#
# by default the plasma2040 will display a randomised shooting star trail effect with a variable colour blink
#
# pressing the buttons on the plasma2040
# user_sw = Halloween
# button_a = Rainbow disco
# button_b = Christmas
#
# press reset to return to the default shooting star effect



import plasma
from plasma import plasma2040
from pimoroni import Button
import time
from random import randrange, uniform, choice

# Set how many LEDs you have
NUM_LEDS = 66

# Define buttons
user_sw = Button(plasma2040.USER_SW)
button_a = Button(plasma2040.BUTTON_A)
button_b = Button(plasma2040.BUTTON_B)

# Pick LED type (uncomment the relevant line)
# led_strip = plasma.APA102(NUM_LEDS, 0, 0, plasma2040.DAT, plasma2040.CLK)  # APA102 / DotStar™ LEDs
led_strip = plasma.WS2812(NUM_LEDS, 0, 0, plasma2040.DAT)  # WS2812 / NeoPixel™ LEDs

# Start updating the LED strip
led_strip.start()

# Light up all the LEDs with random colors and brightness from specified ranges
def anim_halloween():
    HUE_START = 180
    HUE_END = 360
    BRIGHTNESS_MIN = 0.2
    BRIGHTNESS_MAX = 0.7
    SPEED = 0.3

    while True:
        if not read_buttons():
            break
        led_strip.set_hsv(randrange(NUM_LEDS), randrange(HUE_START, HUE_END) / 360, 1.0, uniform(BRIGHTNESS_MIN, BRIGHTNESS_MAX))
        time.sleep(SPEED)

def anim_rainbow():
    HUE_START = 0
    HUE_END = 360
    BRIGHTNESS_MIN = 0.2
    BRIGHTNESS_MAX = 0.7
    SPEED = 0.01

    while True:
        if not read_buttons():
            break
        led_strip.set_hsv(randrange(NUM_LEDS), randrange(HUE_START, HUE_END) / 360, 1.0, uniform(BRIGHTNESS_MIN, BRIGHTNESS_MAX))
        time.sleep(SPEED)

def anim_christmas():
    HUE_1 = 0  # Red
    HUE_2 = 127  # Green
    BRIGHTNESS = 0.5
    SPEED = 1

    while True:
        if not read_buttons():
            break
        for i in range(NUM_LEDS):
            if i % 2 == 0:
                led_strip.set_hsv(i, HUE_1 / 360, 1.0, BRIGHTNESS)
            else:
                led_strip.set_hsv(i, HUE_2 / 360, 1.0, BRIGHTNESS)
        time.sleep(SPEED)
        for i in range(NUM_LEDS):
            if i % 2 == 0:
                led_strip.set_hsv(i, HUE_2 / 360, 1.0, BRIGHTNESS)
            else:
                led_strip.set_hsv(i, HUE_1 / 360, 1.0, BRIGHTNESS)
        time.sleep(SPEED)

def ping_pong_leds_with_trails():
    NUM_LEDS = 66
    NUM_LEDS_MOVING = 5  # Number of moving LEDs
    BRIGHTNESS = 0.5
    fade_factor = 0.8

    # Initialize the positions, directions, and speeds for each moving LED
    positions = [randrange(NUM_LEDS) for _ in range(NUM_LEDS_MOVING)]
    directions = [choice([-1, 1]) for _ in range(NUM_LEDS_MOVING)]
    speeds = [uniform(0.05, 0.5) for _ in range(NUM_LEDS_MOVING)]
    color_durations = [0 for _ in range(NUM_LEDS_MOVING)]  # Duration timers for colored LEDs
    color_hues = [0 for _ in range(NUM_LEDS_MOVING)]  # Hues for colored LEDs

    # Initialize a list to keep track of the brightness levels of the LEDs
    brightness_levels = [0] * NUM_LEDS

    while True:
        if not read_buttons():
            break

        # Update the brightness levels for the trail effect
        for i in range(NUM_LEDS):
            brightness_levels[i] *= fade_factor

        # Move each LED and update the strip
        for i in range(NUM_LEDS_MOVING):
            if color_durations[i] > 0:
                # Continue displaying the current color
                color_durations[i] -= 1
                led_strip.set_hsv(positions[i], color_hues[i], 1.0, BRIGHTNESS)
            else:
                # Occasionally change color with 20% chance
                if randrange(100) < 20:
                    color_hues[i] = randrange(0, 360) / 360
                    color_durations[i] = randrange(10, 30)  # Keep color for a longer time
                    led_strip.set_hsv(positions[i], color_hues[i], 1.0, BRIGHTNESS)
                else:
                    brightness_levels[positions[i]] = BRIGHTNESS

            # Move the LED index
            positions[i] += directions[i]

            # Reverse direction if we reach the end of the strip
            if positions[i] >= NUM_LEDS or positions[i] < 0:
                directions[i] = -directions[i]  # Reverse direction
                positions[i] += directions[i] * 2  # Ensure we stay within bounds

        # Update the LED strip with the new brightness levels
        for j in range(NUM_LEDS):
            led_strip.set_hsv(j, 0, 0, brightness_levels[j])

        # Randomly change speed of each LED occasionally
        if randrange(100) < 10:  # 10% chance to change speed
            speeds = [uniform(0.05, 0.5) for _ in range(NUM_LEDS_MOVING)]

        # Wait for the specified speed duration for each LED
        time.sleep(min(speeds))

def read_buttons():
    if user_sw.read():
        print("HALLOWEEN Pressed User SW - {}".format(time.ticks_ms()))
        anim_halloween()
        return False
    if button_a.read():
        print("RAINBOW Pressed A - {}".format(time.ticks_ms()))
        anim_rainbow()
        return False
    if button_b.read():
        print("CHRISTMAS Pressed B - {}".format(time.ticks_ms()))
        anim_christmas()
        return False
    return True

# Start the ping pong LED animation with trails on board initialization
ping_pong_leds_with_trails()

# Main loop
while True:
    read_buttons()

