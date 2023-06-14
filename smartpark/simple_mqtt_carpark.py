from datetime import datetime

from config_parser import parse_config
import mqtt_device
import paho.mqtt.client as paho
from paho.mqtt.client import MQTTMessage


class CarPark(mqtt_device.MqttDevice):
    """Creates a carpark object to store the state of cars in the lot"""

    def __init__(self, config):
        super().__init__(config)
        self.total_spaces = config['total-spaces']
        self.total_cars = config['total-cars']
        self.client.on_message = self.on_message
        self.client.subscribe('sensor')
        self._temperature = None
        self.client.loop_forever()


    @property
    def available_spaces(self):
        available = self.total_spaces - self.total_cars
        return max(available, 0)

    @property
    def temperature(self):
        self._temperature
    
    @temperature.setter
    def temperature(self, value):
        self._temperature = value
        
    def _publish_event(self):
        readable_time = datetime.now().strftime('%H:%M')
        print(
            (
                f"TIME: {readable_time}, "
                + f"SPACES AVAILABLE: {self.available_spaces}, "
                + f"TEMPERATURE: {self._temperature}°C"
            )
        )
        message = (
            f"TIME: {readable_time}, "
            + f"SPACES AVAILABLE: {self.available_spaces}, "
            + f"TEMPERATURE: {self._temperature}°C"
        )
        self.client.publish('display', message)

    def on_car_entry(self):
        self.total_cars += 1
        self._publish_event()



    def on_car_exit(self):
        self.total_cars -= 1
        self._publish_event()

    def on_message(self, client, userdata, msg: MQTTMessage):
        payload = msg.payload.decode()
        payload = payload.split(",")
        print(payload)




        self.temperature = payload[1]
        if 'exit' in payload[0]:

            self.on_car_exit()
        else:
            self.on_car_entry()




if __name__ == '__main__':
    config = parse_config("package.json")
    car_park = CarPark(config)
    print("Car-park initialized")
    print("Car-park initialized")
