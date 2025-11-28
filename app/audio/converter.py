import subprocess
import imageio_ffmpeg
import os

def convert_to_wav(input_path, output_path):
    """
    Converts an audio/video file to WAV format using ffmpeg directly.
    """
    try:
        ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
        
        # Command: ffmpeg -y -i input -acodec pcm_s16le -ar 44100 -ac 1 output
        command = [
            ffmpeg_exe,
            '-y', # Overwrite output
            '-i', input_path,
            '-acodec', 'pcm_s16le',
            '-ar', '44100', # Sample rate
            '-ac', '1', # Mono (SpeechRecognition prefers mono)
            output_path
        ]
        
        # Run command, suppress output
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except Exception as e:
        print(f"Error converting file: {e}")
        return False
