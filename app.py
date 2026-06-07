from flask import Flask, render_template, request

app = Flask(__name__)

common_passwords = [
    "password",
    "123456",
    "12345678",
    "admin",
    "welcome",
    "qwerty"
]

def analyze_password(password):
    score = 0
    suggestions = []

    has_upper = False
    has_lower = False
    has_digit = False
    has_special = False

    special_chars = "@#$%^&*()_+-=[]{}|;:,.<>?/!"

    # Length Check
    if len(password) >= 8:
        score += 1
    else:
        suggestions.append("Increase password length (minimum 8 characters)")

    # Character Checks
    for ch in password:
        if ch.isupper():
            has_upper = True
        elif ch.islower():
            has_lower = True
        elif ch.isdigit():
            has_digit = True
        elif ch in special_chars:
            has_special = True

    if has_upper:
        score += 1
    else:
        suggestions.append("Add at least one uppercase letter")

    if has_lower:
        score += 1
    else:
        suggestions.append("Add at least one lowercase letter")

    if has_digit:
        score += 1
    else:
        suggestions.append("Add at least one number")

    if has_special:
        score += 1
    else:
        suggestions.append("Add at least one special character")

    if password.lower() not in common_passwords:
        score += 1
    else:
        suggestions.append("Avoid common passwords")

    # Strength Classification
    if score <= 2:
        strength = "Weak"
        color = "red"
    elif score <= 4:
        strength = "Medium"
        color = "orange"
    else:
        strength = "Strong"
        color = "green"

    return strength, color, score, suggestions


@app.route("/", methods=["GET", "POST"])
def home():
    strength = None
    color = None
    score = None
    suggestions = []

    if request.method == "POST":
        password = request.form["password"]

        strength, color, score, suggestions = analyze_password(password)

    return render_template(
        "index.html",
        strength=strength,
        color=color,
        score=score,
        suggestions=suggestions
    )


if __name__ == "__main__":
    app.run(debug=True)