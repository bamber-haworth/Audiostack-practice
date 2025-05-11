import os
import time
import audiostack

audiostack.api_key = os.environ['AUDIOSTACK_API_KEY']


# Product name and description are required
product_name = "Bamber's chocolate cookies"
product_description = (
    "Delicious chocolate chip cookies that nobody can resist. Try Bamber's cookies today and discover a world of chocolicious delight."
)
mood_name = "Happy"
tone_name = "confident"

# Use AI to generate your script
print("Generating your script...")
advert = audiostack.Content.Script.generate_advert(
    product_name=product_name,
    product_description=product_description,
    mood=mood_name
)

ad_text = advert.data['adText']
ad_name = advert.data['adName']
script_id = advert.data['scriptId']
print(f"Your AI Generated Ad: {ad_text}")

# Recommends an AI voice
voices = audiostack.Speech.Voice.select_for_content(
    content=ad_text,
    tone=tone_name
)

voice_names = voices.data['voices']
recommended_voice = voice_names[0]['alias']
recommended_speed = voice_names[0]['speed']
print(f"Recommended Voice: {recommended_voice}")
print(f"Recommended Speed: {recommended_speed}")

# Generates speech
print(f"Generating speech for {recommended_voice}")
speech = audiostack.Speech.TTS.create(
    scriptId=script_id,
    voice=recommended_voice,
    speed=recommended_speed
)

# Chooses a sound template
print("Selecting the music...")
sound_templates = audiostack.Production.Sound.Template.select_for_script(
    scriptId=script_id,
    mood=mood_name
)

sound_template_names = sound_templates.data['templates']
recommended_template = sound_template_names[0]['name']
print(f"Recommended Sound Template: {recommended_template}")

# Create mix
print("Creating your advert...")
mix = audiostack.Production.Mix.create(
    speechItem=speech,
    soundTemplate=recommended_template,
    masteringPreset="balanced"
)

# Download the final advert as an MP3 file
print("Downloading your MP3")
encoder = audiostack.Delivery.Encoder.encode_mix(
    productionItem=mix,
    preset="mp3"
)
encoder.download(
    fileName=f"{ad_name}__{recommended_voice}",
    path="."
)

