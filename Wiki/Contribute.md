<h3 align='center'> Contribute to community bunq web app</h3>

![gif]

---

All contributions are welcome, even if they don't pass the [tests] I'll take a look at it and make the appropriate changes. Of course your pull request must make sense, and should not be something completely random.

---

<h3 align='center'> Run local development server</h3>

If you want to run the entire app locally via the development server you must perform a few setup steps. Before you do the following, it would be smart to set up a [virtual environment] so that nothing gets installed system wide.

  1. Clone the repo `$ git clone  https://github.com/OGKevin/ComBunqWebApp.git` and `cd` to the root directory of the project.
  2. Install the requirements via `$ pip install -r requirements.txt` and `npm install`. (You must have [pip] and [npm] installed)
  3. Set up a [postgres] database, start it and change the the following section in the settings.py
   
   ```python
    else:  # pragma: no cover
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME':  'KevinH',
        }
    }
   ```

  4. Make the migrations in the database by running `$ python manage.py migrate`
  5. The local development server does not run with HTTPS enabled so you will need to disable this in the settings
    
   ```python
    
    DEBUG = True
    SECURE_SSL_REDIRECT = True  # change this to False
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    ALLOWED_HOSTS = ['.combunqweb.herokuapp.com', '.127.0.0.1']
    LOGIN_URL = 'two_factor:login'
    SESSION_EXPIRE_AT_BROWSER_CLOSE = True
    SESSION_COOKIE_SECURE = True  # change this to False

   ```
  6. Now you should be able to run the local development server by running `$ python manage.py runserver`

---
<h3 align='center'> Front end </h3>

For front end contributions you can skip the local development server however it would be better to get the local development server running either way. The HTML, CSS and JS of this project are stored in the templates and static folder.
Please maintain the current folder structure. Add new files in the right folder, Eg. you want to add some CSS to the home page ?
1. Create a file called `index.css`. Same name as the HTML name.
2. Its HTML is stored in `templates/Home/index.html`, so the `.css` file will be saved in `static/Home/CSS/index.css`
3. Load the css in the html file by placing the following code:
  ```html
  <link rel="stylesheet" href="{%static "Path/to/file/without/static"%}"/>
  <link rel="stylesheet" href="{%static "Home/CSS/index.css"%}"/>
  ```
  
In the HTML files you can encounter code like `{{description}}` and `{{balance.value}}` which are placeholders for values that will be returned from the server. For examples of what these values can be you can read it on the [bunq api docs]. Basically each [button] has its own html located in `static/{appName}/templates/mustache` and renders the data return. Via the documentation links you can se examples of the returned data.
```
+-static/
  |
  +-BunqAPI/
  | |
  | +-CSS/
  | |
  | +-JS/
  | | |
  | | +-decrypt.js
  | |
  | +-templates/
  |   |
  |   +-mustache/
  |     |
  |     +-accounts.html
  |     |
  |     +-payments.html
  |     |
  |     +-start_session.html
  |     |
  |     +-users.html
  |
  +-Manager/
    |
    +-CSS/
    | |
    | +-form.css
    | |
    | +-index.css
    |
    +-images/
    | |
    | +-bunq-Desktop.png
    |
    +-JS/
      |
      +-index.js

+-templates/
  |
  +-BunqAPI/
  | |
  | +-decrypt.html
  | |
  | +-error/
  | | |
  | | +-notLogIn.html
  | | |
  | | +-notYourFile.html
  | |
  | +-index.html
  |
  +-Home/
  | |
  | +-index.html
  |
  +-Manager/
  | |
  | +-form.html
  | |
  | +-index.html
  | |
  | +-thanks.html
  |
  +-registration/
    |
    +-logged_out.html
    |
    +-register.html
```

---
<h3 align='center'> Make pull request</h3>

After you are done making your changes you can make a pull request, there are some tests that need to pass before this pr can be accepted. To run these tests locally you can run `$ coverage run manage.py test && coverage html -d htmlcov/ && open htmlcov/index.html`. This will run the tests and open a web page that shows you the coverage of the test. Please try to follow [PEP8] rules while coding in python.

[gif]:<https://pressmagazineonline.files.wordpress.com/2016/04/contribute-word-animated.gif>
[tests]:<https://travis-ci.org/OGKevin/ComBunqWebApp>
[django]:<django>
[virtual environment]:<https://virtualenv.pypa.io/en/stable/>
[pip]:<https://pip.pypa.io>
[npm]:<https://www.npmjs.com>
[postgres]:<https://www.postgresql.org>
[PEP8]:<https://www.python.org/dev/peps/pep-0008/>
[bunq api docs]:<https://doc.bunq.com/api/1/page/introduction>
[Button]:<https://github.com/OGKevin/ComBunqWebApp/wiki#buttons-explained>
