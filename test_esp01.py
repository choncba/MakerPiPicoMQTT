from machine import Pin, UART
import time
import binascii

esp = UART(0, baudrate=9600, tx=Pin(16), rx=Pin(17))
# esp.init(bits=8, parity=None, stop=2)
esp.init()

# esp.write("crc32 off\n\r")

def startup():
    
    print("ESP Response")
    espTX("get echo")
    time.sleep(0.5)
    print(espRX())

    print("WiFi Status")
    espTX("get wifistatus")
    time.sleep(0.5)
    print(espRX())

    print("MQTT Status")
    espTX("get mqttstatus")
    time.sleep(0.5)
    print(espRX())

    print("Subscribe to pico/#")
    espTX("subscribe pico/#")
    time.sleep(0.5)
    print(espRX())    


def espTX(msg):
    return esp.write(bytes(msg+"\n\r",'utf-8'))

def espRX():
    
    num_chars = esp.any()   # Lee el número de bytes en el buffer

    if num_chars > 0:       # Si hay
        byte_str = esp.read(num_chars)  # Lee los bytes del buffer
        str_str = ''.join([chr(b) for b in byte_str])   # Convierto el byte array a un string
        print(str_str)
        keys = str_str.split()  # El firmware del ESP manda "CRC32 [MENSAJE]", separo el string por espacios 
        crc_code = keys[0]      # Extraigo el código CRC32 de verificación
        data = keys[1]          # Extraigo el mensaje
        data_crc = str(binascii.crc32(data)) # Codifico el mensaje en CRC32
        if crc_code in data_crc:    # Si el mensaje esta correcto
            return data             # lo devuelvo

    return None                 # Si no, None

startup()
print("Wait for MQTT Message")

while True:
    
    #esp.write(b"get echo\n\r")
    #time.sleep(1)

    msj = espRX()
    if msj:
        print(msj)
        
    time.sleep(1)