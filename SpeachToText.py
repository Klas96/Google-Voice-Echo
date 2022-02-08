import os
from gtts import gTTS
# import required module
from playsound import playsound
import pyaudio
import wave
from google.cloud import speech
from record_from_mic import record_from_mic
from google.cloud import texttospeech



# for playing note.wav file

credential_path = "/home/klas/Documents/Programering/web/GoogleSpechTextAPI/key.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

speach_to_text_client = speech.SpeechClient()
text_to_speach_client = texttospeech.TextToSpeechClient()

def mimic_me():

    # start Recording

    record_from_mic()

    with open(speech_file, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=44100,
        language_code="sv-SE",
    )


    operation = speach_to_text_client.long_running_recognize(config=config, audio=audio)

    print("Waiting for operation to complete...")
    response = operation.result(timeout=90)

    # Text to Speach
    speach_to_text_client
    language = 'fr'
    
    
    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        #print(u"Transcript: {}".format(result.alternatives[0].transcript))
        say_this = result.alternatives[0].transcript
        print(say_this)

        # Set the text input to be synthesized
        synthesis_input = texttospeech.SynthesisInput(text=say_this)

        voice = texttospeech.VoiceSelectionParams(
            language_code="sv-SV", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
        )

        # Select the type of audio file you want returned
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

        # Perform the text-to-speech request on the text input with the selected
        # voice parameters and audio file type
        response = speach_to_text_client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        # The response's audio_content is binary.
        with open("output.mp3", "wb") as out:
            # Write the response to the output file.
            out.write(response.audio_content)
            print('Audio content written to file "output.mp3"')

        myobj = gTTS(text=say_this, lang=language, slow=False)

        audio_file = "output.mp3"
        myobj.save(audio_file)
  
        # Playing the converted file
        playsound(audio_file)
        #os.system("  " + audio_file)
        #print("Confidence: {}".format(result.alternatives[0].confidence))



speech_file = './file.wav'


while True:
    mimic_me()
