from retrieve_movie import get_movie_metadata

from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app= Flask(__name__)

@app.route('/sms', methods=['GET', 'POST'])
def process_request():
    movie_title = request.values.get('Body', None)
    phone_number = request.values.get('From', None)

    # give the requester an ack
    resp = MessagingResponse()
    resp.message(f"Getting the details about '{movie_title}' right now...")
    
    # get the formatted movie metadata
    response = get_movie_metadata(movie_title)
    
    # movie results part 1
    movie_information = resp.message(response['movie_information'])
    
    # return the review of the movie if it exists
    review = response['review_nyt']
    
    if review != 'None':
        msg = f"From the NYT: {review}"
        resp.message(msg)
    
    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)