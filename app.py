import os
import mysql.connector
from flask import Flask, render_template, request, redirect
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()


def get_db_connection():
    return mysql.connector.connect(
        host=os.environ["DB_HOST"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.environ["DB_NAME"],
        port=3306
    )


@app.route("/", methods=["GET", "POST"])
def home():

    connection = get_db_connection()
    cursor = connection.cursor()

    if request.method == "POST":
        task = request.form["task"]

        cursor.execute(
            "INSERT INTO tasks (task) VALUES (%s)",
            (task,)
        )

        connection.commit()

    cursor.execute("SELECT id, task FROM tasks ORDER BY id")
    tasks = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template("index.html", tasks=tasks)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)