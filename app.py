from flask import Flask, request, render_template, redirect
from engine.database import Database

app = Flask(__name__)
db = Database()

db.create_table("users", ["id", "name"], primary_key="id")
db.create_table("orders", ["id", "user_id", "product"], primary_key="id")

@app.route("/")
def index():
    users = db.get_table("users").select()
    orders = db.get_table("orders").select()
    return render_template("index.html", users=users, orders=orders)

@app.route("/users", methods=["POST"])
def add_user():
    db.get_table("users").insert([
        int(request.form["id"]),
        request.form["name"]
    ])
    return redirect("/")

@app.route("/orders", methods=["POST"])
def add_order():
    db.get_table("orders").insert([
        int(request.form["id"]),
        int(request.form["user_id"]),
        request.form["product"]
    ])
    return redirect("/")

@app.route("/join")
def join():
    users = db.get_table("users")
    orders = db.get_table("orders")

    results = []
    for o in orders.rows:
        for u in users.rows:
            if o["user_id"] == u["id"]:
                results.append({**o, **u})

    return {"results": results}

if __name__ == "__main__":
    app.run(debug=True)
