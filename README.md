# EvernoteWrapper
The project provides a wrapper for Evernote SDK.

# Dependency
The project depends on [CountPackage](https://github.com/CountChu/CountPackage).

# Installation
## Install the package
[EvernoteWrapper]

```
$ pip install .
```

## Install the package to be editable
[EvernoteWrapper]
```
$ pip install -e .
```

## Usage
```
$ python test.py
```

## API

`eve_util.py`
``` python
def build_note(ew, nb, title, body, res_ls=None):
def build_a_href(ew, nb_guid, guid, title):
def build_open_link(natives, dn, bn):
def build_open_link_2(natives, dn):
def build_open_link_3(natives, title):
def build_image(fn, alt, width, resources):
def update_res_fn(ew, res_fn, new_notes):
```


`__init__.py`

``` python
class EvernoteWrapper:
	def __init__(self):
	def connect(self, user_name, auth_token):
	def get_tags(self, tagGuids):
	def get_tag_names(self, tag_guids):
	def get_tag(self, tagName):
	def get_notebook(self, notebook_name):	
	def search_notes_by_notebook(self, notebook_name): 	
	def search_notes_by_title(self, title):	
	def search_notes_by_tag(self, tag):
	def search_notes_by_year(self, year):	
	def search_created_notes_by_date(self, yyyymmdd):     
	def search_updated_notes_by_date(self, yyyymmdd):  
	def search_updated_notes_within_days(self, days):
	def get_note_content(self, guid):
	def get_note(self, guid):	
	def get_note2(self, guid):	
	def check_note_exists(self, guid):
	def update_note(self, note):	
	def get_resource_url(self, resource):	
	def download_resource(self, url):
```
