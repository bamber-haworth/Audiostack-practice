import audiostack
import os

# Assign the API key from environment variable
audiostack.api_key = os.getenv("AUDIOSTACK_API_KEY")

print("In Content you can create scripts and manage your production assets.")

scriptText = """
Welcome to AudioStack, the world's most powerful AI audio creation infrastructure.
The unlimited possibilities of generative AI at your fingertips. In one single API.
"""

script = audiostack.Content.Script.create(
  scriptText=scriptText,
  projectName="testingthings"
)
print(script)

print("In Speech you can access almost a thousand AI voice models or your own, cloned voice.")
tts = audiostack.Speech.TTS.create(
  scriptItem=script,
  voice="sara"
)

print("In Production you can dynamically mix it with a sound design of your choice and master it so it sounds great.")
mix = audiostack.Production.Mix.create(
  speechItem=tts,
  soundTemplate="spooky_strings",
  masteringPreset="balanced"
)
print(mix)

print("In Delivery, we produce a great sounding file with your choice of extension.")
encoder = audiostack.Delivery.Encoder.encode_mix(productionItem=mix, preset="mp3")
encoder.download(fileName="myFirstAudioStackTrack")
