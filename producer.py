from azure.servicebus import ServiceBusClient, ServiceBusMessage

CONNECTION_STR = "Connection String"
TOPIC_NAME = "orders"

with ServiceBusClient.from_connection_string(CONNECTION_STR) as client:

    sender = client.get_topic_sender(topic_name=TOPIC_NAME)

    with sender:

        normal_msg = ServiceBusMessage("Normal Order")
        normal_msg.application_properties = {
            "severity": "info"
        }

        error_msg = ServiceBusMessage("Order Failed")
        error_msg.application_properties = {
            "severity": "error"
        }

        sender.send_messages([normal_msg, error_msg])

print("Messages sent successfully!")