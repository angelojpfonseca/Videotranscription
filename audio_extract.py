import os
from moviepy.editor import VideoFileClip

def extract_audio(video_path, output_dir):
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Get the video file name without extension
    video_name = os.path.splitext(os.path.basename(video_path))[0]

    # Create the output audio file path
    audio_path = os.path.join(output_dir, f"{video_name}.mp3")

    # Load the video file
    video = VideoFileClip(video_path)

    # Extract the audio
    audio = video.audio

    # Write the audio file
    audio.write_audiofile(audio_path, bitrate="320k")

    # Close the video and audio objects
    audio.close()
    video.close()

    print(f"Audio extracted: {audio_path}")

def get_valid_path(prompt, is_file=True):
    while True:
        path = input(prompt)
        if is_file:
            if os.path.isfile(path) and path.lower().endswith('.mp4'):
                return path
            else:
                print("Invalid file path. Please enter a valid path to an MP4 file.")
        else:
            if os.path.isdir(path):
                return path
            else:
                print("Invalid directory path. Please enter a valid directory path.")

def main():
    print("MP4 Audio Extractor")
    print("-------------------")

    # Get video file path from user
    video_path = get_valid_path("Enter the path to your MP4 file: ")

    # Get output directory from user
    output_dir = get_valid_path("Enter the path to save the extracted audio: ", is_file=False)

    # Extract audio
    extract_audio(video_path, output_dir)

if __name__ == "__main__":
    main()