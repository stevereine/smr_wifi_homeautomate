/************************************************************
ESP8266_Shield_Demo.h
SparkFun ESP8266 AT library - Demo
Jim Lindblom @ SparkFun Electronics
Original Creation Date: July 16, 2015
https://github.com/sparkfun/SparkFun_ESP8266_AT_Arduino_Library

This example demonstrates the basics of the SparkFun ESP8266
AT library. It'll show you how to connect to a WiFi network,
get an IP address, connect over TCP to a server (as a client),
and set up a TCP server of our own.

Development environment specifics:
  IDE: Arduino 1.6.5
  Hardware Platform: Arduino Uno
  ESP8266 WiFi Shield Version: 1.0

This code is released under the MIT license.

Distributed as-is; no warranty is given.
************************************************************/

/***************************************************************************
  This is a library for the BME280 humidity, temperature & pressure sensor

  Designed specifically to work with the Adafruit BME280 Breakout
  ----> http://www.adafruit.com/products/2650

  These sensors use I2C or SPI to communicate, 2 or 4 pins are required
  to interface. The device's I2C address is either 0x76 or 0x77.

  Adafruit invests time and resources providing this open source code,
  please support Adafruit andopen-source hardware by purchasing products
  from Adafruit!

  Written by Limor Fried & Kevin Townsend for Adafruit Industries.
  BSD license, all text above must be included in any redistribution
  See the LICENSE file for details.
 ***************************************************************************/

//////////////////////
// Library Includes //
//////////////////////
// SoftwareSerial is required (even you don't intend on
// using it).
#include <SoftwareSerial.h> 
#include <SparkFunESP8266WiFi.h>

//SoftwareSerial ESPSerial(19, 18); // RX, TX

//////////////////////////////
// WiFi Network Definitions //
//////////////////////////////
// Replace these two character strings with the name and
// password of your WiFi network.
const char mySSID[] = "Linksys00981";
const char myPSK[] = "tesla123";

//////////////////////////////
// ESP8266Server definition //
//////////////////////////////
// server object used towards the end of the demo.
// (This is only global because it's called in both setup()
// and loop()).
ESP8266Server server = ESP8266Server(80);

//////////////////
// HTTP Strings //
//////////////////
//const char destServer[] = "example.com";
//const String htmlHeader = "HTTP/1.1 200 OK\r\n"
//                          "Content-Type: text/html\r\n"
//                          "Connection: close\r\n\r\n"
//                          "<!DOCTYPE HTML>\r\n"
//                          "<html>\r\n";

//const String httpRequest = "GET / HTTP/1.1\n"
//                           "Host: example.com\n"
//                           "Connection: close\n\n";

// All functions called from setup() are defined below the
// loop() function. They modularized to make it easier to
// copy/paste into sketches of your own.

#include <Wire.h>
#include <SPI.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>

#include <Adafruit_BusIO_Register.h>
#include <Adafruit_I2CDevice.h>
#include <Adafruit_I2CRegister.h>
#include <Adafruit_SPIDevice.h>

#include <Adafruit_INA219.h>

#define BME_SCK 13
#define BME_MISO 12
#define BME_MOSI 11
#define BME_CS 10

#define SEALEVELPRESSURE_HPA (1013.25)

Adafruit_BME280 bme; // I2C
//Adafruit_BME280 bme(BME_CS); // hardware SPI
//Adafruit_BME280 bme(BME_CS, BME_MOSI, BME_MISO, BME_SCK); // software SPI

Adafruit_INA219 ina219;

unsigned long delayTime;

