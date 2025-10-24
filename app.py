from flask import Flask, request, render_template, send_from_directory,redirect,url_for,after_this_request
import yt_dlp
import os
import threading
import time
import uuid
app = Flask(__name__)
DOWNLOAD_FOLDER = "downloads"

def delayed_delete(file_path, delay=0.4):
    def delete():
        time.sleep(delay)
        
        os.remove(file_path)
        print(f"Deleted: {file_path}")
    threading.Thread(target=delete).start()



filename = f"{uuid.uuid4()}.mp3"



@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        video_url = request.form["url"]
        unique_id = str(uuid.uuid4())
        filename = f"{unique_id}.mp3"

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'{DOWNLOAD_FOLDER}/{unique_id}.%(ext)s',
            'cookiefile': 'cookies.txt',



            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(video_url, download=True)
            except:  
                print("Erro")
            #filename = f"{info['title']}.mp3"  
            #filename = f"{uuid.uuid4()}.mp3"

      #  return redirect(url_for("download_file", filename=filename))
        return redirect(url_for("thank_you", filename=filename))


    return render_template("index.html")

@app.route("/thank-you/<filename>")
def thank_you(filename):
    return render_template("thanks.html", filename=filename)


@app.route("/download/<filename>")
def download_file(filename):

    delayed_delete(f"downloads/{filename}")
    return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True) 

port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)






#it will download file and return to the server


