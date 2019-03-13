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
Vref = 3.32
 */

#include <LFlash.h>
#include <LSD.h>
#include <LStorage.h>
#include <Servo.h>
#include <Wire.h> // Used to establied serial communication on the I2C bus
#include "SparkFunTMP102.h" // Used to send and recieve specific information from our sensor
#define Drv LFlash          // use Internal 10M Flash
//#define Drv LSD           // use SD card

#include <LiquidCrystal_I2C.h> // Screen Setups
LiquidCrystal_I2C lcd(0x27,20,4);
TMP102 sensor0(0x48); // Initialize sensor at I2C address 0x48
Servo myservo;


boolean foo = 0; 
float temperature = 0.0;
uint32_t InterruptPinD2 = 0;
int screen = 1;
boolean measurement_flag = 0; 
int routine_time = 7000;
float current = 0.0;
float voltage = 0.0;
float hall_voltage = 0.0;



//---------------------------Current Sensor---------------------------
const int analogInPin = A0;

// Number of samples to average the reading over
// Change this to make the reading smoother... but beware of buffer overflows!
const int avgSamples = 10;

int sensorValue = 0;

float sensitivity = 66; //8122.4;//100.0 / 500.0; //100mA per 500mV = 0.2
float Vref = 2465; // Output voltage with no current: ~ 2500mV or 2.5V
//-------------------------------------------

void setup()
{

    lcd.init(); // Activate the LCD screen 
    lcd.backlight(); 
    lcd.print("Hello");
    delay(1000);
    lcd.clear();
    // Open serial communications and wait for port to open:
    Serial.begin(9600);
    myservo.attach(9);
    pinMode(2,INPUT_PULLUP);
    //digitalWrite(2,HIGH);
    pinMode(3,INPUT_PULLUP);
    attachInterrupt(1,ISR,FALLING); // 1 Corresponds to pin 3 (D3)
    interrupts();
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


  switch(screen)
  {
    case 1:
    {
      lcd.clear();
      lcd.print("Press button to");
      lcd.setCursor(0,1);
      lcd.print("Start");
      delay(500);
      if (measurement_flag == 1)
      {
        TestRoutine();
        measurement_flag = 0;
        
      }
    }
  }


  
}

float CheckVoltage()
{
  return voltage;
}

float CheckCurrent()
{
  current = 0.0;
  for (int i = 0; i < avgSamples; i++)
  {
    sensorValue += analogRead(analogInPin);

    // wait 2 milliseconds before the next loop
    // for the analog-to-digital converter to settle
    // after the last reading:
    delay(2);
  }
  sensorValue = sensorValue / avgSamples;

  // The on-board ADC is 10-bits -> 2^10 = 1024 -> 5V / 1024 ~= 4.88mV
  // The voltage is in millivolts
  
  //voltage = 4.88 * sensorValue;
  hall_voltage = (sensorValue/1024.0) * 5000; // to get mV

  // This will calculate the actual current (in mA)
  // Using the Vref and sensitivity settings you configure
  current = (hall_voltage - Vref) / sensitivity;
  
  return current; 
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

String DataRegister()
{ 
    String dataString = "";
    dataString += String(CheckVoltage());
    dataString += ",";
    dataString += String(CheckCurrent());
    dataString += ",";
    dataString += String(CheckTemp());
    return dataString;
}

void SaveToFile(String dataString)
{
     LFile dataFile = Drv.open("datalog2.csv", FILE_WRITE);

    // if the file is available, write to it:
    if (dataFile) 
      {
    dataFile.println(dataString);
    dataFile.close();
    // print to the serial port too:
      }
  // if the file isn't open, pop up an error:
     else 
     {
    Serial.println("error opening datalog.txt");
     }
}

void TestRoutine()
{
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("Test Initiated");
  delay(700);
  int time_point = millis();
  myservo.write(90);
  delay(1000);
  myservo.write(87);
  delay(500);
  myservo.write(84);
  delay(500);
  myservo.write(80); // Start motor
  delay(500);
  while ((millis()-time_point) < routine_time)
  {
    SaveToFile(DataRegister());

  }

  myservo.write(84);
  delay(500);
  myservo.write(87);
  delay(500);
  myservo.write(90); // Stop motor 
  lcd.clear();
  lcd.print("Test Completed");
  delay(1500);
}

void ISR()
{
  measurement_flag = 1;
}






