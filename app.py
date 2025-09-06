from flask import Flask, render_template, redirect, url_for, request, flash
from forms import EventForm, RegisterForm
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "supersecretkey"

# -----------------------|1
# Datos en memoria
# -----------------------
events = [
    {
        'id': 1,
        'title': 'Conferencia de juegos',
        'slug': 'conferencia-juegos',
        'description': 'Aprende sobre desarrollo con Python y Flask para juegos',
        'date': '2025-09-15',
        'time': '14:00',
        'location': 'Auditorio Principal',
        'category': 'Tecnología',
        'max_attendees': 50,
        'attendees': [
            {'name': 'Juan Pérez', 'email': 'juan@example.com'}
        ],
        'featured': True
    }
]

categories = ['Tecnología', 'Académico', 'Cultural', 'Deportivo', 'Social']

# -----------------------
# Rutas
# -----------------------

@app.route("/")
def index():
    return render_template("index.html", events=events, categories=categories)

@app.route("/event/<slug>/")
def event_detail(slug):
    event = next((e for e in events if e['slug'] == slug), None)
    if not event:
        flash("Evento no encontrado", "danger")
        return redirect(url_for("index"))
    return render_template("event_detail.html", event=event)

@app.route("/admin/event/", methods=["GET", "POST"])
def create_event():
    form = EventForm()
    form.category.choices = [(c, c) for c in categories]

    if form.validate_on_submit():
        new_event = {
            "id": len(events) + 1,
            "title": form.title.data,
            "slug": secure_filename(form.title.data.lower().replace(" ", "-")),
            "description": form.description.data,
            "date": str(form.date.data),
            "time": form.time.data.strftime("%H:%M"),
            "location": form.location.data,
            "category": form.category.data,
            "max_attendees": form.max_attendees.data,
            "attendees": [],
            "featured": form.featured.data
        }
        events.append(new_event)
        flash("Evento creado con éxito ✅", "success")
        return redirect(url_for("index"))
    return render_template("event_form.html", form=form)

@app.route("/event/<slug>/register/", methods=["GET", "POST"])
def register_event(slug):
    event = next((e for e in events if e['slug'] == slug), None)
    if not event:
        flash("Evento no encontrado", "danger")
        return redirect(url_for("index"))

    form = RegisterForm()
    if form.validate_on_submit():
        if len(event['attendees']) >= event['max_attendees']:
            flash("El evento ya alcanzó el número máximo de asistentes ❌", "danger")
        else:
            event['attendees'].append({
                "name": form.name.data,
                "email": form.email.data
            })
            flash("Registro exitoso 🎉", "success")
            return redirect(url_for("event_detail", slug=slug))
    return render_template("register_form.html", form=form, event=event)

@app.route("/events/category/<category>/")
def filter_category(category):
    filtered = [e for e in events if e['category'] == category]
    return render_template("index.html", events=filtered, categories=categories)

if __name__ == "__main__":
    app.run(debug=True)

