import os
import subprocess
from pydub import AudioSegment
import argparse

def extract_audio_track(video_path, output_audio_path, track_number=3):
    """
    Extracts a specific audio track from a video file using ffmpeg.

    :param video_path: Path to the input video file.
    :param output_audio_path: Path to the output audio file.
    :param track_number: Audio track number to extract (1-based index).
    """
    try:
        # Run ffmpeg command to extract the audio track
        command = [
            "ffmpeg",
            "-i", video_path,
            "-map", f"0:a:{track_number - 1}",  # Audio track index is 0-based in ffmpeg
            "-ac", "1",  # Ensure audio is mono for easier analysis
            "-ar", "44100",  # Set sample rate for consistency
            "-y",  # Overwrite output file if it exists
            output_audio_path
        ]
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to extract audio track: {e}")
        return False
    return True

def detect_audio_activity(audio_file_path, in_time=None, out_time=None, fps=25, threshold=-50, chunk_size=None):
    """
    Detects activity in an audio file and returns timestamps of activity.

    :param audio_file_path: Path to the extracted audio file.
    :param in_time: Start time for analysis (in seconds). If None, starts from the beginning.
    :param out_time: End time for analysis (in seconds). If None, ends at the last frame.
    :param threshold: Amplitude threshold for detecting activity (in dB).
    :param chunk_size: Size of chunks to analyze (in ms).
    :return: List of timestamps (in seconds) where audio activity is detected.
    """
    # Load the audio file using pydub
    audio = AudioSegment.from_file(audio_file_path)
    
    # Set default in_time and out_time if not provided
    if in_time is None:
        in_time = 0
    if out_time is None:
        out_time = len(audio) / 1000.0  # Convert milliseconds to seconds
    
    # Slice the audio to the specified range
    audio = audio[in_time * 1000:out_time * 1000]  # Convert seconds to milliseconds
    
    # Analyze in chunks and detect where the audio is above the threshold
    active_timestamps = []
    # Dynamically figure out chunk size based on the frame rate
    chunk_size = int(1000/fps) if chunk_size is None else chunk_size
    
    is_active = False  # To track if we are in an active state
    for i in range(0, len(audio), chunk_size):
        chunk = audio[i:i + chunk_size]
        # Use RMS (Root Mean Square) to measure volume
        if chunk.dBFS > threshold:  # dBFS is the decibel relative to full scale
            if not is_active:  # Start of a new activity
                active_timestamps.append(i / 1000.0)  # Convert ms to seconds
                is_active = True
        else:
            is_active = False  # Reset when below the threshold
    
    return active_timestamps

def analyze_video_audio_activity(**kwargs):
    """
    Analyzes a specific audio track in a video file for activity and returns timestamps.

    :param video_path: Path to the input video file.
    :param in_time: Start time for analysis (in seconds).
    :param out_time: End time for analysis (in seconds).
    :param track_number: Audio track number to analyze (1-based index).
    :return: List of timestamps (in seconds) where audio activity is detected.
    """
    # Define temporary audio file path
    temp_audio_path = os.path.join(kwargs.get("project_path"), "temp_audio.wav")
    
    # Extract the specified audio track from the video
    if extract_audio_track(kwargs.get("video_path"), temp_audio_path, kwargs.get("track_number")):
        # Detect audio activity in the extracted track
        timestamps = detect_audio_activity(temp_audio_path, kwargs.get("in_time"), kwargs.get("out_time"), kwargs.get("fps"), kwargs.get("threshold"), kwargs.get("chunk_size"))
        
        # Clean up temporary audio file
        os.remove(temp_audio_path)
        
        return timestamps
    else:
        print("Audio track extraction failed.")
        return []

def main():
    parser = argparse.ArgumentParser(description="Analyze the third audio track in a video for activity and return a list of timestamps.")
    parser.add_argument("video_path", type=str, help="Path to the input video file.")
    parser.add_argument("project_path", type=str, help="Path to the Premiere Project file.")

    parser.add_argument("--in_time", type=float, help="Start time for analysis (in seconds). If not provided, defaults to the start of the track.")
    parser.add_argument("--out_time", type=float, help="End time for analysis (in seconds). If not provided, defaults to the end of the track.")
    parser.add_argument("--track_number", type=int, default=3, help="Audio track number to analyze (default: 3).")
    parser.add_argument("--threshold", type=float, default=-50.0, help="Amplitude threshold for detecting activity (in dB, default: -50.0).")
    parser.add_argument("--chunk_size", type=int, default=400, help="Size of chunks to analyze (in ms, default: 100).")
    parser.add_argument("--fps", type=int, default=25, help="Framerate of the video (default: 25).")
    
    args = parser.parse_args()
    
    # Call the analyze function with the provided arguments
    timestamps = analyze_video_audio_activity(**vars(args))
    
    # Print the results
    if timestamps:
        print("Detected audio activity at timestamps:")
        for ts in timestamps:
            print(f"{ts} seconds")
        # save the timestamps to a json file
        import json
        with open('C:\\Users\\Cheha\\Desktop\\PremiereBlippr\\timestamps.json', 'w') as f:
            json.dump(timestamps, f)
    else:
        print("No audio activity detected or extraction failed.")

if __name__ == "__main__":
    main()
