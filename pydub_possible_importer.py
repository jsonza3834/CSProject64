from pydub import AudioSegment
import os
import tempfile
import ffmpeg


def read_audio(file_path):
    try:
        audio = AudioSegment.from_file(file_path)
        return audio
    except Exception as e:
        print(f"Error loading audio file: {e}")
        return None

def clean_audio(audio):
    # Convert to one channel if multichannel
    if audio.channels > 1:
        audio = audio.set_channels(1)

    return audio

def convert_to_wav(audio, output_path):
    # Convert to wav format
    if format != "wav":
        audio.export(output_path, format="wav")

def remove_metadata(input_path, output_path):
    # Use ffmpeg to remove metadata
    os.system(f'ffmpeg -i "{input_path}" -map_metadata -1 -acodec copy "{output_path}"')

if __name__ == "__main__":
    input_file_path = "file.m4a"  # Replace with the path to your audio file
    output_file_path = "cleaned.wav"  # Replace with the desired output path

    # Step 1: Load the audio
    audio_data = read_audio(input_file_path)

    if audio_data:
        # Step 2: Clean the audio data
        cleaned_audio = clean_audio(audio_data)

        # Step 3: Save cleaned audio to temporary wav file
        temp_wav_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        convert_to_wav(cleaned_audio, temp_wav_file.name)

        # Step 4: Remove metadata from the temporary wav file
        remove_metadata(temp_wav_file.name, output_file_path)

        # Step 5: Print the cleaned audio information
        print("Cleaned Audio Information:")
        print(cleaned_audio)
    else:
        print("Audio file not loaded.")
