# Community BunqWeb

[![Greenkeeper badge](https://badges.greenkeeper.io/OGKevin/ComBunqWebApp.svg)](https://greenkeeper.io/)



[![N|Solid](https://lh3.googleusercontent.com/B0u_lzpnrZMdR8o3ece3N9sLQtOgc1UayCJLYUhzJh7Xkr4oJEdQk0-PJFhx0-a0CA=w300)][BunqPic]

[![Build Status](https://travis-ci.org/OGKevin/ComBunqWebApp.svg?branch=master)](https://travis-ci.org/OGKevin/ComBunqWebApp)
[![Coverage Status](https://coveralls.io/repos/github/OGKevin/ComBunqWebApp/badge.svg?branch=master)](https://coveralls.io/github/OGKevin/ComBunqWebApp?branch=master)
[![Code Climate](https://codeclimate.com/github/OGKevin/ComBunqWebApp/badges/gpa.svg)](https://codeclimate.com/github/OGKevin/ComBunqWebApp)
[![Updates](https://pyup.io/repos/github/OGKevin/ComBunqWebApp/shield.svg)](https://pyup.io/repos/github/OGKevin/ComBunqWebApp/)
[![Python 3](https://pyup.io/repos/github/OGKevin/ComBunqWebApp/python-3-shield.svg)](https://pyup.io/repos/github/OGKevin/ComBunqWebApp/)



Community BunqWeb is going to be a web interface for bunqers using the [Bunq API](https://www.bunq.com/en/api).



Disclaimer: Bunq it self has nothing to do with this project



View the app live based on the latest release: <https://combunqweb.herokuapp.com/manager>

# Goals

  - Bunqer can see his/her current(total) balance

  - Bunqer can see his/her transactions and can use filters/sorting

  - Bunqer can generate a bunq.me QR code

  - Beautiful Front-End work

  - Secure way to handle users API keys



# Current Features!



  - Use Bunq CSV file and see a Pie of income, exapnses, transaction names and percentages
 

# Why Community ?

> Would be convenient to have a non-mobile version of bunq! Is there something on the roadmap? -[Tezzlicious][ForumLink]



> We kijken naar de mogelijkheden, maar hebben hier geen korte termijnplannen voor, aangezien we ons volledig op het ontwikkelen van de app focussen. -[Bunq][Answer]



### Contribute

All pull request are welcome, because this project is mixed with Front- and Back-end, there can be 2 ways to contribute to the project.



#### Front End



1. In the folder [templates](../master/templates/) u will find HTML documnets. These templates are used to render the front end. In some of these files there might be wierd markings like:

    ```html

    <link rel="stylesheet" href="{%static "Manager/CSS/index.css"%}"/>

    {%for x in data%}

        <tr>

		    <td>{{x.0}}</td>

		    <td>{{x.1}}</td>

		    <td>{{x.2}}</td>

	    </tr>

    {%endfor%}

    ```

    This is  back end stuff and u shouldnt worry much about it for now.

- In the folder [static](../master/static/) u will find the CSS and JS documents used by the templates.

- Change the ```href=''``` and ```src=''``` atributes by dublicating it, commenting one of them out and change the other one to```/static/Manager...``` like u normaly would. After you're done and ready to make a pull request uncomment the original line and remove the edited one.



For Front End packages we use [npm][npm] so make sure u install and use the dependencies in the [package.json](../master/package.json) file by running

```sh

$ npm install

```
U can also make use of placeholder texts :-)
##### Todo

- create a front page

- beautify the page too show graphs and additional transactions info etc





#### Back End

For this project were gonna use [Django][django] and [Heroku][heroku], make sure u have these 2 softwares installed. Beofre u perfomr any of the follwoing commands make sure your are in the root directroy of the project.

1. run ```$ pip install -r requirements.txt``` to install the python packages used in this project. It might be a good idea to setup and use [virtualenv][virtualenv].

- setup local postgress database and change the database settings in [settings.py](../master/BunqWebApp/settings.py) file

- now we need to collect static files by running the following:

    ```sh

    $ ./manage.py npm install

    $ ./manage.py collectstatic

    ```

- to run a local develepment server:

    ```sh

    $ ./manage.py runserver

    ```

    Before u push your chages make sure it runs on heroku aswell by using

    ```sh

    $ heroku local

    ```

    and see if heroku can handle the greatness that awaits.

    

##### Todo

- Create database models for storing user info
- ~~Create database models for storing catagories~~

- Hook it up to the Bunq API

- ~~Fix staticfiles issue #1~~



License

----



MIT





**Free Software, Hell Yeah!**





   [BunqPic]: <https://www.bunq.com/en/>

   [ForumLink]:<https://together.bunq.com/topic/is-there-a-browser-web-desktop-client-planned>

   [Answer]:<https://together.bunq.com/topic/is-there-a-browser-web-desktop-client-planned#comment-1881>

   [django]:<https://www.djangoproject.com/>

   [heroku]:<https://www.heroku.com/>

   [npm]:<https://www.npmjs.com/>

   [virtualenv]:<https://virtualenv.pypa.io/en/stable/>

   
