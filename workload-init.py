import Adafruit_DHT,time,rpi_ws281x,argparse,math
import RPi.GPIO as GPIO
from neopixel import *

# LED strip configuration:
LED_COUNT      = 32      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
# LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

# Define GPIO to LCD mapping
LCD_RS = 7
LCD_E  = 8
LCD_D4 = 25
LCD_D5 = 24
LCD_D6 = 23
LCD_D7 = 17

gktime=time.mktime(time.strptime("2023-06-07 00:00:00","%Y-%m-%d %H:%M:%S"))

GPIO.setmode(GPIO.BCM)
# Main program block
GPIO.setwarnings(False)
GPIO.setup(LCD_E, GPIO.OUT)  # E
GPIO.setup(LCD_RS, GPIO.OUT) # RS
GPIO.setup(LCD_D4, GPIO.OUT) # DB4
GPIO.setup(LCD_D5, GPIO.OUT) # DB5
GPIO.setup(LCD_D6, GPIO.OUT) # DB6
GPIO.setup(LCD_D7, GPIO.OUT) # DB7
# Initialise display


# DHT22 DEFINATIONS
DHT22_SENSOR = Adafruit_DHT.DHT22
DHT22_PIN = 4  #GPIO4


 
# Define some device constants
LCD_WIDTH = 16    # Maximum characters per line
LCD_CHR = True
LCD_CMD = False
 
LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
 
# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005
 
def main():
    lcd_init()
    while True:
        # Send some test
        lcd_string("Raspberry Pi",LCD_LINE_1)
        lcd_string("Class15, Grade1",LCD_LINE_2)
    
        time.sleep(2.5)
        Adafruit_DHT.read(DHT22_SENSOR, DHT22_PIN)
        time.sleep(2.5)
        humidity, temperature = Adafruit_DHT.read(DHT22_SENSOR, DHT22_PIN)
        if humidity is not None and temperature is not None:
            lcd_string('Temp:{0:0.1f}C'.format(temperature),LCD_LINE_1)
            lcd_string('Humidity:{0:0.1f}%'.format(humidity),LCD_LINE_2)
            time.sleep(5)

        lcd_string(time.strftime("%Y-%m-%d", time.localtime()),LCD_LINE_1)
        lcd_string(time.strftime("%H:%M", time.localtime()),LCD_LINE_2)

        time.sleep(5)
        lcd_string("Alarm Set",LCD_LINE_1)
        lcd_string("6:00",LCD_LINE_2)

        time.sleep(5)
        lcd_string("Time to Gaokao",LCD_LINE_1)
        lcd_string(str(math.ceil((gktime-time.time())/86400))+" Day(s)",LCD_LINE_2)

        time.sleep(5)
        lcd_string("Weather Today",LCD_LINE_1)
        lcd_string("9/-1 Light Rain",LCD_LINE_2)

        time.sleep(5)
 
def lcd_init():
    # Initialise display
    lcd_byte(0x33,LCD_CMD) # 110011 Initialise
    lcd_byte(0x32,LCD_CMD) # 110010 Initialise
    lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
    lcd_byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off
    lcd_byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
    lcd_byte(0x01,LCD_CMD) # 000001 Clear display
    time.sleep(E_DELAY)
 
def lcd_byte(bits, mode):
    # Send byte to data pins
    # bits = data
    # mode = True  for character
    #        False for command
    
    GPIO.output(LCD_RS, mode) # RS
    
    # High bits
    GPIO.output(LCD_D4, False)
    GPIO.output(LCD_D5, False)
    GPIO.output(LCD_D6, False)
    GPIO.output(LCD_D7, False)
    if bits&0x10==0x10:
        GPIO.output(LCD_D4, True)
    if bits&0x20==0x20:
        GPIO.output(LCD_D5, True)
    if bits&0x40==0x40:
        GPIO.output(LCD_D6, True)
    if bits&0x80==0x80:
        GPIO.output(LCD_D7, True)
    
    # Toggle 'Enable' pin
    lcd_toggle_enable()
    
    # Low bits
    GPIO.output(LCD_D4, False)
    GPIO.output(LCD_D5, False)
    GPIO.output(LCD_D6, False)
    GPIO.output(LCD_D7, False)
    if bits&0x01==0x01:
        GPIO.output(LCD_D4, True)
    if bits&0x02==0x02:
        GPIO.output(LCD_D5, True)
    if bits&0x04==0x04:
        GPIO.output(LCD_D6, True)
    if bits&0x08==0x08:
        GPIO.output(LCD_D7, True)
    
    # Toggle 'Enable' pin
    lcd_toggle_enable()
 
def lcd_toggle_enable():
    # Toggle enable
    time.sleep(E_DELAY)
    GPIO.output(LCD_E, True)
    time.sleep(E_PULSE)
    GPIO.output(LCD_E, False)
    time.sleep(E_DELAY)
 
def lcd_string(message,line):
    # Send string to display
    
    message = message.ljust(LCD_WIDTH," ")
    
    lcd_byte(line, LCD_CMD)
    
    for i in range(LCD_WIDTH):
        lcd_byte(ord(message[i]),LCD_CHR)

def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        
    time.sleep(wait_ms/1000.0)
    strip.show()


if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()
 
    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, ws.WS2811_STRIP_GRB)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    try:
        colorWipe(strip, Color(255,255,255))
        main()
    except KeyboardInterrupt:
        pass
    finally:
        lcd_byte(0x01, LCD_CMD)
        lcd_string("Goodbye!",LCD_LINE_1)
        GPIO.cleanup()