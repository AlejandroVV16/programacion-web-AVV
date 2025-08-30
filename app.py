from flask import Flask, render_template, url_for, request, redirect, flash
from forms import EventForm, RegisterForm
from datetime import date, datetime
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tengo-hambre'


events = [
    {
        'id': 1,
        'title': 'Clase programacion web',
        'slug': 'clase-programacion',
        'description': 'Trabajo de final de primer corte.',
        'date': '2025-09-29',
        'time': '20:00',
        'location': 'Salon Ingenieria',
        'category': 'Tecnología',
        'max_attendees': 50,
        'attendees': [
            {'name': 'Sebastian Diaz', 'email': 'Diaz@hotmail.com'},
            {'name': 'Marí', 'email': 'yeral@gmail.com'}
        ],
        'featured': True
    },
    {
        'id': 2,
        'title': 'Festival Cultural Universitario',
        'slug': 'festival-cultural-universitario',
        'description': 'Un evento cultural con música, danza y arte estudiantil.',
        'date': '2025-09-20',
        'time': '18:00',
        'location': 'Plaza Central',
        'category': 'Cultural',
        'max_attendees': 200,
        'attendees': [
            {'name': 'Ana López', 'email': 'ana@gmail.com'}
        ],
        'featured': False
    },
    {
        'id': 3,
        'title': 'Torneo de Fútbol Interfacultades',
        'slug': 'torneo-futbol-interfacultades',
        'description': 'Competencia deportiva entre las diferentes facultades.',
        'date': '2025-09-25',
        'time': '09:00',
        'location': 'Campo Deportivo',
        'category': 'Deportivo',
        'max_attendees': 100,
        'attendees': [],
        'featured': True
    }
]

categories = ['Tecnología', 'Académico', 'Cultural', 'Deportivo', 'Social']


def create_slug(title):
    """Crear un slug URL-friendly a partir del título"""
    slug = title.lower()
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    slug = re.sub(r'\s+', '-', slug)
    return slug.strip('-')

def get_next_id():
    """Obtener el siguiente ID disponible"""
    if not events:
        return 1
    return max(event['id'] for event in events) + 1

def get_upcoming_events():
    """Obtener eventos próximos (ordenados por fecha)"""
    today = date.today().strftime('%Y-%m-%d')
    upcoming = [event for event in events if event['date'] >= today]
    return sorted(upcoming, key=lambda x: x['date'])

def get_featured_events():
    """Obtener eventos destacados"""
    return [event for event in events if event.get('featured', False)]

@app.route('/')
def index():
    """Página principal con lista de eventos próximos"""
    upcoming_events = get_upcoming_events()
    featured_events = get_featured_events()
    return render_template('index.html', 
                        upcoming_events=upcoming_events, 
                        featured_events=featured_events)

@app.route('/event/<slug>/')
def event_detail(slug):
    """Detalle de un evento específico"""
    event = next((e for e in events if e['slug'] == slug), None)
    if not event:
        flash('Evento no encontrado', 'error')
        return redirect(url_for('index'))
    
    # Calcular espacios disponibles
    available_spots = event['max_attendees'] - len(event['attendees'])
    
    return render_template('event_detail.html', 
                        event=event, 
                        available_spots=available_spots)

@app.route('/admin/event/', methods=['GET', 'POST'])
def create_event():
    """Formulario para crear un nuevo evento"""
    form = EventForm()
    form.category.choices = [(cat, cat) for cat in categories]
    
    if form.validate_on_submit():
        new_event = {
            'id': get_next_id(),
            'title': form.title.data,
            'slug': create_slug(form.title.data),
            'description': form.description.data,
            'date': form.date.data.strftime('%Y-%m-%d'),
            'time': form.time.data.strftime('%H:%M'),
            'location': form.location.data,
            'category': form.category.data,
            'max_attendees': form.max_attendees.data,
            'attendees': [],
            'featured': form.featured.data
        }
        
        events.append(new_event)
        flash(f'Evento "{new_event["title"]}" creado exitosamente!', 'success')
        return redirect(url_for('event_detail', slug=new_event['slug']))
    
    return render_template('create_event.html', form=form)

@app.route('/event/<slug>/register/', methods=['GET', 'POST'])
def register_event(slug):
    """Formulario para registrarse a un evento"""
    event = next((e for e in events if e['slug'] == slug), None)
    if not event:
        flash('Evento no encontrado', 'error')
        return redirect(url_for('index'))
    
    # Verificar si el evento está lleno
    if len(event['attendees']) >= event['max_attendees']:
        flash('Lo sentimos, este evento ya está lleno.', 'error')
        return redirect(url_for('event_detail', slug=slug))
    
    form = RegisterForm()
    
    if form.validate_on_submit():
        # Verificar si el email ya está registrado
        existing_attendee = next((a for a in event['attendees'] 
                                if a['email'] == form.email.data), None)
        
        if existing_attendee:
            flash('Este email ya está registrado para este evento.', 'error')
        else:
            # Agregar nuevo asistente
            new_attendee = {
                'name': form.name.data,
                'email': form.email.data
            }
            event['attendees'].append(new_attendee)
            flash(f'¡Te has registrado exitosamente para "{event["title"]}"!', 'success')
            return redirect(url_for('event_detail', slug=slug))
    
    return render_template('register_event.html', form=form, event=event)

@app.route('/events/category/<category>/')
def events_by_category(category):
    """Filtrar eventos por categoría"""
    if category not in categories:
        flash('Categoría no válida', 'error')
        return redirect(url_for('index'))
    
    filtered_events = [event for event in get_upcoming_events() 
                    if event['category'] == category]
    
    return render_template('events_by_category.html', 
                        events=filtered_events, 
                        category=category,
                        categories=categories)

@app.route('/categories/')
def list_categories():
    """Listar todas las categorías disponibles"""
    return render_template('categories.html', categories=categories)

if __name__ == '__main__':
    app.run(debug=True)