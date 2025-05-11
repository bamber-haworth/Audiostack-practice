import audiostack
import os
import pandas as pd

audiostack.api_key = os.environ.get('AUDIOSTACK_API_KEY')

scriptText = """
<as:section name="main" soundsegment="main"> 
Parrots are highly intelligent and social birds known for their vibrant plumage and remarkable ability to mimic sounds, including human speech. These colorful avian companions are found in tropical regions around the world and are known for their playful and affectionate nature, often forming strong bonds with their human caregivers.  Parrots and generative audio both exhibit remarkable abilities for mimicry and creativity, with parrots mimicking sounds and voices, and generative audio systems producing compelling sound through imitation and adaptation. At AudioStack, we're big fans of parrots and take inspiration from them in everything from our voice cloning capabilities to our branding. Find out more at www.audiostack.ai
</as:section>"""

print("Generating your script...")
script = audiostack.Content.Script.create(scriptText=scriptText, scriptName="test")

print("Synthesizing speech...")
tts = audiostack.Speech.TTS.create(scriptItem=script, voice="cosmo", speed=1)
speechId = tts.speechId

print("Applying auto mixing and mastering...")
mix = audiostack.Production.Mix.create(speechItem=tts, exportSettings={"ttsTrack": True}, masteringPreset="balanced")

print("Annotating with time stamps...")
tts = audiostack.Speech.TTS.annotate(speechId=speechId)

print("Preparing for download...")
encoder = audiostack.Delivery.Encoder.encode_mix(
    productionItem=mix,
    preset="custom",
    sampleRate=44100,
    bitDepth=16,
    public=False,
    format="wav",
    channels=2,
    loudnessPreset="podcast"
)

encoder.download(fileName="parrots_voiceover")
print(encoder)

# === Parse timestamps from annotation response ===

print("Formatting your timestamp data as a table...")

# Get annotation timestamp list
data_list = None
for key, value in tts['data'].items():
    if 'annotations_timestamps' in value:
        data_list = value['annotations_timestamps']
        break

if not data_list:
    raise ValueError("No 'annotations_timestamps' found in TTS annotation response.")

# Create DataFrame
df = pd.DataFrame(data_list)

# Ensure required columns exist
required_columns = {'Offset', 'Duration', 'Word', 'Confidence'}
if not required_columns.issubset(df.columns):
    raise ValueError(f"Missing expected columns in annotations: {required_columns - set(df.columns)}")

# Rename and scale
df.rename(columns={'Offset': 'Timestamp'}, inplace=True)
df['Timestamp'] = df['Timestamp'] / 10_000_000
df['Duration'] = df['Duration'] / 10_000_000

print(df)

# === Generate Transcript ===

def format_transcript(row):
    start_time = row['Timestamp'].iloc[0]
    end_time = row['Timestamp'].iloc[-1] + row['Duration'].iloc[-1]
    words = ' '.join(row['Word'])
    return f"{start_time:.2f}-{end_time:.2f}\n\"{words}\""

segments = []
current_segment = pd.DataFrame(columns=['Word', 'Timestamp', 'Duration', 'Confidence'])

for _, row in df.iterrows():
    current_segment = pd.concat([current_segment, row.to_frame().T], ignore_index=True)
    words_in_segment = ' '.join(current_segment['Word']).split()
    if len(words_in_segment) >= 5:
        segments.append(current_segment)
        current_segment = pd.DataFrame(columns=['Word', 'Timestamp', 'Duration', 'Confidence'])

if not current_segment.empty:
    segments.append(current_segment)

# Write Transcript
with open("transcript.txt", "w") as f:
    for segment in segments:
        formatted_segment = format_transcript(segment)
        print(formatted_segment)
        f.write(f"{formatted_segment}\n\n")

# === Write SRT Subtitles ===

def format_time(milliseconds):
    seconds, milliseconds = divmod(milliseconds, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

def segment_to_text(segment):
    return ' '.join(segment['Word'])

start_time = 0
srt_counter = 1

with open("transcript.srt", "w") as srt_file:
    for segment in segments:
        end_time = start_time + int(segment['Duration'].sum() * 1000)
        srt_entry = f"{srt_counter}\n{format_time(start_time)} --> {format_time(end_time)}\n{segment_to_text(segment)}\n\n"
        srt_file.write(srt_entry)
        srt_counter += 1
        start_time = end_time

print("Done: transcript.txt and transcript.srt generated.")
