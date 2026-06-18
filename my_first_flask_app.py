# IMPORTS SECTION

# IMPORT THE FLASK CLASS TO CREATE THE WEB APP FRAMEWORK, 
# AND RENDER_TEMPLATE TO RENDER EXTERNAL HTML FILES FROM THE /TEMPLATES/ FOLDER.
from flask import Flask, render_template, redirect, request

# IMPORT SQLALCHEMY TO CONNECT THE PYTHON APP TO A DATABASE LATER.
# THIS ALLOWS US TO STORE, READ, UPDATE, AND DELETE (CRUD) USER DATA.
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime


# INITIALIZATION SECTION

# CREATE AN INSTANCE OF THE FLASK APP ENGINE AND STORE IT IN A VARIABLE CALLED 'APP'.
# '__NAME__' IS A SPECIAL PYTHON VARIABLE THAT TELLS FLASK WHERE THE FILE IS LOCATED
# SO IT CAN FIND THE TEMPLATES, CSS, AND SCSS STATIC FILES CORRECTLY.
app = Flask(__name__)

#CONFIGURE SQLALCHEMY EXTENSION
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)

#DATA CLASS FOR ROW OF DATA
class MyTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    complete =db.Column(db.Integer)
    created = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return F'TASK{self.id}'


# ROUTING & CONTROLLER SECTION

# THIS IS A DECORATOR (@). IT ACTS AS A TRAFFIC COP FOR THE WEB APPLICATION.
# '@APP.ROUTE("/")' TELLS FLASK: "WHEN A USER VISITS THE ROOT URL (E.G., HTTP://127.0.0.1:5000/),
# AUTOMATICALLY TRIGGER AND RUN THE 'INDEX' FUNCTION RIGHT BELOW IT."
#ROUTES TO WEBPAGES
# HOME PAGE
@app.route("/", methods=["POST","GET"])
def index():
    # RENDER_TEMPLATE LOOKS INSIDE THE '/TEMPLATES/' DIRECTORY FOR 'INDEX.HTML',
    # INJECTS ANY PYTHON DATA INTO IT, AND SENDS THE FINAL HTML BACK TO THE BROWSER.

    #ADDING A NEW TASK (POST REQUEST)
    if request.method == "POST":
        current_task = request.form['content']
        new_task = MyTask(content = current_task)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"ERROR: {e}")
            return f"ERROR:{e}"
    
    else:
        tasks = MyTask.query.order_by(MyTask.created).all()
        return render_template("index.html",tasks=tasks)


# EXECUTION SECTION

# THIS CONDITIONAL STATEMENT CHECKS IF THIS PYTHON FILE IS RUNNING DIRECTLY.
# IF YOU TYPE 'PYTHON MY_FIRST_FLASK_APP.PY' IN THE TERMINAL, THIS EVALUATES TO TRUE.
# IF THIS SCRIPT IS IMPORTED INTO ANOTHER SCRIPT, IT WILL NOT RUN.
if __name__ in "__main__":
    # STARTS THE LOCAL WEB SERVER.
    # 'DEBUG=TRUE' IS A LIFESAVER FOR BEGINNERS: IT AUTOMATICALLY RELOADS THE SERVER 
    # ANY TIME YOU SAVE A CODE CHANGE AND PRINTS DETAILED ERRORS IN THE BROWSER IF SOMETHING BREAKS.
    with app.app_context():
        db.create_all()
    app.run(debug=True)

