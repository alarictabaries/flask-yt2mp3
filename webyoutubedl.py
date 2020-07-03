from flask import Flask, render_template, request, send_file, redirect
import subprocess
from os import chdir as cd
from re import match
import youtube_dl

app = Flask(__name__)

@app.route("/")
def root():
    return render_template("index.html")

@app.route("/download", methods=['POST'])
def download():
    url = request.form.get('yt-link', type=str)
    if url == "":
        return redirect("/")

    ydl_opts = {
        'outtmpl': 'C:/Users/altab/WebstormProjects/flask-yt2mp3/mp3/%(title)s-%(id)s.%(ext)s',
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        title = info.get("title")
        filename = ydl.prepare_filename(info)


    print(filename)

    return send_file(filename.replace(".m4a", ".mp3"),
                     attachment_filename=title,
                     as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True, host="localhost")

