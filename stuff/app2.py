from flask import Flask, render_template, request, redirect, url_for
import psycopg2
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
import requests
import os
import json


url = "http://localhost:5001/model/predict"

# message = {
#     "text": [
#         "The Korean Air executive who kicked up a fuss over a bag of nuts will resign from her remaining posts with the airline , the company chairman -- who is also her father -- said Friday . The executive , Heather Cho , found herself at the center of a media storm after she ordered that a plane turn back to the gate and that a flight attendant be removed -- all because she was served nuts in a bag instead of on a plate in first class . Although her role put her in charge of in-flight service , she was only a passenger on the flight and was not flying in an official capacity . The incident , which took place last week at New York 's JFK airport , stirred anger among the South Korean public over Cho 's behavior . Cho , whose Korean name is Cho Hyun-ah , resigned Tuesday from the airline 's catering and in-flight sales business , and from its cabin service and hotel business divisions , the company said . But the 40-year-old kept her title as a vice president of the national carrier , according to company spokesman . That 's going to change , her father , Cho Yang-ho , said Friday as he made a public apology for what happened . She will be resigning from the vice president job and positions held in affiliate companies , he said . Asked by reporters how the incident could have happened , the company chairman blamed himself , saying he 'd raised her badly . ` Outburst of anger ' A local English-language newspaper , The Korea Times , said her behavior has deepened public resentment of South Korea 's large family-owned corporations , known as chaebol . `` Through her outburst of anger , she not only caused inconvenience to KAL passengers , but also to those on other flights , '' the newspaper said in an editorial Tuesday . The most annoying type of airline passenger is ... South Korean authorities are now investigating the incident , which occurred on a flight due to take off for Incheon International Airport near Seoul . Cho arrived at the Ministry of Land , Infrastructure and Transport on Friday as part of the investigation , according to local TV coverage . She spoke in such a low voice that it was inaudible from the TV footage . ` An excessive act ' Korean Air apologized for any inconvenience to those on the flight and said there had been no safety issues involved . The plane arrived at its destination 11 minutes behind schedule , according to the South Korean news agency Yonhap . `` Even though it was not an emergency situation , backing up the plane to order an employee to deplane was an excessive act , '' the airline said earlier this week . `` We will re-educate all our employees to make sure service within the plane meets high standards . '' The airline also issued an apology on Heather Cho 's behalf , Yonhap reported , in which she asked for forgiveness and said she would take `` full responsibility '' for the incident . According to her biography on the website of Nanyang Technological University , Heather Cho joined the airline in 1999 and has since been `` actively involved in establishing a new corporate identity for Korean Air . '' She studied at Cornell University and the University of Southern California . @highlight Airline chairman : Heather Cho will be resigning from all posts with the company @highlight Korean Air said previously she had resigned from some roles but was keeping her VP title @highlight The chairman , who is also her father , blames himself , saying he raised her badly  Cho ordered a plane back to the gate after a flight attendant served nuts in a bag"
#     ]
# }
app = Flask(__name__)


app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://wym_admin:admin@5432:5432/postgres"

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "contact"
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(40))
    lname = db.Column(db.String(40))
    email = db.Column(db.String(40))
    object = db.Column(db.String(40))
    message = db.Column(db.String(5000))

    def __init__(self, fname, lname, object="", email="", message=""):
        self.fname = fname
        self.lname = lname
        self.email = email
        self.object = object
        self.message = message


@app.route("/")
def home_page():
    return render_template("home.html")


@app.route("/about")
def about_page():
    return render_template("about.html")


def user(name):
    return "<p>welcome %s</p>" % name


@app.route("/contact")
def contact_page():
    return render_template("contact.html")


@app.route("/contactme", methods=["POST"])
def contactme():

    user = User(
        request.form["fname"],
        lname=request.form["lname"],
        message=request.form["lname"],
    )
    db.session.add(user)
    to_summarize = request.form["message"]
    messagedict = {"text": [f"{to_summarize}"]}
    response = requests.post(url, json=messagedict)
    print(response.content)
    db.session.commit()

    json1_str = json.loads(response.content["summary_text"])[0]
    return render_template("success.html", data=f"{json1_str}")


try:
    db.create_all()
except:
    pass
app.run(debug=True, port=5002, threaded=True, host=("0.0.0.0"))
# app.run(debug=True, host="0.0.0.0", port=5000)
