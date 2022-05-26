from pynput.mouse import Listener
from pynput import mouse
from countdown import countdown
import pyperclip as pc
from pynput.keyboard import Key
from pynput import keyboard
import time
from jsonfunctions import open_json

def countdown(tm):
    if tm == 0:
        tm = 0.3
    time.sleep(tm)

def position_to_string(pos):
    return str(pos[0]) + " " + str(pos[1])

def string_to_position(str):
    return (float(str.split(" ")[0]), float(str.split(" ")[1]))

def grabArea(msg):
    print(msg)
    points = []
    def appr_equal(a, b):
        return abs(a[0] - b[0]) <= 5 and abs(a[1] - b[1]) <= 5
    def last_three_equal():
        if len(points) < 3:
            return False
        return appr_equal(points[-1], points[-2]) and appr_equal(points[-1], points[-3])
    def on_click(x, y, button, pressed):
        if pressed:
            points.append([x, y])
        if not pressed and last_three_equal():
            return False
    with Listener(on_click=on_click) as listener:
        listener.join()
    return points[-1]

CONFIG_PATH = "config"

class WeChatBot:
    def __init__(self, set_new):
        if not set_new:
            try:
                f = open(CONFIG_PATH, "r")    
                self.contacts_button = string_to_position(f.readline())
                self.add_contacts_button = string_to_position(f.readline())
                self.add_button = string_to_position(f.readline())
                self.friend_request_field = string_to_position(f.readline())
                self.ok_button = string_to_position(f.readline())
                print(self.contacts_button)
                print(self.add_contacts_button)
                print(self.add_button)
                print(self.friend_request_field)
                f.close()
            except:
                set_new = True

        if set_new:
            self.contacts_button = grabArea("press 'contacts' button on the left menu")
            self.add_contacts_button = grabArea("press 'add contacts' button")
            self.add_button = grabArea("press 'add' button")
            self.friend_request_field = grabArea("press 'send friend request' field")
            self.ok_button = grabArea("press 'OK' button")
            f = open(CONFIG_PATH, "w")
            f.write(position_to_string(self.contacts_button) + "\n")
            f.write(position_to_string(self.add_contacts_button) + "\n")
            f.write(position_to_string(self.add_button) + "\n")
            f.write(position_to_string(self.friend_request_field) + "\n")
            f.write(position_to_string(self.ok_button) + "\n")
            f.close()

    def add_new_contact(self, phone_number):
        pc.copy(phone_number)
        ms = mouse.Controller()
        kb = keyboard.Controller()

        ms.position = self.contacts_button
        countdown(0)
        ms.press(mouse.Button.left)
        ms.release(mouse.Button.left)
        countdown(0)

        ms.position = self.add_contacts_button
        countdown(0)
        ms.press(mouse.Button.left)
        ms.release(mouse.Button.left)
        countdown(0)

        kb.press(Key.cmd.value)
        kb.press('v')
        kb.release('v')
        kb.release(Key.cmd.value)
        countdown(0.7)

        kb.press(Key.enter)
        kb.release(Key.enter)
        countdown(1)

        ms.position = self.add_button
        countdown(0)
        ms.press(mouse.Button.left)
        ms.release(mouse.Button.left)
        countdown(0)

        ms.position = self.friend_request_field
        countdown(0)
        ms.press(mouse.Button.left)
        ms.release(mouse.Button.left)
        countdown(0)

        kb.press(Key.cmd.value)
        kb.press('a')
        kb.release('a')
        kb.release(Key.cmd.value)
        countdown(0)

        f = open("request_message", "r")
        offer_message = f.read()
        pc.copy(offer_message)
        kb.press(Key.cmd.value)
        kb.press('v')
        kb.release('v')
        kb.release(Key.cmd.value)
        countdown(0)
        f.close()

        ms.position = self.ok_button
        countdown(0)
        ms.press(mouse.Button.left)
        ms.release(mouse.Button.left)

import sys

def convert(phone):
    res = "+86"
    for c in phone:
        if c == '(' or c == ')':
            continue
        res = res + c
    return res

if __name__ == "__main__":
    n_args = len(sys.argv)
    set_new = False
    for arg in sys.argv:
        print(arg)
        if arg == "set_new=True":
            set_new = True
        if arg == "set_new=False":
            set_new = False

    request = input("Request: ")

    wechatbot = WeChatBot(set_new=set_new)

    js = open_json(f"{request}_contacts.json")

    countdown(4)

    cnt = 0
    for block in js:
        cnt += 1
        if cnt == 5:
            break
        phones = block["contact"].split(",")
        for phone_ in phones:
            phone = convert(phone_)
            wechatbot.add_new_contact(phone)
            countdown(3)