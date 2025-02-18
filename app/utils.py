import whisper

model = whisper.load_model("base")  # "base" / "tiny" / "small" / "medium" / "large"

def transcribe_file(file_path):
    log_prefix = '[utils | transcribe_file]'
    try:
        result = model.transcribe(file_path)
        # result = {"text": "TEXT"}

        print(f"{log_prefix} transciption with Whisper OK")
        return result['text'], None
    
    except Exception as e:
        print(f"{log_prefix} Whisper error: {str(e)}")
        return None, f"{log_prefix} {str(e)}"

def test():
    pass