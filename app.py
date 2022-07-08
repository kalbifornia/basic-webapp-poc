#app.py
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://joe:password@localhost:3306/mywebappdb' #Replace the username and password with the actual username and password used for your workstation MySQL database
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False #Set = False to suppress a warning
db = SQLAlchemy(app)

from db_models import MiddlewareApp, MiddlewareServer, MiddlewareAppServer #Ordering is important here. Since db_models imports db from this module, this import of db_models must not occur until after db has been created. Otherwise we get a circular import error.

@app.route("/middlewareapp/<app_name>")
def middleware_app(app_name):
    app = MiddlewareApp.query.filter_by(name = app_name).first()

    if app == None:
        errorMessage="No Middleware App named {app_name} in the system.".format(app_name=app_name)
        return render_template("error.html",errorMessage=errorMessage)

    return render_template("middlewareapp.html",app=app)

@app.route("/middlewareserver/<server_name>")
def middleware_server(server_name):
    server = MiddlewareServer.query.filter_by(name = server_name).first()

    if server == None:
        errorMessage="No Middleware Server named {server_name} in the system.".format(server_name=server_name)
        return render_template("error.html",errorMessage=errorMessage)

    return render_template("middlewareserver.html",server=server)


@app.route("/load-the-database")
def load_the_database():
    app1 = MiddlewareApp(name="SomeApp1",description="This is an app that does A, B, and C")
    app2 = MiddlewareApp(name="SomeApp2",description="This app does D, E, and F")
    app3 = MiddlewareApp(name="SomeApp3",description="This app searches an internal database for the text of Chicka Chicka Boom Boom")

    server1 = MiddlewareServer(name="MyLinuxServerA",is_windows=False)
    server2 = MiddlewareServer(name="MyWindowsServerB",is_windows=True)
    server3 = MiddlewareServer(name="MyServerC")

    app1Server1 = MiddlewareAppServer(app=app1,server=server1)
    app1Server2 = MiddlewareAppServer(app=app1,server=server2)
    app2Server1 = MiddlewareAppServer(app=app2,server=server1)
    app3Server1 = MiddlewareAppServer(app=app3,server=server1)
    app3Server3 = MiddlewareAppServer(app=app3,server=server3)

    db.session.add_all([app1Server1,app1Server2,app2Server1,app3Server1,app3Server3])
    db.session.commit()
    return "Loaded the database."
