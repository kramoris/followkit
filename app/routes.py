from flask import Blueprint, redirect, render_template, url_for, flash
from flask_login import current_user, login_required

from app import db
from app.forms import QuoteForm
from app.models import Quote

main = Blueprint("main", __name__)


@main.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    return render_template("index.html")


@main.route("/dashboard")
@login_required
def dashboard():
    recent_quotes = (
        Quote.query
        .filter_by(user_id=current_user.id)
        .order_by(Quote.created_at.desc())
        .limit(5)
        .all()
    )
    return render_template("dashboard.html", recent_quotes=recent_quotes)


@main.route("/quotes")
@login_required
def quote_list():
    quotes = (
        Quote.query
        .filter_by(user_id=current_user.id)
        .order_by(Quote.created_at.desc())
        .all()
    )
    return render_template("quotes/list.html", quotes=quotes)


@main.route("/quotes/new", methods=["GET", "POST"])
@login_required
def quote_create():
    form = QuoteForm()

    if form.validate_on_submit():
        quote = Quote(
            user_id=current_user.id,
            customer_name=form.customer_name.data.strip(),
            job_description=form.job_description.data.strip(),
            quote_amount=form.quote_amount.data,
            date_sent=form.date_sent.data,
            status=form.status.data,
            next_follow_up_date=form.next_follow_up_date.data,
            notes=form.notes.data.strip() if form.notes.data else None,
            contact_method=form.contact_method.data,
            customer_email=form.customer_email.data.strip().lower() if form.customer_email.data else None,
            customer_phone=form.customer_phone.data.strip() if form.customer_phone.data else None,
        )

        db.session.add(quote)
        db.session.commit()

        flash("Quote created successfully.", "success")
        return redirect(url_for("main.quote_list"))

    return render_template("quotes/create.html", form=form)
