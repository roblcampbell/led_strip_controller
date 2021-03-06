"""
This module is used to fake the original hyperion functions

Created on 27.11.2014

@author: Fabian Hertwig
"""
import imp
import json_client

ledCount = 0

# the data as set in the hypercon application
horizontal = 0
vertical = 0
first_led_offset = 0
clockwise_direction = False
corner_leds = False
# the dictionary the hyperion effect will access
args = {
    #snake
    # "rotation-time" : 8.0,
    # "color" : [0, 255, 0],
    # "percentage" : 100,

    #christmaslights
    # "color1" : [255, 0, 0],
    # "color2" : [0, 255, 0],
    # "color3" : [255, 255, 0],
    # "color4" : [0, 0, 255],
    # "color5" : [0, 255, 255],
    # "bulbSize" : 1,
    # "gapWidth" : 0,
    # "changeInterval" : 0.5,

    #christmaslights2
    # "fadeCycleTime" : 3.0,

    #randomBalls
    # "ballSize" : 1,
    # "ballCount" : 3

    #random matrix fades
    "blockCount" : 28,
    # "color1" : [0, 255, 255],
    "color1" : [255, 0, 0],
    # "color2" : [0, 255, 0],
    "color2" : [255, 255, 0],
    "color3" : [255, 129, 0],
    # "color4" : [0, 0, 255],
    # "color5" : [0, 255, 255],
    # "color6" : [255, 0, 255],
    # "color7" : [255, 255, 255],

    # warm matrix fade colors (red, orange, yellow)
    # "color1" : [255, 0, 0],
    # "color2" : [255, 255, 0],
    # "color3" : [255, 129, 0],

    # cold matrix fade colors (blue, cyan, white)
    "color1" : [0, 0, 255],
    "color2" : [0, 255, 255],
    "color3" : [255, 255, 255],

    # "randomColor" : "True",
    "fadeSpeed" : 8,
    "fadeRandom" : 4

}

_ledData = None
_abort = False

""" helper functions """

def init(horizontal_led_num, vertical_led_num, first_led_offset_num, leds_in_clockwise_direction, has_corner_leds):
    """
    Initialise the fake hyperion configuration. The values should be identical to your hyperion configuration.
    :param horizontal_led_num: the number of your horizontal leds
    :param vertical_led_num: the number of your vertical leds
    :param first_led_offset_num: the offset value
    :param leds_in_clockwise_direction: boolean: are your leds set up clockwise or not
    :param has_corner_leds: boolean: are there corner leds
    """
    global ledCount, _ledData, horizontal, vertical, first_led_offset, clockwise_direction, corner_leds

    ledCount = (2 * horizontal_led_num) + (2 * vertical_led_num)
    horizontal = horizontal_led_num
    vertical = vertical_led_num
    first_led_offset = first_led_offset_num
    clockwise_direction = leds_in_clockwise_direction
    corner_leds = has_corner_leds

    _ledData = bytearray()
    for x in range(ledCount * 3):
        _ledData.append(0)


def set_abort(abort_hyperion):
    global _abort
    _abort = abort_hyperion


def get_led_data():
    led_data_copy = bytearray()
    if _ledData:
        imp.acquire_lock()
        led_data_copy = bytearray(_ledData)
        imp.release_lock()

    return led_data_copy


""" fake hyperion functions """


def abort():
    return _abort


def set_color(led_data):
    global _ledData
    imp.acquire_lock()
    _ledData = bytearray(led_data)
    imp.release_lock()
    json_client.send_led_data(led_data)


def setColor(led_data):
    set_color(led_data)

""" cant overload functions in python """
# def setColor(red, green, blue):
#     acquire_lock()
#     for i in range(len(_ledData) / 3):
#         _ledData[3*i] = red
#         _ledData[3*i + 1] = green
#         _ledData[3*i + 2] = blue
#     release_lock()


