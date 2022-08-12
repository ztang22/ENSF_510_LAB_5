# code from https://peppe8o.com/using-raspberry-pi-with-dht11-temperature-and-humidity-sensor-and-python/
import time
import board
import adafruit_dht
import RPi.GPIO as GPIO

dhtDevice = adafruit_dht.DHT11(board.D17)
#Initial the dht device, with data pin connected to:
def temp_humidity():
    

    try:
         # Print the values to the serial port
        temperature_c = dhtDevice.temperature

        humidity = dhtDevice.humidity
        print("Temp: {:.1f} C    Humidity: {}% ".format(temperature_c, humidity))
        return [temperature_c,humidity]

    except RuntimeError as error:     # Errors happen fairly often, DHT's are hard to read, just keep going
         print(error.args[0])
    # time.sleep(2.0)

    
if __name__ =="__main__":
     while True:
          print(temp_humidity())
          time.sleep(2)


    