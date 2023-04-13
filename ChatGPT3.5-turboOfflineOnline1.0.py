import speech_recognition as sr
import pyttsx3
import openai
import os
import time
import textwrap
from pocketsphinx import LiveSpeech


# Set up speech recognition
r = sr.Recognizer()
mic = sr.Microphone()

# Set up text-to-speech
engine = pyttsx3.init()

# Set the desired rate of speech. (default is 200)
rate = engine.getProperty('rate')
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)
engine.setProperty('rate', 180)
engine.setProperty('volume', 1)
engine.setProperty('pitch', 1.5)
#engine.setProperty('proxy', 'http://proxy.example.com')
engine.setProperty('debug', True)
engine.setProperty('lang', 'en-US')
#engine.setProperty('voiceURI', 'http://example.com/voices/male')
WAKE_UP_WORD = "maria"  # must be all lower case
QUIT_WORD = "goodbye" + WAKE_UP_WORD  
API_KEY = "enter your API_KEY here"  # only the key in ""
openai.api_key = API_KEY
model_id = "gpt-3.5-turbo"
max_tokens = 100


def ChatGPT_conversation(conversation):
    if not conversation:
        conversation = [{"role": "system", "content": "general and expert on everything. I will not anounce who i am, i will just answer"}]
    response = openai.ChatCompletion.create(model=model_id, messages=conversation)
    conversation.append({"role": response.choices[0].message.role, "content": response.choices[0].message.content})
    return conversation


def listen_for_input():
    print("Listening for input...")
    for phrase in LiveSpeech():
        return str(phrase)


def Glisten_for_input():
    with mic as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, phrase_time_limit=20)
    return r.recognize_google(audio, show_all=False)


def main():
    conversation = []
    while True:
        try:
            # Listen for the wake-up word
            print("Listening for wake-up word....")
            input_text = listen_for_input()
            print(input_text)
            if WAKE_UP_WORD in input_text.lower():
                # Wake-up word recognized
                print("Wake-up word recognized!")
                time.sleep(0.5)
                engine.say("Hello")
                engine.say("How can I help you")
                engine.runAndWait()
                while True:
                    print('Listening for initial interaction for this current conversation...')
                    #engine.say("Listening for initial interaction for this current conversation")
                    #engine.runAndWait()
                    
                    input_text = Glisten_for_input()
                    print(input_text)
                    if QUIT_WORD in input_text.lower():
                        engine.say("Goodbye.  If you require further assistance from me, just call out my name,  " + WAKE_UP_WORD )
                        print("Stopping conversation and ending conversation history")                        
                        engine.runAndWait()
                        time.sleep(2)                        
                        break
                    conversation.append({"role": "user", "content": input_text})                    
                    conversation = ChatGPT_conversation(conversation)
                    #wrapped_text = textwrap.fill("{0}: {1}\n".format(conversation[-1]["role"].strip(), conversation[-1]["content"].strip(), width=80))
                    wrapped_text = textwrap.fill("{1}\n".format(conversation[-1]["role"].strip(), conversation[-1]["content"].strip(), width=80))
                    print("{0}: {0}\n{2}".format(conversation[-1]["role"].strip(), conversation[-1]["content"].strip(), wrapped_text))                    
                    engine.say("{1}\n".format(conversation[-1]["role"].strip(), conversation[-1]["content"].strip()))
                    engine.runAndWait()
                    time.sleep(1)
                    engine.say("anything else I can help you with?")
                    engine.runAndWait()
            else:
                engine.say("Wake-up word not recognized")
                print("Wake-up word not recognized!")
                engine.runAndWait()

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error occurred: {e}")
            engine.say("I'm sorry, an error has occured. Please start another session.")
            engine.runAndWait()


# Call the main function
if __name__ == "__main__":
    main()
