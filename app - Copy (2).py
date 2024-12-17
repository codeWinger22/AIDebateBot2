# from flask import Flask, render_template, request, jsonify, send_file
# import requests
# import speech_recognition as sr
# from gtts import gTTS
# from pydub import AudioSegment
# import os
# import logging
# import google.generativeai as genai

# app = Flask(__name__)

# # Dummy API credentials (replace with real ones if available)
# GEMINI_API_URL = "https://api.gemini.google.com/v1/messages"
# GEMINI_API_KEY = "AIzaSyCDEm8zz2nYtX4ziR5Edl6kzbwcoz-Kvng"

# # Configure logging
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# # Initialize recognizer
# recognizer = sr.Recognizer()

# # List of debate topics
# TOPICS = [
#     "Please Select One Topic",
#     "Should animals be kept in zoos?",
#     "Is homework necessary for learning?",
#     "Should school uniforms be mandatory?",
#     "Is social media harmful to teenagers?"
# ]

# @app.route('/')
# def home():
#     return render_template('index.html', topics=TOPICS)

# @app.route('/debate', methods=['POST'])
# def debate():
#     # Get selected topic and user argument audio
#     topic = request.form.get('topic')
#     if not topic:
#         logging.error("No topic selected")
#         return jsonify({"error": "No topic selected"}), 400

#     if 'audio' not in request.files:
#         logging.error("No audio file provided")
#         return jsonify({"error": "No audio file provided"}), 400

#     audio_file = request.files['audio']
#     audio_path = 'user_audio.wav'

#     # Convert audio file to WAV format
#     try:
#         audio_data = AudioSegment.from_file(audio_file)
#         audio_data.export(audio_path, format='wav', parameters=["-acodec", "pcm_s16le", "-ar", "16000"])
#         logging.info("Audio file converted to WAV successfully.")
#     except Exception as e:
#         logging.error(f"Audio conversion failed: {e}")
#         return jsonify({"error": f"Audio conversion failed: {e}"}), 500

#     # Recognize speech from audio
#     try:
#         with sr.AudioFile(audio_path) as source:
#             audio = recognizer.record(source)
#             user_text = recognizer.recognize_google(audio)
#             logging.info(f"User's argument transcribed: {user_text}")
#     except sr.UnknownValueError:
#         logging.error("Speech recognition could not understand the audio")
#         return jsonify({"error": "Speech recognition could not understand the audio"}), 500
#     except sr.RequestError as e:
#         logging.error(f"Speech recognition service error: {e}")
#         return jsonify({"error": f"Speech recognition service error: {e}"}), 500
#     finally:
#         os.remove(audio_path)

#     # Prepare prompt for AI to take the opposing side
#     prompt = f"The topic is: '{topic}'. The user argued: '{user_text}'. Please respond by taking the opposing side in this debate."

#     # Request AI response
#     try:
#         genai.configure(api_key=GEMINI_API_KEY)
#         model = genai.GenerativeModel("gemini-1.5-flash")
#         response = model.generate_content(prompt)
#         logging.info(f"AI response received: {response.text}")
#     except requests.exceptions.RequestException as e:
#         logging.error(f"API request failed: {e}")
#         return jsonify({"error": f"API request failed: {e}"}), 500
#     except KeyError:
#         logging.error("Unexpected response format from the Gemini API")
#         return jsonify({"error": "Unexpected response format from the Gemini API"}), 500

#     # Convert AI response to audio
#     response_audio_path = "bot_response.mp3"
#     try:
#         tts = gTTS(response.text, lang='en')
#         tts.save(response_audio_path)
#         logging.info("AI response converted to speech successfully.")
#     except Exception as e:
#         logging.error(f"Text-to-speech conversion failed: {e}")
#         return jsonify({"error": f"Text-to-speech conversion failed: {e}"}), 500

#     return send_file(response_audio_path, as_attachment=False)

# if __name__ == '__main__':
#     app.run(debug=True)






# from flask import Flask, render_template, request, jsonify, send_file
# import requests
# import speech_recognition as sr
# from gtts import gTTS
# from pydub import AudioSegment
# import os
# import logging
# import google.generativeai as genai

# app = Flask(__name__)

# # Dummy API credentials (replace with real ones if available)
# GEMINI_API_URL = "https://api.gemini.google.com/v1/messages"
# GEMINI_API_KEY = "AIzaSyCDEm8zz2nYtX4ziR5Edl6kzbwcoz-Kvng"

# # Configure logging
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# # Initialize recognizer
# recognizer = sr.Recognizer()

