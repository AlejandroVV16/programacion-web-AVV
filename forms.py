from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, IntegerField, BooleanField, DateField, TimeField
from wtforms.validators import DataRequired, Email, NumberRange, Length
from wtforms.widgets import TextArea
from datetime import date, time

class EventForm(FlaskForm):
    """Formulario para crear nuevos eventos"""
    title = StringField('Título del Evento', 
                    validators=[DataRequired(message="El título es obligatorio"),
                                Length(min=3, max=100, message="El título debe tener entre 3 y 100 caracteres")])
    
    description = TextAreaField('Descripción', 
                            validators=[DataRequired(message="La descripción es obligatoria"),
                                        Length(min=10, max=500, message="La descripción debe tener entre 10 y 500 caracteres")],
                            widget=TextArea())
    
    date = DateField('Fecha del Evento', 
                    validators=[DataRequired(message="La fecha es obligatoria")],
                    default=date.today)
    
    time = TimeField('Hora del Evento', 
                    validators=[DataRequired(message="La hora es obligatoria")],
                    default=time(14, 0))  # 2:00 PM por defecto
    
    location = StringField('Ubicación', 
                        validators=[DataRequired(message="La ubicación es obligatoria"),
                                    Length(min=3, max=100, message="La ubicación debe tener entre 3 y 100 caracteres")])
    
    category = SelectField('Categoría', 
                        validators=[DataRequired(message="Debe seleccionar una categoría")],
                        choices=[])  # Se poblará dinámicamente en la vista
    
    max_attendees = IntegerField('Número máximo de asistentes', 
                                validators=[DataRequired(message="Debe especificar el número máximo de asistentes"),
                                        NumberRange(min=1, max=1000, message="El número debe estar entre 1 y 1000")])
    
    featured = BooleanField('Evento destacado')

    def validate_date(self, field):
        """Validación personalizada para la fecha"""
        if field.data and field.data < date.today():
            raise ValidationError('La fecha del evento no puede ser en el pasado.')

class RegisterForm(FlaskForm):
    """Formulario para registro a eventos"""
    name = StringField('Nombre completo', 
                    validators=[DataRequired(message="El nombre es obligatorio"),
                                Length(min=2, max=100, message="El nombre debe tener entre 2 y 100 caracteres")])
    
    email = StringField('Correo electrónico', 
                    validators=[DataRequired(message="El correo electrónico es obligatorio"),
                                Email(message="Debe ser un correo electrónico válido"),
                                Length(max=100, message="El correo no puede exceder 100 caracteres")])

class SearchForm(FlaskForm):
    """Formulario para búsqueda de eventos (opcional - para funcionalidad adicional)"""
    search = StringField('Buscar eventos...', 
                        validators=[Length(max=50, message="La búsqueda no puede exceder 50 caracteres")])
    
    category = SelectField('Filtrar por categoría', 
                        choices=[('', 'Todas las categorías')],  # Se poblará dinámicamente
                        default='')

# Validaciones adicionales personalizadas
from wtforms.validators import ValidationError

def validate_future_date(form, field):
    """Validador personalizado para fechas futuras"""
    if field.data and field.data < date.today():
        raise ValidationError('La fecha debe ser hoy o en el futuro.')

def validate_business_hours(form, field):
    """Validador personalizado para horarios de eventos (opcional)"""
    if field.data:
        hour = field.data.hour
        if hour < 8 or hour > 22:  # Entre 8 AM y 10 PM
            raise ValidationError('Los eventos deben programarse entre las 8:00 AM y 10:00 PM.')