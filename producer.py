import json
import uuid
from datetime import datetime, timezone
from jsonschema import validate, ValidationError
from azure.servicebus import ServiceBusClient, ServiceBusMessage

CONNECTION_STR = "YOUR_CONNECTION_STRING

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

def create_message(message_type, severity, payload):
    return {
        "message_id": str(uuid.uuid4()),
        "message_type": message_type,
        "severity": severity,
        "source": "lab-one-7-python-producer",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "payload": payload
    }

def validate_message(message):
    validate(instance=message, schema=ORDER_SCHEMA)

def send_messages():
    messages_to_send = [
        create_message(
            "order",
            "info",
            {
                "order_id": "ORD-701",
                "customer": "Hafiz Shahzaib Rauf",
                "item": "Laptop Stand",
                "quantity": 1,
                "price": 29.99
            }
        ),
        create_message(
            "error",
            "error",
            {
                "error_code": "PAYMENT_FAILED",
                "description": "Payment could not be processed",
                "order_id": "ORD-702"
            }
        )
    ]

    with ServiceBusClient.from_connection_string(CONNECTION_STR) as client:
        sender = client.get_topic_sender(topic_name=TOPIC_NAME)

        with sender:
            for msg_body in messages_to_send:
                try:
                    validate_message(msg_body)

                    servicebus_msg = ServiceBusMessage(
                        json.dumps(msg_body),
                        subject=msg_body["message_type"],
                        content_type="application/json"
                    )

                    servicebus_msg.application_properties = {
                        "message_type": msg_body["message_type"],
                        "severity": msg_body["severity"],
                        "source": msg_body["source"]
                    }

                    sender.send_messages(servicebus_msg)

                    print("Sent message:")
                    print(json.dumps(msg_body, indent=2))

                except ValidationError as e:
                    print(f"JSON schema validation failed: {e.message}")

if __name__ == "__main__":
    send_messages()
    print("Lab One.7 messages sent successfully!")