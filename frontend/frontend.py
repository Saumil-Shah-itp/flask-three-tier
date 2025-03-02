from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

# ✅ Backend API URL - Replace with your actual backend DNS or IP
BACKEND_API = "http://<replace-with-private-instance-backend-ip>:5000"  # Update this with Load Balancer later

# ✅ Dummy data for fallback
tasks = [{"id": 1, "name": "Frontend Dummy Task 1"}, {"id": 2, "name": "Frontend Dummy Task 2"}]


@app.route("/", methods=["GET", "POST"])
def index():
    global tasks

    if request.method == "POST":
        task_name = request.form.get("task_name")
        try:
            requests.post(f"{BACKEND_API}/add", json={"name": task_name})
        except requests.exceptions.RequestException:
            new_id = max([task["id"] for task in tasks]) + 1 if tasks else 1
            tasks.append({"id": new_id, "name": task_name})

        return redirect(url_for("index"))

    try:
        response = requests.get(f"{BACKEND_API}/tasks")
        response.raise_for_status()
        tasks = response.json()
    except requests.exceptions.RequestException as e:
        print(f"⚠ Backend API failed: {e}")

    return render_template("index.html", tasks=tasks)


@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    global tasks
    try:
        requests.delete(f"{BACKEND_API}/delete/{task_id}")
    except requests.exceptions.RequestException:
        tasks = [task for task in tasks if task["id"] != task_id]

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