# # List of debate topics
# TOPICS = [
#     "Please Select One Topic",
#     "Should animals be kept in zoos?",
#     "Is homework necessary for learning?",
#     "Should school uniforms be mandatory?",
#     "Is social media harmful to teenagers?"
# ]

# @app.route('/')
# def home():
#     return render_template('index.html', topics=TOPICS)

# @app.route('/debate', methods=['POST'])
# def debate():
#     # Get selected topic and user argument audio
#     topic = request.form.get('topic')
#     if not topic:
#         logging.error("No topic selected")
#         return jsonify({"error": "No topic selected"}), 400

#     if 'audio' not in request.files:
#         logging.error("No audio file provided")
#         return jsonify({"error": "No audio file provided"}), 400

#     audio_file = request.files['audio']
#     audio_path = 'user_audio.wav'

#     # Convert audio file to WAV format
#     try:
#         audio_data = AudioSegment.from_file(audio_file)
#         audio_data.export(audio_path, format='wav', parameters=["-acodec", "pcm_s16le", "-ar", "16000"])
#         logging.info("Audio file converted to WAV successfully.")
#     except Exception as e:
#         logging.error(f"Audio conversion failed: {e}")
#         return jsonify({"error": f"Audio conversion failed: {e}"}), 500

#     # Recognize speech from audio
#     try:
#         with sr.AudioFile(audio_path) as source:
#             audio = recognizer.record(source)
#             user_text = recognizer.recognize_google(audio)
#             logging.info(f"User's argument transcribed: {user_text}")
#     except sr.UnknownValueError:
#         logging.error("Speech recognition could not understand the audio")
#         return jsonify({"error": "Speech recognition could not understand the audio"}), 500
#     except sr.RequestError as e:
#         logging.error(f"Speech recognition service error: {e}")
#         return jsonify({"error": f"Speech recognition service error: {e}"}), 500
#     finally:
#         os.remove(audio_path)

#     # Prepare prompt for AI to take the opposing side with length guidance
#     user_argument_length = len(user_text.split())
#     if user_argument_length < 20:
#         length_instruction = "Keep the response brief."
#     elif user_argument_length < 50:
#         length_instruction = "Provide a moderate-length response."
#     else:
#         length_instruction = "Provide a detailed response."

#     prompt = f"The topic is: '{topic}'. The user argued: '{user_text}'. Please respond by taking the opposing side in this debate. {length_instruction}"

#     # Request AI response
#     try:
#         genai.configure(api_key=GEMINI_API_KEY)
#         model = genai.GenerativeModel("gemini-1.5-flash")
#         response = model.generate_content(prompt)
#         logging.info(f"AI response received: {response.text}")
#     except requests.exceptions.RequestException as e:
#         logging.error(f"API request failed: {e}")
#         return jsonify({"error": f"API request failed: {e}"}), 500
#     except KeyError:
#         logging.error("Unexpected response format from the Gemini API")
#         return jsonify({"error": "Unexpected response format from the Gemini API"}), 500

#     # Convert AI response to audio
#     response_audio_path = "bot_response.mp3"
#     try:
#         tts = gTTS(response.text, lang='en')
#         tts.save(response_audio_path)
#         logging.info("AI response converted to speech successfully.")
#     except Exception as e:
#         logging.error(f"Text-to-speech conversion failed: {e}")
#         return jsonify({"error": f"Text-to-speech conversion failed: {e}"}), 500

#     return send_file(response_audio_path, as_attachment=False)

# if __name__ == '__main__':
#     app.run(debug=True)



# from flask import Flask, render_template, request, send_file
# import speech_recognition as sr
# from gtts import gTTS
# from pydub import AudioSegment
# import google.generativeai as genai
# import os

# app = Flask(__name__)

# TOPICS = [
#     "Should animals be kept in zoos?",
#     "Is homework necessary for learning?",
#     "Should school uniforms be mandatory?",
#     "Is social media harmful to teenagers?"
# ]

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/debate')
# def debate():
#     topic = request.args.get('topic')
#     return render_template('debate.html', topic=topic)

# @app.route('/debate', methods=['POST'])
# def handle_debate():
#     topic = request.form.get('topic')
#     audio_file = request.files['audio']
#     audio_path = 'user_audio.wav'
    
#     audio_data = AudioSegment.from_file(audio_file)
#     audio_data.export(audio_path, format='wav')
    
#     recognizer = sr.Recognizer()
#     with sr.AudioFile(audio_path) as source:
#         audio = recognizer.record(source)
#         user_text = recognizer.recognize_google(audio)
    
#     prompt = f"Topic: {topic}. Oppose: '{user_text}'"
#     genai.configure(api_key="YOUR_GEMINI_API_KEY")
#     model = genai.GenerativeModel("gemini-1.5-flash")
#     response = model.generate_content(prompt)
    
