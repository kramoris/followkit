from datetime import UTC, datetime

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app import db


def utc_now():
    return datetime.now(UTC)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=utc_now, nullable=False)

    quotes = db.relationship(
        "Quote", backref="user", lazy=True, cascade="all, delete-orphan"
    )
    templates = db.relationship(
        "FollowUpTemplate", backref="user", lazy=True, cascade="all, delete-orphan"
    )

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        return f"<User {self.email}>"


class Quote(db.Model):
    STATUS_DRAFT = "draft"
    STATUS_SENT = "sent"
    STATUS_FOLLOW_UP_DUE = "follow_up_due"
    STATUS_WON = "won"
    STATUS_LOST = "lost"
    STATUS_NO_RESPONSE = "no_response"

    STATUS_CHOICES = [
        STATUS_DRAFT,
        STATUS_SENT,
        STATUS_FOLLOW_UP_DUE,
        STATUS_WON,
        STATUS_LOST,
        STATUS_NO_RESPONSE,
    ]

    CONTACT_EMAIL = "email"
    CONTACT_PHONE = "phone"
    CONTACT_SMS = "sms"
    CONTACT_WHATSAPP = "whatsapp"
    CONTACT_OTHER = "other"

    CONTACT_METHOD_CHOICES = [
        CONTACT_EMAIL,
        CONTACT_PHONE,
        CONTACT_SMS,
        CONTACT_WHATSAPP,
        CONTACT_OTHER,
    ]

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id"), nullable=False, index=True
    )

    customer_name = db.Column(db.String(120), nullable=False)
    job_description = db.Column(db.Text, nullable=False)
    quote_amount = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    date_sent = db.Column(db.Date, nullable=True)

    status = db.Column(db.String(30), nullable=False, default=STATUS_DRAFT, index=True)
    next_follow_up_date = db.Column(db.Date, nullable=True, index=True)
    notes = db.Column(db.Text, nullable=True)

    contact_method = db.Column(db.String(20), nullable=False, default=CONTACT_EMAIL)
    customer_email = db.Column(db.String(255), nullable=True)
    customer_phone = db.Column(db.String(50), nullable=True)

    last_followed_up_at = db.Column(db.DateTime(timezone=True), nullable=True)

    created_at = db.Column(db.DateTime(timezone=True), default=utc_now, nullable=False)
    updated_at = db.Column(
        db.DateTime(timezone=True),
        default=utc_now,
        onupdate=utc_now,
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"<Quote {self.customer_name} - {self.status}>"


class FollowUpTemplate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id"), nullable=False, index=True
    )

    name = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(255), nullable=True)
    body = db.Column(db.Text, nullable=False)

    created_at = db.Column(db.DateTime(timezone=True), default=utc_now, nullable=False)
    updated_at = db.Column(
        db.DateTime(timezone=True),
        default=utc_now,
        onupdate=utc_now,
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"<FollowUpTemplate {self.name}>"
