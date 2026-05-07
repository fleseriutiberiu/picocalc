
const int BUFF_SIZE = 32; // make it big enough to hold your longest command
static char buffer[BUFF_SIZE+1]; // +1 allows space for the null terminator
static int length = 0; // number of characters currently in the buffer
static unsigned long lastKeepAliveTime = 0; // track time for keep-alive messages
const unsigned long KEEP_ALIVE_INTERVAL = 15000; // 15 seconds in milliseconds

void setup() {
  pinMode(13, OUTPUT);
  pinMode(7, OUTPUT);
  Serial.begin(115200);
  // put your setup code here, to run once:
}

void loop() {
  handleSerial();
  handleKeepAlive();
}

void handleKeepAlive()
{
  // Send keep-alive message every 15 seconds
  unsigned long currentTime = millis();
  if(currentTime - lastKeepAliveTime >= KEEP_ALIVE_INTERVAL) {
    Serial.println("GateKeepAlive");
    lastKeepAliveTime = currentTime;
  }
}

void handleSerial()
{
    if(Serial.available())
    {
        char c = Serial.read();
        if((c == '\r') || (c == '\n'))
        {
            // end-of-line received
            if(length > 0)
            {
                handleReceivedMessage(buffer);
            }
            length = 0;
        }
        else
        {
            if(length < BUFF_SIZE)
            {
                buffer[length++] = c; // append the received character to the array
                buffer[length] = 0; // append the null terminator
            }
            else
            {
                // buffer full - discard the received character
            }
        }
    }
}

void handleReceivedMessage(char *msg)
{
// strip message from receiver node so only the message remains

  char *semicolon_pos = strchr(msg, ':');
  char message_stripped[BUFF_SIZE+1] = "";
  if(semicolon_pos != NULL)
  {
    //2 is added because after semicolon we have a space we need to eliminate
    strcpy(message_stripped, semicolon_pos + 2);
    Serial.print(message_stripped);
  }
  
//strip message from receiver node so only the message remains


  if(strcmp(message_stripped, "salut") == 0)
  {
    // handle the command "on"
    // 13 is the onboard LED
    digitalWrite(13, HIGH); 
    digitalWrite(7, HIGH); 
    delay(200);
    digitalWrite(7, LOW);
    digitalWrite(13, LOW); 
    
  }
  else
  {
    digitalWrite(13, LOW);    
    digitalWrite(7, LOW); 
  }
}
