from flask import Flask, render_template, request, redirect, session
from auth.login import signup_user, verify_user
from auth.otp import send_otp, verify_otp

app = Flask(__name__)
app.secret_key = "supersecretkey"

@app.route("/", methods=["GET"])
def home():
    return redirect("/login")

# ----------------- SIGNUP -----------------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    error = ""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        confirm = request.form["confirm"]
        if password != confirm:
            error = "Passwords do not match"
        else:
            success, msg = signup_user(username, password)
            if success:
                session["username"] = username
                return redirect("/otp")
            else:
                error = msg
    return render_template("signup.html", error=error)

# ----------------- LOGIN -----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    error = ""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if verify_user(username, password):
            session["username"] = username
            return redirect("/otp")
        else:
            error = "Invalid username or password"
    return render_template("login.html", error=error)

# ----------------- OTP -----------------
@app.route("/otp", methods=["GET", "POST"])
def otp_page():
    error = ""
    if request.method == "POST":
        mobile = request.form["mobile"]
        entered_otp = request.form.get("otp")
        # send OTP if first submission
        if "send" in request.form:
            if send_otp(mobile):
                session["mobile"] = mobile
                error = "OTP sent! Enter it below."
            else:
                error = "Failed to send OTP."
        # verify OTP
        elif "verify" in request.form:
            mobile = session.get("mobile")
            if verify_otp(mobile, entered_otp):
                return render_template("success.html", username=session.get("username"))
            else:
                error = "Wrong OTP!"
    return render_template("otp.html", error=error)

if __name__ == "__main__":
    print("Starting Secure Authentication Module Flask App...")
    app.run(debug=True)
