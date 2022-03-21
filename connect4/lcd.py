import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd
import time

'''lcd_rs = digitalio.DigitalInOut(board.P2_10)
lcd_en = digitalio.DigitalInOut(board.P2_17)
lcd_d7 = digitalio.DigitalInOut(board.P2_8)
lcd_d6 = digitalio.DigitalInOut(board.P2_6)
lcd_d5 = digitalio.DigitalInOut(board.P2_4)
lcd_d4 = digitalio.DigitalInOut(board.P2_2)'''

LCD_COLUMNS = 16
LCD_ROWS = 2
'''lcd = characterlcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, LCD_COLUMNS, LCD_ROWS)

lcd.message = "qwertyuiopasdfgh\njklzxcvbnm"
'''
print("test")

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
    disp.display("abcdefghijklmnop\nqrstuv")