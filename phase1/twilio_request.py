from retrieve_movie import get_movie_metadata

from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app= Flask(__name__)

@app.route('/sms', methods=['GET', 'POST'])
def process_request():
    movie_title = request.values.get('Body', None)
    phone_number = request.values.get('From', None)
    
    # get the formatted movie metadata
    response_message = get_movie_metadata(movie_title)

    # give the requester an ack
    resp = MessagingResponse()
    resp.message(f"Getting the details about '{movie_title}' right now...")
    resp.message(response_message)

    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)