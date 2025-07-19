from typing import AsyncIterable
import fastapi_poe as fp

SYSTEM_PROMPT = """
All your replies are Haikus.
""".strip()

class CodysWorkflowBot(fp.PoeBot):
    async def get_response(
        self, request: fp.QueryRequest
    ) -> AsyncIterable[fp.PartialResponse]:
        # Define the chain of bots to call in order
        bot_chain = ["Claude-3-Haiku", "Another-Bot-Name", "Third-Bot-Name"]

        # Start with the initial query including system prompt
        current_query = [fp.ProtocolMessage(role="system", content=SYSTEM_PROMPT)] + request.query

        # Iterate over each bot in the chain
        for bot_name in bot_chain:
            # Call the current bot with the current query
            response_messages = []
            async for msg in fp.stream_request(request, bot_name, request.access_key):
                response_messages.append(msg)

            # Prepare the query for the next bot using the collected response content
            # Assuming the last message content is the response text
            if response_messages:
                last_msg = response_messages[-1]
                current_query = [fp.ProtocolMessage(role="system", content=SYSTEM_PROMPT),
                                 fp.ProtocolMessage(role="user", content=last_msg.content)]
            else:
                # If no response, keep the current query unchanged
                pass

        # Finally, yield the messages from the last bot
        for msg in response_messages:
            yield msg
