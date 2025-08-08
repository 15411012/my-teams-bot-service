import logging
from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings, TurnContext
from botbuilder.schema import Activity
from flask import Flask, request, Response
from asyncio import run
from mybot_rag_impl_azurepipeline import get_mybot_response
from config import DefaultConfig

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

app = Flask(__name__)
CONFIG = DefaultConfig()
adapter_settings = BotFrameworkAdapterSettings(CONFIG.APP_ID, CONFIG.APP_PASSWORD)
adapter = BotFrameworkAdapter(adapter_settings)

# Respond to Teams messages
async def on_message_activity(turn_context: TurnContext):
    user_msg = turn_context.activity.text
    answer = get_mybot_response(user_msg)
    logging.info(f"Sending response: {answer}")
    await turn_context.send_activity(Activity(type="message", text=answer))


# Endpoint for Teams to talk to your bot
@app.route("/api/messages", methods=["POST"])
def messages():
    if request.headers.get("Content-Type", "").startswith("application/json"):
        body = request.json
    else:
        logging.warning("Unsupported media type")
        return Response("Unsupported Media Type", status=415)

    activity = Activity().deserialize(body)
    auth_header = request.headers.get("Authorization", "")

    try:
        logging.info(">>> Processing activity")
        run(adapter.process_activity(activity, auth_header, on_message_activity))
        logging.info(">>> Successfully processed activity")
        return Response(status=201)
    except Exception as error:
        logging.exception(">>> Error processing activity")
        return Response("Internal Server Error", status=500)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3978)
