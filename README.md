# MP-Config

This app helps to save custom site settings in admin and use them in views or templates.
Supported field types:

* CharField
* TextField
* HTMLField
* IntegerField
* FloatField
* BooleanField
* UrlField
* EmailField
* FileField
* ImageField

### Installation

Install with pip:

```sh
$ pip install django-mp-config
```

Add config to settings.py:
```
INSTALLED_APPS = [
    'site_config',
]
```

Context processors:
```
site_config.context_processors.config
```
Example of usage in template:
```{{ config.test }}```


Run migrations:
```
$ python manage.py migrate
```
Sync translation fields:
```
$ python manage.py sync_translation_fields
```

### Usage
```
# import config class instance
from site_config import config

# get config field value
print config.my_var

# set config field value
config.my_var = 'example'

# save updated config fields
config.save()

# reload config fields cache
config.reload()
```

### Template tags

To get config in template you should load 'site_config' tags and add 'get_site_config' template tag into your template. 
Examples:

```
{% load site_config %}

{% get_site_config as config %}

{{ config.my_var }}
```

### Requirements

App require this packages:

* django-modeltranslation
* beautifulsoup4
* django-prose-editor
