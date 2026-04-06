from flask import Blueprint, redirect, render_template, url_for
from flask_login import current_user, login_required

main = Blueprint("main", __name__)


@main.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    return render_template("index.html")


@main.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")
