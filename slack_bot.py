from slack_bolt.adapter.socket_mode.aiohttp import AsyncSocketModeHandler
from slack_bolt.async_app import AsyncApp
import asyncio
import aiohttp
import os
from dotenv import load_dotenv
load_dotenv()

"""
Todo:
- [x] show some logs while it's running
- [ ] find out more about timeouts and other things that might go wrong
- [ ] write an initial message warning of time it might take
"""

# Load environment variables
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
SLACK_APP_TOKEN = os.environ["SLACK_APP_TOKEN"]
API_SERVER_KEY = os.environ["API_SERVER_KEY"]
FORECAST_API_URL = "https://metaculus-bot-production.up.railway.app/forecast-binary"

app = AsyncApp(token=SLACK_BOT_TOKEN)

print("[INFO] Slack bot is starting up...")


@app.event("app_mention")
async def handle_app_mention(body, say, logger):
    print(f"[INFO] Received app_mention event: {body}")
    event = body.get("event", {})
    text = event.get("text", "")
    user = event.get("user", "")
    question = text.split(">", 1)[-1].strip()
    if not question:
        await say(f"<@{user}> Please provide a question after mentioning me.")
        return

    # Send an initial message to let the user know the process has started
    intro_message = (
        f"<@{user}> Thanks for your question! :crystal_ball:\n"
        "I'm thinking about it now. This may take a few minutes, so feel free to check back in this thread.\n"
        ":hourglass_flowing_sand: (The forecasting process can take up to 5 minutes or more.)"
    )
    await say(intro_message)

    print(f"[INFO] Sending question to forecasting API: {question}")
    try:
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    FORECAST_API_URL,
                    json={"question": question, "resolution_criteria": ""},
                    headers={"Authorization": f"Bearer {API_SERVER_KEY}"},
                    # 350 seconds, adjust as needed
                    timeout=aiohttp.ClientTimeout(total=350)
                ) as resp:
                    print(
                        f"[INFO] Forecast API response status: {resp.status}")
                    if resp.status == 200:
                        data = await resp.json()
                        print(f"[INFO] Forecast API response data: {data}")
                        prediction = data.get("prediction", "N/A")
                        reasoning = data.get(
                            "reasoning", "No reasoning provided.")
                        await say(f"*Prediction:* {prediction}\n*Reasoning:* {reasoning}")
                    else:
                        body = await resp.text()
                        print(f"[ERROR] Forecast API error body: {body}")
                        await say(f"Sorry, I couldn't get a forecast. (Status {resp.status})")
            except asyncio.TimeoutError:
                print("[ERROR] Forecast API request timed out.")
                await say("Sorry, the forecasting API took too long to respond. Please try again later.")
    except Exception as e:
        print(f"[ERROR] Exception during API call: {e}")
        await say(f"Sorry, an error occurred: {e}")


async def main():
    print("[INFO] Connecting to Slack via Socket Mode...")
    handler = AsyncSocketModeHandler(app, SLACK_APP_TOKEN)
    await handler.start_async()

if __name__ == "__main__":
    asyncio.run(main())
