from os.path import realpath
from pathlib import Path
from flask import Flask, render_template, Response
from werkzeug.utils import secure_filename

SCRIPT_PATH = Path(realpath(__file__))
ROOT_DIRECTORY = SCRIPT_PATH.parent.parent
TEMPLATE_DIRECTORY = Path(f"{ROOT_DIRECTORY}/templates")
STATIC_DIRECTORY = Path(f"{ROOT_DIRECTORY}/static")

app = Flask(__name__, template_folder=TEMPLATE_DIRECTORY, static_folder=STATIC_DIRECTORY)


@app.route("/<string:page>")
def static_page(page: str):
    sanitized_page_path = secure_filename(page)

    if sanitized_page_path.strip() == "":
        return Response("Sanitized path is empty.", status=400)

    page_file = Path(f"{TEMPLATE_DIRECTORY}/{sanitized_page_path}.html")
    if not page_file.exists():
        return Response("Unknown path.", status=404)

    return render_template(f"{sanitized_page_path}.html")


@app.route("/")
def index():
    return static_page("index")


if __name__ == "__main__":
    app.run("0.0.0.0", 8080, debug=True)
