import Adafruit_DHT,time

sensor = Adafruit_DHT.DHT22

pin = 4  #GPIO4

f = open("out.txt", "w")
while True:
    Adafruit_DHT.read(sensor, pin)
    time.sleep(2.5)
    humidity, temperature = Adafruit_DHT.read(sensor, pin)
    if humidity is not None and temperature is not None:
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),'Temp={0:0.1f}℃  Humidity={1:0.1f}%'.format(temperature, humidity),file=f)
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),'Temp={0:0.1f}℃  Humidity={1:0.1f}%'.format(temperature, humidity))
    else:
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),"ErrorGettingData",file=f)
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),"ErrorGettingData")
    f.flush()
    time.sleep(60)
