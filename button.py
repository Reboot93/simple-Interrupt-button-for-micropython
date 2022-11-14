'''
simple-Interrupt-button-for-micropython

https://github.com/Reboot93/simple-Interrupt-button-for-micropython

====================================================
MIT License

Copyright (c) 2022 Reboot93

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

from machine import Pin, Timer

class Button:

    def __init__(self, pin, single_click_time=130, long_press_time=210, pull=Pin.PULL_UP, trigger=Pin.IRQ_FALLING):
        self.pin = pin
        self.callback = None
        self.isEnable = False
        self._single_click_time = single_click_time
        self._long_press_time = long_press_time
        self._timer_count = 0
        self.button = Pin(pin, Pin.IN, pull)
        self.trigger = trigger
        self._long_press_timer = Timer(0)

    def setEnable(self, flag: bool):
        if flag:
            self.button.irq(handler=self._irq_callback, trigger=self.trigger)
            self.isEnable = True
        else:
            self.button.irq(handler=None)
            self.isEnable = False

    def connect(self, fun):
        self.callback = fun

    def _irq_callback(self, pin):
        self.setEnable(False)
        self.click_flag = False
        self.long_press_flag = False
        self._long_press_timer.init(period=2, callback=self._timer_irp_callback)

    def _timer_irp_callback(self, msg):
        if self.button.value() != 0 or self._timer_count > self._long_press_time + 10:
            print(self._timer_count)
            if 5 < self._timer_count < self._single_click_time:
                self._long_press_timer.deinit()
                print('Button %s clicked' % str(self.pin))
                self.callback(self.pin, 0)
            elif self._timer_count > self._long_press_time:
                self._long_press_timer.deinit()
                print('Button %s long pressed' % str(self.pin))
                self.callback(self.pin, 1)
            else:
                self._long_press_timer.deinit()
            self._timer_count = 0
            self.setEnable(True)
        else:
            self._timer_count += 1
