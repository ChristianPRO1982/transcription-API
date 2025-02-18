import pytest
import os
from app.utils import transcribe_file


def test_transcribe_file_error():
    error_message = "[utils | transcribe_file] ERROR:"
    
    transcribe, error = transcribe_file("none.mp3")

    assert transcribe == None
    assert error[:len(error_message)] == error_message


def test_transcribe_file_ok():
    error_message = "[utils | transcribe_file] ERROR:"
    current_directory = os.getcwd()
    texts = ["Good Morning Business", "Nicolas Sarkozy", "qui a été secrétaire général", "Il avait été jugé pour prises illégales d'intérêt"]

    transcribe, error = transcribe_file(f"{current_directory}/test/example.mp3")
    
    for text in texts:
        assert text.lower() in transcribe.lower()