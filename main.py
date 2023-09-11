from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy

# create the extension
db = SQLAlchemy()
# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
# initialize the app with the extension
db.init_app(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)

with app.app_context():
    db.create_all()

@app.route("/")
def user_list():
    users = db.session.execute(db.select(User).order_by(User.username)).scalars()
    return render_template("list.html", users=users)

@app.route("/input", methods=["GET", "POST"])
def user_create():
    if request.method == "POST":
        user = User(
            username=request.form["username"],
            email=request.form["email"],
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("user_detail", id=user.id))

    return render_template("input.html")

@app.route("/user/<int:id>")
def user_detail(id):
    user = db.get_or_404(User, id)
    return render_template("detail.html", user=user)

@app.route("/user/<int:id>/delete", methods=["GET", "POST"])
def user_delete(id):
    user = db.get_or_404(User, id)

    if request.method == "POST":
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for("user_list"))

    return render_template("delete.html", user=user)

app.run(host='localhost', port=5000)