#     response_audio_path = "bot_response.mp3"
#     tts = gTTS(response.text, lang='en')
#     tts.save(response_audio_path)

#     return send_file(response_audio_path, as_attachment=False)

# if __name__ == '__main__':
#     app.run(debug=True)


# from flask import Flask, render_template, request, send_file
# import speech_recognition as sr
# from gtts import gTTS
# from pydub import AudioSegment
# import google.generativeai as genai
# import os

# app = Flask(__name__)

# TOPICS = [
#     "Should animals be kept in zoos?",
#     "Is homework necessary for learning?",
#     "Should school uniforms be mandatory?",
#     "Is social media harmful to teenagers?"
# ]

# # Initialize Generative AI
# genai.configure(api_key="AIzaSyCDEm8zz2nYtX4ziR5Edl6kzbwcoz-Kvng")
# model = genai.GenerativeModel("gemini-1.5-flash")

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/debate')
# def debate():
#     topic = request.args.get('topic')
#     return render_template('debate.html', topic=topic)

# @app.route('/debate', methods=['POST'])
# def handle_debate():
#     topic = request.form.get('topic')
#     audio_file = request.files['audio']
#     audio_path = 'user_audio.wav'

#     # Convert audio to WAV
#     audio_data = AudioSegment.from_file(audio_file)
#     audio_data.export(audio_path, format='wav')

#     # Transcribe user audio
#     recognizer = sr.Recognizer()
#     with sr.AudioFile(audio_path) as source:
#         audio = recognizer.record(source)
#         user_text = recognizer.recognize_google(audio)

#     # Generate AI response
#     prompt = f"Topic: {topic}. Oppose: '{user_text}'"
#     response = model.generate_content(prompt)

#     # Convert AI response to audio
#     response_audio_path = "bot_response.mp3"
#     tts = gTTS(response.text, lang='en')
#     tts.save(response_audio_path)

#     # Save arguments for AI-based winner analysis
#     with open("arguments.txt", "a") as f:
#         f.write(f"User: {user_text}\n")
#         f.write(f"Bot: {response.text}\n")

#     return send_file(response_audio_path, as_attachment=False)

# @app.route('/end_debate', methods=['GET'])
# def end_debate():
#     # Compile all arguments for analysis
#     with open("arguments.txt", "r") as f:
#         arguments = f.read()

#     # Ask AI to decide the winner
#     prompt = f"Review the following debate arguments and decide the winner based on strength, clarity, and relevance of points. Respond with a winner and a brief reasoning. Debate arguments:\n{arguments}"
#     decision = model.generate_content(prompt)

#     # Convert winner announcement to audio
#     winner_audio_path = "winner_announcement.mp3"
#     tts = gTTS(decision.text, lang='en')
#     tts.save(winner_audio_path)

#     # Clear the arguments file for the next debate
#     open("arguments.txt", "w").close()

#     return send_file(winner_audio_path, as_attachment=False)

# if __name__ == '__main__':
#     app.run(debug=True)


# from flask import Flask, render_template, request, send_file
# import speech_recognition as sr
# from gtts import gTTS
# from pydub import AudioSegment
# import google.generativeai as genai
# import os

# app = Flask(__name__)

# TOPICS = [
#     "Should animals be kept in zoos?",
#     "Is homework necessary for learning?",
#     "Should school uniforms be mandatory?",
#     "Is social media harmful to teenagers?"
# ]

# # Initialize Generative AI with API key from environment variable
# genai.configure(api_key="AIzaSyCDEm8zz2nYtX4ziR5Edl6kzbwcoz-Kvng")
# model = genai.GenerativeModel("gemini-1.5-flash")

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/debate')
# def debate():
#     topic = request.args.get('topic')
#     return render_template('debate.html', topic=topic)

# @app.route('/debate', methods=['POST'])
# def handle_debate():
#     topic = request.form.get('topic')
#     audio_file = request.files['audio']
#     audio_path = 'user_audio.wav'

#     # Convert audio to WAV
#     audio_data = AudioSegment.from_file(audio_file)
#     audio_data.export(audio_path, format='wav')

#     # Transcribe user audio
#     recognizer = sr.Recognizer()
#     with sr.AudioFile(audio_path) as source:
#         audio = recognizer.record(source)
#         user_text = recognizer.recognize_google(audio)

#     # Limit response length to match user input length
#     user_word_count = len(user_text.split())
#     max_response_length = user_word_count + 50

