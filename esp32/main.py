import mfrc522_read
import machine
from machine import Pin, SoftI2C
from lcd_api import LcdApi
from i2c_lcd import I2cLcd
from time import sleep

# lcd setting
sdaPIN=machine.Pin(21)
sclPIN=machine.Pin(22)
I2C_ADDR = 0x3f
totalRows = 2
totalColumns = 16


if __name__ == '__main__':
    
    i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=10000)
    lcd = I2cLcd(i2c, I2C_ADDR, totalRows, totalColumns)
    while True:
        lcd.putstr("start")
        sleep(1)
        lcd.clear()
        uid = mfrc522_read.do_read()
        print('get uid')
        
        lcd.putstr(str(uid))
        sleep(1)
        lcd.clear()