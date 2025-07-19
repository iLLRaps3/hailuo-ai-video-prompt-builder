from typing import AsyncIterable
import fastapi_poe as fp
import random
import re
import aiohttp
import asyncio

SYSTEM_PROMPT = """
You are a Rap Algorithm bot. Your task is to generate rap lyrics and content that cover every aspect of rap culture, style, and music. Your responses should be creative, fresh, never corny or predictable, and reflect authentic hip hop artistry. Use idioms, metaphors, rhyme density, and syllable selections to enhance the lyrics. You also have a system that searches the internet for rap lyrics and transforms them into thematic maps.
""".strip()

# A more advanced rap algorithm incorporating idioms, metaphors, rhyme density, syllable selections
IDIOMS = [
    "break the ice", "hit the spot", "spill the beans", "kick the bucket",
    "piece of cake", "under the weather", "once in a blue moon", "burn the midnight oil"
]

METAPHORS = [
    "life is a highway", "time is a thief", "heart of stone", "storm in a teacup",
    "lightning in a bottle", "drowning in sorrow", "fire in the belly", "ocean of dreams"
]

def count_syllables(word):
    # Simple heuristic to count syllables in a word
    word = word.lower()
    syllables = re.findall(r'[aeiouy]+', word)
    return max(1, len(syllables))

def generate_rap_line():
    subjects = ["I", "You", "We", "They", "The streets", "The beat", "My flow", "The game"]
    verbs = ["rock", "drop", "pop", "flow", "show", "glow", "grow", "know"]
    objects = ["the mic", "the crowd", "the block", "the spot", "the top", "the beat", "the rhyme", "the time"]
    rhymes = ["tight", "right", "fight", "night", "light", "height", "flight", "sight"]

    idiom = random.choice(IDIOMS)
    metaphor = random.choice(METAPHORS)

    subject = random.choice(subjects)
    verb = random.choice(verbs)
    obj = random.choice(objects)
    rhyme = random.choice(rhymes)

    line1 = f"{subject} {verb} on {obj}"
    line2 = f"My rhymes are {rhyme} all night"
    line3 = f"I {idiom} and {metaphor}"

    # Calculate rhyme density and syllable count (simplified)
    syllable_count = sum(count_syllables(word) for word in line1.split())
    rhyme_density = len(re.findall(r'[aeiouy]+', rhyme))

    return f"{line1},\n{line2},\n{line3}.\n(Syllables: {syllable_count}, Rhyme density: {rhyme_density})"

async def fetch_lyrics_from_web(query: str) -> str:
    # Dummy async function to simulate web search and fetch lyrics
    # In real implementation, this would call an API or scrape web pages
    await asyncio.sleep(1)  # simulate network delay
    sample_lyrics = (
        "The final problem is solved by throwin' sulfuric acid all over your back to see your spinal column dissolve\n"
        "Droppin' bodies like it was domino season\n"
        "My phenomenal legion will shoot out\n"
        "Your fuckin' abdominal region\n"
        "Slim Shady, responsible for your permanent stillness\n"
        "Just escaped from the hospital with terminal illness\n"
        "Itchin' to rip your fuckin' frame out\n"
        "'Cause I ain't got nothing to lose\n"
        "Like that movie that just came out\n"

def transform_lyrics_to_map(lyrics: str) -> str:
    # Dummy function to transform lyrics into thematic maps (conceptual)
    themes = ["struggle", "success", "fear", "ambition"]
    map_representation = " -> ".join(themes)
    return f"Thematic Map: {map_representation}"

bot_access_key = "WtZGJvUaiyJrfYE7KM1jDS8uxa9Zk8U8"
bot_name = "The-Rap-Algorithm-Ai"

class RapAlgorithmBot(fp.PoeBot):
    async def get_response(
        self, request: fp.QueryRequest
    ) -> AsyncIterable[fp.PartialResponse]:
        current_query = [fp.ProtocolMessage(role="system", content=SYSTEM_PROMPT)] + request.query

        # Generate a rap line using the advanced rap algorithm
        rap_lyrics = generate_rap_line()

        # Fetch lyrics from the web asynchronously
        web_lyrics = await fetch_lyrics_from_web("rap lyrics")

        # Transform fetched lyrics into thematic map
        thematic_map = transform_lyrics_to_map(web_lyrics)

        # Combine all parts into the final response
        final_response = f"{rap_lyrics}\n\nSample Lyrics from Web:\n{web_lyrics}\n\n{thematic_map}"

        # Yield the rap lyrics as a single response message
        yield fp.PartialResponse(content=final_response)

app_instance = fp.make_app(
    RapAlgorithmBot(),
    access_key=bot_access_key,
    bot_name=bot_name,
    allow_without_key=not (bot_access_key and bot_name),
)
