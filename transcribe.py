import os
from openai import OpenAI
from dotenv import load_dotenv

def transcribe_audio(client, audio_path, output_dir):
    # Open the audio file
    with open(audio_path, "rb") as audio_file:
        # Transcribe the audio using OpenAI API
        transcript = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file
        )

    # Get the audio file name without extension
    audio_name = os.path.splitext(os.path.basename(audio_path))[0]

    # Create the output transcript file path
    transcript_path = os.path.join(output_dir, f"{audio_name}_transcript.txt")

    # Write the transcript to a file
    with open(transcript_path, "w", encoding="utf-8") as f:
        f.write(transcript.text)

    print(f"Transcription saved: {transcript_path}")
    return transcript_path

def get_valid_path(prompt, is_file=True):
    while True:
        path = input(prompt)
        if is_file:
            if os.path.isfile(path):
                return path
            else:
                print("Invalid file path. Please enter a valid path to an audio file.")
        else:
            if os.path.isdir(path):
                return path
            else:
                print("Invalid directory path. Please enter a valid directory path.")

def main():
    print("Audio Transcriber using OpenAI API")
    print("----------------------------------")

    # Load environment variables from .env file
    load_dotenv()

    # Get OpenAI API key from environment variable
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY not found in .env file.")
        return

    # Initialize OpenAI client
    client = OpenAI(api_key=api_key)

    # Get audio file path from user
    audio_path = get_valid_path("Enter the path to your audio file: ")

    # Get output directory from user
    output_dir = get_valid_path("Enter the path to save the transcript: ", is_file=False)

    # Transcribe audio
    transcript_path = transcribe_audio(client, audio_path, output_dir)

    print("\nTranscription completed!")
    print(f"Transcript file: {transcript_path}")

if __name__ == "__main__":
    main()