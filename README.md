# ToDo List Application

This is a Django-based ToDo list application. It allows users to create, manage, and share ToDo lists with others. Users can create tasks, mark them as completed, set deadlines, and more. All in simple style of sticky notes.

You can try the app [here](https://www.todo-list.cz).

## Features

- User authentication and authorization system.
- CRUD operations for ToDo lists and tasks.
- Share lists with other users via shareable links.
- Dark mode and font settings for users.
- Responsive design for mobile and desktop.

## Usage
- **Login or Signup**: Access the application and either login with existing credentials or signup for a new account. You can retrieve your password if you dont remember it.
- Create a ToDo List: Once logged in, you can create a new ToDo list by clicking on the "Add new ToDo list" button.
    - Its possible for a list to be either shared or personal.
    - personal lists still can be shared via share link, but cant be edited by another users.

- **Manage Tasks**: Add tasks to your ToDo list by clicking on the edit button. You can mark tasks as completed, set deadlines, and edit or delete tasks as needed.

- **Share Lists**: Share your ToDo lists with others by clicking on the "Share" button. You can stop sharing lists using the "Stop sharing" button.
    - you can see different users that have access to your list at top right of list on your homepage.

- **Customize Settings**: Personalize your experience by enabling dark mode or adjusting email notification settings in the "Settings" page.
    - you can also change username, password or email
    - email is needed only for password retrival

- **Admin Interface**: As a superuser, you can access the admin interface by appending /admin to the application URL. Here, you can manage users, ToDo lists, and tasks.

## Installation

1. Clone this repository to your local machine:
```git clone https://github.com/jnemec91/django-todo.git```
2. Install the required dependencies using pip:
```pip install -r requirements.txt```

3. Edit your settings file according to your set-up using ```sudo nano settings.py``` replace ```nano``` with your favorite editor. Here change ```SECRET_KEY```, Email settings, Database settings and more depending on your set=up. You can refer official django [docs](https://docs.djangoproject.com/en/5.0/ref/settings/) for more information.
4. Apply database migrations:
```python manage.py migrate```
5. Create a superuser account (optional):
```python manage.py createsuperuser```
6. Run the development server:
```python manage.py runserver```
Access the application in your web browser at http://localhost:8000.

## Heroku quick deploy guide

1. Create heroku account
2. Click create new app, choose name and region for app and save it
3. Go to `Resources` page, click find more add-ons and search for `Heroku Postgres`
4. Add it to the project
5. Go to settings, click Reveal config vars and add variables to the project:
    ```
    DATABASE_URL = url_of_your_postgres_db
    DEFAULT_EMAIL = default_email_address
    EMAIL_PASSWORD = default_email_password
    EMAIL_USER = default_email_user
    SMTP_SERVER = default_email_smtp_server
    SMTP_PORT = default_email_smtp_port
    KEY = django_secret_key
    DISABLE_COLLECTSTATIC = 1
    ```
6. You can also add custom domain and configure ssl in settings
7. Connect your repo on github or push your repo to heroku main via [heroku-cli](https://devcenter.heroku.com/articles/heroku-cli)
8. You should be able to access your app now by clicking `Open app` button

## Automatic Deployment via GitHub
1. Connect your GitHub repository to Heroku:
    - Navigate to your Heroku dashboard.
    - Open your app's settings.
    - Scroll down to the "Deployment method" section.
    - Select "GitHub" as the deployment method.
    - Search for your repository and connect it to Heroku.

2. Enable automatic deploys:
    - croll down to the "Automatic deploys" section.
    - Choose the branch you want to deploy automatically (e.g., main).
    - Click on the "Enable Automatic Deploys" button.
    - Now, every time you push changes to the selected branch on GitHub, Heroku will automatically deploy those changes.

## Requirements
- `Python 3.8+`
- `asgiref` library
- `Django` library
- `gunicorn` library
- `packaging` library
- `psycopg2-binary` library
- `sqlparse` library
- `tzdata` library
- `whitenoise` library
- `dj_database_url` library

## Contributors
[Jaroslav Němec](https://github.com/jnemec91) - Creator and maintainer

## License
This project is licensed under the GNU GENERAL PUBLIC LICENSE Version 3. - see the [LICENSE](https://github.com/jnemec91/django-todo/blob/main/LICENSE.txt)