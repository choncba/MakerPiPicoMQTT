from machine import Pin, UART, ADC
import json
import time
import _thread

esp = UART(0, baudrate=9600, tx=Pin(16), rx=Pin(17))
# esp.init(bits=8, parity=None, stop=2)
esp.init()

# Solo para prueba, leo el sensor de temperatura interno
sensor_temp = ADC(4)
conversion_factor = 3.3 / (65535)

def uart_rx():

    num_chars = esp.any()

    if num_chars > 0: 
        
        byte_str = esp.read(num_chars)
        str_str = ''.join([chr(b) for b in byte_str])
        print(str_str, end="")
        
    time.sleep(0.1)

def mqtt_publish(topic, payload):

    pub_cmd = f"publish {topic} {payload}\n\r"
    esp.write(bytes(pub_cmd, 'utf-8'))
    time.sleep(1)
    
    # rx_bytes = bytes()

    # if esp.any() > 0:
    #     while esp.any() > 0:
    #         rx_bytes += esp.read(1)

    #     rx_string = ''.join([chr(b) for b in rx_bytes])

    #     print(rx_string)
    #     return(rx_string)
    # else:
    #     return None

# _thread.start_new_thread(uart_rx, ())
_thread.start_new_thread(mqtt_publish, ("pico", "Hola"))

esp.write(b"subscribe pico/#\n\r")
time.sleep(1)

while True:
    reading = sensor_temp.read_u16() * conversion_factor
    temperature = 27 - (reading - 0.706)/0.001721
    print(f"{temperature} ºC")

    time.sleep(1)

