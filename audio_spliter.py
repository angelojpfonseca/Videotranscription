import os
import math
from pydub import AudioSegment

def split_audio(file_path, output_dir, max_size_mb=25):
    # Create output directory if it doesn't exist
    chunks_dir = os.path.join(output_dir, "audio_chunks")
    os.makedirs(chunks_dir, exist_ok=True)

    # Load the audio file
    audio = AudioSegment.from_file(file_path)
    
    # Calculate the number of chunks needed
    file_size = os.path.getsize(file_path) / (1024 * 1024)  # Size in MB
    num_chunks = math.ceil(file_size / max_size_mb)
    
    # Get the base name of the audio file
    base_name = os.path.splitext(os.path.basename(file_path))[0]

    # Split the audio into chunks
    chunk_length_ms = len(audio) // num_chunks
    chunks = []
    for i in range(num_chunks):
        start = i * chunk_length_ms
        end = (i + 1) * chunk_length_ms
        chunk = audio[start:end]
        chunk_path = os.path.join(chunks_dir, f"{base_name}_chunk_{i+1}.mp3")
        chunk.export(chunk_path, format="mp3")
        chunks.append(chunk_path)
    
    print(f"Audio split into {num_chunks} chunks. Saved in: {chunks_dir}")
    return chunks

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
    print("Audio File Splitter")
    print("------------------")

    # Get audio file path from user
    audio_path = get_valid_path("Enter the path to your audio file: ")

    # Get output directory from user
    output_dir = get_valid_path("Enter the path to save the audio chunks: ", is_file=False)

    # Get maximum chunk size from user (default to 25 MB if not specified)
    max_size_mb = input("Enter the maximum size for each chunk in MB (press Enter for default 25 MB): ")
    max_size_mb = int(max_size_mb) if max_size_mb.strip() else 25

    # Split audio
    chunk_paths = split_audio(audio_path, output_dir, max_size_mb)

    print("\nAudio splitting completed!")
    print(f"Number of chunks created: {len(chunk_paths)}")
    print(f"Chunks saved in: {os.path.join(output_dir, 'audio_chunks')}")

if __name__ == "__main__":
    main()