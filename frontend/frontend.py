from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

# ✅ Backend API URL - Replace with your actual backend DNS or IP
BACKEND_API = "http://<replace-with-private-instance-backend-ip>:5000"  # Update this with Load Balancer later

# ✅ Dummy data for fallback
tasks = [{"id": 1, "name": "Frontend Dummy Task 1"}, {"id": 2, "name": "Frontend Dummy Task 2"}]

# ✅ Function to Get EC2 Instance ID
def get_instance_id():
    try:
        # Get the IMDSv2 token
        token_url = "http://169.254.169.254/latest/api/token"
        headers = {"X-aws-ec2-metadata-token-ttl-seconds": "21600"}
        token_response = requests.put(token_url, headers=headers, timeout=1)
        token_response.raise_for_status()
        token = token_response.text

        # Use the token to fetch the instance ID
        metadata_url = "http://169.254.169.254/latest/meta-data/instance-id"
        headers = {"X-aws-ec2-metadata-token": token}
        response = requests.get(metadata_url, headers=headers, timeout=1)
        response.raise_for_status()

        return response.text
    except requests.exceptions.RequestException:
        return "Unknown-Instance"

# Example usage


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

    return render_template("index.html", tasks=tasks, instance_id=get_instance_id())

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
