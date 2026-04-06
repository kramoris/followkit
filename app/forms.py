from flask_wtf import FlaskForm
from wtforms import DateField, DecimalField, PasswordField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange, Optional


class RegistrationForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(max=120)])
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=255)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8, max=255)])
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[DataRequired(), EqualTo("password", message="Passwords must match")],
    )
    submit = SubmitField("Create account")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=255)])
    password = PasswordField("Password", validators=[DataRequired(), Length(max=255)])
    submit = SubmitField("Log in")


class QuoteForm(FlaskForm):
    customer_name = StringField("Customer name", validators=[DataRequired(), Length(max=120)])
    job_description = TextAreaField("Job description", validators=[DataRequired()])
    quote_amount = DecimalField(
        "Quote amount",
        validators=[DataRequired(), NumberRange(min=0)],
        places=2,
    )
    date_sent = DateField("Date sent", validators=[Optional()], format="%Y-%m-%d")
    status = SelectField(
        "Status",
        validators=[DataRequired()],
        choices=[
            ("draft", "Draft"),
            ("sent", "Sent"),
            ("follow_up_due", "Follow-up due"),
            ("won", "Won"),
            ("lost", "Lost"),
            ("no_response", "No response"),
        ],
    )
    next_follow_up_date = DateField("Next follow-up date", validators=[Optional()], format="%Y-%m-%d")
    notes = TextAreaField("Notes", validators=[Optional()])
    contact_method = SelectField(
        "Contact method",
        validators=[DataRequired()],
        choices=[
            ("email", "Email"),
            ("phone", "Phone"),
            ("sms", "SMS"),
            ("whatsapp", "WhatsApp"),
            ("other", "Other"),
        ],
    )
    customer_email = StringField("Customer email", validators=[Optional(), Email(), Length(max=255)])
    customer_phone = StringField("Customer phone", validators=[Optional(), Length(max=50)])
    submit = SubmitField("Save quote")
