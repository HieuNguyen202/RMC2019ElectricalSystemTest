#include <Arduino.h>
#include <Kangaroo.h>

HardwareSerial *server = &Serial2;
KangarooSerial  K(Serial1);
KangarooChannel K1(K, '1');
KangarooChannel K2(K, '2');
KangarooChannel K3(K, '3');
KangarooChannel K4(K, '4');

long maxSpeed;
long minSpeed;

enum Commands {
  CMD_FORWARD,
  CMD_BACKWARD,
  CMD_LEFT,
  CMD_RIGHT,
  CMD_STOP,
  CMD_RELEASE_MOTORS,
  CMD_RESET_ARDUINO,
};

struct Message {
  uint8_t commmand;
  int8_t value1;
  int8_t value2;
};

struct Message oMsg;
struct Message iMsg;

// Write the content of message m to server
void writeToServer() { server->write((byte *)&oMsg, sizeof(oMsg)); }

void send(uint8_t command, int8_t value1, int8_t value2) {
  oMsg.commmand = command;
  oMsg.value1 = value1;
  oMsg.value2 = value2;
  writeToServer();
}

void setupKangaroo(){
  Serial1.begin(9600);  //Kangaroo  
  K1.start();
  K2.start();
  K3.start();
  K4.start();
  minSpeed = K1.getMin().value();
  maxSpeed = K1.getMax().value();
}

void powerDownMotors(){
  K1.powerDown();
  K2.powerDown();
  K3.powerDown();
  K4.powerDown();
}

void forward(long speed){
  K1.s(speed);
  K2.s(speed);
  K3.s(speed);
  K4.s(speed);
}

void backward(long speed){
  K1.s(-speed);
  K2.s(-speed);
  K3.s(-speed);
  K4.s(-speed);
}

void right(long speed){
  K1.s(speed);
  K2.s(speed);
  K3.s(-speed);
  K4.s(-speed);
}

void left(long speed){
  K1.s(-speed);
  K2.s(-speed);
  K3.s(speed);
  K4.s(speed);
}

// Receive and execute a command from server
void serialReceive() {
    while (server->available() >= sizeof(iMsg)) {
      server->readBytes((byte *)&iMsg, sizeof(iMsg));  // Read new message
      switch (iMsg.commmand) {
        case CMD_FORWARD:
          Serial.print("serialReceive: CMD_FORWARD ");
          forward(iMsg.value1);
          break;
        case CMD_BACKWARD:
          Serial.print("serialReceive: CMD_BACKWARD ");
          backward(iMsg.value1);
          break;
        case CMD_LEFT:
          Serial.print("serialReceive: CMD_LEFT ");
          left(iMsg.value1);
          break;
        case CMD_RIGHT:
          Serial.print("serialReceive: CMD_RIGHT ");
          right(iMsg.value1);
          break;
        case CMD_STOP:
          Serial.print("serialReceive: CMD_STOP ");
          forward(0);
          break;
        case CMD_RELEASE_MOTORS:
          Serial.print("serialReceive: CMD_RELEASE_MOTORS ");
          powerDownMotors();
          break;
        case CMD_RESET_ARDUINO:
          Serial.print("serialReceive: CMD_RESET_ARDUINO ");
          break;
        default:
          Serial.print("serialReceive: Unknown command ");
          break;
      }
      Serial.print(iMsg.commmand);
      Serial.print(" ");
      Serial.print(iMsg.value1);
      Serial.print(" ");
      Serial.print(iMsg.value2);
      Serial.println("");
    }
  }






void setup() {
  Serial.begin(9600);   //Debug
  setupKangaroo();
  server->begin(9600);  //Tinker
  Serial.println("Setting up");
}
void loop() {
  serialReceive();
}