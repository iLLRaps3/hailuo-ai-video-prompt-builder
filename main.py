from __future__ import annotations
from typing import AsyncIterable
import fastapi_poe as fp
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import os

# Sample PoeBot subclass demonstrating key features
class RealPromptBot(fp.PoeBot):
    async def get_response(self, request: fp.QueryRequest) -> AsyncIterable[fp.PartialResponse]:
        # Forward the prompt to GPT-4o for real generation
        async for msg in fp.stream_request(request, "GPT-4o", request.access_key):
            yield msg

    async def get_settings(self, setting: fp.SettingsRequest) -> fp.SettingsResponse:
        # Enable file attachments and set introduction message
        return fp.SettingsResponse(
            allow_attachments=True,
            expand_text_attachments=True,
            enable_image_comprehension=True,
            introduction_message="Welcome to RealPromptBot! Send me a message or a file."
        )

# Create the FastAPI app instance directly for Uvicorn
bot = RealPromptBot()
import os
access_key = os.getenv("POE_ACCESS_KEY", "igGtBmXsZLS1d9nEPxwtuzlVCEUD9UDW")
bot_name = os.getenv("POE_BOT_NAME", "iLL-Ai-OFFICIAL")
app = fp.make_app(bot, access_key=access_key, bot_name=bot_name)

