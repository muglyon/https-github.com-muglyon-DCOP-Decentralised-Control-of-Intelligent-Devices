from helpers import log
from helpers.constants import Constants
from mqtt.mqtt_manager import MQTTManager


class EventObserver(object):

    def __init__(self, monitored_area, mqtt_client):
        self.monitored_area = monitored_area
        self.mqtt_manager = MQTTManager(mqtt_client, monitored_area)

    def notify_emergency(self):
        log.info("device enter in critical state", self.monitored_area.id, Constants.EVENT)
        self.mqtt_manager.publish_urgent_msg_to_server(self.monitored_area.id)

    def notify_intervention_detected(self):
        log.info("intervention detected (device reprog)", self.monitored_area.id, Constants.EVENT)
        self.monitored_area.tau = 0
