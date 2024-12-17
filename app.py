#main code 
from flask import Flask, render_template, request, send_file, jsonify,redirect,url_for,session
import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment
import google.generativeai as genai
import os
import re
from werkzeug.utils import secure_filename
app = Flask(__name__)

TOPICS = [
    "Would you like to live on Mars one day?",
    "Should humans spend more money exploring space?",
    "Is it better to travel to space or explore the deep ocean?",
    "Is the Moon landing the greatest achievement in space?",
    "Do you think there is life on other planets?",
    ""
]

# Initialize Generative AI with API key from environment variable
genai.configure(api_key="AIzaSyDY2Ssf83kk33ZKcYQsMfF90TFKWsCLYBo")  # Replace with your actual API key
model = genai.GenerativeModel("gemini-1.5-flash")
app.secret_key = 'your_secret_key'

@app.route('/startdebate')
def startdebate():
    print(" Clearing the arguments file after response.")
    arguments_path = "arguments.txt"
    with open(arguments_path, "w") as f:
        f.truncate()  # Clear the file contents safely
        f.close()
    
    
    return render_template('index.html')

scenarios = [
    {
        'scenario': 'Which planet is known as the Red Planet?',
        'options': ['Earth', 'Mars', 'Jupiter', 'Venus'],
        'correct': 1
    },
    
]


@app.route('/')
def start_quiz():
    session['current_question'] = 0
    session['trust_score'] = 0  # Set initial meter value to 0
    return redirect(url_for('quiz'))

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    current_question = session.get('current_question', 0)
    trust_score = session.get('trust_score', 0)
    
    if request.method == 'POST':
        selected_option = request.form.get('option')
        correct_option = scenarios[current_question]["correct"]
        
        # Update the trust score based on the answer
        if int(selected_option) == correct_option:
            session['trust_score'] += 10
        else:
            session['trust_score'] -= 10
        
        # Cap trust score between 0 and 100
        if session['trust_score'] > 100:
            session['trust_score'] = 100
        elif session['trust_score'] < 0:
            session['trust_score'] = 0

        # Move to the next question
        session['current_question'] += 1
        current_question = session['current_question']
    
    # Check if the quiz is completed
    if current_question >= len(scenarios):
        return redirect(url_for('startdebate'))

    return render_template('quiz.html', scenario=scenarios[current_question], question_num=current_question + 1, trust_score=session['trust_score'])





@app.route('/debate', methods=['POST', 'GET'])
def handle_debate():
    if request.method == 'GET':
        # Handle the request from index.html to pass the debate topic
        topic = request.args.get('topic')
        with open("topic.txt", "w") as f:
            f.truncate()  # Clear the file contents safely
            f.close()
        if not topic:
            return "No topic provided. Please go back and select a topic.", 400
        
       
        

        try:
            with open("topic.txt", "w") as topic_file:
                topic_file.write(topic)
            print(f"Topic file created successfully.")
        except Exception as e:
            return jsonify({"error": f"Could not create topic file: {str(e)}"}), 500

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
        print(topic)
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
    f"if it slightly exceeds the word limit. Keep your arguments relevant to the topic and structured like a human-friendly debate partner. "
    f"If the user's argument is unrelated to the debate topic, gently correct them by saying, 'This is our topic: {topic}. Please try to stay relevant to the discussion.' "
    f"If the user appears to be repeating previous arguments without adding new ideas, politely inform them: "
    f"'It seems like you're repeating earlier points. Repeated arguments may not help strengthen your position. "
    f"Let’s explore new angles or ideas for a more engaging debate.' "
    f"Always maintain a friendly and encouraging tone while keeping the conversation on track."
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

def generate_audio_response(message):
    """
    This function generates an audio response for a given text message using Google Text-to-Speech (gTTS).
    It saves the audio as an MP3 file and returns it as a response.
    """
    audio_path = "error_response.mp3"
    tts = gTTS(message, lang='en')
    tts.save(audio_path)
    return send_file(audio_path, as_attachment=False)





