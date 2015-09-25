# NsPortal




## Features


## Installation


### Requirements

 - [Node.js](https://nodejs.org/) (for [npm](https://www.npmjs.com/))
 - [bower](http://bower.io/) `npm install -g bower`
 - [python3.4](https://www.python.org/download/releases/3.4.0/) (for Windows you can install [miniconda3.4](http://conda.pydata.org/miniconda.html))


*Verify that node is in your PATH*

### Installation Process

#### Front
- `npm install`
- `bower install`

optional but recommended :

- `grunt build`

#### Back

Install those packages with `pip` or `conda` :

- pyodbc (for SQL Server database) or psycopg2 (for PostrgreSQL database)
- reportlab
- [scikit-learn](http://scikit-learn.org/stable/)
- [sqlalchemy](http://www.sqlalchemy.org/)
- zope.interface
- pandas=0.15.0
- pyjwt

Run the setup install : 
- `python setup.py install`


## Technolgies && Usage

### Front

> npm
> bower

* Grunt :
 `grunt build` build the code : 
  1. compile less files to app/styles/main.css (+ map file in dev mode)
  2. build html files with JST (app/build/templates.js)
  3. build js files : requirejs optimisation, minify and uglify (app/buil/prod.js)

- `grunt release` : launch `grunt build` then change entry file in the index for production mode (prod.js)

- `grunt dev` : launch `grunt build` then change entry file in the index for development mode

 RequireJS
 Backbone Underscore
 MarionetteJs

- rename the config.js.default to config.js then add your specifications (url of the REST server, can be a reverse proxy)

### Back

 >[Pyramid](http://docs.pylonsproject.org/projects/pyramid/en/latest/)
 >[SQLAlchemy](http://www.sqlalchemy.org/)


You have to configure the [development.ini](https://github.com/NaturalSolutions/NsPortal/tree/master/Back/development.ini.default) which can be found in the [Back folder](https://github.com/NaturalSolutions/NsPortal/tree/master/Back/).
You have to enter the siteName parameter which the site name of the local site (### Site name).
Run `pserve development.ini` command in order to launch a Pyramid server.

#### Database configuaration

## Quality && Test

### Style Guide

### Test

## Workflow && Contribution

Natural Solutions (NS) is based upon the collaborative development process of Git/GitHub.

![gitWorkflow](http://img11.hostingpics.net/pics/424731gitflow.png)

If you want to contribute on this project, please create a new pull request :
1. Fork the repository into your own GitHub repository in order to work on this one,
2. Then create a new branch first,
3. Finally, send a pull request to the [main repository](https://github.com/NaturalSolutions/NsPortal/) when the task is ready for review.
4. When the pull request received at least one validation comment from an owner member of the repository, it will be merge to this one.

Thank you!


## Demo


## Commercial Support

We have programs for companies that require additional level of assistance through training or commercial support, need special licensing or want additional levels of capabilities. Please visit the [Natural Solutions](http://www.natural-solutions.eu/) Website for more information about the portal or contact us by email at contact@natural-solutions.com.

## License

Copyright (c) 2015 Natural Solutions
Licensed under the MIT license.
