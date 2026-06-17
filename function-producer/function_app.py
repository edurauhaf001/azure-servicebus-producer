import azure.functions as func
from azure.servicebus import ServiceBusClient, ServiceBusMessage
import os

app = func.FunctionApp()

@app.route(route="ServiceBusHttpProducer", auth_level=func.AuthLevel.ANONYMOUS)
def ServiceBusHttpProducer(req: func.HttpRequest) -> func.HttpResponse:
    connection_str = os.getenv("AZURE_SERVICEBUS_CONNECTION_STRING")
    topic_name = "orders"

    message_text = req.params.get("message", "Hello from Azure Function")
    severity = req.params.get("severity", "info")

    try:
        with ServiceBusClient.from_connection_string(connection_str) as client:
            sender = client.get_topic_sender(topic_name=topic_name)

            with sender:
                message = ServiceBusMessage(message_text)
                message.application_properties = {
                    "severity": severity
                }
                sender.send_messages(message)

        return func.HttpResponse(
            f"Message sent successfully: {message_text}, severity={severity}",
            status_code=200
        )

    except Exception as e:
        return func.HttpResponse(
            f"Error: {str(e)}",
            status_code=500
        )