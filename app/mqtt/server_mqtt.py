from logs.message_types import MessageTypes
from mqtt.custom_mqtt_class import CustomMQTTClass
from dcop_server.starter import Starter
from dcop_server.urgt_starter import UrgentStarter


class ServerMQTT(CustomMQTTClass):

    def __init__(self, hospital):
        CustomMQTTClass.__init__(self, "#")

        self.hospital = hospital
        self.starter = None
        self.client.urgent_msg_list = []

    def on_connect(self, client, obj, flags, rc):
        super().on_connect(client, obj, flags, rc)

        self.starter = Starter(self.hospital.zones, client)
        # self.starter = Starter(self.hospital.monitored_area_list, client)
        self.starter.start()

    def on_message(self, client, obj, msg):
        super().on_message(client, obj, msg)

        str_msg = str(msg.payload.decode('utf-8'))

        if self.client.SERVER_TOPIC in msg.topic:

            if MessageTypes.URGT.value in str_msg:

                urgt_thread = UrgentStarter(
                    self.starter,
                    client,
                    int(str_msg.split(MessageTypes.URGT.value + "_")[1]),
                )

                urgt_thread.start()
                return urgt_thread

            elif MessageTypes.VALUES.value in str_msg:

                client.value_msgs.append(str_msg)

            else:
                client.list_msgs_waiting.append(str_msg)
