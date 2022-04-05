"""
--------------------------------------------------------------------------
LCD Library
--------------------------------------------------------------------------
License:   
Copyright 2022 Samuel Sarver

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this 
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, 
this list of conditions and the following disclaimer in the documentation 
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors 
may be used to endorse or promote products derived from this software without 
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE 
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, 
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
--------------------------------------------------------------------------
"""

import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd
import time

LCD_COLUMNS = 16
LCD_ROWS = 2
'''lcd = characterlcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, LCD_COLUMNS, LCD_ROWS)

lcd.message = "qwertyuiopasdfgh\njklzxcvbnm"
'''
#print("test")

class LCD_Display():
    lcd_rs = None
    lcd_en = None
    lcd_d7 = None
    lcd_d6 = None
    lcd_d5 = None
    lcd_d4 = None
    lcd = None
    
    def __init__(self, lcd_rs=board.P2_10, lcd_en=board.P2_17, lcd_d4=board.P2_2, lcd_d5=board.P2_4, lcd_d6=board.P2_6, lcd_d7=board.P2_8):
        self.rs = digitalio.DigitalInOut(lcd_rs)
        self.en = digitalio.DigitalInOut(lcd_en)
        self.d4 = digitalio.DigitalInOut(lcd_d4)
        self.d5 = digitalio.DigitalInOut(lcd_d5)
        self.d6 = digitalio.DigitalInOut(lcd_d6)
        self.d7 = digitalio.DigitalInOut(lcd_d7)
        self.lcd = characterlcd.Character_LCD_Mono(self.rs, self.en, self.d4, self.d5, self.d6, self.d7, LCD_COLUMNS, LCD_ROWS)
        self._setup()
    
    def _setup(self):
        self.display("")
    
    def display(self, text):
        self.lcd.message = "                \n                "
        time.sleep(0.1)
        self.lcd.message = text

if __name__ == '__main__':
    disp = LCD_Display()
    #disp.display("abcdefghijklmnop\nqrstuv")
    disp.display("                \n                ")