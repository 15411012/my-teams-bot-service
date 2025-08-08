import logging
import sys
import traceback
from datetime import datetime
from http import HTTPStatus

from aiohttp import web
from aiohttp.web import Request, Response, json_response
from botbuilder.core import TurnContext
from botbuilder.core.integration import aiohttp_error_middleware
from botbuilder.integration.aiohttp import CloudAdapter, ConfigurationBotFrameworkAuthentication
from botbuilder.schema import Activity, ActivityTypes

from mybot_rag_impl_azurepipeline import get_mybot_response
from config import DefaultConfig

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)


CONFIG = DefaultConfig()
print("MICROSOFT_APP_ID =", CONFIG.APP_ID)
print("MICROSOFT_APP_PASSWORD =", CONFIG.APP_PASSWORD)
print("MICROSOFT_APP_TENANT_ID =", CONFIG.APP_TENANTID)
# Create adapter
ADAPTER = CloudAdapter(ConfigurationBotFrameworkAuthentication(CONFIG))

# Catch-all for errors
async def on_error(context: TurnContext, error: Exception):
    print(f"\n [on_turn_error] unhandled error: {error}", file=sys.stderr)
    traceback.print_exc()

    await context.send_activity("The bot encountered an error or bug.")
    await context.send_activity("Please fix the bot source code to continue.")

    if context.activity.channel_id == "emulator":
        trace_activity = Activity(
            label="TurnError",
            name="on_turn_error Trace",
            timestamp=datetime.utcnow(),
            type=ActivityTypes.trace,
            value=f"{error}",
            value_type="https://www.botframework.com/schemas/error",
        )
        await context.send_activity(trace_activity)
ADAPTER.on_turn_error = on_error

# Message handler
async def on_message_activity(turn_context: TurnContext):
    user_msg = turn_context.activity.text
    answer = get_mybot_response(user_msg)
    logging.info(f"Sending response: {answer}")
    await turn_context.send_activity(Activity(type="message", text=answer))

# Main endpoint for Teams
async def messages(req: Request) -> Response:
    if "application/json" in req.headers.get("Content-Type", ""):
        body = await req.json()
    else:
        logging.warning("Unsupported media type")
        return Response(status=HTTPStatus.UNSUPPORTED_MEDIA_TYPE)

    activity = Activity().deserialize(body)
    auth_header = req.headers.get("Authorization", "")
    logging.info(">>> auth_header", auth_header)

    logging.info(">>> Processing activity")
    response = await ADAPTER.process_activity(auth_header, activity, on_message_activity)
    logging.info(">>> Successfully processed activity")
    if response:
        return json_response(data=response.body, status=response.status)
    return Response(status=HTTPStatus.OK)

# Setup web app
APP = web.Application(middlewares=[aiohttp_error_middleware])
APP.router.add_post("/api/messages", messages)


async def ping(request):
    return web.Response(text="Bot service is running good!", status=200)
APP.router.add_get("/ping", ping)



if __name__ == "__main__":
    try:
        web.run_app(APP, port=int(CONFIG.PORT))
    except Exception as error:
        raise error
