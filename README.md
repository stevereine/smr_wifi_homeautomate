This project uses the following code files;

Python 3.5, whch uses PyQt5 and PyQtGraph
Arduino.ino

The following Arduino libraries;

SoftwareSerial (Arduino talk to ESP8266 wifi shield)
BME280 (Sparkfun BME280, via I2C, Arduino shield for temperature, humidity, atmos pressure)
INA219 (Sparkfun INA219, via I2C, Arduino shield for current and voltage measurement

and the following hardware;

Arduino Mega, seem to need this over the Uno for all the code that this includes
Sparkfun ESP8266 wifi shield
BME280
INA219
Velleman VMA203 LCD display shield

The project monitors remote temperature, humidity, and atmospheric pressure, as well as
the system voltage and current being drawn fro the source. Data points are taken every two
minutes and then continuously update a pyqtgraph plot.

The VMA203 displays the current temperature and IP address acquired by the ESP8266. The IP
addresses that your project acquires will likely be different than mine. Also, you will need
to add your own wifi SSID and password to the following code in the .ino file;

const char mySSID[] = "";
const char myPSK[] = "";

There is a lot of the ESP8266 example code left in the Arduino code. My apologies that I have not
cleaned this up.

I'm happy to help, please contact me if you have interest in this, or run into issues making it run.

Steve

s.reine@comcast.net