void setup() {
  // put your setup code here, to run once:

  pinMode(13,OUTPUT);
  pinMode(12,OUTPUT);
  pinMode(7,OUTPUT);
  pinMode(6,OUTPUT);
  digitalWrite(13, LOW);
  digitalWrite(12, LOW);
  digitalWrite(7, LOW);
  digitalWrite(6, LOW);

  // Serial Monitor is used to control the demo and view
  // debug information.
  Serial.begin(115200);
  while(!Serial);    // time to get serial running
  //Serial.println(F("BME280 test"));
  //serialTrigger(F("Press any key to begin."));

  // read the input on analog pin 0:
  int sensorValue = analogRead(A0);
  // Convert the analog reading (which goes from 0 - 1023) to a voltage (0 - 5V):
  float voltage = sensorValue * 3 * (5.0 / 1023.0);
  // print out the value you read:
  Serial.println(voltage);  

  // initializeESP8266() verifies communication with the WiFi
  // shield, and sets it up.
  initializeESP8266();

  // connectESP8266() connects to the defined WiFi network.
  connectESP8266();

  // displayConnectInfo prints the Shield's local IP
  // and the network it's connected to.
  displayConnectInfo();

  //serialTrigger(F("Press any key to connect client."));
  //clientDemo();

  unsigned status;
    
  // default settings

  if ( ina219.begin())
  Serial.println("Found INA219 chip");
  else
  Serial.println("Failed to find INA219 chip");

    
  status = bme.begin();  
  // You can also pass in a Wire library object like &Wire2
  // status = bme.begin(0x76, &Wire2)
  if (!status) {
      Serial.println("Could not find a valid BME280 sensor, check wiring, address, sensor ID!");
      Serial.print("SensorID was: 0x"); Serial.println(bme.sensorID(),16);
      Serial.print("        ID of 0xFF probably means a bad address, a BMP 180 or BMP 085\n");
      Serial.print("   ID of 0x56-0x58 represents a BMP 280,\n");
      Serial.print("        ID of 0x60 represents a BME 280.\n");
      Serial.print("        ID of 0x61 represents a BME 680.\n");
      while (1) delay(10);
    }
    
    //Serial.println("-- Default Test --");
    delayTime = 1000;

    //Serial.println();
  
  //serialTrigger(F("Press any key to test server."));
  serverSetup();


}

void loop() {
  // put your main code here, to run repeatedly:

  serverDemo();

}

void initializeESP8266()
{
  // esp8266.begin() verifies that the ESP8266 is operational
  // and sets it up for the rest of the sketch.
  // It returns either true or false -- indicating whether
  // communication was successul or not.
  // true
  
  int test = esp8266.begin();

  //if (esp8266.portmode==1)
  //  Serial.println(F("portmode = software"));

  //if (esp8266.portmode==2)
  //  Serial.println(F("portmode = hardware"));
  
  if (test != true)
  {
    Serial.println(F("Error talking to ESP8266."));
    errorLoop(test);
  }
  //Serial.println(F("ESP8266 Shield Present"));
}

void connectESP8266()
{
  // The ESP8266 can be set to one of three modes:
  //  1 - ESP8266_MODE_STA - Station only
  //  2 - ESP8266_MODE_AP - Access point only
  //  3 - ESP8266_MODE_STAAP - Station/AP combo
  // Use esp8266.getMode() to check which mode it's in:

  //esp8266.setMode(ESP8266_MODE_AP);
  
  int retVal = esp8266.getMode();
  if (retVal != ESP8266_MODE_STA)
  { // If it's not in station mode.
    // Use esp8266.setMode([mode]) to set it to a specified
    // mode.
    retVal = esp8266.setMode(ESP8266_MODE_STA);
    if (retVal < 0)
    {
      Serial.println(F("Error setting mode."));
      errorLoop(retVal);
    }
  }
  //Serial.println(F("Mode set to station mode"));

  // esp8266.status() indicates the ESP8266's WiFi connect
  // status.
  // A return value of 1 indicates the device is already
  // connected. 0 indicates disconnected. (Negative values
  // equate to communication errors.)
  retVal = esp8266.status();
  if (retVal <= 0)
  {
    Serial.print(F("Connecting to "));
    Serial.println(mySSID);
    // esp8266.connect([ssid], [psk]) connects the ESP8266
    // to a network.
    // On success the connect function returns a value >0
    // On fail, the function will either return:
    //  -1: TIMEOUT - The library has a set 30s timeout
    //  -3: FAIL - Couldn't connect to network.
    retVal = esp8266.connect(mySSID, myPSK);
    if (retVal < 0)
    {
      Serial.println(F("Error connecting"));
      errorLoop(retVal);
    }
  }
}

