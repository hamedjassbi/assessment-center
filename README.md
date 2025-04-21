# Assessment Center Project - README

## Overview

This project is an AI-powered Assessment Center that allows users to choose from various psychological and career-related tests, and then interact with an AI to take the test step-by-step. The system is designed to be embeddable and fully functional within a Squarespace website.

## Features

- Multiple psychological and career assessment tests
- Step-by-step guided test experience
- AI-powered question flow and results analysis
- Click-only interface (no typing required)
- Responsive design for all devices
- Squarespace compatibility

## Project Structure

```
assessment_center/
├── main.py                 # Flask backend with OpenAI Assistant API integration
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (create this file)
├── test_backend.py         # Backend testing script
├── squarespace_embedding_guide.html  # Guide for embedding in Squarespace
├── static/                 # Frontend files
│   ├── index.html          # Test selection page
│   └── quiz.html           # Quiz interface
```

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- OpenAI API key with access to the Assistant API
- Web hosting for the backend (Replit, Heroku, etc.)

### Installation

1. Clone this repository or download the files
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

### Configuration

The system uses an OpenAI Assistant for test administration. The assistant ID is loaded from `assistant.json` or uses a default value. Make sure your OpenAI Assistant:

1. Has access to the evaluation models document
2. Is configured with the retrieval tool
3. Is trained to administer tests and provide results

## Running Locally

1. Start the Flask server:
   ```
   python main.py
   ```
2. The server will run on `http://localhost:8080` by default
3. Open a browser and navigate to `http://localhost:8080`

## Testing

Run the backend tests to verify API integration:
```
python test_backend.py
```

## Deployment

### Backend Deployment

The backend can be deployed to various platforms:

1. **Replit**: Upload the files to a Python Repl, set the `OPENAI_API_KEY` secret, and run the Repl
2. **Heroku/Render/Vercel**: Follow the platform's deployment instructions for Python applications

### Squarespace Integration

See `squarespace_embedding_guide.html` for detailed instructions on embedding the Assessment Center in Squarespace.

## Customization

- The primary color scheme uses `#8C1045` (burgundy) and white
- Modify the CSS in the HTML files to match your branding
- Add or remove tests by editing the buttons in `index.html`

## Troubleshooting

- **CORS Issues**: Ensure your backend allows requests from your Squarespace domain
- **API Errors**: Verify your OpenAI API key and Assistant ID are correct
- **Loading Issues**: Check browser console for JavaScript errors

## License

This project is provided for your personal use only. Please respect the terms of service for all APIs used.
