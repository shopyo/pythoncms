# Welcome to pythoncms


## Local dev

Install package


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

Each theme must have

```
index.html
contact.html
page.html
```

- info.json

```json
{
	"author": "ARJ",
	"version": "1.0.20000000000003"
}
```
