import audiostack
import os

# API key
audiostack.api_key = os.getenv("AUDIOSTACK_API_KEY")

SCRIPT = """
<as:section name="intro">
You train and you train, it never gets easier. You just get better.
</as:section>

<as:section name="main1" soundSegment="main">
Every time the fight starts, you give your best.
</as:section>

<as:section name="main2" soundSegment="main">
Only you and your boxing gloves against the world
</as:section>

<as:section name="main3">
So you better get the best ones you can buy, go to our website this month and you'll get 50 per cent discount!
</as:section>

<as:section name="main4">
Boxing.
</as:section>
     
<as:section name="outro" soundSegment="outro">
Give it your best.
</as:section>
"""

print("Creating script...")
script = audiostack.Content.Script.create(scriptText=SCRIPT)

print("Generating speech...")
speech = audiostack.Speech.TTS.create(scriptItem=script, voice="isaac", sections={
    "main2": {"voice": "elora"},
    "outro": {"voice": "whispering_ethan"},
})

print("Creating mix...")
mix = audiostack.Production.Mix.create(
    speechItem=speech,
    soundTemplate="visible",
    masteringPreset="atmosphere_test",
    sections={
        "intro": {"atmosphere": "boxing_training"},
        "main1": {"atmosphere": "boxing_round_start"},
        "main3": {"atmosphere": "boxing_fighting"},
        "outro": {"atmosphere": "boxing_round_start"}
    }
)

print(mix.productionId)

print("Downloading WAV")
mix.download(fileName="boxingExample")