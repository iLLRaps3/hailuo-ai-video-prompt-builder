
Built by https://www.blackbox.ai

---

# Hailuo AI Video Prompt Builder

## Project Overview
The Hailuo AI Video Prompt Builder is a FastAPI-based application designed to generate optimized video prompts. It utilizes the Poe API to connect with AI capabilities and allows users to submit specific parameters relating to video generation, including models, styles, and camera movements. The application includes a user-friendly web interface for ease of access and interaction.

## Installation

To set up the project locally, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/hailuo-ai-video-prompt-builder.git
   cd hailuo-ai-video-prompt-builder
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows, use `env\Scripts\activate`
   ```

3. **Install dependencies:**
   ```bash
   pip install fastapi uvicorn fastapi_poe
   ```

4. **Set environment variables:**
   You need to set the `POE_ACCESS_KEY` and `POE_BOT_NAME` variables. You can do this in your terminal or in a `.env` file.

   ```bash
   export POE_ACCESS_KEY=your_poe_access_key
   export POE_BOT_NAME=iLL-Ai-OFFICIAL
   ```

5. **Run the application:**
   ```bash
   python main.py
   ```

6. **Open in a web browser:**
   Go to `http://localhost:8000` to access the Hailuo AI Video Prompt Builder interface.

## Usage

Once the application is running, navigate to the provided URL. You can fill out the form on the homepage to generate video prompts. The application will take the input parameters and call the AI to produce structured output based on the specified criteria.

## Features

- **AI-Driven Prompt Generation:** Users can generate video prompts using AI by specifying various parameters.
- **User-Friendly Interface:** The web UI allows for easy interaction and submission of parameters.
- **File Attachment Support:** Users can attach files within their requests.
- **Advanced Settings:** Users can customize various aspects of the generated prompts, including realism, styles, and camera movements.

## Dependencies

The project relies on the following libraries, which are included in the `requirements.txt` file (implicitly from `main.py`):
- `fastapi`
- `uvicorn`
- `fastapi_poe`

To install dependencies, simply run:
```bash
pip install -r requirements.txt
```

## Project Structure
The project is organized as follows:

```
hailuo-ai-video-prompt-builder/
├── main.py                # Main application file containing the FastAPI server and endpoint logic
├── ui.html                # HTML template for the user interface
├── requirements.txt       # All the necessary Python packages to run the application
└── server-bot-quick-start/  # Static files required for serving the client UI
    └── assets/             # Video and other asset files
```

--- 

For any further questions or contributions, feel free to contact the project maintainers through the issue tracker or email.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.