import os
from google.cloud import speech
from google.cloud import texttospeech
from playsound import playsound #TODO replace with pysound
import constants as c


from record_from_mic import record_from_mic


credential_path = "/home/klas/Documents/Programering/web/GoogleSpechTextAPI/key.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

speach_to_text_client = speech.SpeechClient()
text_to_speach_client = texttospeech.TextToSpeechClient()

mic_recording_path = './file.wav'


def spech_to_text() -> str:
    pass


def text_to_audio():
    pass


def mimic_me():
    '''
    Records A audio sampel from the mic and translates it to text 
    then translate it to audio and plays it back to you.
    '''
    #TODO Return audio buffer
    speach_audio_buffer = record_from_mic()

    with open(mic_recording_path, "rb") as audio_file:
        speach_audio_buffer = audio_file.read()

    audio = speech.RecognitionAudio(content=speach_audio_buffer)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz = 44100,
        language_code = c.LANGUAGE,
    )

    response = speach_to_text_client.recognize(config=config, audio=audio)

    say_this_string = ""
    for result in response.results:

        sepach_translate_ret = result.alternatives[0].transcript
        
        say_this_string = say_this_string + sepach_translate_ret
    
    synthesis_input = texttospeech.SynthesisInput(text=say_this_string)

    voice = texttospeech.VoiceSelectionParams(
        language_code = c.LANGUAGE, ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding = texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = text_to_speach_client.synthesize_speech(
        input = synthesis_input, voice=voice, audio_config=audio_config
    )


    mimic_audio_path = "output.mp3"
    with open(mimic_audio_path, "wb") as out:
        out.write(response.audio_content)

    print(say_this_string)
    # Playing the converted file
    playsound(mimic_audio_path)



while True:
    mimic_me()
