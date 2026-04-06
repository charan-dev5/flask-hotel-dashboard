from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("hotel.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            guest_name TEXT,
            room_number INTEGER,
            check_in TEXT,
            check_out TEXT
        )
    """)
    conn.commit()
    return conn

@app.route("/")
def index():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bookings")
    bookings = cursor.fetchall()
    conn.close()
    return render_template("index.html", bookings=bookings)

@app.route("/add", methods=["POST"])
def add():
    guest_name = request.form["guest_name"]
    room_number = request.form["room_number"]
    check_in = request.form["check_in"]
    check_out = request.form["check_out"]
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO bookings(guest_name, room_number, check_in, check_out) VALUES (?, ?, ?, ?)", (guest_name, room_number, check_in, check_out))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

@app.route("/delete/<int:id>")
def delete(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM bookings WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)