#include <Arduino.h>
#include <U8g2lib.h>
#include <Servo.h>
#include <BNO055_support.h>
#include <Wire.h>

#define BNO055_I2C_ADDR  0x28
#define srfAddress 0x70                           // Address of the SRF08
#define cmdByte 0x00                              // Command byte
#define lightByte 0x01                            // Byte to read light sensor
#define rangeByte 0x02                            // Byte for start of ranging data
 
byte highByte = 0x00;                             // Stores high byte from ranging
byte lowByte = 0x00;                              // Stored low byte from ranging
 
 
/*issu de l'exemple U8g2lib*/


// U8g2 Contructor List (Frame Buffer)
// The complete list is available here: https://github.com/olikraus/u8g2/wiki/u8g2setupcpp
U8G2_SH1106_128X64_NONAME_F_HW_I2C u8g2(U8G2_R0, /* reset=*/ U8X8_PIN_NONE);

//This structure contains the details of the BNO055 device that is connected. (Updated after initialization)
struct bno055_t myBNO;
struct bno055_euler myEulerData; //Structure to hold the Euler data


char chaine_caracteres[50]={}; //variables
char chaine_caracteres1[50]={};
int capteurIR_D_Pin = A2;
int capteurIR_D_Value;
int capteurIR_G_Pin = A1;
int capteurIR_G_Value;
int largeur_pulse_moteur = 0;
const int buttonPin2 = 3;     // the number of the pushbutton pin
const int ledPin4  =  20;      // the number of the LED pin
const int buttonPin1 = 2;     // the number of the pushbutton pin
const int ledPin3 =  21;      // the number of the LED pin
int FOURCHE_pin=14;
int buttonState2 = 0;         // variable for reading the pushbutton status
int buttonState1 = 0;
int sensorPin = A2;    // select the input pin for the potentiometer
int sensorValue = 0;  // variable to store the value coming from the sensor
int frequence = 0;
int capteurUS = 0;

Servo cmd_propulsion;  // create servo object pour contrôler la propulsion
Servo cmd_direction;  // create servo object pour contr$oler la direction

//fonction d'acquisition de la distance du télémètre ultrason  
int getRange(){                                   // This function gets a ranging from the SRF08
 
  int range = 0; 
 
  Wire.beginTransmission(srfAddress);             // Start communticating with SRF08
  Wire.write(cmdByte);                             // Send Command Byte
  Wire.write(0x51);                                // Send 0x51 to start a ranging
  Wire.endTransmission();
 
  delay(100);                                     // Wait for ranging to be complete
 
  Wire.beginTransmission(srfAddress);             // start communicating with SRFmodule
  Wire.write(rangeByte);                           // Call the register for start of ranging data
  Wire.endTransmission();
  Wire.requestFrom(srfAddress, 2);                // Request 2 bytes from SRF module
  
  while(Wire.available() < 2);                    // Wait for data to arrive
  highByte = Wire.read();                      // Get high byte
  lowByte = Wire.read();                       // Get low byte
 
  range = (highByte << 8) + lowByte;              // Put them together
 
  return(range);                                  // Returns Range
}
  

  
void setup(void) {
   //Initialization of the BNO055
  
  // initialize the LED pin as an output:
  pinMode(ledPin3, OUTPUT);
    //Initialize I2C communication
  Wire.begin();
  // initialize the pushbutton pin as an input:

  BNO_Init(&myBNO); //Assigning the structure to hold information about the device
  bno055_set_operation_mode(OPERATION_MODE_NDOF);
  delay(1);
  pinMode(buttonPin2 , INPUT);
   // initialize the LED pin as an output:
  pinMode(ledPin4, OUTPUT);
  // initialize the pushbutton pin as an input:
  pinMode(buttonPin1, INPUT);
  pinMode(FOURCHE_pin, INPUT);
  delay(1);
  cmd_propulsion.attach(9);  // attaches the servo on pin 9 to the servo object
  cmd_propulsion.write(90);  
  cmd_direction.attach(10);  // attaches the servo on pin 9 to the servo object
  cmd_direction.write(100);    
  u8g2.begin();
  u8g2.clearBuffer();
}

void loop(void) {

  capteurUS = getRange();
  bno055_read_euler_hrp(&myEulerData);
  buttonState2 = digitalRead(buttonPin2);// lectures des capteurs
  buttonState1 = digitalRead(buttonPin1);
  capteurIR_D_Value= analogRead(capteurIR_D_Pin);
  capteurIR_G_Value= analogRead(capteurIR_G_Pin);
  largeur_pulse_moteur = pulseIn(FOURCHE_pin, LOW);
  u8g2.clearBuffer();					// clear the internal memory
  
  u8g2.setFont(u8g2_font_ncenB08_tr);	// choose a suitable font
  sprintf(chaine_caracteres,"Yaw : %d",myEulerData.h);//affichage de l'ecran
  u8g2.drawStr(0,10,chaine_caracteres); 
  sprintf(chaine_caracteres,"Roll : %d",myEulerData.r);
  u8g2.drawStr(0,25,chaine_caracteres);
  sprintf(chaine_caracteres,"Pitch : %d",myEulerData.p);
  u8g2.drawStr(0,40,chaine_caracteres);
  sprintf(chaine_caracteres,"F : %d",largeur_pulse_moteur);
  u8g2.drawStr(0,55,chaine_caracteres);
  sprintf(chaine_caracteres,"IR_D = %d",capteurIR_D_Value);
  u8g2.drawStr(60,10,chaine_caracteres);
  sprintf(chaine_caracteres1,"IR_G = %d",capteurIR_G_Value);	
  u8g2.drawStr(60,25,chaine_caracteres1);
  sprintf(chaine_caracteres,"US = %d",capteurUS);
  u8g2.drawStr(70,40,chaine_caracteres); 
  u8g2.drawStr(30,62,"test en cours"); 
  u8g2.sendBuffer();					// transfer internal memory to the display
  delay(250);

  if (buttonState2 == LOW)//si bouton 2 pressé
  { 
    cmd_propulsion.write(120);//moteur tourne
    delay(1000);
    cmd_direction.write(80);//tourne a gauche
    digitalWrite(ledPin3, HIGH);//led 3 allumé
    tone(6, 523, 250);//musique
    delay(250);
    tone(6, 523, 250);
    delay(250);
    tone(6, 523, 250);
    delay(250);
    tone(6, 523, 250);
    delay(250);
    

  }else
  { 
    digitalWrite(ledPin3, LOW);//led 3 éteinte 
    cmd_propulsion.write(90); //moteur arrêté
    cmd_direction.write(100);// direction tout droit
    delay(100);
  }
  if (buttonState1 == LOW) //si bouton 1 pressé
{ digitalWrite(ledPin4, HIGH);//led 4 allumé
  tone(6, 523, 250);//musique
    delay(250);
    tone(6, 659, 250);
    delay(250);
    tone(6, 784, 250);
    delay(250);
    tone(6, 1047, 300);
    delay(500);
    tone(6, 523, 100);
    delay(100);
    tone(6, 659, 100);
    delay(100);
    tone(6, 784, 100);
    delay(100);
    tone(6, 1047, 100);
    delay(100);
    cmd_direction.write(120);
    cmd_propulsion.write(110); //moteur tourne 
    delay(1000);
} else
  { digitalWrite(ledPin4, LOW);//led éteinte  
    cmd_propulsion.write(90); //moteur arrêté
    cmd_direction.write(100);// direction tout droit
    delay(100);
  }
}
