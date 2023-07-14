import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/home')
def home():
    return render_template('home.html')

@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        card = request.form["card"]
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_card_description(card),
            temperature=0.6,
            max_tokens=500,
        )
        return redirect(url_for("index", result=response.choices[0].text))
    result = request.args.get("result")
    return render_template("index.html", result=result, image_description=parse_card_description(result), inside_message=extract_inside_message(result))


@app.route('/frontCover', methods=("GET", "POST"))
def coverImage():
    if request.method == "POST":
        frontCover = request.form["frontCover"]
        response = openai.Image.create(
            prompt=frontCover,
            n=1,
            size="1024x1024"
        )
        return redirect(url_for("coverImage", result=response["data"][0]["url"]))

    result = request.args.get("result")
    return render_template("image.html", result=result)

@app.route("/reserveBar", methods=("GET", "POST"))
def reserveBar():
    if request.method == "POST":
        shoppingList = request.form["shoppingList"]
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_cocktail_list(shoppingList),
            temperature=0.6,
            max_tokens=500,
        )
        return redirect(url_for("reserveBar", result=response.choices[0].text))
    result = request.args.get("result")
    return render_template("reserveBar.html", result=result)

@app.route("/reserveBarDinnerPairing", methods=("GET", "POST"))
def reserveBarDinnerPairing():
    if request.method == "POST":
        dinner = request.form["dinner"]
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_cocktail_pairing_list(dinner),
            temperature=0.6,
            max_tokens=500,
        )
        return redirect(url_for("reserveBarDinnerPairing", result=response.choices[0].text))
    result = request.args.get("result")
    return render_template("reserveBarDinnerPairing.html", result=result)

@app.route("/aiMusings", methods=("GET", "POST"))
def aiMusings():
    return render_template("aiMusings.html")

@app.route("/reserveBarRecipieGenerator", methods=("GET", "POST"))
def reserveBarRecipieGenerator():
    if request.method == "POST":
        drink = request.form["drink"]
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_cocktail_recipie(drink),
            temperature=0.6,
            max_tokens=500,
        )
        return redirect(url_for("reserveBarRecipieGenerator", result=response.choices[0].text))
    result = request.args.get("result")
    return render_template("reserveBarRecipieGenerator.html", result=result)




def generate_card_description(card):
    return """Convert this description into a detailed description of a greeting cardto a programmatic command:

Example: My brother is graduating  college in two weeks.  He can play the guitar really well, is super smart, and loves working out.  Can you describe a greeting card that I could send him
Output: 
Image: A cartoon illustration of a young man wearing a graduation cap and gown, holding an electric guitar in one hand and a diploma in the other. Surrounding him are books and workout equipment like dumbbells and a jump rope
Text: Congratulations on your graduation, (brother's name)! Your incredible journey through college has shown us just how talented, dedicated, and awesome you truly are. Your passion for music, your brilliant mind, and your commitment to staying fit are all a testament to the amazing person you've become. As you embark on this next chapter of your life, always remember to keep rocking, stay curious, and never give up on your dreams. We're incredibly proud of you and can't wait to see what amazing things you'll accomplish next! With all our love and support, [Your name]

Example: My mother loves gardening, canning, and quality time with family.  Can you describe a greeting card I might send her for Mother's Day?
Output:
Image: A watercolor of a woman in a garden, surrounded by colorful flowers and vegetables. She is wearing a sun hat and has a basket of freshly picked produce in one hand and a canning jar in the other.
Text: Happy Mother's Day to the most amazing gardener, canner, and memory-maker! Thank you for the countless hours you spend making our lives and the world around us more beautiful. Today, we celebrate you and the incredible love you've planted in our hearts. Wishing you a day filled with love, laughter, and cherished moments with your favorite people. Love always, [Your Name]

Example: A sympathy card for a close male friend who just lost his dog
Output:
Image: A rendering of a man sitting on a bench in a park, looking sadly at a paw print in the ground. He is surrounded by trees and flowers, and the sky is filled with stars.
Text: We are so sorry for your loss. Our hearts go out to you during this difficult time. We know how much your beloved pup meant to you and how much you will miss them. May the memories of all the happy times you shared together bring you comfort and peace. With love and support, [Your Name]

Example: A congradulations card for a female coworker who just landed a big promotion in software sales
Output:
Image: A cartoon of a woman standing in front of a computer screen, with a big smile on her face and her arms raised in celebration. She is surrounded by software boxes and a stack of paperwork.
Text: Congratulations on your big promotion! You have worked so hard and it's wonderful to see your hard work pay off. Your dedication to software sales and your commitment to excellence have been an inspiration to us all. We are so proud of you and can't wait to see what amazing things you'll accomplish next! Wishing you continued success in all your future endeavors. With love and admiration, [Your Name]

{}
Output:""".format(
        card.capitalize()
    )

def generate_cocktail_list(cocktail):
    return """I have
{}
list the names of five cocktails I can make with only these ingredients""".format(
        cocktail.capitalize()
    )

def generate_cocktail_pairing_list(cocktail):
    return """I am having miso soup and sushi for dinner.  Can you compile a panel of 3 mixologists and facilitate a discussion on what drink I should pair with my meal?  At the end of their discussion compile a list of only the drink names.

Suggested Drinks:
- Sparkling Blueberry Mint Fizz
- Spicy Ginger Punch
- Rob Roy (Scotch-based cocktail)
- Wasabi Tini
- Melon Flip 
- Japanese Blonde (rum-based cocktail)
- Plum Sake Margarita
- Bamboo Cocktail (vodka-based)

I am having {} for dinner.  Can you compile a panel of 3 mixologists and facilitate a discussion on what drink I should pair with my meal?  At the end of their discussion compile a list of only the drink names.

Suggested Drinks:
""".format(
        cocktail.capitalize()
    )

def generate_cocktail_recipie(cocktail):
    return """What is the recipie for {} 
""".format(
        cocktail.capitalize()
    )

def parse_card_description(prompt):
    try:
        image_description_start = int(7)
        image_description_end = int(prompt.rfind("Text: "))
        image_description = prompt[image_description_start:image_description_end]
    except:
        image_description = "not generated yet"
    return image_description

def extract_inside_message(prompt):
    try:
        inside_message_start = int(prompt.rfind("Text: "))+6
        inside_message_end = int(len(prompt))
        inside_message = prompt[inside_message_start:inside_message_end]
    except:
        inside_message = "not generated yet"
    return inside_message