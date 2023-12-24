import paho.mqtt.client as mqtt

# Set the broker address and port
broker_address = "172.20.10.3"
port = 1883

#MQTT setting
mq_id = 'server' 
mq_topic_input = b'uid'
mq_user='teresa'
mq_pass='12709155'
mq_topic_input = "uid"
mq_topic_output = "student_id"

students = {
    "Teresa": {
        "uid": "43600409",
        "id": "109033132",
        "state": False
    },
    "Tiger": {
        "uid": "2773188413",
        "id": "12345678",
        "state": False
    },
}

def roll_call(uid):
    for student_name, student_info in students.items():
        if student_info['uid'] == uid:
            student_info['state'] = True
            print(f"Student {student_name} checked in.")
            client.publish(mq_topic_output, student_info['id'])

# Callback when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker")
        # Subscribe to a topic upon successful connection
        client.subscribe(mq_topic_input)
        # Publish a message to the topic "uid"
        client.publish(mq_topic_input, "Hello, MQTT! from client")
    else:
        print("Connection failed with code", rc)

# Callback when a message is received from the broker
def on_message(client, userdata, msg):
    print(f"Received message on topic {msg.topic}: {msg.payload.decode()}")
    roll_call(msg.payload.decode())

if __name__ == '__main__':
    # Create an MQTT client instance
    client = mqtt.Client(client_id = mq_id)
    client.username_pw_set(mq_user,mq_pass)

    # Set the callbacks
    client.on_connect = on_connect
    client.on_message = on_message

    # Connect to the broker
    client.connect(broker_address, port, keepalive=60)

    # Start the MQTT client loop (this is a blocking call)
    client.loop_start()

    try:
        # Keep the program running to receive messages
        while True:
            pass

    except KeyboardInterrupt:
        # Disconnect from the broker when the program is interrupted
        client.disconnect()
        client.loop_stop()
        print("Disconnected from MQTT Broker")
