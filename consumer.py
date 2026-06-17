from azure.servicebus import ServiceBusClient

CONNECTION_STR = "Connection STring"
TOPIC_NAME = "orders"
SUBSCRIPTION_NAME = "everything"

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
            print("Received:")
            print(str(message))
            receiver.complete_message(message)

print("Done!")