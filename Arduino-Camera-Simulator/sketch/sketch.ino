int camera_old = 0;
int camera = 0;

void setup() {
        Serial.begin(9600);
        for(int i = 10; i < 14; i++){
            pinMode(i, OUTPUT);
            digitalWrite(i, LOW);
        }
}

void loop() {
        while (Serial.available() > 0){
            camera = Serial.parseInt();
            if (Serial.read() == '\n'){}
        }
        
        if (camera != camera_old){
            digitalWrite(camera_old, LOW);
            digitalWrite(camera, HIGH);
            camera_old = camera;
        }
}
