from machine import Pin, UART
import time

esp = UART(0, baudrate=9600, tx=Pin(16), rx=Pin(17))
# esp.init(bits=8, parity=None, stop=2)
esp.init()

# esp.write("crc32 off\n\r")

while True:
    
    esp.write(b"get echo\n\r")
    
    time.sleep(1)

    num_chars = esp.any()

    if num_chars > 0: 
        
        byte_str = esp.read(num_chars)
        str_str = ''.join([chr(b) for b in byte_str])
        print(str_str, end="")
        
    time.sleep(1)