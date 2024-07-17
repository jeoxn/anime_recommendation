from flask import Blueprint, render_template, request, redirect, flash, url_for
from .models import recommend

views = Blueprint('views', __name__)

@views.route("/", methods=['GET', 'POST'])
def home():
    reccomendations = []
    anime_name = ''
    start = 0
    # get the anime name and start from the url
    if request.method == 'GET':
        anime_name = request.args.get('title', '')
        start = int(request.args.get('start', 0))
    
    reccomendations = recommend(anime_name, start=start, end=start+20)

    return render_template("index.html", reccomendations=reccomendations, start=str(start), anime_name=anime_name, next=str(start+20), prev=str(start-20))