#     # Generate AI response with improved debate tone
#     prompt = (
#         f"Topic: {topic}. You are debating against this statement: '{user_text}'. "
#         f"Craft a strong, clear, and respectful rebuttal, arguing in the opposite direction. "
#         f"Keep the response engaging and similar in length to the user's argument."
#     )
#     response = model.generate_content(prompt)

#     # Convert AI response to audio
#     response_audio_path = "bot_response.mp3"
#     tts = gTTS(response.text, lang='en')
#     tts.save(response_audio_path)

#     # Save arguments for AI-based winner analysis
#     with open("arguments.txt", "a") as f:
#         f.write(f"User: {user_text}\n")
#         f.write(f"Bot: {response.text}\n")

#     return send_file(response_audio_path, as_attachment=False)

# @app.route('/end_debate', methods=['GET'])
# def end_debate():
#     # Compile all arguments for analysis
#     with open("arguments.txt", "r") as f:
#         arguments = f.read()

#     # Ask AI to decide the winner concisely
#     prompt = (
#         f"Based on the debate arguments below, determine the winner based on the strength and clarity "
#         f"of their points. Provide a concise, friendly, and encouraging winner announcement.\n\n"
#         f"Debate arguments:\n{arguments}"
#     )
#     decision = model.generate_content(prompt)

#     # Convert winner announcement to audio
#     winner_audio_path = "winner_announcement.mp3"
#     tts = gTTS(decision.text, lang='en')
#     tts.save(winner_audio_path)

#     # Clear the arguments file for the next debate
#     open("arguments.txt", "w").close()

#     return send_file(winner_audio_path, as_attachment=False)

# if __name__ == '__main__':
#     app.run(debug=True)



#working code below last 


# from flask import Flask, render_template, request, send_file, jsonify
# import speech_recognition as sr
# from gtts import gTTS
# from pydub import AudioSegment
# import google.generativeai as genai
# import os

# app = Flask(__name__)

# TOPICS = [
#     "Should animals be kept in zoos?",
#     "Is homework necessary for learning?",
#     "Should school uniforms be mandatory?",
#     "Is social media harmful to teenagers?"
# ]

# # Initialize Generative AI with API key from environment variable
# genai.configure(api_key="AIzaSyCDEm8zz2nYtX4ziR5Edl6kzbwcoz-Kvng")  # Replace with your actual API key
# model = genai.GenerativeModel("gemini-1.5-flash")

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/debate')
# def debate():
#     topic = request.args.get('topic')
#     return render_template('debate.html', topic=topic)

# @app.route('/debate', methods=['POST'])
# def handle_debate():
#     topic = request.form.get('topic')
#     audio_file = request.files.get('audio')

#     # Check if the audio file is present in the request
#     if not audio_file:
#         return jsonify({"error": "No audio file provided. Please upload your audio."}), 400

#     audio_path = 'user_audio.wav'

#     try:
#         # Convert audio to WAV
#         audio_data = AudioSegment.from_file(audio_file)
#         audio_data.export(audio_path, format='wav')

#         # Transcribe user audio with error handling
#         recognizer = sr.Recognizer()
#         with sr.AudioFile(audio_path) as source:
#             audio = recognizer.record(source)
#             try:
#                 user_text = recognizer.recognize_google(audio)
#             except sr.UnknownValueError:
#                 # If speech recognition fails to understand the audio
#                 error_message = "Sorry, I couldn't understand the audio. Please try again."
#                 return generate_audio_response(error_message)
#             except sr.RequestError as e:
#                 # Handle issues with the Google Speech API
#                 return jsonify({"error": f"Could not request results from Google Speech Recognition service; {e}"}), 500

#     except Exception as e:
#         return jsonify({"error": f"Error processing audio: {str(e)}"}), 500

#     if not user_text.strip():  # Check if no valid text was recognized
#         error_message = "No speech detected in the audio. Please speak clearly."
#         return generate_audio_response(error_message)

#     # Calculate the user's input length
#     user_word_count = len(user_text.split())

#     # Generate AI response with improved debate tone
#     prompt = (
#         f"Topic: {topic}. The user argued: '{user_text}'. "
#         f"Respond in a clear, respectful, and engaging rebuttal, closely matching the length of the user's argument "
#         f"which is approximately {user_word_count} words."
#     )
#     response = model.generate_content(prompt)

#     # Convert AI response to audio
#     response_audio_path = "bot_response.mp3"
#     tts = gTTS(response.text, lang='en')
#     tts.save(response_audio_path)

#     # Save arguments for AI-based winner analysis
#     with open("arguments.txt", "a") as f:
#         f.write(f"User: {user_text}\n")
#         f.write(f"Bot: {response.text}\n")

#     return send_file(response_audio_path, as_attachment=False)