@app.route('/end_debate', methods=['GET','POST'])
def end_debate():
    print("called again")
    try:
        winner = "No Winner"
        arguments_path = "arguments.txt"

        # Check if the arguments file exists and read arguments
        if not os.path.exists(arguments_path):
            return jsonify({"error": "No debate data available. Please start a debate first."}), 400

        if not os.path.exists("topic.txt"):
            return jsonify({"error": "No topic found please select the topic again."}), 400
        
        with open("topic.txt","r") as file:
            topic =  file.readline().strip()  # Read the first line and strip any whitespace or newline characters
            print("Extracted Line:", topic)
        
        
            
        with open(arguments_path, "r") as f:
            arguments = f.readlines()

        if not arguments:
            relevance_response =  ""
            return render_template('winner.html', topic=topic, winner=winner, evaluation=relevance_response)

   
        user_arguments = [arg for arg in arguments if arg.startswith("User:")]
        bot_arguments = [arg for arg in arguments if arg.startswith("Bot:")]
        print(topic)

        # Combine user arguments for a single AI relevance evaluation
#         relevance_prompt = (
#     f"Evaluate the relevance of the following user arguments to the debate topic:\n\n"
#     f"Debate topic: '{topic}'\n\n"
#     f"User arguments:\n" + "\n".join(user_arguments) + "\n\n"
#     f"Criteria:\n"
#     f"1. Ignore minor speech-to-text errors and evaluate intended meaning.\n"
#     f"2. Treat deliberate repetitions as **non-relevant** arguments.\n"
#     f"3. An argument is relevant if it contains 1+ sentence related to the debate topic.\n"
#     f"4. Calculate the total number of relevant arguments.\n\n"
#     f"Output:\n"
#     f"- 'Yes' if relevant percentage >= 60%, otherwise 'No'.\n"
#     f"- Total arguments.\n"
#     f"- Relevant arguments count.\n"
#     f"- Percentage of relevant arguments.\n"
#     f"- Then follow with an analysis explaining the results.\n"
# )
        relevance_prompt = (
    f"Evaluate the relevance of the following user arguments to the debate topic:\n\n"
    f"Debate topic: '{topic}'\n\n"
    f"User arguments:\n" + "\n".join(user_arguments) + "\n\n"
    f"Criteria:\n"
    f"1. Ignore minor speech-to-text errors and evaluate intended meaning.\n"
    f"2. Treat deliberate repetitions as **non-relevant** arguments.\n"
    f"3. An argument is relevant if it contains 1+ sentence related to the debate topic and supports the same stance the user initially took.\n"
    f"4. If the user changes sides (contradicting their own earlier arguments), treat such arguments as **non-relevant**.\n"
    f"5. Calculate the total number of relevant arguments.\n\n"
    f"Output:\n"
    f"- 'Yes' if relevant percentage >= 60%, otherwise 'No'.\n"
    f"- Total arguments.\n"
    f"- Relevant arguments count.\n"
    f"- Percentage of relevant arguments.\n"
    f"- Provide a one-paragraph summary analysis explaining the results in a concise manner, highlighting overall performance and areas of improvement, without detailing each argument individually."
)


        relevance_response = model.generate_content(relevance_prompt).text.strip()
        print(relevance_response)
        
        lines = relevance_response.splitlines()
        prompt = "based on this relevance response just answer in word who is the winner, user or bot or NoWinner. just answer in one word bot , user no winner"
# Check the first line for "Yes" or "No"
        relevance_response = model.generate_content(relevance_prompt).text.strip()
        print(relevance_response)
        for line in lines:
            print(line)
            if "user" in line:
                
                winner = "User"
                break
            elif "bot" in line:
                winner = "Bot"
                break
            else :
                winner = "No Winner"
        
        # Generate winner announcement audio
        print(winner)
        winner = f"The winner is: {winner}."
        return render_template('winner.html', topic=topic, winner=winner, evaluation=relevance_response)

    
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# @app.route('/quiz/<int:team_number>', methods=['GET', 'POST'])
# def quiz(team_number):
#     # Retrieve age group from query parameters
#     age_group = request.args.get('age_group')

#     # Ensure age group is provided
#     if not age_group:
#         return "Age group is required to proceed with the quiz.", 400

#     # Retrieve questions for the specified team and age group
#     age_group_questions = questions_db.get(age_group)

#     if not age_group_questions:
#         return f"No questions found for age group {age_group}", 404

#     questions = age_group_questions.get(team_number)

#     if not questions:
#         return f"No quiz found for team {team_number} in age group {age_group}", 404

#     correct_answers = [question["answer"] for question in questions]

#     return render_template(
#         "quiz.html",
#         team_number=team_number,
#         questions=questions,
#         age_group=age_group,
#         correct_answers=correct_answers
#     )


if __name__ == '__main__':
    app.run(debug=True)

