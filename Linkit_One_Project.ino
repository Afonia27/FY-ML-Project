/*
  SD card datalogger

 This example shows how to log data from three analog sensors
 to an SD card using the SD library.

 created  24 Nov 2010
 modified 9 Apr 2012
 by Tom Igoe
 
 
   port to LinkIt ONE
 by Loovee
 2014-10-12

 This example code is in the public domain.

 */

#include <LFlash.h>
#include <LSD.h>
#include <LStorage.h>
#include <Wire.h> // Used to establied serial communication on the I2C bus
#include "SparkFunTMP102.h" // Used to send and recieve specific information from our sensor
#define Drv LFlash          // use Internal 10M Flash
//#define Drv LSD           // use SD card

#include <LiquidCrystal_I2C.h> // Screen Setups
LiquidCrystal_I2C lcd(0x27,20,4);
TMP102 sensor0(0x48); // Initialize sensor at I2C address 0x48

boolean foo = 0; 
float temperature = 0.0;

void setup()
{

    lcd.init(); // Activate the LCD screen 
    lcd.backlight(); 
    lcd.print("Hello");
    delay(1000);
    lcd.clear();
    // Open serial communications and wait for port to open:
    Serial.begin(9600);
 
    //Serial.print("Initializing SD card...");
    //lcd.print("Initializing SD card...");
    // make sure that the default chip select pin is set to
    // output, even if you don't use it:
    pinMode(10, OUTPUT);
    delay(1000);
    // see if the card is present and can be initialized:
    Drv.begin();
    //Serial.println("card initialized.");
    //lcd.println("card initialized.");
    
    sensor0.begin(); // initialise the temp sensor
    // set the Conversion Rate (how quickly the sensor gets a new reading)
    //0-3: 0:0.25Hz, 1:1Hz, 2:4Hz, 3:8Hz
    sensor0.setConversionRate(2);
    //set Extended Mode.
    //0:12-bit Temperature(-55C to +128C) 1:13-bit Temperature(-55C to +150C)
    sensor0.setExtendedMode(0);

}

void loop()
{
  // make a string for assembling the data to log:
  String dataString = "";

  // read three sensors and append to the string:
  for (int analogPin = 0; analogPin < 3; analogPin++) {
    int sensor = analogRead(analogPin);
    dataString += String(sensor);
    if (analogPin < 2) {
      dataString += ",";
    }
  }
  lcd.print(CheckTemp());
  

  // open the file. note that only one file can be open at a time,
  // so you have to close this one before opening another.
 if (foo == 1){
  LFile dataFile = Drv.open("datalog.csv", FILE_WRITE);

  // if the file is available, write to it:
  if (dataFile) {
    dataFile.println(dataString);
    dataFile.close();
    // print to the serial port too:
    Serial.println(dataString);
    
  }
  // if the file isn't open, pop up an error:
  else {
    Serial.println("error opening datalog.txt");
  }
 }
 delay(500);
 lcd.clear();
}

float CheckTemp()
{
  float temperature;
  // Turn sensor on to start temperature measurement.
  // Current consumtion typically ~10uA.
  sensor0.wakeup();
  temperature = sensor0.readTempC(); // F for Fahrenheit
  // Place sensor in sleep mode to save power.
  // Current consumtion typically <0.5uA.
  sensor0.sleep();
  return temperature;
}









