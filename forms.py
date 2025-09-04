from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, TimeField, SelectField, IntegerField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, NumberRange

class EventForm(FlaskForm):
    title = StringField("Título", validators=[DataRequired()])
    description = TextAreaField("Descripción", validators=[DataRequired()])
    date = DateField("Fecha", validators=[DataRequired()])
    time = TimeField("Hora", validators=[DataRequired()])
    location = StringField("Ubicación", validators=[DataRequired()])
    category = SelectField("Categoría", choices=[])
    max_attendees = IntegerField("Máximo de asistentes", validators=[DataRequired(), NumberRange(min=1)])
    featured = BooleanField("Evento destacado")
    submit = SubmitField("Crear evento")

class RegisterForm(FlaskForm):
    name = StringField("Nombre", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Registrarse")
