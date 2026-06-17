import json
from jsonschema import validate, ValidationError
from azure.servicebus import ServiceBusClient

CONNECTION_STR = "YOUR_CONNECTION_STRING"
TOPIC_NAME = "orders"
SUBSCRIPTION_NAME = "everything"

ORDER_SCHEMA = {
    "type": "object",
    "required": ["message_id", "message_type", "severity", "source", "created_at", "payload"],
    "properties": {
        "message_id": {"type": "string"},
        "message_type": {"type": "string", "enum": ["order", "error"]},
        "severity": {"type": "string", "enum": ["info", "warning", "error"]},
        "source": {"type": "string"},
        "created_at": {"type": "string"},
        "payload": {"type": "object"}
    }
}

with ServiceBusClient.from_connection_string(CONNECTION_STR) as client:
    receiver = client.get_subscription_receiver(
        topic_name=TOPIC_NAME,
        subscription_name=SUBSCRIPTION_NAME
    )

    with receiver:
        messages = receiver.receive_messages(
            max_message_count=10,
            max_wait_time=5
        )

        for message in messages:
            try:
                body = str(message)
                data = json.loads(body)

                validate(instance=data, schema=ORDER_SCHEMA)

                print("Received valid JSON message:")
                print(json.dumps(data, indent=2))
                print("Message properties:")
                print(dict(message.application_properties))

                receiver.complete_message(message)

            except json.JSONDecodeError:
                print("Invalid JSON message received")
                receiver.dead_letter_message(message)

            except ValidationError as e:
                print(f"Schema validation failed: {e.message}")
                receiver.dead_letter_message(message)

print("Consumer finished.")