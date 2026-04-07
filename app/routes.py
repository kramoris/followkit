from datetime import UTC, date, datetime

from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from app import db
from app.forms import QuoteForm, QuoteFollowUpForm
from app.models import Quote

main = Blueprint("main", __name__)


def utc_now():
    return datetime.now(UTC)


@main.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    return render_template("index.html")


@main.route("/dashboard")
@login_required
def dashboard():
    quotes = (
        Quote.query
        .filter_by(user_id=current_user.id)
        .order_by(Quote.created_at.desc())
        .all()
    )

    today = date.today()

    active_follow_up_statuses = {
        Quote.STATUS_SENT,
        Quote.STATUS_FOLLOW_UP_DUE,
        Quote.STATUS_NO_RESPONSE,
    }

    open_quote_statuses = {
        Quote.STATUS_SENT,
        Quote.STATUS_FOLLOW_UP_DUE,
        Quote.STATUS_NO_RESPONSE,
    }

    recent_quotes = quotes[:5]

    due_today_quotes = [
        quote for quote in quotes
        if quote.next_follow_up_date == today and quote.status in active_follow_up_statuses
    ]

    overdue_quotes = [
        quote for quote in quotes
        if quote.next_follow_up_date
        and quote.next_follow_up_date < today
        and quote.status in active_follow_up_statuses
    ]

    status_counts = {
        "draft": sum(1 for quote in quotes if quote.status == Quote.STATUS_DRAFT),
        "sent": sum(1 for quote in quotes if quote.status == Quote.STATUS_SENT),
        "follow_up_due": sum(1 for quote in quotes if quote.status == Quote.STATUS_FOLLOW_UP_DUE),
        "won": sum(1 for quote in quotes if quote.status == Quote.STATUS_WON),
        "lost": sum(1 for quote in quotes if quote.status == Quote.STATUS_LOST),
        "no_response": sum(1 for quote in quotes if quote.status == Quote.STATUS_NO_RESPONSE),
    }

    total_quotes = len(quotes)

    open_quote_value = sum(
        quote.quote_amount for quote in quotes if quote.status in open_quote_statuses
    )

    return render_template(
        "dashboard.html",
        recent_quotes=recent_quotes,
        due_today_quotes=due_today_quotes,
        overdue_quotes=overdue_quotes,
        status_counts=status_counts,
        total_quotes=total_quotes,
        open_quote_value=open_quote_value,
    )


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


@main.route("/quotes/<int:quote_id>")
@login_required
def quote_detail(quote_id):
    quote = (
        Quote.query
        .filter_by(id=quote_id, user_id=current_user.id)
        .first_or_404()
    )

    follow_up_form = QuoteFollowUpForm()
    follow_up_form.status.data = quote.status
    follow_up_form.next_follow_up_date.data = quote.next_follow_up_date

    return render_template(
        "quotes/detail.html",
        quote=quote,
        follow_up_form=follow_up_form,
    )


@main.route("/quotes/<int:quote_id>/edit", methods=["GET", "POST"])
@login_required
def quote_edit(quote_id):
    quote = (
        Quote.query
        .filter_by(id=quote_id, user_id=current_user.id)
        .first_or_404()
    )

    form = QuoteForm(obj=quote)

    if form.validate_on_submit():
        quote.customer_name = form.customer_name.data.strip()
        quote.job_description = form.job_description.data.strip()
        quote.quote_amount = form.quote_amount.data
        quote.date_sent = form.date_sent.data
        quote.status = form.status.data
        quote.next_follow_up_date = form.next_follow_up_date.data
        quote.notes = form.notes.data.strip() if form.notes.data else None
        quote.contact_method = form.contact_method.data
        quote.customer_email = form.customer_email.data.strip().lower() if form.customer_email.data else None
        quote.customer_phone = form.customer_phone.data.strip() if form.customer_phone.data else None

        db.session.commit()
        flash("Quote updated successfully.", "success")
        return redirect(url_for("main.quote_detail", quote_id=quote.id))

    return render_template("quotes/edit.html", form=form, quote=quote)


@main.route("/quotes/<int:quote_id>/follow-up", methods=["POST"])
@login_required
def quote_follow_up(quote_id):
    quote = (
        Quote.query
        .filter_by(id=quote_id, user_id=current_user.id)
        .first_or_404()
    )

    follow_up_form = QuoteFollowUpForm()

    if follow_up_form.validate_on_submit():
        quote.status = follow_up_form.status.data
        quote.next_follow_up_date = follow_up_form.next_follow_up_date.data
        quote.last_followed_up_at = utc_now()

        note_text = follow_up_form.follow_up_note.data.strip() if follow_up_form.follow_up_note.data else ""
        if note_text:
            timestamp = utc_now().strftime("%Y-%m-%d %H:%M UTC")
            new_note_entry = f"[{timestamp}] Follow-up: {note_text}"

            if quote.notes:
                quote.notes = f"{quote.notes}\n\n{new_note_entry}"
            else:
                quote.notes = new_note_entry

        db.session.commit()
        flash("Follow-up saved.", "success")
    else:
        flash("Please correct the errors in the follow-up form.", "danger")

    return redirect(url_for("main.quote_detail", quote_id=quote.id))
