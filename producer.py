from azure.servicebus import ServiceBusClient, ServiceBusMessage

CONNECTION_STR = "TEST"
QUEUE_NAME = "queue1"

with ServiceBusClient.from_connection_string(CONNECTION_STR) as client:
    sender = client.get_queue_sender(queue_name=QUEUE_NAME)

    with sender:
        sender.send_messages(
            ServiceBusMessage("Hello from Azure Service Bus!")
        )

print("Message sent successfully!")
