
int camera = 0;

void setup() {
        Serial.begin(9600);
        pinMode(13, OUTPUT);
}

void loop() {

        // send data only when you receive data:
        if (Serial.available() > 0) {
                // read the incoming byte:
                camera = Serial.read()-'0';

                if (camera == 0){
                    digitalWrite(13, LOW);
                }else{
                    digitalWrite(13, HIGH);
                }
        }
        
        //delay(10);
}
