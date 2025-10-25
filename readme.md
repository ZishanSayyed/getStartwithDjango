# Django Beginner Cheat Sheet & Overview

## What is Django?
Django is a high-level Python web framework that allows rapid development of secure and maintainable web applications. It follows the **MVC (Model-View-Controller)** pattern (called **MTV** in Django: Model-Template-View).

- **Models**: Define the database structure.
- **Views**: Handle business logic and return responses.
- **Templates**: Define the HTML structure and rendering.

Django comes with an **admin interface**, URL routing, ORM, authentication, and more out-of-the-box.

---

## File Structure Overview
A typical Django project structure looks like this:

```
projectname/
    manage.py                 # CLI for running server, migrations, etc.
    projectname/              # Project configuration folder
        __init__.py
        settings.py           # Project settings: DB, installed apps, middleware
        urls.py               # Project-level URL routing
        wsgi.py / asgi.py    # Web server entry points
    appname/                  # Example app folder
        __init__.py
        admin.py              # Admin configuration for models
        apps.py               # App configuration
        models.py             # Database models
        views.py              # Request handling logic
        urls.py               # App-level URL routing
        migrations/           # Database migration files
            __init__.py
        templates/            # HTML templates for rendering views
            appname/
                detail.html
        static/               # CSS, JS, images
```

### Explanation of Key Files
- **manage.py** → Command-line utility for running server, migrations, shell, etc.
- **settings.py** → Define installed apps, databases, static files, middleware.
- **urls.py** → Map URL patterns to views; project-level includes app URLs.
- **wsgi.py / asgi.py** → Connects Django with web servers.
- **models.py** → Define the data structure, relationships, and database schema.
- **views.py** → Handle HTTP requests and return responses.
- **admin.py** → Configure how models appear in Django admin interface.
- **migrations/** → Auto-generated files to apply changes in models to the database.
- **templates/** → HTML files with template tags for dynamic content.
- **static/** → Store static files like CSS, JavaScript, images.

---

## Common Commands
| Command | Purpose |
|---------|--------|
| `pip install django` | Install Django framework |
| `django-admin startproject projectname` | Create a new Django project |
| `python manage.py startapp appname` | Create a new app within project |
| `python manage.py runserver` | Start development server |
| `python manage.py makemigrations` | Create migration files from models changes |
| `python manage.py migrate` | Apply migrations to the database |
| `python manage.py createsuperuser` | Create admin user for admin interface |
| `python manage.py shell` | Open interactive Django shell |

---

## Quick Overview of Key Files
### models.py
- Defines the database structure.
- Example:
```python
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
```
- **Why:** Models map Python classes to database tables. ForeignKey defines relationships.

### views.py
- Handles requests and generates responses.
- Example:
```python
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'appname/detail.html', {'question': question})
```
- **Why:** Views separate logic from presentation; use templates for HTML rendering.

### urls.py
- Maps URL patterns to views.
- Example:
```python
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:question_id>/', views.detail, name='detail'),
]
```
- **Why:** Provides clean URL routing and modular URL management.

### templates/
- HTML templates with Django template language.
- Example `detail.html`:
```html
<h1>{{ question.question_text }}</h1>
<ul>
{% for choice in question.choice_set.all %}
    <li>{{ choice.choice_text }}</li>
{% endfor %}
</ul>
```
- **Why:** Templates allow dynamic content rendering while keeping HTML separate from Python logic.

### admin.py
- Registers models for Django admin interface.
- Example:
```python
from django.contrib import admin
from .models import Question, Choice

admin.site.register(Question)
admin.site.register(Choice)
```
- **Why:** Admin interface allows easy database management without coding CRUD operations manually.

### migrations/
- Auto-generated files for database schema changes.
- **Why:** Tracks model changes over time; ensures consistent database schema across environments.
- Typical commands:
```bash
python manage.py makemigrations  # Create migration files
python manage.py migrate         # Apply migrations to database
```

---

## Tips for Beginners
- Always check URL patterns; they must match exactly.
- Use `ForeignKey` and reverse lookups (`choice_set.all()`) for related data.
- Keep templates organized in `templates/appname/`.
- Use the admin site for easy data entry and management.
- Test views in browser and Django shell.
- Keep `DEBUG = True` in development for detailed errors; set to `False` in production.
- Use migrations to version control your database schema.

---

## Quick URL Reference (Example Polls App)
- `/polls/` → Index page (list of questions)
- `/polls/1/` → Detail page for question with ID 1
- `/polls/1/results/` → Results page for question 1
- `/polls/1/vote/` → Voting page for question 1

