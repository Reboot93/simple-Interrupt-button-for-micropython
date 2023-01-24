# Micropython Button Class Based on Hardware Interrupt and Timer
用于 micropython 的简单中断按钮类，使用Timer


能够实现与分配定时器数量相同个数的按键同时检测，空闲按键数量不受定时器数量限制


It can realize simultaneous detection of keys with the same number as the number of allocated timers. The number of idle keys is not limited by the number of timers

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


接受一个必要参数，4个可选参数

Accept one required parameter and four optional parameters

``` python
Button(pin, single_click_time=130, long_press_time=210, pull=Pin.PULL_UP, trigger=Pin.IRQ_FALLING)
```
| argument       | description           | value |
|-------------|-------------|-----------|  
|pin|Input pin|int|

| Optional argument       | description           | value |
|-------------|-------------|-----------|  
|short_press_time|Click Maximum Duration|int|
|long_press_time|Long press the maximum duration|int|
|pull|Pin pull-up or pull-down|Pin.PULL_UP or Pin.PULL_DOWN|
|trigger|Interrupt trigger mode|According to different master controllers|

## Callback
| argument       | description           | value |
|-------------|-------------|-----------|  
|pin|Interrupt pin|int|
|msg|short press or long press|int: short press 0, long press 1|