# def generate_audio_response(message):
#     """
#     This function generates an audio response for a given text message using Google Text-to-Speech (gTTS).
#     It saves the audio as an MP3 file and returns it as a response.
#     """
#     audio_path = "error_response.mp3"
#     tts = gTTS(message, lang='en')
#     tts.save(audio_path)
#     return send_file(audio_path, as_attachment=False)


# @app.route('/end_debate', methods=['GET'])
# def end_debate():
#     # Compile all arguments for analysis
#     with open("arguments.txt", "r") as f:
#         arguments = f.read()

#     # Ask AI to decide the winner concisely
#     prompt = (
#         f"Based on the debate arguments below, determine the winner based on the strength and clarity "
#         f"of their points. Provide a concise, friendly, and encouraging winner announcement.\n\n"
#         f"Debate arguments:\n{arguments}"
#     )
#     decision = model.generate_content(prompt)

#     # Convert winner announcement to audio
#     winner_audio_path = "winner_announcement.mp3"
#     tts = gTTS(decision.text, lang='en')
#     tts.save(winner_audio_path)

#     # Clear the arguments file for the next debate
#     open("arguments.txt", "w").close()

#     return send_file(winner_audio_path, as_attachment=False)

# if __name__ == '__main__':
#     app.run(debug=True)



#main code 
from flask import Flask, render_template, request, send_file, jsonify
import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment
import google.generativeai as genai
import os

app = Flask(__name__)

TOPICS = [
    "Should animals be kept in zoos?",
    "Is homework necessary for learning?",
    "Should school uniforms be mandatory?",
    "Is social media harmful to teenagers?"
]

# Initialize Generative AI with API key from environment variable
genai.configure(api_key="AIzaSyCX4TV1u09XHV_tSGhsT16WKx16gmNRCC8")  # Replace with your actual API key
model = genai.GenerativeModel("gemini-1.5-flash")

@app.route('/')
def index():
    print("Step 6: Clearing the arguments file after response.")
    arguments_path = "arguments.txt"
    with open(arguments_path, "w") as f:
        f.truncate()  # Clear the file contents safely
        f.close()
    return render_template('index.html')



@app.route('/debate', methods=['POST', 'GET'])
def handle_debate():
    if request.method == 'GET':
        # Handle the request from index.html to pass the debate topic
        topic = request.args.get('topic')
        if not topic:
            return "No topic provided. Please go back and select a topic.", 400

        # Prime the AI with the debate topic
        priming_prompt = (
            f"You will engage in a debate on the topic: '{topic}'. "
            f"Your opponent is a child aged 6–10 years old. Your responses should be clear, engaging, and respectful, "
            f"using simple language that a child of this age can understand. Keep your arguments relevant to the topic "
            f"and structured like a friendly human debate partner."
        )
        model.generate_content(priming_prompt)  # Prime the AI with the topic context

        # Render the debate page and pass the topic
        return render_template('debate.html', topic=topic)

    elif request.method == 'POST':
        # Handle the debate processing when audio is uploaded
        topic = request.form.get('topic')  # Retrieve topic from form data if available
        audio_file = request.files.get('audio')

        # Check if the audio file is present in the request
        if not audio_file:
            return jsonify({"error": "No audio file provided. Please upload your audio."}), 400

        audio_path = 'user_audio.wav'

        try:
            # Convert audio to WAV
            audio_data = AudioSegment.from_file(audio_file)
            audio_data.export(audio_path, format='wav')

            # Transcribe user audio with error handling
            recognizer = sr.Recognizer()
            with sr.AudioFile(audio_path) as source:
                audio = recognizer.record(source)
                try:
                    user_text = recognizer.recognize_google(audio)
                except sr.UnknownValueError:
                    error_message = "Sorry, I couldn't understand the audio. Please try again."
                    return generate_audio_response(error_message)
                except sr.RequestError as e:
                    return jsonify({"error": f"Could not request results from Google Speech Recognition service; {e}"}), 500

        except Exception as e:
            return jsonify({"error": f"Error processing audio: {str(e)}"}), 500

        if not user_text.strip():  # Check if no valid text was recognized
            error_message = "No speech detected in the audio. Please speak clearly."
            return generate_audio_response(error_message)

        # Generate AI response
        user_word_count = len(user_text.split())
        target_word_count = user_word_count * 2  # Ensure AI response is approximately double the user's length
        prompt = (
            f"Topic: '{topic}'. The user argued: '{user_text}'. "
            f"Respond with a clear, respectful, and engaging rebuttal, "
            f"using simple language suitable for a child aged 6–10. "
            f"Ensure your response is approximately {target_word_count} words, but complete the last sentence even "
            f"if it slightly exceeds the word limit. Keep your arguments relevant to the topic and structured like a human-friendly debate partner."
        )
        response = model.generate_content(prompt)

        # Convert AI response to audio
        response_audio_path = "bot_response.mp3"
        tts = gTTS(response.text, lang='en')
        tts.save(response_audio_path)

        # Save arguments for AI-based winner analysis
        with open("arguments.txt", "a") as f:
            f.write(f"Debate Topic: {topic}\n")
            f.write(f"User: {user_text}\n")
            f.write(f"Bot: {response.text}\n\n")
            print("arguments saved successfully")
            f.close()

        return send_file(response_audio_path, as_attachment=False)



