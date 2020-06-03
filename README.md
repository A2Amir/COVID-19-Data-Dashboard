# COVID-19 Dashboard

## Link to Coronavirus API Data Dashboard:
<center>dgfdsdsfdsfdsfdsfdsm</center>


## Introduction:

This is a flask app that visualizes data from the COVID-19 API. Data is pulled directly from the API and then visualized using Plotly.

This flask app first gives an overview of the three base languages for web development: **html, css**, and **JavaScript** to work with the web template and make a data dashboard. If you want to customize the dashboard, you can do so with just a few changes to the html code but the underlying technologies of data dashboard will be css, html, JavaScript, and Python.

* The Basics of the web app
  *	[html](https://www.w3schools.com/tags/default.asp)
  *	[css](https://www.lifewire.com/what-does-cascade-mean-3466872)
  * [javascript](https://plot.ly/javascript/getting-started/)

* The Front-end libraries
  * [boostrap](https://getbootstrap.com/)
  * [plotly](https://plot.ly/)

* The Back-end libraries
  * [flask](http://flask.pocoo.org/)


## Prerequisites

To install the flask app, you need:

  * python3
  * python packages in the requirements.txt file

Install the packages with

 * pip install -r requirements.txt
 * To create an environment using: **conda create --name <env> --file requirements.txt**


## Installing

On a MacOS/linux/Window system, installation is easy. Open a terminal, and go into the directory with the flask app files. Run python **python covid19.py** in the terminal then open a new web browser window, and type the following in the address bar:

          http://localhost:3001/

* DON'T FORGET TO INCLUDE-3001. You should be able to see the web app. The number 3001 represents the port for accessing your web app.


## Deploy the web app to the cloud

1. To run the web app, go into the directory where the file **covid19.py** is and open the terminal and type:

       python covid19.py
       
* Make sure that the web app is working locally.
2. Next, go to [www.heroku.com](https://www.heroku.com/) and create an account if you haven't already.

3. Create a new folder and move all of the covid19-web app folders and files into the folder:

       mkdir web_app
       mv -t web_app data covidapp wrangling_scripts covid19.py
      
4. Update python using the terminal command **conda update python**

5. The next step is to create a virtual environment (next to the new folder to which all files and folders have been moved) and then activate the environment:

* Windows System:

      python -m venv covid19_venv
      .\covid19_venv\Scripts\activate
   
* Linux Systems:

      python3 -m venv worldbankvenv
      source worldbankenv/bin/activate

  Then, pip install the Python libraries needed for the web app (In this case those are presented below)
  
      pip install flask pandas plotly gunicorn plotly-express numpy  requests matplotlib
      
6. The next step is to install the [heroku command line tools](https://devcenter.heroku.com/articles/heroku-cli):


* Windows System:

      curl https://cli-assets.heroku.com/install.sh | sh
      
        
* Ubuntu Systems:

      sudo snap install --classic heroku
      
  Then check the installation with the command:

      heroku —-version
     
7. log into heroku with the following comman
   
       heroku login
  
 * Heroku asks for your account email address and password, which you type into the terminal and press enter.

8. The next steps involved some housekeeping:

*	Remove app.run() from covid19.py
*	Type **cd web_app** into the Terminal so that you are inside the folder with your web app code
 
9. Then create a proc file, which tells Heroku what to do when starting your web app:
     
        touch Procfile
    
    Then open the Procfile and type:
    
        web gunicorn covid19:app
        
* The Flask application file is called covid19.py. In the template code, the same file is called covid19.py. So the Procfile should contain the line    

10. Next, create a requirements file, which lists all of the Python library that your app depends on:

        pip freeze > requirements.txt
11. Initialize a git repository and make a commit:

        git init
        git add .
        git commit -m ‘first commit’
   
   Now, create a heroku app:
   
        heroku create my-app-name
   
   where my-app-name is a unique name that nobody else on Heroku has already used. The **heroku create** command should create a git repository on Heroku and a web address for accessing your web app. You can check that a remote repository was added to your git repository with the following terminal command:
    
        git remote -v
   Next, you need to push your git repository to the remote heroku repository with this command:
   
       git push heroku master
       
 Now, you can type your web app's address in the browser to see the results.
