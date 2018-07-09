
import paho.mqtt.client as mqtt
import mqtt_config as mqtt_c
import topic_config as topic_c
import DBC as dbc
import Rule as RuleClass

#Load MQTT Server Config from JSON File
conf=mqtt_c.read_mqtt_conf()

print "MQTT Server Config:"
print conf['mqtt_host'] + ":" + str(conf['mqtt_port']) + " " +  conf['mqtt_username'] + " " + conf['mqtt_password']

def on_connect(client, userdata, flags,rc):
    print("Connected with result code "+str(rc))
# Subscribe to all rule topics defined in RuleList
    for aRule in RuleList:
        client.subscribe(aRule.getTopic())

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

#Create Database Class
db = dbc.DBConnector()

#Connect to Database
db.connect()

#Load Topics List from JSON File
topic=topic_c.read_topic_conf()

RuleList=[]

#Parse Topics to be subscribed to from JSON File and add it to RuleList[]
for aTopic in topic.items():
    r=RuleClass.Rule(db,name=aTopic[0], topic=aTopic[1]['TOPIC'], tablename=aTopic[1]['TABLE'], insert=aTopic[1]['INSERT'])
    RuleList.append(r)


print str(len(RuleList)) + " topic rules added."

#MQTT paho Client
client = mqtt.Client()
if conf['mqtt_username'] != '':
    client.username_pw_set(conf['mqtt_username'],conf['mqtt_password'])
client.on_connect = on_connect
client.on_message = on_message

#Connect to MQTT Server
client.connect(conf['mqtt_host'], conf['mqtt_port'], 60)


client.loop_forever()