#working code but ai responses not better
# @app.route('/debate', methods=['POST', 'GET'])
# def handle_debate():
#     if request.method == 'GET':
#         # Handle the request from index.html to pass the debate topic
#         topic = request.args.get('topic')
#         if not topic:
#             return "No topic provided. Please go back and select a topic.", 400
#         # Render the debate page and pass the topic
#         return render_template('debate.html', topic=topic)

#     elif request.method == 'POST':
#         # Handle the debate processing when audio is uploaded
#         topic = request.form.get('topic')  # Retrieve topic from form data if available
#         audio_file = request.files.get('audio')

#         # Check if the audio file is present in the request
#         if not audio_file:
#             return jsonify({"error": "No audio file provided. Please upload your audio."}), 400

#         audio_path = 'user_audio.wav'

#         try:
#             # Convert audio to WAV
#             audio_data = AudioSegment.from_file(audio_file)
#             audio_data.export(audio_path, format='wav')

#             # Transcribe user audio with error handling
#             recognizer = sr.Recognizer()
#             with sr.AudioFile(audio_path) as source:
#                 audio = recognizer.record(source)
#                 try:
#                     user_text = recognizer.recognize_google(audio)
#                 except sr.UnknownValueError:
#                     error_message = "Sorry, I couldn't understand the audio. Please try again."
#                     return generate_audio_response(error_message)
#                 except sr.RequestError as e:
#                     return jsonify({"error": f"Could not request results from Google Speech Recognition service; {e}"}), 500

#         except Exception as e:
#             return jsonify({"error": f"Error processing audio: {str(e)}"}), 500

#         if not user_text.strip():  # Check if no valid text was recognized
#             error_message = "No speech detected in the audio. Please speak clearly."
#             return generate_audio_response(error_message)

#         # Generate AI response
#         user_word_count = len(user_text.split())
#         prompt = (
#             f"Topic: {topic}. The user argued: '{user_text}'. "
#             f"Respond in a clear, respectful, and engaging rebuttal, closely matching the length of the user's argument. "
#             f"Also keep in mind that the user is of age 6 to 10, so argue according to the level of the children, "
#             f"which is approximately {user_word_count} words."
#         )
#         response = model.generate_content(prompt)

#         # Convert AI response to audio
#         response_audio_path = "bot_response.mp3"
#         tts = gTTS(response.text, lang='en')
#         tts.save(response_audio_path)

#         # Save arguments for AI-based winner analysis
#         with open("arguments.txt", "a") as f:
#             f.write(f"Debate Topic: {topic}\n")
#             f.write(f"User: {user_text}\n")
#             f.write(f"Bot: {response.text}\n\n")

#         return send_file(response_audio_path, as_attachment=False)


# @app.route('/debate', methods=['POST','GET'])
# def handle_debate():
#     if(request.method == 'GET'):

#         topic = request.args.get('topic')
#         print(topic)
#     audio_file = request.files.get('audio')

#     # Check if the audio file is present in the request
#     if not audio_file:
#         return jsonify({"error": "No audio file provided. Please upload your audio."}), 400

#     audio_path = 'user_audio.wav'

#     try:
#         # Convert audio to WAV
#         audio_data = AudioSegment.from_file(audio_file)
#         audio_data.export(audio_path, format='wav')

#         # Transcribe user audio with error handling
#         recognizer = sr.Recognizer()
#         with sr.AudioFile(audio_path) as source:
#             audio = recognizer.record(source)
#             try:
#                 user_text = recognizer.recognize_google(audio)
#             except sr.UnknownValueError:
#                 # If speech recognition fails to understand the audio
#                 error_message = "Sorry, I couldn't understand the audio. Please try again."
#                 return generate_audio_response(error_message)
#             except sr.RequestError as e:
#                 # Handle issues with the Google Speech API
#                 return jsonify({"error": f"Could not request results from Google Speech Recognition service; {e}"}), 500

