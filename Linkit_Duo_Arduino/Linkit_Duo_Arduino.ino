
#include <ArduinoJson.h>
DynamicJsonBuffer jsonBuffer;

void setup() { 
    Serial.begin(115200);  // open serial connection to USB Serial //port(connected to your computer)           
    Serial1.begin(57600);  // open internal serial connection to MT7688   
    pinMode(9, OUTPUT);
}


void loop() { 
      String json = Serial1.readStringUntil('\n');      // read from MT7688
      //Serial.println(json);
      if (json.length()>0) {

          JsonObject& root = jsonBuffer.parseObject(json);
                  // Test if parsing succeeds.
            if (!root.success()) {
              Serial.println("parseObject() failed");
              return;
            }

            // Fetch values. "{\"gpio\":3,\"state\":1}"
            const char* device_name = root["device-name"];
            Serial.print("device-name=");
            Serial.print(device_name);
            int gpio = atoi(root["gpio"]);
            Serial.print(" GPIO=");
            Serial.print(gpio);
            int state = atoi(root["state"]);
            Serial.print(", State=");
            Serial.print(state);
            
            
            if(state==0) { 
                 //case "OFF":                // turn off D13 when receiving "0"
                  digitalWrite(gpio, LOW); 
                  Serial.println(" ==>Turning OFF");
            }else{
                  //case "ON":                // turn on D13 when receiving "1" 
                  digitalWrite(gpio, HIGH); 
                  Serial.println(" ==>Turning ON");
 
            } 
      } 
}
