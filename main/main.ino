

#define NEXT_FRAME_INTERVAL 500
#define MSG_START 128
#define MSG_END 129
#define ACK_START 130
#define ACK_END 131

uint8_t resp_buf[24];
uint8_t recv_buf[24] = {0};
unsigned long currentMillis;
unsigned long previous_millis = 0;
bool msg_started = false;
int recv_index = 0;

void setup()
{
    Serial.begin(250000);
    pinMode(LED_BUILTIN, OUTPUT);
}

void loop()
{ // run over and over
    if (checkMessageComeplete())
    {
        // pretty_print();
        ack_response();
        zeroBuffer(recv_buf);
        recv_index = 0;
    }
    currentMillis = millis();
    if (currentMillis - previous_millis >= NEXT_FRAME_INTERVAL)
    {
        previous_millis = currentMillis;
        digitalWrite(LED_BUILTIN, HIGH);
        delay(100);
        digitalWrite(LED_BUILTIN, LOW);
        delay(500);
    }
}

void ack_response()
{
    // Serial.print(ACK_START);
    Serial.write(ACK_START);
    for (int i = 0; i < recv_index; i++)
    {
        Serial.write(recv_buf[i]);
    }
    Serial.write(ACK_END);
}

void pretty_print()
{
    Serial.print("[");
    for (int i = 0; i < recv_index - 1; i++)
    {
        Serial.print(recv_buf[i]);
        Serial.print(", ");
    }
    Serial.print(recv_buf[recv_index - 1]);
    Serial.print("]");
}

void zeroBuffer(uint8_t buf[])
{
    for (int i = 0; i < sizeof(buf); i++)
    {
        buf[i] = 0;
    }
}

int checkMessageComeplete()
{
    while (Serial.available())
    {
        if (!msg_started)
        {
            int msg_part = Serial.read();
            msg_started = msg_part == MSG_START;
        }
        else
        {
            int msg_part = Serial.read();
            if (msg_part == MSG_END)
            {
                msg_started = false;
                return 1;
            }
            else
            {
                recv_buf[recv_index] = msg_part;
                recv_index++;
            }
        }
    }
    return 0;
}