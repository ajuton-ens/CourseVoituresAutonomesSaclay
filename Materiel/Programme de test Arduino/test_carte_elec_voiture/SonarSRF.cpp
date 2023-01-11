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

#include "SonarSRF.h"
#include <Wire.h>

/// <summary>
/// Setting up the sensor
/// </summary>
/// <param name="address">I2C Address</param>
/// <param name="gainRegister">SRF Location 1</param>
/// <param name="rangeLocation">SRF Location 2</param>
SonarSRF::SonarSRF(int address, int gainRegister, int rangeLocation)
{
    _address = (uint8_t)(address);
    _gainRegister = (uint8_t)(gainRegister);
    _rangeLocation = (uint8_t)(rangeLocation);
}

/// <summary>
/// Initiates the connection with the sensor and start I2C bus
/// </summary>
void SonarSRF::begin(void)
{
    Wire.begin();
}

/// <summary>
/// Communicates with Sonar to send commands
/// </summary>
/// <param name="command">SRF Command</param>
/// <param name="addressRegister">SRF Location 0</param>
void SonarSRF::write(unsigned int command, unsigned int addressRegister)
{
    Wire.beginTransmission(_address); // Start I2C transmission
    Wire.write((uint8_t)(addressRegister));
    if (command != 0)
    {
        Wire.write((uint8_t)(command)); // Send command
        if (_gainRegister && _rangeLocation)
        {
            Wire.write(_gainRegister); // SRF Location 1
            Wire.write(_rangeLocation); // SRF Location 2
        }
    }
    Wire.endTransmission(); // End I2C transmission
}

/// <summary>
/// Sets Units for display / storage
/// </summary>
/// <remarks>
/// * 'i' for inches
/// * 'c' for centimeters
/// * 'm' for microseconds
/// </remarks>
/// <param name="unit">Unit used</param>
void SonarSRF::writeUnit(char unit)
{
    switch (unit)
    {
    case 'i':
        write(INCHES);
        break;
    case 'c':
        write(CENTIMETERS);
        break;
    case 'm':
        write(MICROSECONDS);
        break;
    default:
        Serial.println("Invalid units entered... using micro-seconds");
        write(MICROSECONDS);
    }
}

/// <summary>
/// Set a new address
/// </summary>
/// <remarks>
/// The address given in Arduino 7bit has to be converted back into SRF 8bit
/// newAddress can be set to any of E0, E2, E4, E6, E8, EA, EC, EE, F0, F2,
/// F4, F6, F8, FA, FC, FE.
/// </remarks>
/// <param name="newAddress">The new address</param>
void SonarSRF::writeAddress(unsigned int newAddress)
{
    write(0xA0);
    write(0xAA);
    write(0xA5);
    write(newAddress << 1);
}

/// <summary>
/// Read data from a command
/// </summary>
/// <param name="command">Reading operation command</param>
/// <param name="length">Expected length of the data</param>
int SonarSRF::read(unsigned int command, unsigned int length)
{
    write(0x00, command);
    Wire.requestFrom(_address, (uint8_t)(length)); // Request length bytes
    while (Wire.available() < length); // Wait for result while bytes available
    int res; // Read the bytes, and combine them into one int
    for (; length > 0; length--)
    {
        res += Wire.read() << (8 * (length - 1));
    }

    return res;
}

/// <summary>
/// Read data from register return result
/// </summary>
/// <param name="unit">Unit used</param>
/// <param name="andStart"></param>
/// <returns>The range number (two bytes)</returns>
/// <seealso cref="writeUnit"/>
uint16_t SonarSRF::readRange(char unit, bool andStart)
{
    if (andStart)
    {
        writeUnit(unit);
        waitForCompletion();
    }

    return (uint16_t)(read(RANGE_REGISTER, 2));
}

/// <summary>
/// Get software revision
/// </summary>
/// <returns>The software revision (one byte)</returns>
int8_t SonarSRF::readVersion(void)
{
    return (int8_t)(read(SOFTWARE_REVISION, 1));
}

/// <summary>
/// Wait for completion
/// </summary>
void SonarSRF::waitForCompletion(void)
{
    while (readVersion() == -1)
    {
        delay(1);
    }
}
