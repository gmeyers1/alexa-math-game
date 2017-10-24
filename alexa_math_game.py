import logging
from random import randint
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session, audio

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)

@ask.launch
def new_game():
    welcome_msg = render_template('welcome') #render_template looks for the templates.yaml file
    return question(welcome_msg) #return is what gets returned to Alexa, in this case the welcome message as found in the yaml template above

@ask.intent("YesIntent")
def next_round():
    question_number = randint(1,9) # generates a random number between 1 and 9
    round_msg = render_template('round', question_number=question_number) # calls the render template passing the number above to the function 
    session.attributes['question_number'] = question_number  # session attribute is a flask-ask method that keeps a variable in memory throughout the session
    session.attributes['answer_number'] = 10-question_number  # assigns the correct anser to a session attribute
    print'finished ask.intent', question_number # prints to console for debugging
    return question(round_msg) \
        .reprompt("What's your answer") # tells Alexa to speak the question, and if there is no response after 6 seconds to reprompt for an answer

@ask.intent("NoIntent")
def no_intent():
    bye_text = "Ok, Thanks for playing."
    return statement(bye_text)
    session.attributes['answer_number'] = 10-question_number  # assigns the correct anser to a session attribute
    print'finished ask.intent', question_number # prints to console for debugging
    return question(round_msg) \
        .reprompt("What's your answer") # tells Alexa to speak the question, and if there is no response after 6 seconds to reprompt for an answer

@ask.intent("AnswerIntent", convert={'number': int}) #Alexa's Skillkit API always returns a string, so we have to conver it to an integer
def answer(number):
    print 'starting answer-intent', number # for debugging
    winning_number = session.attributes['answer_number'] # assign the correct answer to a new variable
    #uttered_number = session.attributes['number']
    if number == winning_number: # if the number the user uttered = to correct answer that read back the win message in the template
        msg = render_template('win')
    else:
        msg = render_template('lose') # else read the lose message
    return question(msg)

if __name__ == '__main__':
    app.run(debug=True) #standard flask method to begin listening on port 5000 (flask's default port)