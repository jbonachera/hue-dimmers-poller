# HUE Dimmers poller

Polls a philips HUE bridge, and reports button state change via MQTT.
Bridge IP and username are not automatically discovered yet: you have to create a username yourself.
See Philips HUE developper documentation for more information about HUE lightning system API: http://www.developers.meethue.com/.

Configuration parameters are passed to the application via environment variables:

| Env var | Description| Required | Default |
|---------|------------|----------|---------|
| MQTT_BROKER| mqtt broker to connect to| yes | None |
| MQTT_TOPIC| MQTT topic to publish to. '{}' will be replaced with the dimmer unique id| no | dimmer/{}|
| HUE_BRIDGE | HUE bridge IP| yes | None |
| HUE_USERNAME | HUE username to use| yes | None|

## How to run

```
docker run -it -e  MQTT_BROKER=<MQTT broker ip> -e HUE_BRIDGE=<HUE bridge IP> -e HUE_USERNAME=<HUE username> jbonachera/dimmers-poller
```
