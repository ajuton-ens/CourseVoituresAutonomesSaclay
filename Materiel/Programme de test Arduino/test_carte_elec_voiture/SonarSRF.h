//
// SonarSRF
// Arduino Library for controlling SRF sonar sensors
// http://www.arduino.cc/playground/Main/SonarSrf08
//
// MIT License
// Copyright(c) 2009 Zach Foresta
// Copyright(c) 2012 Philipp A. Mohrenweiser
// Copyright(c) 2012-2016 Leo Colombaro
//

// Sensor connections:
// * SDA - Analog pin 4
// * SCL - Analog pin 5

#ifndef SONARSRF_H
#define SONARSRF_H

#include <Arduino.h>

// Read
#define SOFTWARE_REVISION 0x00
#define LIGHT_SENSOR      0x01
// Write
#define COMMAND_REGISTER  0x00
#define MAX_GAIN_REGISTER 0x01
#define RANGE_REGISTER    0x02
// Units
#define INCHES            0x50
#define CENTIMETERS       0x51
#define MICROSECONDS      0x52

class SonarSRF
{
private:
    uint8_t _address;
    uint8_t _gainRegister;
    uint8_t _rangeLocation;
public:
    SonarSRF(int address, int gainRegister = 0, int rangeLocation = 0);
    void begin(void);
    void writeAddress(unsigned int newAddress);
    uint16_t readRange(char unit = 'c', bool andStart = true);
    int8_t readVersion(void);
protected:
    void write(unsigned int command, unsigned int addressRegister = COMMAND_REGISTER);
    void writeUnit(char unit);
    int read(unsigned int command, unsigned int length);
    virtual void waitForCompletion(void);
};

#endif // SONARSRF_H
