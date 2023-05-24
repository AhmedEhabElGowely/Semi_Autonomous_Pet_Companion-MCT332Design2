
//Front_Right Pins
#define FR_ENCA 2
#define FR_ENCB 22
#define FR_IN1 8 // 13
#define FR_IN2 12

//Rear_Right Pins
#define RR_ENCA 3
#define RR_ENCB 23
#define RR_IN1 11
#define RR_IN2 10

//Front_Left Pins
#define FL_ENCA 19
#define FL_ENCB 25
#define FL_IN1 9
#define FL_IN2 5 //8

//Rear_Left Pins
#define RL_ENCA 18
#define RL_ENCB 24
#define RL_IN1 7
#define RL_IN2 6

// globals
bool CW = true;
bool CCW = false;
long prevT = 0;

//PID Parameters
//KP
float FR_kp = 1.9;  //0.2,30,35(90)
float RR_kp = 1.775;  //0.2,30,35(90)
float FL_kp = 0.825;
float RL_kp = 7;

//Ki
float FR_ki = 5;  //0.5,17,19(90),16,
float RR_ki = 5;  //0.5,17,19(90),16,
float FL_ki = 0.003;
float RL_ki = 9;

//Kd
float FR_kd = 0.02;  //0.01
float RR_kd = 0.02;  //0.01
float FL_kd = 0.0015;
float RL_kd = 0.02;

int FR_posPrev = 0;
int RR_posPrev = 0;
int FL_posPrev = 0;
int RL_posPrev = 0;

// Use the "volatile" directive for variables
// used in an interrupt
volatile int FR_pos_i = 0;
volatile int RR_pos_i = 0;
volatile int FL_pos_i = 0;
volatile int RL_pos_i = 0;

float FR_v1Filt = 0;
float RR_v1Filt = 0;
float FL_v1Filt = 0;
float RL_v1Filt = 0;

float FR_v1Prev = 0;
float RR_v1Prev = 0;
float FL_v1Prev = 0;
float RL_v1Prev = 0;

float FR_eintegral = 0;
float RR_eintegral = 0;
float FL_eintegral = 0;
float RL_eintegral = 0;

float FR_ed = 0;
float RR_ed = 0;
float FL_ed = 0;
float RL_ed = 0;

float FR_ePrev = 0;
float RR_ePrev = 0;
float FL_ePrev = 0;
float RL_ePrev = 0;



void setup() {
  Serial.begin(57600);

  pinMode(FR_ENCA, INPUT);
  pinMode(FR_ENCB, INPUT);
  pinMode(FR_IN1, OUTPUT);
  pinMode(FR_IN2, OUTPUT);

  pinMode(RR_ENCA, INPUT);
  pinMode(RR_ENCB, INPUT);
  pinMode(RR_IN1, OUTPUT);
  pinMode(RR_IN2, OUTPUT);

  pinMode(FL_ENCA, INPUT);
  pinMode(FL_ENCB, INPUT);
  pinMode(FL_IN1, OUTPUT);
  pinMode(FL_IN2, OUTPUT);

  pinMode(RL_ENCA, INPUT);
  pinMode(RL_ENCB, INPUT);
  pinMode(RL_IN1, OUTPUT);
  pinMode(RL_IN2, OUTPUT);

  attachInterrupt(digitalPinToInterrupt(FR_ENCA), FR_readEncoder, RISING);
  attachInterrupt(digitalPinToInterrupt(RR_ENCA), RR_readEncoder, RISING);
  attachInterrupt(digitalPinToInterrupt(FL_ENCA), FL_readEncoder, RISING);
  attachInterrupt(digitalPinToInterrupt(RL_ENCA), RL_readEncoder, RISING);
}

void loop() 
{
  while (Serial.available())
  {
    char command = Serial.read();
    if (command == 'F')
    {
      Forward ();
    }
    else if (command == 'S')
    {
      Stop();
    }
    else if (command == 'R')
    {
      Rotate90Right ();
    }
    else if (command == 'L')
    {
      Rotate90Left();
    } 
    else if (command == 'B')
    {
      Back();
    }
    else if (command == 'O')
    {
      Rotate360Right ();
    }
    else if (command == 'D')
    {
      Dance();
    }   
  }
}

