"""
GPT voice assistant

1. user says "Hey GPT"
2. then says a command, command is transcribed to text
3. GPT responds to the command
4. use tts to play the response
"""

import os
import openai
import pyttsx3
import dotenv
import speech_recognition as sr

# load environment variables
dotenv.load_dotenv()

# set openai api key
openai.api_key = os.getenv("OPENAI_API_KEY")

# initialize pyttsx3 audio engine
audio_engine = pyttsx3.init()

# gpt model
model = os.getenv("GPT_MODEL")

# keep track of entire conversation, sp that GPT can respond to it and use context, we can set personality in by setting the first prompt
conversation_all = "You are voice assistant, your task is to reply to the user's commands.\n\n"

def speech_to_text():
    """
    Transcribes speech to text
    """
    print("Listening...")
    r = sr.Recognizer()
    with sr.Microphone() as source: # use the default microphone as the audio source
        source.pause_threshold = 1 # seconds of non-speaking audio before a phrase is considered complete
        audio = r.listen(source, timeout=None, phrase_time_limit=None) # record audio prompt
        try:
            text = r.recognize_google(audio) # convert speech to text
            print(text)
            return text
        except Exception as e:
            print(e)
            return ""

def text_to_speech(text):
    """
    Converts text to speech
    """
    audio_engine.say(text)
    audio_engine.runAndWait()

def chatgpt_response(text):
    """
    Get response from chatgpt
    """
    try:
        response = openai.Completion.create(
            model=model,
            prompt=text,
            temperature=0.5,
            max_tokens=4000,
            n=1, # number of responses
            stop=[" Human:", " AI:"], # stop when one of these strings is reached
        )

        # check if valid response
        if 'choices' in response and len(response['choices']) > 0:
            # check if response is not empty
            if response['choices'][0]['text'] != "":
                print('ChatGPT response: ', response['choices'][0]['text'])
                global conversation_all
                conversation_all += ' ' + response['choices'][0]['text'] # add response to conversation
                return response['choices'][0]['text']

        return False

    except Exception as e:
        print(e)
        return False

def main():
    print("Say 'Hey GPT' to start the conversation")
    while True: # run in loop
        text = speech_to_text()
        if text.lower() == "hey gpt": # use lower case to avoid case sensitivity
            text = speech_to_text() # get command

            if text:
                print("Human: " + text)

                global conversation_all
                conversation_all += '\nHuman: ' + text + '\nAI:' # add command to conversation and AI start

                response = chatgpt_response(text)

                if response:
                    text_to_speech(response)
                else:
                    text_to_speech("Sorry, I did not get that.")

if __name__ == "__main__":
    main()