import whisper
from logs import init_log, logging_msg

model = whisper.load_model("base")  # "base" / "tiny" / "small" / "medium" / "large"

def transcribe_file(file_path):
    log_prefix = '[utils | transcribe_file]'
    if init_log:
        try:
            result = model.transcribe(file_path)
            return result['text'], None
        
        except Exception as e:
            e= str(e)
            return None, "{log_prefix} {e}"
        
    else:
        return None, f"{log_prefix} Error initializing logs"