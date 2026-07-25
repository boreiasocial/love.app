import os
from datetime import datetime

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    jsonify,
    send_from_directory,
)

from werkzeug.utils import secure_filename

from models import db, Profile, Image, Letter

app = Flask(__name__)

app.config["SECRET_KEY"] = "diario_casal_2026"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["UPLOAD_FOLDER"] = "uploads"

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

db.init_app(app)

with app.app_context():
    db.create_all()

    if Profile.query.first() is None:
        profile = Profile(
            slideshow_seconds=10
        )
        db.session.add(profile)
        db.session.commit()


LOGIN_1 = "14/11/12"
LOGIN_2 = "16/09/12"

DATA_NAMORO = datetime(2025, 6, 15)


@app.route("/")
def login():

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def do_login():

    data = request.form.get("data", "").strip()

    if data == LOGIN_1 or data == LOGIN_2:
        return redirect(url_for("home"))

    return redirect(url_for("login"))


@app.route("/home")
def home():

    dias = (datetime.now() - DATA_NAMORO).days

    return render_template(
        "home.html",
        dias=dias
    )
  # ==========================
# Upload de fotos
# ==========================

@app.route("/upload", methods=["POST"])
def upload():

    arquivos = request.files.getlist("images")

    if len(arquivos) == 0:
        return redirect(url_for("home"))

    for arquivo in arquivos:

        if arquivo.filename == "":
            continue

        nome = secure_filename(arquivo.filename)

        caminho = os.path.join(
            app.config["UPLOAD_FOLDER"],
            nome
        )

        arquivo.save(caminho)

        nova = Image(
            filename=nome
        )

        db.session.add(nova)

    db.session.commit()

    return redirect(url_for("home"))


# ==========================
# Lista de imagens
# ==========================

@app.route("/images")
def images():

    lista = []

    imagens = Image.query.order_by(
        Image.uploaded_at.desc()
    ).all()

    for img in imagens:

        lista.append({

            "id": img.id,

            "url": "/uploads/" + img.filename

        })

    return jsonify(lista)


# ==========================
# Mostrar uploads
# ==========================

@app.route("/uploads/<arquivo>")
def uploads(arquivo):

    return send_from_directory(

        app.config["UPLOAD_FOLDER"],

        arquivo

    )


# ==========================
# Tempo do slideshow
# ==========================

@app.route("/tempo", methods=["GET", "POST"])
def tempo():

    profile = Profile.query.first()

    if request.method == "POST":

        segundos = int(

            request.form["segundos"]

        )

        profile.slideshow_seconds = segundos

        db.session.commit()

        return redirect(url_for("home"))

    return jsonify({

        "segundos": profile.slideshow_seconds

    })
  # ==========================
# Criar carta
# ==========================

@app.route("/letter", methods=["POST"])
def create_letter():

    titulo = request.form.get("title", "").strip()
    conteudo = request.form.get("content", "").strip()
    autor = request.form.get("author", "").strip()

    if titulo == "" or conteudo == "":
        return redirect(url_for("home"))

    if autor == "":
        autor = "Anônimo"

    carta = Letter(
        title=titulo,
        content=conteudo,
        author=autor
    )

    db.session.add(carta)
    db.session.commit()

    return redirect(url_for("home"))


# ==========================
# Listar cartas
# ==========================

@app.route("/letters")
def letters():

    cartas = Letter.query.order_by(
        Letter.created_at.desc()
    ).all()

    lista = []

    for carta in cartas:

        lista.append({

            "id": carta.id,

            "title": carta.title,

            "author": carta.author,

            "date": carta.created_at.strftime("%d/%m/%Y")

        })

    return jsonify(lista)


# ==========================
# Abrir carta
# ==========================

@app.route("/letter/<int:id>")
def open_letter(id):

    carta = Letter.query.get_or_404(id)

    return jsonify({

        "id": carta.id,

        "title": carta.title,

        "author": carta.author,

        "date": carta.created_at.strftime("%d/%m/%Y"),

        "content": carta.content

    })


# ==========================
# Excluir carta
# ==========================

@app.route("/letter/delete/<int:id>", methods=["POST"])
def delete_letter(id):

    carta = Letter.query.get_or_404(id)

    db.session.delete(carta)
    db.session.commit()

    return redirect(url_for("home"))