#     except Exception as e:
#         return jsonify({"error": f"Error processing audio: {str(e)}"}), 500

#     if not user_text.strip():  # Check if no valid text was recognized
#         error_message = "No speech detected in the audio. Please speak clearly."
#         return generate_audio_response(error_message)

#     # Calculate the user's input length
#     user_word_count = len(user_text.split())

#     # Generate AI response with improved debate tone
#     prompt = (
#         f"Topic: {topic}. The user argued: '{user_text}'. "
#         f"Respond in a clear, respectful, and engaging rebuttal, closely matching the length of the user's argument. also keep in mind that user is of age 6 to 10 so argue according to the level of the childrens"
#         f"which is approximately {user_word_count} words."
#     )
#     response = model.generate_content(prompt)

#     # Convert AI response to audio
#     response_audio_path = "bot_response.mp3"
#     tts = gTTS(response.text, lang='en')
#     tts.save(response_audio_path)

#     # Save arguments for AI-based winner analysis
#     with open("arguments.txt", "a") as f:
#         f.write(f"Debate Topic: {topic}\n")
#         f.write(f"User: {user_text}\n")
#         f.write(f"Bot: {response.text}\n\n")

#     return send_file(response_audio_path, as_attachment=False)


# def generate_audio_response(message):
#     """
#     This function generates an audio response for a given text message using Google Text-to-Speech (gTTS).
#     It saves the audio as an MP3 file and returns it as a response.
#     """
#     audio_path = "error_response.mp3"
#     tts = gTTS(message, lang='en')
#     tts.save(audio_path)
#     return send_file(audio_path, as_attachment=False)


#last working

# @app.route('/end_debate', methods=['GET', 'POST'])
# def end_debate():
#     try:
#         print("Step 1: Reached end_debate endpoint")  # Log when the endpoint is accessed
        
#         # Compile all arguments for analysis
#         print("Step 2: Reading arguments from file")
#         arguments_path = "arguments.txt"
        
#         # Check if the arguments file exists
#         if not os.path.exists(arguments_path):
#             print(f"Error: Arguments file '{arguments_path}' does not exist.")
#             return jsonify({"error": "No debate data available. Please start a debate first."}), 400
        
#         with open(arguments_path, "r") as f:
#             arguments = f.readlines()  # Read arguments line-by-line for evaluation
        
#         # Check if arguments exist
#         if not arguments:
#             print("Step 3: No arguments found in the file.")
#             winner = "No winner"
#         else:
#             print("Step 3: Arguments loaded successfully.")
#             # Extract and count user and bot arguments
#             user_arguments = [arg for arg in arguments if arg.startswith("User:")]
#             bot_arguments = [arg for arg in arguments if arg.startswith("Bot:")]

#             total_user_args = len(user_arguments)
#             total_bot_args = len(bot_arguments)
#             print(f"User Arguments: {total_user_args}, Bot Arguments: {total_bot_args}")

#             # Calculate debate duration and threshold
#             debate_duration = 3  # in minutes (set according to your logic)
#             min_expected_args = debate_duration   # Minimum threshold
            
#             # Check if user meets the criteria for evaluation
#             if total_user_args > min_expected_args:
#                 print("Step 4: User meets the criteria for evaluation.")
#                 # Evaluate user arguments for relevance and length
#                 relevance_prompt = (
#     f"Evaluate whether all of the user's arguments are relevant to the debate topic. "
#     f"Respond with 'Yes' if all arguments are relevant, otherwise respond with 'No'. "
#     f"Debate topic is the context.\n\n"
#     f"User arguments:\n" + "\n".join(user_arguments)
# )
#                 relevance_score = model.generate_content(relevance_prompt).text.strip()
#                 print(f"AI Relevance Score: {relevance_score}")

#                 # Parse the relevance score
#                 ##   relevance_score = float(relevance_score)
#                 #except ValueError:
#                  #   print("Error: Relevance score is not a valid number. Defaulting to 0.")
#                   #  relevance_score = 0.0  # Fallback to 0 if the AI response is invalid

#                 # Determine the winner based on criteria
#                 if relevance_score == "Yes":
#                     winner = "User"
#                 else:
#                     winner = "Bot"
#             else:
#                 print("Step 4: User does not meet the criteria for evaluation.")
#                 winner = "Bot"

#         # Convert winner announcement to audio
#         winner_audio_path = "winner_announcement.mp3"
#         if winner == "No winner":
#             tts = gTTS(f"No winner declared for this debate.", lang='en')
#         else:
#             tts = gTTS(f"The winner is: {winner}.", lang='en')
#         tts.save(winner_audio_path)
#         print("Step 5: Winner announcement audio generated.")

