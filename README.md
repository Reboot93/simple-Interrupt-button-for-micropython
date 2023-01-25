# Micropython Button Class Based on Hardware Interrupt and Timer
用于 micropython 的简单中断按钮类，使用Timer


能够实现与分配定时器数量相同个数的按键同时检测，空闲按键数量不受定时器数量限制

可以检测：单击、长按、按住（通过告知 hold 与 release 实现）


It can realize simultaneous detection of keys with the same number as the number of allocated timers. The number of idle keys is not limited by the number of timers

Can be detected: click, hold and hold (realized by telling hold and release)

## Usage
example: ESP32, pin(25), pull=Pin.PULL_DOWN, trigger=Pin.IRQ_RISING

``` python
from button import Button

def button_callback(pin, msg):
  if msg == 0:
    print('Button Short Press | Pin: %s' % pin)
  elif msg == 1:
    print('Button Long Press | Pin: %s' % pin)

button = Button(25)
button.connect(button_callback)
button.setEnable(True)
```

## Set the number of timers (number)
设置定时器数量（编号）

在class Button中，通过给 timer_number_range 赋值 来设置定时器数量

In the class button, by giving the timer_ number_ Range assignment to set the number of timers

``` python
class Button:
    # 设置 定时器范围      eg. Timer(0),Timer(1),Timer(2),Timer(3) --> (0, 3)
    # Set timer range
    timer_number_range = (0, 3)

    # ================================================================
```


接受一个必要参数，5个可选参数

Accept one required parameter and five optional parameters

``` python
Button(pin, single_click_time=100, press_hold_time=350, pull=Pin.PULL_UP, trigger=Pin.IRQ_FALLING)
```
| argument       | description           | value |
|-------------|-------------|-----------|  
|pin|Input pin|int|

| Optional argument       | description           | value |
|-------------|-------------|-----------|  
|short_press_time|短按上限时间      Short Click Maximum Duration (The actual time depends on the timer interval)|int|
|press_hold_time|按住开始时间       Hold start duration (The actual time depends on the timer interval))|int|
|timer_interval|定时器间隔 timer interval (ms)|int|
|pull|上下拉 Pin pull-up or pull-down|Pin.PULL_UP or Pin.PULL_DOWN|
|trigger|上下沿触发 Interrupt trigger mode|According to different master controllers|

## Callback
| argument       | description           | value |
|-------------|-------------|-----------|  
|pin|Interrupt pin|int|
|msg|short press\long press\hold\release |int: short press 0, long press 1, hold 2, release 3|
