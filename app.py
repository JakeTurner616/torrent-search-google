from flask import Flask, render_template, request
import requests
import os
import json

app = Flask(__name__)

# Replace with your Google Programmable Search API key and search engine ID
API_KEY=""
SEARCH_ENGINE_ID=""

@app.route("/", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        # Get user input from form and append ".torrent" to search for torrent files
        query = request.form["query"] + ' .torrent movie download site:archive.org OR site:yts.mx OR site:1337x.to OR site:nyaa.si OR site:rarbg.to OR site:thepiratebay.org OR site:torrentgalaxy.to OR site:eztv.re OR site:limetorrents.so OR site:torlock.live OR site:icefilms.tv OR site:torrentdownloads.pro OR site:yts.torrentbay.to OR site:yts.rs OR site:groups.google.com OR site:youtube.com OR site:reddit.com -"The Pirate Bay is the galaxy\'s most resilient BitTorrent site."'

        # Search in local index
        with open(os.path.join("static", "index.txt"), "r", encoding="utf8") as f:
            index = f.readlines()
        local_results = []

        for line in index:
            if query.lower() in line.lower():
                movie = json.loads(line)
                local_results.append({"title": movie["title_long"], "url": movie["url"]})

        # Send search request to Google Programmable Search API
        url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}"
        response = requests.get(url)
        try:
            # Parse JSON response and extract search results
            google_results = response.json()["items"]
        except KeyError:
            # Render no_results template if search returns no results
            return render_template("no_results.html")

        # Combine and render search results
        results = local_results + google_results
        return render_template("results.html", results=results)

    else:
        # Render search form template
        return render_template("search.html")

if __name__ == "__main__":
    app.run()
