/* Cece PROTOTYPE BENCH DIAGNOSTIC, not compiled or tested on hardware.
 * I2C scan, display and ultrasonic readings only. This sketch deliberately
 * does not command servos; disconnect servo power for initial tests. Audio,
 * LEDs, battery monitoring and walking are not implemented. Pin assignments
 * are provisional. Requires Adafruit SSD1306 and Adafruit GFX libraries.
 */
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
constexpr int SDA_PIN=0, SCL_PIN=1, TRIG_PIN=7, ECHO_PIN=10;
constexpr uint8_t PCA=0x44, OLED=0x3C;
Adafruit_SSD1306 display(128,32,&Wire,-1);
bool screen_ok=false, driver_ok=false;
uint32_t previous=0;
void setup() {
  Serial.begin(115200); Wire.begin(SDA_PIN,SCL_PIN);
  pinMode(TRIG_PIN,OUTPUT); pinMode(ECHO_PIN,INPUT); digitalWrite(TRIG_PIN,LOW);
  Wire.beginTransmission(PCA); driver_ok=Wire.endTransmission()==0;
  screen_ok=display.begin(SSD1306_SWITCHCAPVCC,OLED);
  Serial.println("Cece bench diagnostic; no servo control. Disconnect servo power.");
}
void loop() {
  if(millis()-previous<500) return; previous=millis();
  digitalWrite(TRIG_PIN,LOW); delayMicroseconds(2);
  digitalWrite(TRIG_PIN,HIGH); delayMicroseconds(10); digitalWrite(TRIG_PIN,LOW);
  unsigned long us=pulseIn(ECHO_PIN,HIGH,30000); float cm=us/58.0f;
  Serial.printf("distance: %s %.1f cm; driver: %s\n",us?"":"no echo",cm,driver_ok?"found":"missing");
  if(screen_ok) {
    display.clearDisplay(); display.setTextSize(1); display.setTextColor(SSD1306_WHITE);
    display.setCursor(0,0); display.println("Cece bench prototype");
    display.print("Range cm: "); if(us) display.println(cm,1); else display.println("no echo");
    display.print("Servo driver: "); display.println(driver_ok?"found":"missing");
    display.display();
  }
}
