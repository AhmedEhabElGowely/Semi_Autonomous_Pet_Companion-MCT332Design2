#include <Servo.h>
#include <SoftwareSerial.h>

//Ultrasonic front
#define Front_Ultra_Echo A5
#define Front_Ultra_Trigger A4

//Ultrasonic right
#define Right_Ultra_Echo 2
#define Right_Ultra_Trigger 3

//Ultrasonic left
#define Left_Ultra_Echo 4
#define Left_Ultra_Trigger  5

//IR
#define IR_sensor A3

//Servo
//#define Servo_control 10
Servo FeedServo;
char msg_sent = 0;
char command = 'S';
//Laser
#define Laser 9
char Ultra_read (int echo , int trigger);

void setup()
{
  Serial.begin(57600);
  pinMode(Front_Ultra_Trigger, OUTPUT);
  pinMode(Front_Ultra_Echo, INPUT);

  pinMode(Right_Ultra_Trigger, OUTPUT);
  pinMode(Right_Ultra_Echo, INPUT);

  pinMode(Left_Ultra_Trigger, OUTPUT);
  pinMode(Left_Ultra_Echo, INPUT);

  pinMode(IR_sensor, INPUT);

  pinMode(Laser, OUTPUT);
  FeedServo.attach(10);
}

void loop()
{

  char Front_reading , Right_reading , Left_reading , IR_reading;
  Front_reading = Ultra_read (Front_Ultra_Echo, Front_Ultra_Trigger);

  Right_reading = Ultra_read (Right_Ultra_Echo, Right_Ultra_Trigger);

  Left_reading = Ultra_read (Left_Ultra_Echo, Left_Ultra_Trigger);

  IR_reading = digitalRead(IR_sensor);

  msg_sent =  (msg_sent & 0x00) | (Front_reading << 3) | (Right_reading << 2) | (Left_reading << 1) | (IR_reading << 0);
  Serial.write(msg_sent);
  delay (100); 
  if (Serial.available())
  {
    command = Serial.read();
    if (command == 'S')
    {
      digitalWrite(Laser, LOW);
      FeedServo.write(0);
    }
    else if (command == 'L')
    {
      digitalWrite(Laser, HIGH);
    }
    else if (command == 'F')
    {
      FeedServo.write(55);
      //my_delay(1000);
      //FeedServo.write(0);
    }
  }
}
/*
void my_delay(int time)
{
  int n = time / 10;
  int i = 0;
  while ( (i < n) && (command != 'S') )
  {
    check_command();
    delay (10);
    i++;
  }
}
*/
void check_command (void)
{
  //while (Serial.available())
  //{
  command = Serial.read();
  //}

}

char Ultra_read (int echo , int trigger)
{
  long duration, cm;
  char result;
  pinMode(trigger, OUTPUT);
  digitalWrite(trigger, LOW);
  delayMicroseconds(2);
  digitalWrite(trigger, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigger, LOW);
  pinMode(echo, INPUT);
  duration = pulseIn(echo, HIGH);
  cm = duration / 29 / 2;
  if (cm > 30)
  {
    result = 0;
  }
  else
  {
    result = 1;
  }
  return result;
}
