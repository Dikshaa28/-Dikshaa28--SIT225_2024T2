 #include <DHT.h>

#define DHTPIN 2      // Pin where the DHT22 sensor is connected
#define DHTTYPE DHT22  

DHT dht(DHTPIN, DHTTYPE);

void setup() {
    Serial.begin(9600); 
    dht.begin();         
}

void loop() {
    float temperature = dht.readTemperature();  
    float humidity = dht.readHumidity();        

    if (isnan(temperature) || isnan(humidity)) {
        Serial.println("Error reading from DHT sensor!");
    } else {
        Serial.print(temperature);
        Serial.print(",");
        Serial.println(humidity);
    }

    delay(2000);  // Reduce delay to 2 seconds for quicker updates
}  



