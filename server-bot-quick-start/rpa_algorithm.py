from typing import AsyncIterable
import fastapi_poe as fp

SYSTEM_PROMPT = """
You are an RAAP (Robotic Autonomous Algorithmic Process) bot. Your task is to autonomously execute algorithmic processes in a structured and efficient manner.
""".strip()

class RaapAlgorithmBot(fp.PoeBot):
    async def get_response(
        self, request: fp.QueryRequest
    ) -> AsyncIterable[fp.PartialResponse]:
        # Define the sequence of bots or steps in the RAAP workflow
        raap_steps = [
            "Data-Extraction-Bot",
            "Data-Processing-Bot",
            "Report-Generation-Bot"
        ]

        current_query = [fp.ProtocolMessage(role="system", content=SYSTEM_PROMPT)] + request.query

        for bot_name in raap_steps:
            response_messages = []
            async for msg in fp.stream_request(request, bot_name, request.access_key):
                response_messages.append(msg)

            if response_messages:
                last_msg = response_messages[-1]
                current_query = [fp.ProtocolMessage(role="system", content=SYSTEM_PROMPT),
                                 fp.ProtocolMessage(role="user", content=last_msg.content)]
            else:
                # If no response, keep the current query unchanged
                pass

        for msg in response_messages:
            yield msg
