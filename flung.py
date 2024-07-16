from openai import OpenAI
import librosa
import openai
import numpy as np  # Make sure numpy is imported
from pychoru6.pychorus.helpers import find_and_output_choruses



# Replace 'your_openai_api_key' with your actual OpenAI API key
client = OpenAI(api_key="KEY")



# Function to transcribe the audio using OpenAI Whisper
def transcribe_audio(filename):
    with open(filename, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="verbose_json",
            timestamp_granularities=["word"]
        )
    return transcript['words'] if 'words' in transcript else transcript

# Function to load and process the audio file
def load_audio(filename):
    y, sr = librosa.load(filename, sr=None)
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    if isinstance(tempo, np.ndarray):
        tempo = tempo.item()
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)
    return tempo, beat_times

# Function to integrate beat data with transcript data
def integrate_data(beat_times, transcript, choruses):
    combined_data = []
    for word in transcript:
        if 'start' in word and 'end' in word:
            text = word['word']
            start = word['start']
            end = word['end']
            segment_beats = [beat for beat in beat_times if start <= beat <= end]
            is_chorus = any(chorus - 0.5 <= start <= chorus + 0.5 for chorus in choruses)
            combined_data.append({
                'start': start,
                'end': end,
                'text': text,
                'beats': segment_beats,
                'is_chorus': is_chorus
            })
    return combined_data

# Function to get transition recommendation from ChatGPT
def get_transition_recommendation(tempo, combined_data):
    transcript_str = ' '.join(f"{segment['text']}({segment['start']:.2f}-{segment['end']:.2f})" for segment in combined_data)
    chorus_times = [segment['start'] for segment in combined_data if segment['is_chorus']]
    prompt = (
        f"The song has a tempo of {tempo:.2f} BPM. Here are the detected chorus times: {chorus_times}. "
        f"Below is the song's transcript with timing information: {transcript_str}. "
        f"Using this information, suggest the best times and techniques to transition to another song for a smooth DJ set, "
        f"including the exact times to start and end the transition and any overlap suggestions."
    )

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    return completion.choices[0].message.content.strip()

# Main workflow
def main(filename):
    # Transcribe the audio file
    print("Transcribing audio...")
    transcript = transcribe_audio(filename)
    print("Transcript:", transcript)

    # Load and process the audio file
    print("Loading and processing audio...")
    tempo, beat_times = load_audio(filename)
    print(f"Estimated tempo: {tempo:.2f} BPM")
    print("Beat times:", beat_times)

    # Detect choruses
    print("Detecting choruses...")
    choruses_start_sec = find_and_output_choruses(
        filename,
        r"C:\Users\pagug\Downloads\AIDJ\chorus_output.wav",
        clip_length=15,
        num_choruses=10,
        line_threshold=0.5,
        num_iterations=30,
        overlap_percent_margin=1.0
    )
    print("Detected choruses start at:", choruses_start_sec)

    # Integrate beat data with transcript data and chorus information
    print("Integrating beat data with transcript data...")
    combined_data = integrate_data(beat_times, transcript, choruses_start_sec)
    print("Combined data:", combined_data)

    # Get transition recommendation
    print("Getting transition recommendation...")
    transition_recommendation = get_transition_recommendation(tempo, combined_data)
    print("Transition recommendation:", transition_recommendation)

# Example usage
filename = r'C:\Users\pagug\Downloads\AIDJ\Tems - Free Fall (Visualizer) ft. J. Cole.mp3'
main(filename)
