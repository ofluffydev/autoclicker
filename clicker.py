import threading
import time

import pyautogui
from pynput import mouse


class Clicker:
    def __init__(self, delay):
        self.delay = delay
        self.running = False
        self.click_thread = None
        self.mouse_listener = None
        self.mouse_controller = mouse.Controller()

    def click(self, x, y):
        pyautogui.click(x, y)
        time.sleep(self.delay)

    def click_many(self, x, y, times):
        for _ in range(times):
            if not self.running:
                break
            self.click(x, y)

    def click_until_stop(self, x, y):
        self.running = True
        self.click_thread = threading.Thread(target=self._click_loop, args=(x, y))
        self.click_thread.start()

    def _click_loop(self, x, y):
        while self.running:
            self.click(x, y)

    def stop(self):
        self.running = False
        if self.click_thread:
            self.click_thread.join()
        if self.mouse_listener:
            self.mouse_listener.stop()

    def is_running(self):
        return self.running

    def click_while_pressed(self):
        self.running = True
        self.mouse_listener = mouse.Listener(on_press=self._on_press, on_release=self._on_release)
        self.mouse_listener.start()

    def _on_press(self, button, pressed):
        if button == mouse.Button.left and pressed:
            self.click_thread = threading.Thread(target=self._click_loop_at_cursor)
            self.click_thread.start()

    def _on_release(self, button):
        if button == mouse.Button.left:
            self.stop()

    def _click_loop_at_cursor(self):
        while self.running:
            x, y = self.mouse_controller.position
            self.click(x, y)