void setMotor(int direction, int speed, int pin1, int pin2) {
  int pwm = speed;
  if (direction == CW) {
    analogWrite(pin1, pwm);
    analogWrite(pin2, LOW);
  } else {
    analogWrite(pin2, pwm);
    analogWrite(pin1, LOW);
  }
}

void PID( int vt1 ,int vt2 , int vt3 , int vt4)
{
  // read the position and velocity
  int FR_pos = 0;
  int RR_pos = 0;
  int FL_pos = 0;
  int RL_pos = 0;

  noInterrupts();  // disable interrupts temporarily while reading
  FR_pos = FR_pos_i;
  RR_pos = RR_pos_i;
  FL_pos = FL_pos_i;
  RL_pos = RL_pos_i;
  interrupts();  // turn interrupts back on

  // Compute velocity with method 1
  long currT = micros();
  float deltaT = ((float)(currT - prevT)) / 1.0e6;

  float FR_velocity1 = (FR_pos - FR_posPrev) / deltaT;
  float RR_velocity1 = (RR_pos - RR_posPrev) / deltaT;
  float FL_velocity1 = (FL_pos - FL_posPrev) / deltaT;
  float RL_velocity1 = (RL_pos - RL_posPrev) / deltaT;  

  FR_posPrev = FR_pos;
  RR_posPrev = RR_pos;
  FL_posPrev = FL_pos;
  RL_posPrev = RL_pos;

  prevT = currT;

  // Convert count/s to RPM
  float FR_v1 = FR_velocity1 / 700 * 60.0;  //10x70
  float RR_v1 = RR_velocity1 / 700 * 60.0;  //10x70
  float FL_v1 = FL_velocity1 / 700 * 60.0;  //10x70
  float RL_v1 = RL_velocity1 / 700 * 60.0;  //10x70

  // Low-pass filter (25 Hz cutoff)
  FR_v1Filt = 0.854 * FR_v1Filt + 0.0728 * FR_v1 + 0.0728 * FR_v1Prev;
  RR_v1Filt = 0.854 * RR_v1Filt + 0.0728 * RR_v1 + 0.0728 * RR_v1Prev;
  FL_v1Filt = 0.854 * FL_v1Filt + 0.0728 * FL_v1 + 0.0728 * FL_v1Prev;
  RL_v1Filt = 0.854 * RL_v1Filt + 0.0728 * RL_v1 + 0.0728 * RL_v1Prev;
  

  FR_v1Prev = FR_v1;
  RR_v1Prev = RR_v1;
  FL_v1Prev = FL_v1;
  RL_v1Prev = RL_v1;

  // Compute the control signal FR_u

  float FR_e = vt1 - FR_v1Filt;
  float RR_e = vt2 - RR_v1Filt;
  float FL_e = vt3 - FL_v1Filt;
  float RL_e = vt4 - RL_v1Filt;

  FR_eintegral = FR_eintegral + FR_e * deltaT;
  RR_eintegral = RR_eintegral + RR_e * deltaT;
  FL_eintegral = FL_eintegral + FL_e * deltaT;
  RL_eintegral = RL_eintegral + RL_e * deltaT;

  FR_ed = (FR_e - FR_ePrev) / deltaT;
  RR_ed = (RR_e - RR_ePrev) / deltaT;
  FL_ed = (FL_e - FL_ePrev) / deltaT;
  RL_ed = (RL_e - RL_ePrev) / deltaT;

  float FR_u = FR_kp * FR_e + FR_ki * FR_eintegral + FR_kd * FR_ed;
  float RR_u = RR_kp * RR_e + RR_ki * RR_eintegral + RR_kd * RR_ed;
  float FL_u = FL_kp * FL_e + FL_ki * FL_eintegral + FL_kd * FL_ed;
  float RL_u = RL_kp * RL_e + RL_ki * RL_eintegral + RL_kd * RR_ed;


  // Set the motor speed and direction
  int FR_dir = CW;
  if (FR_u < 0) {
    FR_dir = CCW;
  }

  int RR_dir = CW;
  if (RR_u < 0) {
    RR_dir = CCW;
  }

  int FL_dir = CW;
  if (FL_u < 0) {
    FL_dir = CCW;
  }

  int RL_dir = CW;
  if (RL_u < 0) {
    RL_dir = CCW;
  }

//Check PWM
  int FR_pwr = (int)fabs(FR_u);
  if (FR_pwr > 255) {
    FR_pwr = 255;
  }
  
  int RR_pwr = (int)fabs(RR_u);
  if (RR_pwr > 255) {
    RR_pwr = 255;
  }

int FL_pwr = (int)fabs(FL_u);
  if (FL_pwr > 255) {
    FL_pwr = 255;
  }

  int RL_pwr = (int)fabs(RL_u);
  if (RL_pwr > 255) {
    RL_pwr = 255;
  }

  setMotor(FR_dir, FR_pwr, FR_IN1, FR_IN2);
  setMotor(RR_dir, RR_pwr, RR_IN1, RR_IN2);
  setMotor(FL_dir, FL_pwr, FL_IN1, FL_IN2);
  setMotor(RL_dir, RL_pwr, RL_IN1, RL_IN2);
}

