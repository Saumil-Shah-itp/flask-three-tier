from flask import Flask, jsonify, request
import pymysql

app = Flask(__name__)

# ✅ Replace with your RDS MySQL details
DB_CONFIG = {
    "host": "<replace-with-rds-host-dns>",
    "user": "DB_user",
    "password": "DB_passwd",
    "database": "DB name"
}

# ✅ Try to connect to DB
try:
    conn = pymysql.connect(**DB_CONFIG, cursorclass=pymysql.cursors.DictCursor)
    use_db = True
except Exception as e:
    print(f"⚠ Database connection failed, using dummy data. Error: {e}")
    use_db = False

# ✅ Dummy tasks for fallback
tasks = [{"id": 1, "name": "Dummy Task 1"}, {"id": 2, "name": "Dummy Task 2"}]


@app.route("/tasks", methods=["GET"])
def get_tasks():
    if use_db:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM tasks")
            db_tasks = cursor.fetchall()
        return jsonify(db_tasks)
    
    return jsonify(tasks)  # Return dummy data if no DB


@app.route("/add", methods=["POST"])
def add_task():
    data = request.json
    task_name = data.get("name")

    if use_db:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO tasks (name) VALUES (%s)", (task_name,))
            conn.commit()
    else:
        new_id = max([task["id"] for task in tasks]) + 1 if tasks else 1
        tasks.append({"id": new_id, "name": task_name})

    return jsonify({"message": "Task added successfully"})


@app.route("/delete/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    if use_db:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
            conn.commit()
    else:
        global tasks
        tasks = [task for task in tasks if task["id"] != task_id]

    return jsonify({"message": "Task deleted successfully"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
