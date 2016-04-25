# HUE Dimmers poller

Polls a philips HUE bridge, and reports button state change via MQTT.
I use this poller to set the light temperature of my HUE lights according to the current time (it does not seem possible to do this with the HUE bridge without creating dozen of "if time is between.." rules), by sending MQTT event to an external processor.

Bridge IP and username are not automatically discovered yet: you have to create a username yourself.
See Philips HUE developper documentation for more information about HUE lightning system API: http://www.developers.meethue.com/.

Configuration parameters are passed to the application via environment variables:

| Env var | Description| Required | Default |
|---------|------------|----------|---------|
| MQTT_BROKER| mqtt broker to connect to| yes | None |
| MQTT_TOPIC| MQTT topic to publish to. '{}' will be replaced with the dimmer unique id| no | dimmer/{}|
| HUE_BRIDGE | HUE bridge IP| yes | None |
| HUE_USERNAME | HUE username to use| yes | None|
| SLEEP_TIME | Time to sleep between 2 polls | no | 0.3s |

## How to run

```
docker run -it -e  MQTT_BROKER=<MQTT broker ip> -e HUE_BRIDGE=<HUE bridge IP> -e HUE_USERNAME=<HUE username> jbonachera/dimmers-poller
```

## Known issues

* Because we poll the bridge, and we are not reacting to events from it, we sometimes miss events. This is not something that bother me however.
* There is currently no parameter validation, or clean error messages.
