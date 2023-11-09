# EvernoteWrapper
The project provides a wrapper for Evernote SDK.

## Install the package
```
[PyTemplates/BuildPackage/package1]
$ pip install .
```

## Install the package to be editable
```
[EvernoteWrapper]
$ pip install -e .
```

## Usage
```
$ python test.py
```

## API
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
	def get_note_content(self, guid):
	def get_note(self, guid):	
	def get_note2(self, guid):	
	def update_note(self, note):	
	def get_resource_url(self, resource):	
	def download_resource(self, url):
```
