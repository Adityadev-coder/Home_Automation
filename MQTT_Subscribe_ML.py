import sklearn
import random
import pickle

from sklearn.neighbors import KNeighborsClassifier
from paho.mqtt import client as mqtt_client

broker = '52.66.6.183'
port = 1883
topic = "notification"
# Generate a Client ID with the subscribe prefix.
client_id = f'subscribe-{random.randint(0, 100)}'

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    client = mqtt_client.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        r=0
        r=int(msg.payload.decode())+100
        #ML code starts here
        #print(sklearn.__version__)
        model_pkl_file = "ML_model_latest.pkl"

        with open(model_pkl_file, 'rb') as file:
            model = pickle.load(file)

        r1=[]
        r1.append(r)
        result = int(model.predict([r1]))
        print("Res=",result)
        if result == 1:
            client.publish("notification", "OFF")
        else:
            client.publish("notification", "ON")

    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()
