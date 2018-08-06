import paho.mqtt.client as mqtt


class MQTTHandlerClass(object):
    def __init__(self):
        self.client = None
        self.conf = None
        super(MQTTHandlerClass, self).__init__()

    def setRuleList(self, rl):
        self.RuleList = rl

    def connect_to_server(self, conf):
        # MQTT paho Client
        self.client = mqtt.Client()
        self.conf = conf

        if conf['mqtt_username'] != '':
            self.client.username_pw_set(conf['mqtt_username'], conf['mqtt_password'])

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        # Connect to MQTT Server
        self.client.connect(conf['mqtt_host'], conf['mqtt_port'], 60)

    def on_connect(self, client, userdata, flags,rc):
        print("Connected with result code "+str(rc))
    # Subscribe to all rule topics defined in RuleList
        for aRule in self.RuleList:
            client.subscribe(aRule.getTopic())

    def on_message(self, client, userdata, msg):
        # Find correct rule from RuleList
        # Pass message JSON Payload to Rule for writing to correct table

        # Loop through RuleList and find if message topic applies
        for aRule in self.RuleList:
            if mqtt.topic_matches_sub(aRule.getTopic(), msg.topic):
                aRule.message_in(msg=msg)
                # print msg.payload
        # Call RuleList message_in method