#         # Clear the arguments file for the next debate
#         open(arguments_path, "w").close()
#         print("Step 6: Arguments file cleared for the next debate.")

#         # Send the winner announcement audio as a response
#         return send_file(winner_audio_path, as_attachment=False)

#     except Exception as e:
#         print(f"Error in end_debate: {e}")
#         return jsonify({"error": "An error occurred while processing the debate."}), 500


@app.route('/end_debate', methods=['GET', 'POST'])
def end_debate():
    try:
        print("Step 1: Reached end_debate endpoint")  # Log when the endpoint is accessed
        
        # Compile all arguments for analysis
        print("Step 2: Reading arguments from file")
        arguments_path = "arguments.txt"
        
        # Check if the arguments file exists
        if not os.path.exists(arguments_path):
            print(f"Error: Arguments file '{arguments_path}' does not exist.")
            return jsonify({"error": "No debate data available. Please start a debate first."}), 400
        
        with open(arguments_path, "r") as f:
            arguments = f.readlines()  # Read arguments line-by-line for evaluation
        
        # Check if arguments exist
        if not arguments:
            print("Step 3: No arguments found in the file.")
            winner = "No winner"
        else:
            print("Step 3: Arguments loaded successfully.")
            
            topic_line = next((line for line in arguments if line.startswith("Topic:")), None)
            topic = topic_line.split("Topic: ")[1].strip() if topic_line else "Unknown Topic"
            # Extract and count user and bot arguments
            user_arguments = [arg for arg in arguments if arg.startswith("User:")]
            bot_arguments = [arg for arg in arguments if arg.startswith("Bot:")]

            total_user_args = len(user_arguments)
            total_bot_args = len(bot_arguments)
            print(f"User Arguments: {total_user_args}, Bot Arguments: {total_bot_args}")

            # Calculate debate duration and threshold
            debate_duration = 3  # in minutes (set according to your logic)
            min_expected_args = debate_duration   # Minimum threshold
            
            # Check if user meets the criteria for evaluation
            if total_user_args >= min_expected_args:
                print("Step 4: User meets the criteria for evaluation.")
                # Evaluate user arguments for relevance and length
                #relevance_prompt = (
                 #   f"Evaluate whether all of the user's arguments are relevant to the debate topic. "
                  ##  f"Respond with 'Yes' if all arguments are relevant, otherwise respond with 'No'. "
                   # f"Debate topic is the context.\n\n"
                   # f"User arguments:\n" + "\n".join(user_arguments)
                #)
                relevance_prompt = (
    f"Evaluate the relevance of the user's arguments based on the following conditions:\n"
    f"1. Ignore errors caused by speech-to-text misinterpretation (e.g., 'shoes' instead of 'zoos') and evaluate the intended meaning.\n"
    f"2. Include deliberate repetitions of the same argument made more than twice.\n"
    f"3. For all arguments, consider an argument relevant if it contains at least 3 words related to the debate topic.\n"
    f"4. Calculate the total number of arguments made by the user.\n"
    f"5. If at least 60% of the user's arguments are deemed relevant, respond with 'Yes'; otherwise, respond with 'No'.\n\n"
    f"Debate topic: '{topic}'\n\n"
    f"User arguments:\n" + "\n".join(user_arguments)
)

            
                relevance_score = model.generate_content(relevance_prompt).text.strip()
                print(f"AI Relevance Score: {relevance_score}")

                # Determine the winner based on criteria
                if relevance_score == "Yes":
                   winner = "User"
                else:
                   winner = "Bot"
            #     try:
            #         relevance_score = float(relevance_score)
            #     except ValueError:
            #         relevance_score = 0.0  # Fallback to 0 if the AI response is invalid

            # # Determine the winner based on criteria
            #     if relevance_score >= 3:
            #         winner = "User"
            #     else:
            #         winner = "Bot"
            else:
                print("Step 4: User does not meet the criteria for evaluation.")
                winner = "Bot"

        # Convert winner announcement to audio
        winner_audio_path = "winner_announcement.mp3"
        if winner == "No winner":
            tts = gTTS(f"No winner declared for this debate.", lang='en')
        else:
            tts = gTTS(f"The winner is: {winner}.", lang='en')
        tts.save(winner_audio_path)
        print("Step 5: Winner announcement audio generated.")

        # Send the winner announcement audio as a response
        response = send_file(winner_audio_path, as_attachment=False)

        # Clear the arguments file only after the response has been sent
        
        
        return response

    except Exception as e:
        print(f"Error in end_debate: {e}")
        return jsonify({"error": "An error occurred while processing the debate."}), 500


if __name__ == '__main__':
    app.run(debug=True)

