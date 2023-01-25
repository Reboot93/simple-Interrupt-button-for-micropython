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


# callback msg : 1: single click
#                2: long click
#                3: hold
#                4: release


class Button:
    # 设置 定时器范围      eg. Timer(0),Timer(1),Timer(2),Timer(3) --> (0, 3)
    # Set timer range
    timer_number_range = (0, 3)

    # ================================================================

    timer_dict = {}
    for i in range(timer_number_range[0], timer_number_range[1] + 1):
        timer_dict[i] = 0
    timer_count = 0
    timer_quantity = len(timer_dict)

    timer_irp_count = 0

    # pin 为 按键 GPIO 号， single_click_time 与 press_hold_time 为 单击最大时长 与 按住开始时长（具体时长取决于定时器设置的触发时间），二者之间为长按
    # Pin is the key GPIO number,
    # single_click_time and press_hold_time is the click detection duration and press detection duration
    # (the specific duration depends on the trigger time set by the timer)
    def __init__(self, pin, single_click_time=100, press_hold_time=350, timer_interval=2, pull=Pin.PULL_DOWN,
                 trigger=Pin.IRQ_RISING):
        self.pin = pin
        self.callback = None
        self.isEnable = False
        self._short_press_time = single_click_time
        self._hold_time = press_hold_time
        self._timer_count = 0
        self._timer_interval = timer_interval
        self.button = Pin(pin, Pin.IN, pull)
        self.trigger = trigger
        self._long_press_timer = None
        self._timer_number = None
        self._flag_hold = False
        if pull == Pin.PULL_DOWN:
            self._timer_bt_value = 1
        else:
            self._timer_bt_value = 0

    def __get_available_timer(self):
        date_value = list(Button.timer_dict.values())
        try:
            i = Button.timer_irp_count
            while i > 0:
                index = date_value.index(0)
                date_value = date_value[index:]
                i -= 1
            date_key = list(Button.timer_dict.keys())
            return date_key[index]
        except ValueError:
            return None

    def __setEnable(self, flag: bool):
        if flag:
            self.button.irq(handler=self._irq_callback, trigger=self.trigger)
            self.isEnable = True
            self._long_press_timer = None
            Button.timer_dict[self._timer_number] = 0
            self._timer_number = None
            Button.timer_count -= 1
        else:
            if Button.timer_count > Button.timer_quantity - 1:
                return 1
            Button.timer_irp_count += 1
            timer_number = self.__get_available_timer()
            if self._timer_number is not None:
                Button.timer_irp_count -= 1
                return 3
            if timer_number is not None:
                Button.timer_dict[timer_number] = 1
                Button.timer_irp_count -= 1
                self.button.irq(handler=None)
                self.isEnable = False
                self._long_press_timer = Timer(timer_number)
                self._timer_number = timer_number
                Button.timer_count += 1
                return 0
            else:
                Button.timer_irp_count -= 1
                return 2

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
        self.button.irq(handler=None)
        if self.__setEnable(False) != 0:
            # print("No more timer, please wait for release")
            self.setEnable(True)
            return
        else:
            self.click_flag = False
            self.long_press_flag = False
            self._long_press_timer.init(period=self._timer_interval, callback=self._timer_irp_callback)

    def _timer_irp_callback(self, msg):
        if self.button.value() != self._timer_bt_value or self._timer_count > self._hold_time:
            # print(self._timer_count)
            if 5 < self._timer_count <= self._short_press_time:
                # Single Click 
                self._long_press_timer.deinit()
                print('Button %s short press' % str(self.pin))
                self.callback(self.pin, 0)
            elif self._short_press_time < self._timer_count <= self._hold_time:
                # Long Click 
                self._long_press_timer.deinit()
                print('Button %s long pressed' % str(self.pin))
                self.callback(self.pin, 1)
            elif self._timer_count > self._hold_time:
                if self._flag_hold:
                    # 非初次 进入hold判断
                    if self.button.value() != self._timer_bt_value:
                        self._long_press_timer.deinit()
                        print('Button %s release' % str(self.pin))
                        self._flag_hold = False
                        self.callback(self.pin, 4)
                    else:
                        self._timer_count += 1
                        return
                else:
                    # 初次 进入hold判断
                    self._flag_hold = True
                    print('Button %s Hold' % str(self.pin))
                    self.callback(self.pin, 3)
                    self._timer_count += 1
                    return
            else:
                try:
                    self._long_press_timer.deinit()
                except AttributeError:
                    pass
            self._timer_count = 0
            self.__setEnable(True)
        else:
            self._timer_count += 1
