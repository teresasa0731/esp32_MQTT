import paho.mqtt.client as mqtt

# Set the broker address and port
broker_address = "test.mosquitto.org"
port = 1883

mqtt_topic = "winston"

# Callback when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker")
        # Subscribe to a topic upon successful connection
        client.subscribe(mqtt_topic)
    else:
        print("Connection failed with code", rc)

# Callback when a message is received from the broker
def on_message(client, userdata, msg):
    print(f"Received message on topic {msg.topic}: {msg.payload.decode()}")

# Create an MQTT client instance
client = mqtt.Client()

# Set the callbacks
client.on_connect = on_connect
client.on_message = on_message

# Connect to the broker
client.connect(broker_address, port, keepalive=60)

# Start the MQTT client loop (this is a blocking call)
client.loop_start()

try:
    # Publish a message to the topic "test/topic"
    client.publish(mqtt_topic, "Hello, MQTT!")

    # Keep the program running to receive messages
    while True:
        pass

except KeyboardInterrupt:
    # Disconnect from the broker when the program is interrupted
    client.disconnect()
    client.loop_stop()
    print("Disconnected from MQTT Broker")
