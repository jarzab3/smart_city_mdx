#include <ESP8266WiFi.h>
#include <WiFiUdp.h>

// Network credentials need need changing here 
const char* ssid = "Air Pen express";
const char* password = "";

WiFiUDP Udp;
unsigned int localUdpPort = 8888;  // local port to listen on
char incomingPacket[255];  // buffer for incoming packets

//Last time receive packet, timestamp
unsigned long last_time_packet = 0;

unsigned long previousMillis = 0;        // will store last time LED was updated

// constants won't change:
const long interval = 10000;  

void setup()
{
  pinMode(D0, OUTPUT);
  pinMode(D2, OUTPUT);
  digitalWrite(D2, LOW); // Inverted Logic
  Serial.begin(115200);
  Serial.println();

  Serial.printf("Connecting to %s ", ssid);
  // IP adress need changing here for each individual traffic light 254,253,252 andd so on
  WiFi.config(IPAddress(192, 168, 200, 150), IPAddress(192, 168, 200, 1), IPAddress(255, 255, 255, 0));
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }
  Serial.println(" connected");

  Udp.begin(localUdpPort);
  Serial.printf("Now listening at IP %s, UDP port %d\n", WiFi.localIP().toString().c_str(), localUdpPort);
}

void random_run(){

      digitalWrite(D0, LOW); // Inverted Logic
      digitalWrite(D2, HIGH); // Inverted Logic
      Serial.println("LED ON");


      digitalWrite(D0, HIGH); // Inverted Logic 
      digitalWrite(D2, LOW); // Inverted Logic
      Serial.println("LED OFF");
}
unsigned long currentMillis = 0;

void loop()
{
  currentMillis = millis();
  int packetSize = Udp.parsePacket();
  if (packetSize)
  {
    // receive incoming UDP packets
    Serial.printf("Received %d bytes from %s, port %d Time: %d previousMillis: %d\n", packetSize, Udp.remoteIP().toString().c_str(), Udp.remotePort(), currentMillis, previousMillis);
    int len = Udp.read(incomingPacket, 255);
    if (len > 0)
    {
      incomingPacket[len] = 0;
    }
    Serial.printf("UDP packet contents: %s\n", incomingPacket);
    if (incomingPacket[0] == 'H') {
       currentMillis = 0;
      digitalWrite(D0, LOW); // Inverted Logic
      digitalWrite(D2, HIGH); // Inverted Logic
      Serial.println("LED ON");
    } else if (incomingPacket[0] == 'L') { 
       currentMillis = 0;
      digitalWrite(D0, HIGH); // Inverted Logic 
      digitalWrite(D2, LOW); // Inverted Logic
      Serial.println("LED OFF");
    }

  }    
  else if(currentMillis - previousMillis > interval) {
//     Run random displaying of red or green lights
      Serial.println("Random run");
      previousMillis = currentMillis;    
    }
    else{
      currentMillis= 0;
    }
    
    
}