void displayConnectInfo()
{
  char connectedSSID[24];
  memset(connectedSSID, 0, 24);
  // esp8266.getAP() can be used to check which AP the
  // ESP8266 is connected to. It returns an error code.
  // The connected AP is returned by reference as a parameter.
  int retVal = esp8266.getAP(connectedSSID);
  if (retVal > 0)
  {
    Serial.print(F("Connected to: "));
    Serial.println(connectedSSID);
  }

  // esp8266.localIP returns an IPAddress variable with the
  // ESP8266's current local IP address.
  IPAddress myIP = esp8266.localIP();
  Serial.print(F("My IP: ")); Serial.println(myIP);
}

//void clientDemo()
//{
  // To use the ESP8266 as a TCP client, use the 
  // ESP8266Client class. First, create an object:
//ESP8266Client client;

  // ESP8266Client connect([server], [port]) is used to 
  // connect to a server (const char * or IPAddress) on
  // a specified port.
  // Returns: 1 on success, 2 on already connected,
  // negative on fail (-1=TIMEOUT, -3=FAIL).
//  int retVal = client.connect(destServer, 80);
//  if (retVal <= 0)
//  {
//    Serial.println(F("Failed to connect to server."));
//    return;
//  }

  // print and write can be used to send data to a connected
  // client connection.
//  client.print(httpRequest);

  // available() will return the number of characters
  // currently in the receive buffer.
//  while (client.available())
//    Serial.write(client.read()); // read() gets the FIFO char
  
  // connected() is a boolean return value - 1 if the 
  // connection is active, 0 if it's closed.
//  if (client.connected())
//    client.stop(); // stop() closes a TCP connection.
//}

void serverSetup()
{
  // begin initializes a ESP8266Server object. It will
  // start a server on the port specified in the object's
  // constructor (in global area)
  server.begin();
  Serial.print(F("Server started! Go to "));
  Serial.println(esp8266.localIP());
  Serial.println();
}

