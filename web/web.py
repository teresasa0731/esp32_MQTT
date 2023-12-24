from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import paho.mqtt.client as mqtt

app = Flask(__name__)
socketio = SocketIO(app)

# MQTT setting
mqtt_server = '172.20.10.3'
mqtt_id = 'web' 
mqtt_topic_input = "student_id"
mqtt_topic_check = "device_check"
mqtt_user = 'teresa'
mqtt_pass = '12709155'

students = {
    "Teresa": {
        "id": "109033132",
        "state": False
    },
    "Tiger": {
        "id": "12345678",
        "state": False
    },
}

# Callback when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker")
        # Subscribe to topics upon successful connection
        client.subscribe(mqtt_topic_input)
        client.subscribe(mqtt_topic_check)
        # Publish a message to the topic "device_check" if not already published
        client.publish(mqtt_topic_check, "Hello, MQTT! from web")
    else:
        print("Connection failed with code", rc)

# Callback when a message is received from the broker
def on_message(client, userdata, msg):
    print(f"Received message on topic {msg.topic}: {msg.payload.decode()}")
    if msg.topic == mqtt_topic_input:
        student_id = msg.payload.decode()
        for student, info in students.items():
            if info['id'] == student_id:
                info['state'] = True
                print(student_id)
                socketio.emit('update_table', students, broadcast=True) 

@app.route('/')
def index():
    return render_template('index.html', students=students)

if __name__ == '__main__':
    # Create an MQTT client instance
    mqtt_client = mqtt.Client(client_id=mqtt_id)
    mqtt_client.username_pw_set(mqtt_user, mqtt_pass)

    # Set the callbacks
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    # Connect to the broker
    mqtt_client.connect(mqtt_server, 1883)

    # Start the MQTT client loop (this is a blocking call)
    mqtt_client.loop_start()
    
    socketio.run(app, debug=True)
