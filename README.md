# rpi-button-mqtt

publishes an mqtt message when a button is pushed

docker run -it \
-e MQTT_BROKER=localhost \
-e MQTT_PORT=1883 \
-e MQTT_PREFIX=prefix \
-e MQTT_TOPIC=topic \
-e MQTT_USER=homeassistant \
-e MQTT_PASSWORD=password \
-e LED_CHANNEL=18 \
-e LED_PWM_CYCLE=0.005 \
-e LED_NUM_FLASHES=3 \
--privileged \
--device /dev/mem:/dev/mem \
--net host \
jonaseck/rpi-led-flash-mqtt