void serverDemo()
{
  // available() is an ESP8266Server function which will
  // return an ESP8266Client object for printing and reading.
  // available() has one parameter -- a timeout value. This
  // is the number of milliseconds the function waits,
  // checking for a connection.

  Serial.print(F("\r\nServer demo 1\r\n"));
  
  ESP8266Client client = server.available(500);
  String mystring;
  String returnstring;
  String returnstring_name;
  String returnstring_value;
  int name_index=0;
  int val_index=0;

  //printValues();
  delay(2000);

  Serial.print(F("\r\ntrying to connect....\r\n"));
  
  if (client) 
  {
    char buf[63];
    
    Serial.println(F("Client Connected!\r\n"));

    float sensorValue = analogRead(A0);
    float voltage = sensorValue * 3 * (5.0 / 1023.0);
    Serial.println(voltage);
    
    while (client.connected()) 
    {
      Serial.println(F("parsing sensor value...\r\n"));
      
      if (client.available()) 
      {
        Serial.println(F("client is available\r\n"));
        
        //mystring = client.readStringUntil('\r');
        mystring = client.readString();                
      }      
    }   

    Serial.print(mystring);
    Serial.print("\r\n\r\n");

    name_index=mystring.indexOf('**');
    //val_index=mystring.indexOf('^^');

    //sprintf(buf," name = %d value = %d \r\n", name_index, val_index);
    //sprintf(buf," name = %d\r\n", name_index);

    //returnstring=mystring.substring(name_index+2,name_index+6)+" "+mystring.substring(val_index+2,val_index+6);

    returnstring_name=mystring.substring(name_index+2,name_index+6);

    //Serial.println(F("\r\n"));

    if (returnstring_name=="dump")
      {
      char str_temp[63];
      char str_press[63];
      //char str_mypressure[63];
      String str_humid="";
      String str_mypressure="";

      int t = 100*bme.readTemperature();
      dtostrf(t,6,2,str_temp);

      int p = 100*(bme.readPressure()/100.0F);
      //Serial.println(bme.readPressure() / 100.0F);      
      dtostrf(p,8,2,str_press);

      int a = 100*bme.readHumidity();
      str_humid=String(a);
      //Serial.println(F("\r\n"));
      //Serial.println(str_humid);
      //Serial.println(F("\r\n"));

      //Serial.println(F("\r\n"));
      //Serial.println(str_press);
      //Serial.println(F("\r\n"));

      float mypressure = (bme.readPressure()/100.0F);
      str_mypressure=String(mypressure);

      str_mypressure = str_mypressure;

      //Serial.println(F("\r\n"));
      //Serial.println(str_mypressure);
      //Serial.println(F("\r\n"));

      String str_voltage = String(voltage);

      float shuntvoltage = 0;
      float busvoltage = 0;
      float current_mA = 0;
      float loadvoltage = 0;
      float power_mW = 0;

  shuntvoltage = ina219.getShuntVoltage_mV();
  busvoltage = ina219.getBusVoltage_V();
  current_mA = ina219.getCurrent_mA();
  power_mW = ina219.getPower_mW();
  loadvoltage = busvoltage + (shuntvoltage / 1000);
  
  Serial.print("Bus Voltage:   "); Serial.print(busvoltage); Serial.println(" V");
  Serial.print("Shunt Voltage: "); Serial.print(shuntvoltage); Serial.println(" mV");
  Serial.print("Load Voltage:  "); Serial.print(loadvoltage); Serial.println(" V");
  Serial.print("Current:       "); Serial.print(current_mA); Serial.println(" mA");
  Serial.print("Power:         "); Serial.print(power_mW); Serial.println(" mW");
      
      String comp_string = (String)str_temp + "HM" + str_humid + "PS" + str_mypressure + "VT" + str_voltage;
      
      comp_string = comp_string + "BV" + busvoltage + "SV" + shuntvoltage + "CU" + current_mA + "LV" + loadvoltage + "PW" + power_mW;

      //sprintf(buf, "%s*%s^%d", str_temp, a, str_mypressure);
      //sprintf(buf, "%s",str_temp);
      Serial.println(comp_string);
      //Serial.println(buf);
      //Serial.println("\r\nending the loop\r\n");
      Serial.println("\r\nprinting the string\r\n");
      client.print(comp_string);
      }

    Serial.println(F("\r\nClient disconnected"));

    client.stop();
  }
  
}

// errorLoop prints an error code, then loops forever.
void errorLoop(int error)
{
  Serial.print(F("Error: ")); Serial.println(error);
  Serial.println(F("Looping forever."));
  for (;;)
    ;
}

// serialTrigger prints a message, then waits for something
// to come in from the serial port.
void serialTrigger(String message)
{
  Serial.println();
  Serial.println(message);
  Serial.println();
  while (!Serial.available())
    ;
  while (Serial.available())
    Serial.read();
}

void printValues() {
    Serial.print("Temperature = ");
    Serial.print(bme.readTemperature());
    Serial.println(" *C");

    Serial.print("Pressure = ");

    Serial.print(bme.readPressure() / 100.0F);
    Serial.println(" hPa");

    Serial.print("Approx. Altitude = ");
    Serial.print(bme.readAltitude(SEALEVELPRESSURE_HPA));
    Serial.println(" m");

    Serial.print("Humidity = ");
    Serial.print(bme.readHumidity());
    Serial.println(" %");

    Serial.println();
}
