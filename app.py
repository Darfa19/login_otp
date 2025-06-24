from flask import Flask, render_template, request, redirect, url_for, session
import smtplib, ssl, random, os

app = Flask(__name__)
app.secret_key = "secret-key-sangat-rahasia"

PASSWORD_DEFAULT = "12345"

# Konfigurasi email pengirim (isi dengan email kamu)
EMAIL_SENDER = "akuname00@gmail.com"
EMAIL_PASSWORD = "fjbf dvsc vwqw jfrh"  # pakai App Password jika Gmail

def send_otp(to_email, otp_code):
    subject = "Kode OTP Login Anda"
    message = f"Kode OTP kamu adalah: {otp_code}"
    email_text = f"Subject: {subject}\n\n{message}"

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, to_email, email_text)

@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        if password == PASSWORD_DEFAULT:
            otp_code = str(random.randint(100000, 999999))
            session["email"] = email
            session["otp"] = otp_code
            try:
                send_otp(email, otp_code)
            except Exception as e:
                error = "Gagal mengirim OTP. Pastikan email pengirim benar."
                return render_template("login.html", error=error)
            return redirect(url_for("otp"))
        else:
            error = "Password salah!"
    return render_template("login.html", error=error)

@app.route("/otp", methods=["GET", "POST"])
def otp():
    error = None
    if "otp" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        input_otp = request.form["otp"]
        if input_otp == session["otp"]:
            session.pop("otp", None)
            return redirect(url_for("success"))
        else:
            error = "Kode OTP salah!"
    return render_template("otp.html", error=error)

@app.route("/success")
def success():
    return render_template("success.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  # port dari environment Railway
    app.run(debug=False, host="0.0.0.0", port=port)
