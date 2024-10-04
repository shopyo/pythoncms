
<div align="center">



<img src="https://github.com/shopyo/pythoncms/raw/main/assets/logo.png" width="200"/>

<br><br>

[![First Timers Only](https://img.shields.io/badge/first--timers--only-friendly-blue.svg)](https://www.firsttimersonly.com/)

🇲🇺

</div>



# Welcome to pythoncms

## Try

![](https://github.com/shopyo/pythoncms/raw/main/assets/term.gif)

In virtual env

```
pip install pythoncms
pythoncms start mysite
cd mysite
shopyo initialise
flask shopyo-seed
flask --debug run
```

If .env file not created, create .env file with content

```.env
ACTIVE_FRONT_THEME = 'editorial'
ACTIVE_BACK_THEME = 'sneat'
APP_NAME = 'Demo'
ACTIVE_ICONSET = 'boxicons'
SITE_TITLE = 'Site title'
SITE_DESCRIPTION = 'Site title'
```

## Local dev

Install package

! Important: Please create and activate a virtual environment.

```
python -m pip install -e .
```
Then initialise

```
cd pythoncms
shopyo initialise
flask --debug run
```

for migrating

```
flask db migrate
flask db upgrade
```

run

```
flask --debug run
```

dashboard

login with `admin@domain.com` | `pass`
```
http://127.0.0.1:5000/dashboard/
```

## Theme

Themes are located at '/static/themes/'

Each front theme must have

```
index.html
contact.html
page.html
```

Each back theme must have

```
base.html
login.html
register.html
unconfirmed.html
```

- info.json

```json
{
	"author": "ARJ",
	"version": "1.0.20000000000003"
}
```

## Info json

```
{
	"display_string": "Admin",
	"type": "show", // hidden if hide
	"icons":{
		"fa": "fas fa-user-lock", // set according to ACTIVE_ICONSET
		"boxicons": "",           // set according to ACTIVE_ICONSET
		"file": "icon.svg" // if present, will be used and searched for
						   // in module/static. Make sure to shopyo collecstatic in production
	},
	"url_prefix": "/appadmin",
	"menu": {
		"list users":"/", // url-prefix will be concatenated with it for sub menus.
		"add user": "/add",
		"roles":"/roles"
	},
	"menu-type": "show-menu", // or no-menu. Expects menu key if show-menu.
	"module_name": "appadmin",
	"author": {
		"name":"Abdur-Rahmaan Janhangeer",
		"website":"https://www.pythonkitchen.com/about-me/",
		"mail":"arj.python@gmail.com"
		}
}
```
## Changelog

1.2.0

- Tiny MCE configured
- start command