void FR_readEncoder() {
  // Read encoder B when FR_ENCA rises
  int b = digitalRead(FR_ENCB);
  int increment = 0;
  if (b > 0) {
    // If B is high, increment forward
    increment = 1;
  } else {
    // Otherwise, increment backward
    increment = -1;
  }
  FR_pos_i = FR_pos_i + increment;
}

void RR_readEncoder() {
  // Read encoder B when RR_ENCA rises
  int b = digitalRead(RR_ENCB);
  int increment = 0;
  if (b > 0) {
    // If B is high, increment forward
    increment = 1;
  } else {
    // Otherwise, increment backward
    increment = -1;
  }
  RR_pos_i = RR_pos_i + increment;
}

void FL_readEncoder() {
  // Read encoder B when FL_ENCA rises
  int b = digitalRead(FL_ENCB);
  int increment = 0;
  if (b > 0) {
    // If B is high, increment forward
    increment = 1;
  } else {
    // Otherwise, increment backward
    increment = -1;
  }
  FL_pos_i = FL_pos_i + increment;
}

void RL_readEncoder() {
  // Read encoder B when RL_ENCA rises
  int b = digitalRead(RL_ENCB);
  int increment = 0;
  if (b > 0) {
    // If B is high, increment forward
    increment = 1;
  } else {
    // Otherwise, increment backward
    increment = -1;
  }
  RL_pos_i = RL_pos_i + increment;
}

void Brake(int in1 , int in2)
{
  analogWrite(in1, HIGH);
  analogWrite(in2, HIGH);

}

void Stop(void)
{
  Brake(FR_IN1 , FR_IN2);
  Brake(RR_IN1 , RR_IN2);
  Brake(FL_IN1 , FL_IN2);
  Brake(RL_IN1 , RL_IN2);
  delay(100);
  PID( 0 ,0, 0, 0);
}
void Forward (void)
{
PID( 90 , 90, 90, 90);
}
void Back (void)
{
PID( -90 , -90, -90, -90);
}
void Rotate360Right(void)
{
PID( -90 , -90, 90, 90);
//delay(6200);
}
void Rotate90Right(void)
{
PID( -90 , -90, 90, 90);
//delay(1490);
}
void Rotate360Left(void)
{
PID( 90 , 90, -90, -90);
  //delay(6250);
}
void Rotate90Left(void)
{
PID( 90 , 90, -90, -90);
  //delay(1500);
}
void Dance(void)
{
  MoveRight();
  delay(1000);
  Stop();
  Rotate360Left();
  delay(6250);
  Stop();
  MoveLeft();
  delay(1000); 
}
void MoveRight(void)
{

PID( -90 , 90, 90, -90);
}
void MoveLeft(void)
{

PID( 90 , -90, -90, 90);
}
