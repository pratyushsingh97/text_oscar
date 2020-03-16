![Bong Joon](/imgs/Bong-Joon-Ho-Oscars-GQ-2020-021020.jpg)
# Text Oscar 

## Background
This project is the first of a personal challenge of mine in 2020 -- build a proof-of-concept in a weekend. Text Oscar was all built in one weekend a couple weeks ago, and I liked this project enough that I am slowly fleshing out the code to make it a legitimate product. Obviously, if you see some ideas that you would like to add, simply open a pull-request or contribute to the project directly :). 

## What is Text Oscar?
Ever run into a situation where you don't know what a movie is about? You would like to know who that movie casts, the director, the rating, along with what the critics are saying? Fear not, TextOscar is here to help. You simply text Oscar the movie name and it returns all of that information. 

## How does it work?
![Text Oscar](/imgs/text_oscar.gif)

### Movie Metadata
TextOscar utilizes Twilio as the front-end and a python backend to process the movie and retrieve the metadata. The data for the movie is retrieved from the OMDB (Open Movie Database) API. 

### Text Summarization
TextOscar also returns a summary of the NYT review of the movie (if it exists). The text summarization is an extractive-text summarization model that uses TF-IDF to calculate word weights, and consequently the sentence weights. The top two highest weighted sentences are returned to the user. In the future, I would like to expand this to use abstractive summarization techniques. Other limitations include that the summarization is only available for movies released in 2019. 

### Other Cool Features
1. [Fuzzy Matching](https://github.com/seatgeek/fuzzywuzzy) - Text Oscar will try to understand your typos and do its best to return the best possible match. 

## Great, How Do I Run This?
Unfortunately, TextOscar only runs on my account for now! However feel free to clone this project and run it off of your own server. 
### What Do You Need?
1. [A Twilio Account and phone number (along with some credits)](https://www.twilio.com)
2. [A Open Movie Database API Key](http://www.omdbapi.com)
4. python 3.*
