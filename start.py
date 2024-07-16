import librosa
import openai

from openai import OpenAI
client = OpenAI(api_key="Key")


######################################################################################
## whisper 
# audio_file = open("Tems - Free Fall (Visualizer) ft. J. Cole.mp3", "rb")
 #transcript = client.audio.transcriptions.create(
  #file=audio_file,
  #model="whisper-1",
  #response_format="verbose_json",
  #timestamp_granularities=["word"]
#)

#print(transcript.words)

#######################################################################################
## open ai stuffz
completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
    {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
  ]
)

print(completion.choices[0].message)

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "compose a nice poem"}
    ],
    max_tokens=150
)

print(response.choices[0].message)


