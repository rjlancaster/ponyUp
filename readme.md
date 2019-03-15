# Welcome to Pony Up developed by Richard Lancaster
----
## What is Pony Up?

> The Pony Up application is built in Python and Django and is used to track and divide household expenses. The user has the option of showing how much is money is due per tenant by choosing to divide bills evenly or by tenant's contribution to overall household income. In the instance of the latter, a percentage of household contribution is calculated per tenant and applied to calculate how much is due for that tenant. Pony Up can store history for multiple cycles and is fully CRUD capable. Data stored in SQLite 3 database.

----

![PonyUpScreenshot1](/src/images/2.png)

![PonyUpScreenshot2](/src/images/1.png)

## What technologies went into the application?

>  Python | Django | SQLite 3 | Bootstrap

## Entity Relationship Diagram
![Pony Up ERD](/src/images/ERD.png "Pony Up ERD")

# Installing Core Technologies

## 1. SQLite

### For OSX Users

```
brew install sqlite
```

### For Windows Users

Visit the [SQLite downloads](https://www.sqlite.org/download.html) and download the 64-bit DLL (x64) for SQLite version, unzip and install it.

## 2. SQL Browser

The [DB browser for SQLite](http://sqlitebrowser.org/) will let you view, query and manage your databases for this project.

## 3. Visual Studio Code

[Visual Studio Code](https://code.visualstudio.com/download) is Microsoft's cross-platform editor that you can use to view Python and Django code.

# Setting up environment and installing dependencies

## 1. Set up your virtual environment

Within the terminal, navigate to the location where you'd like to create the new environment and Pony Up project. Create a folder called PonyUp and navigate within the new folder. Then, enter this text to create the new environment:
```
virtualenv ENV
```
Then activate your environment:
```
source ENV/bin/activate
```
Note that you can type "deactivate" to end the new environment at any time.

## 2. Install Django

Within your new PonyUp folder, download the Django code by typing:
```
pip install django
```

## 3. Download the Pony Up project

Within your new PonyUp project folder, download the source code by typing:
```
git clone https://github.com/rjlancaster/ponyUp.git
```

## 4. Starting the project server

After downloading the Pony Up project, you should have a new folder within the Pony Up Project folder that you created. The new folder will also be called PonyUp.  Navigate within this folder.  Start the server by typing:
```
python manage.py runserver
```

## 5. Navigate to the Pony Up webpage

Within your web browser, navigate to http://localhost:8000/

From here, you should see the main links for the Pony Up application.


# Creating the Pony Up DB

While inside the PonyUp/PonyUp folder, enter this command:
```
python manage.py makemigrations Workforce
```
Then enter
```
python manage.py migrate
```
You now have a database named sqlite3.sql within your existing folder.  Use the DB Browser for SQLite to open the new database if desired.


