import audiostack
import os

audiostack.api_key = "eb719b3449834a03a002a0c6a6f10147" 

script = """

<as:section name="main" soundsegment="main">
Oh, darling, have you heard about the latest train wreck in the music industry? Lily Allen is attempting to pass off her mediocrity as artistry. But let me tell you, her desperate attempts at relevance are about as convincing as her attempts at hitting the high notes. Sorry, Lily, but you're the epitome of trying too hard and failing miserably. It's time to retire that tired act and let the real stars shine.
</as:section>


"""



names = ["Promo_Ramona"]
presets = ["balanced"]
templates = ["future_focus_30"]



script = audiostack.Content.Script.create(scriptText=script, scriptName="test", projectName="mastering_test")        

for name in names:
    # Creates text to speech
    speech = audiostack.Speech.TTS.create(
            scriptItem=script,
            voice=name,
            speed=1.3
    )
    for template in templates:

        for preset in presets:

            mix = audiostack.Production.Mix.create(
                speechItem=speech,
                soundTemplate=template,
                masteringPreset=preset,
            )
            print(mix)

      

            mix.download(fileName=f"V4_{name}_{template}_{preset}")

            print(mix)