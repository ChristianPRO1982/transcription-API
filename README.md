# Transcription API

This project is an API built with FastAPI that generates transcriptions using OpenAI's Whisper. 

## Features

- Input: Audio file
- Output: JSON with the file name, date and time, processing time, and transcription text

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/transcription-API.git
    ```
2. Navigate to the project directory:
    ```bash
    cd transcription-API
    ```
3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Start the FastAPI server:
    ```bash
    uvicorn main:app --reload
    ```
2. Open your browser and go to `http://127.0.0.1:8000/docs` to access the Swagger UI.

## API Endpoints

### POST /transcribe

- **Description**: Transcribe an audio file.
- **Request**:
    - **File**: Audio file to be transcribed.
- **Response**:
    ```json
    {
        "file_name": "example.wav",
        "date_time": "2023-10-01T12:00:00Z",
        "processing_time": "5 seconds",
        "transcription_text": "This is the transcribed text."
    }
    ```

## License

This project is licensed under the MIT License.

## Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com/)
- [Whisper by OpenAI](https://github.com/openai/whisper)

## Contact

For any inquiries, please contact [your email].
