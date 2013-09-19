This is a boilerplate for new Django projects.

Includes 'users' app with custom user model and user login/logout.

Static files are on 'static' branch. The base template uses Foundation framework which is included in 'static'.

Admin panel is enabled by default and is available from url `/admin`.


##Installation:
```
git clone git@github.com:xtranophilist/django-base.git your_project_name
cd your_project_name
pip install -r requirements.txt
```

Edit `app/settings_secret.py` to change static file paths, urls and database settings.


```
./manage.py syncdb
./manage.py migrate
```

For installing static files:
```
git clone git@github.com:xtranophilist/django-base.git your_project_name
git checkout static
````