# Enable CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files for prompt builder UI and video bot UI
app.mount("/static", StaticFiles(directory="server-bot-quick-start/static"), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

VIDEO_PATH = Path(__file__).parent / "server-bot-quick-start" / "assets" / "tiger.mp4"

@app.get("/")
async def root():
    # Render the prompt builder UI HTML directly on root
    html_content = """
<!DOCTYPE html>
<html lang="en">
 <head>
  <meta charset="utf-8"/>
  <meta content="width=device-width, initial-scale=1" name="viewport"/>
  <title>
   Hailuo AI Video Prompt Builder
  </title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css" rel="stylesheet"/>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&amp;display=swap" rel="stylesheet"/>
  <style>
   body {
      font-family: 'Inter', sans-serif;
    }
  </style>
 </head>
 <body class="bg-gray-50 min-h-screen flex flex-col">
  <header class="bg-white shadow">
   <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="flex justify-between items-center py-4">
     <div class="flex items-center space-x-3">
      <img alt="Hailuo AI Video Prompt Builder logo, stylized letters HB in blue and purple gradient" class="h-12 w-12 rounded-md" height="48" src="https://storage.googleapis.com/a1aa/image/91cbba9d-132e-4f73-4b34-d38f00d5630c.jpg" width="48"/>
      <h1 class="text-2xl font-semibold text-gray-900">
       Hailuo AI Video Prompt Builder
      </h1>
     </div>
     <nav class="hidden md:flex space-x-8 text-gray-700 font-medium">
      <a class="hover:text-indigo-600 transition" href="#">
       Home
      </a>
      <a class="hover:text-indigo-600 transition" href="#">
       Docs
      </a>
      <a class="hover:text-indigo-600 transition" href="#">
       API
      </a>
      <a class="hover:text-indigo-600 transition" href="#">
       Contact
      </a>
     </nav>
     <button class="md:hidden text-gray-700 focus:outline-none focus:ring-2 focus:ring-indigo-600" id="mobile-menu-button">
      <i class="fas fa-bars fa-lg"></i>
     </button>
    </div>
   </div>
   <nav class="md:hidden bg-white border-t border-gray-200 hidden" id="mobile-menu">
    <a class="block px-4 py-3 text-gray-700 hover:bg-indigo-50 hover:text-indigo-600" href="#">
     Home
    </a>
    <a class="block px-4 py-3 text-gray-700 hover:bg-indigo-50 hover:text-indigo-600" href="#">
     Docs
    </a>
    <a class="block px-4 py-3 text-gray-700 hover:bg-indigo-50 hover:text-indigo-600" href="#">
     API
    </a>
    <a class="block px-4 py-3 text-gray-700 hover:bg-indigo-50 hover:text-indigo-600" href="#">
     Contact
    </a>
   </nav>
  </header>
  <main class="flex-grow max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
   <h2 class="text-3xl font-extrabold text-gray-900 mb-6 text-center">
    Generate Optimized Video Prompts
   </h2>
   <form class="bg-white shadow-md rounded-lg p-6 space-y-6" id="prompt-form">
    <div>
     <label class="block text-sm font-medium text-gray-700 mb-1" for="model">
      Model
      <span class="text-red-600">*</span>
     </label>
     <select class="block w-full rounded-md border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500" id="model" name="model" required>
      <option disabled selected value="">Select a model</option>
      <option value="director">Director</option>
      <option value="live">Live</option>
      <option value="subject">Subject</option>
      <option value="MiniMax">MiniMax</option>
     </select>
    </div>
    <div>
     <label class="block text-sm font-medium text-gray-700 mb-1" for="style">Style</label>
     <input class="block w-full rounded-md border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500" id="style" name="style" placeholder="e.g. cinematic, abstract, realistic" type="text"/>
    </div>
    <div>
     <label class="block text-sm font-medium text-gray-700 mb-1" for="cartoonStyle">Cartoon Style</label>
     <input class="block w-full rounded-md border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500" id="cartoonStyle" name="cartoonStyle" placeholder="e.g. anime, comic, cel-shaded" type="text"/>
    </div>
    <div>
     <label class="block text-sm font-medium text-gray-700 mb-1" for="subject">
      Subject
      <span class="text-red-600">*</span>
     </label>
     <input class="block w-full rounded-md border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500" id="subject" name="subject" placeholder="Describe the main subject" required type="text"/>
    </div>
    <div>
     <label class="block text-sm font-medium text-gray-700 mb-1" for="action">
      Action
      <span class="text-red-600">*</span>
     </label>
     <input class="block w-full rounded-md border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500" id="action" name="action" placeholder="Describe the main action" required type="text"/>
    </div>
    <div>
     <label class="block text-sm font-medium text-gray-700 mb-1" for="atmosphere">Atmosphere / Setting</label>
     <input class="block w-full rounded-md border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500" id="atmosphere" name="atmosphere" placeholder="e.g. foggy forest, futuristic city" type="text"/>
    </div>
    <div>
     <label class="block text-sm font-medium text-gray-700 mb-1" for="aspect">Aspect Ratio</label>
     <input class="block w-full rounded-md border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500" id="aspect" name="aspect" placeholder="e.g. 16:9, 4:3" type="text"/>
    </div>
    <div>
     <label class="block text-sm font-medium text-gray-700 mb-1" for="effects">Visual Effects</label>
     <input class="block w-full rounded-md border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500" id="effects" name="effects" placeholder="e.g. lens flare, bokeh" type="text"/>
    </div>
    <div>
     <label class="block text-sm font-medium text-gray-700 mb-1" for="realism">Realism (1-10)</label>
     <input class="block w-24 rounded-md border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500" id="realism" max="10" min="1" name="realism" placeholder="1 = cartoon, 10 = photorealistic" step="1" type="number"/>
    </div>
    <fieldset class="border border-gray-300 rounded-md p-4">
     <legend class="text-sm font-medium text-gray-700 mb-2">Camera Movements</legend>
     <div class="flex flex-wrap gap-4">
      <label class="inline-flex items-center space-x-2">
       <input class="form-checkbox text-indigo-600" name="cameraButtons" type="checkbox" value="zoom"/>
       <span>Zoom</span>
      </label>
      <label class="inline-flex items-center space-x-2">
       <input class="form-checkbox text-indigo-600" name="cameraButtons" type="checkbox" value="pan"/>
       <span>Pan</span>
      </label>
      <label class="inline-flex items-center space-x-2">
       <input class="form-checkbox text-indigo-600" name="cameraButtons" type="checkbox" value="tracking"/>
       <span>Tracking</span>
      </label>
      <label class="inline-flex items-center space-x-2">
       <input class="form-checkbox text-indigo-600" name="cameraButtons" type="checkbox" value="dolly"/>
       <span>Dolly</span>
      </label>
      <label class="inline-flex items-center space-x-2">
       <input class="form-checkbox text-indigo-600" name="cameraButtons" type="checkbox" value="shake"/>
       <span>Shake</span>
      </label>
      <label class="inline-flex items-center space-x-2">
       <input class="form-checkbox text-indigo-600" name="cameraButtons" type="checkbox" value="aerial"/>
       <span>Aerial</span>
      </label>
     </div>
     <div class="mt-4 grid grid-cols-2 gap-4">
      <label class="inline-flex items-center space-x-2">
       <input class="form-checkbox text-indigo-600" id="cameraPush" name="cameraPush" type="checkbox"/>
       <span>Push In</span>
      </label>
      <label class="inline-flex items-center space-x-2">
       <input class="form-checkbox text-indigo-600" id="cameraPullout" name="cameraPullout" type="checkbox"/>
       <span>Pull Out</span>
      </label>
      <label class="inline-flex items-center space-x-2">
       <input class="form-checkbox text-indigo-600" id="cameraLowangle" name="cameraLowangle" type="checkbox"/>
       <span>Low Angle</span>
      </label>
      <label class="inline-flex items-center space-x-2">
       <input class="form-checkbox text-indigo-600" id="cameraOverhead" name="cameraOverhead" type="checkbox"/>
       <span>Overhead</span>
      </label>
     </div>
    </fieldset>
    <div class="flex justify-center">
     <button class="inline-flex items-center px-6 py-3 bg-indigo-600 text-white font-semibold rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2" type="submit">
      <i class="fas fa-magic mr-2"></i>
      Generate Prompt
     </button>
    </div>
   </form>
   <section class="mt-10 hidden" id="result-section">
    <h3 class="text-xl font-semibold text-gray-900 mb-4 text-center">
     Generated Prompt
    </h3>
    <div class="bg-white p-6 rounded-md shadow-md text-gray-800 whitespace-pre-wrap break-words" id="generated-prompt">
    </div>
    <div class="flex justify-center mt-4">
     <button class="inline-flex items-center px-5 py-2 bg-green-600 text-white font-semibold rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2" id="copy-button">
      <i class="fas fa-copy mr-2"></i>
      Copy to Clipboard
     </button>
    </div>
   </section>
   <section class="mt-10 hidden" id="error-section">
    <div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
     <strong class="font-bold">
      Error:
     </strong>
     <span class="block sm:inline" id="error-message">
     </span>
    </div>
   </section>
  </main>
  <footer class="bg-white border-t border-gray-200 py-6 mt-12">
   <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center text-gray-500 text-sm">
    © 2024 Hailuo AI Video Prompt Builder. All rights reserved.
   </div>
  </footer>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center text-gray-500 text-sm py-2">
    Poe Server Address: <code>https://poe.com</code>
  </div>
  <script>
   const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');
    mobileMenuButton.addEventListener('click', () => {
      mobileMenu.classList.toggle('hidden');
    });

    const form = document.getElementById('prompt-form');
    const resultSection = document.getElementById('result-section');
    const generatedPromptDiv = document.getElementById('generated-prompt');
    const errorSection = document.getElementById('error-section');
    const errorMessageSpan = document.getElementById('error-message');
    const copyButton = document.getElementById('copy-button');

    form.addEventListener('submit', async (e) => {
      e.preventDefault();

      resultSection.classList.add('hidden');
      errorSection.classList.add('hidden');
      generatedPromptDiv.textContent = '';

      const formData = new FormData(form);
      const data = {
        model: formData.get('model'),
        style: formData.get('style') || '',
        cartoonStyle: formData.get('cartoonStyle') || '',
        subject: formData.get('subject'),
        action: formData.get('action'),
        atmosphere: formData.get('atmosphere') || '',
        aspect: formData.get('aspect') || '',
        effects: formData.get('effects') || '',
        realism: formData.get('realism') ? Number(formData.get('realism')) : null,
        cameraButtons: formData.getAll('cameraButtons'),
        cameraPush: formData.get('cameraPush') === 'on',
        cameraPullout: formData.get('cameraPullout') === 'on',
        cameraLowangle: formData.get('cameraLowangle') === 'on',
        cameraOverhead: formData.get('cameraOverhead') === 'on',
      };

      if (!data.model || !data.subject || !data.action) {
        errorMessageSpan.textContent = 'Please fill in all required fields: Model, Subject, and Action.';
        errorSection.classList.remove('hidden');
        return;
      }

      try {
        const response = await fetch('/generate-prompt', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(data),
        });

        const result = await response.json();

      if (!response.ok) {
        errorMessageSpan.textContent = result.error || 'Failed to generate prompt.';
        errorSection.classList.remove('hidden');
        return;
      }
   });
  </script>
 </body>
</html>
    """
    return HTMLResponse(content=html_content)

# Implement the /generate-prompt POST endpoint
from fastapi import Request
from fastapi.responses import JSONResponse
import json

@app.post("/generate-prompt")
async def generate_prompt(request: Request):
    try:
        data = await request.json()
        # Construct prompt string from form data
        prompt_parts = [
            f"Model: {data.get('model', '')}",
            f"Style: {data.get('style', '')}",
            f"Cartoon Style: {data.get('cartoonStyle', '')}",
            f"Subject: {data.get('subject', '')}",
            f"Action: {data.get('action', '')}",
            f"Atmosphere: {data.get('atmosphere', '')}",
            f"Aspect Ratio: {data.get('aspect', '')}",
            f"Visual Effects: {data.get('effects', '')}",
            f"Realism: {data.get('realism', '')}",
            f"Camera Movements: {', '.join(data.get('cameraButtons', []))}",
            f"Push In: {data.get('cameraPush', False)}",
            f"Pull Out: {data.get('cameraPullout', False)}",
            f"Low Angle: {data.get('cameraLowangle', False)}",
            f"Overhead: {data.get('cameraOverhead', False)}",
        ]
        prompt_text = "Generate a video prompt with the following details:\n" + "\n".join(prompt_parts)

        # Use the SamplePoeBot instance to get a response
        query_request = fp.QueryRequest(query=[fp.ProtocolMessage(role="user", content=prompt_text)])
        response_text = ""
        async for partial_response in bot.get_response(query_request):
            response_text += partial_response.text or ""

        return JSONResponse(content={"prompt": response_text})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

