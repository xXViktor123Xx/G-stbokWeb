import json
from datetime import datetime
from html import escape
from flask import Flask, redirect, request, send_from_directory

app = Flask(__name__)


def read_entries():
    try:
        with open("guestbook.json", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


@app.route("/", methods=["GET", "POST"])
def index():
    entries = read_entries()

    if request.method == "POST":
        name = request.form["name"].strip()
        comment = request.form["comment"].strip()

        if name and comment:
            entries.append({
                "name": name,
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "comment": comment,
            })
            with open("guestbook.json", "w", encoding="utf-8") as f:
                json.dump(entries, f, ensure_ascii=False, indent=4)

        return redirect("/")

    html = ""
    for e in reversed(entries):
        html += "<hr>"
        html += "<p><b>" + escape(e["name"]) + "</b> (" + e["time"] + ")</p>"
        html += '<p style="white-space: pre-wrap;">' + escape(e["comment"]) + "</p>"

    page = open("index.html", encoding="utf-8").read()
    page = page.replace("[[ANTAL]]", str(len(entries)))
    page = page.replace("[[INLAGG]]", html)
    page = page.replace("[[FEL]]", "")
    return page


@app.route("/style.css")
def style():
    return send_from_directory(".", "style.css")


app.run(debug=True)