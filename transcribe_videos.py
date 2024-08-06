import os
from moviepy.editor import VideoFileClip
import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence

def extract_audio_from_video(video_path):
    audio_path = os.path.splitext(video_path)[0] + '.wav'
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path)
    video.close()
    return audio_path

def transcribe_large_audio(file_path, use_sphinx=False):
    recognizer = sr.Recognizer()
    sound = AudioSegment.from_wav(file_path)
    chunks = split_on_silence(sound, min_silence_len=500, silence_thresh=sound.dBFS-14, keep_silence=500)
    
    folder_name = "audio-chunks"
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    
    whole_text = ""
    for i, audio_chunk in enumerate(chunks, start=1):
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        with sr.AudioFile(chunk_filename) as source:
            audio = recognizer.record(source)
        try:
            if use_sphinx:
                text = recognizer.recognize_sphinx(audio)
            else:
                text = recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            print(f"Could not understand audio in chunk {i}")
            text = ""
        except sr.RequestError as e:
            print(f"Could not request results from speech recognition service for chunk {i}; {e}")
            text = ""
        whole_text += text + " "
        print(f"Transcribed chunk {i}")
    
    return whole_text

def save_transcription(transcription, original_file_path):
    output_file_path = os.path.splitext(original_file_path)[0] + '_transcription.txt'
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(transcription)
    print(f"Transcription saved to: {output_file_path}")

def transcribe_audio(file_path):
    if not os.path.isfile(file_path):
        return "File not found. Please check the path and try again."

    audio_path = file_path
    if file_path.lower().endswith('.mp4'):
        print("Extracting audio from MP4...")
        try:
            audio_path = extract_audio_from_video(file_path)
        except Exception as e:
            return f"Error extracting audio from MP4: {e}"

    print("Transcribing audio...")
    try:
        transcript = transcribe_large_audio(audio_path)
        if not transcript.strip():
            print("Google Speech Recognition failed. Trying with Sphinx...")
            transcript = transcribe_large_audio(audio_path, use_sphinx=True)
        
        # Save the transcription to a text file
        save_transcription(transcript, file_path)
        
        return transcript
    except Exception as e:
        return f"An error occurred during transcription: {e}"

def main():
    file_path = input("Please enter the path to your MP4 video file: ")
    transcription = transcribe_audio(file_path)
    print("Transcription:", transcription)

if __name__ == "__main__":
    main()