from flask import Flask, render_template, request, redirect, url_for
import speech_recognition as sr
import yagmail

app = Flask(__name__)

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print('Clearing background noise..')
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Waiting for your message...")
        recorded_audio = recognizer.listen(source)
        print('Done recording..!')

    try:
        print('Printing the message..')
        text = recognizer.recognize_google(recorded_audio, language='en-US')
        print('Your message: {}'.format(text))
        return text
    except Exception as ex:
        print(ex)
        return None
    
@app.route('/', methods=['GET', 'POST'])
def login():
    global SENDER_EMAIL
    global SENDER_PASSWORD

    if request.method == 'POST':
        # Assuming you have a form with input fields 'email' and 'password'
        email = request.form['email']
        password = request.form['password']
        
        # Perform your login authentication here
        # For demonstration purposes, let's assume authentication is successful
        authenticated = True
        
        if authenticated:
            SENDER_EMAIL = email
            SENDER_PASSWORD = password
            return redirect(url_for('record_message'))
    
    return render_template('login.html')

def send_email(receiver, message):
    try:
        yag = yagmail.SMTP(SENDER_EMAIL, SENDER_PASSWORD)
        yag.send(to=receiver, subject='This is an automated mail', contents=message)
        yag.close()
        print('Email sent successfully!')
    except Exception as ex:
        print('Email sending failed:', ex)

@app.route('/record', methods=['GET', 'POST'])
def record_message():
    if request.method == 'POST':
        receiver = request.form['receiver_email']
        recorded_message = recognize_speech()

        if recorded_message:
            send_email(receiver, recorded_message)
            result = 'Email sent successfully'
            return result
        else:
            return "Email not sent!"
    
    return render_template('record.html')

if __name__ == '__main__':
     app.run(host='0.0.0.0', port=5000, debug=False)
