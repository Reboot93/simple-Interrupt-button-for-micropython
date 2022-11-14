# simple-Interrupt-button-for-micropython
Micropython Button Class Based on Hardware Interrupt and Timer
用于 micropython 的简单中断按钮类，使用Timer

## Usage
example: pin(25), pull=Pin.PULL_UP, trigger=Pin.IRQ_FALLING

``` python
from button import Button

def button_callback(pin, msg):
  if msg == 0:
    print('button single click | Pin: %s' % pin)
  elif msg == 1:
    print('%s : button long press | Pin: %s' % pin)

button = Button(25)
button.connect(button_callback)
button.setEnable(True)
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
|single_click_time|Click Maximum Duration|int|
|long_press_time|Long press the maximum duration|int|
|pull|Pin pull-up or pull-down|Pin.PULL_UP or Pin.PULL_DOWN|
|trigger|Interrupt trigger mode|According to different master controllers|
