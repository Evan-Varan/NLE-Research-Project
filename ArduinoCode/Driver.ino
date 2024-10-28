// Define Arduino pin connections to BTS7960
int RPWM = 5; // Right PWM to Arduino pin 5 (PWM capable)
int LPWM = 6; // Left PWM to Arduino pin 6 (PWM capable)
int R_EN = 7; // Right Enable to Arduino pin 7
int L_EN = 8; // Left Enable to Arduino pin 8
int R_IS = A0; // Right current sense pin connected to A0
int L_IS = A1; // Left current sense pin connected to A1

void setup() {
  // Set all the control pins as outputs
  pinMode(RPWM, OUTPUT);
  pinMode(LPWM, OUTPUT);
  pinMode(R_EN, OUTPUT);
  pinMode(L_EN, OUTPUT);
  //pinMode(buttonPin, INPUT);

  // Set the current sense pins as inputs
  pinMode(R_IS, INPUT);
  pinMode(L_IS, INPUT);

  // Start the serial monitor at 9600 baud
  Serial.begin(9600);

  // Enable both sides of the H-Bridge
  digitalWrite(R_EN, HIGH);
  digitalWrite(L_EN, HIGH);

  while (!Serial) {
    // Wait for the serial port to connect.
  }
  Serial.println("Arduino is ready to receive data...");  
}


void loop() {
  if (Serial.available() > 0) {  // Check if data is available on the serial port
    String data = Serial.readStringUntil('\n');  // Read incoming data until newline character
    Serial.println("Data received: " + data);  // Print received data for debugging

    // Process the data (as before)
    int comma1 = data.indexOf(',');
    int comma2 = data.indexOf(',', comma1 + 1);
    int comma3 = data.indexOf(',', comma2 + 1);

    String time_at_peak = data.substring(0, comma1);
    String num_cycles = data.substring(comma1 + 1, comma2);
    String duty_cycle = data.substring(comma2 + 1, comma3);
    String square_type = data.substring(comma3 + 1, data.length());


    // Send confirmation back to Python
    Serial.println("Time at Peak: " + time_at_peak + ", Num Cycles: " + num_cycles + ", Duty Cycle: " + duty_cycle );
    cycle(time_at_peak.toInt(), num_cycles.toInt(), duty_cycle.toFloat(), square_type);
  }

}

void cycle(int time_at_peak, int numCycles, float duty_cycle, String square_type){
  int period = (100/duty_cycle) * time_at_peak;
  int time_at_trough = period - time_at_peak;
  Serial.println("Time on: " + String(time_at_peak) + " Time off: " + String(time_at_trough));
  Serial.println("Cycle called with " + String(numCycles) + " cycles, and " + time_at_peak + " ms time at peak.");
  
  if(square_type == "negative"){
    for(int i = 0; i < numCycles; i++){
      // Drive one direction
      analogWrite(RPWM, 255); // Fully on
      analogWrite(LPWM, 0);   // Fully off
      delay(time_at_peak); // Adjust this delay for proper current measurement
      // Drive the other direction
      analogWrite(RPWM, 0);   // Fully off
      analogWrite(LPWM, 255); // Fully on
      delay(time_at_trough); // Adjust this delay for proper current measurement
    }
  }
  else if(square_type == "positive"){
    for(int i = 0; i < numCycles; i++){
      // Drive one direction
      analogWrite(RPWM, 255); // Fully on
      analogWrite(LPWM, 0);   // Fully off
      delay(time_at_peak); // Adjust this delay for proper current measurement

      analogWrite(RPWM, 0);   // Fully off
      analogWrite(LPWM, 0); // Fully on
      delay(time_at_trough); // Adjust this delay for proper current measurement
    }
  }
  Serial.println("Request Completed");
}



