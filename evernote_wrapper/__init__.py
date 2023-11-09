import logging

import urllib.request
import urllib.parse
import evernote.edam.type.ttypes as Types
import evernote.edam.notestore.ttypes as NoteStore
from evernote.api.client import EvernoteClient

import pdb 
br = pdb.set_trace

class EvernoteWrapper:

    def __init__(self):
        self.note_store = None
        self.user_info = None

    def connect(self, user_name, auth_token):

        #
        # Connect to Evernote
        #

        self.auth_token = auth_token
        client = EvernoteClient(token=auth_token, sandbox=False)

        #
        # Get note store.
        #

        self.note_store = client.get_note_store()

        #
        # Get user info.
        #

        user_store = client.get_user_store()
        self.user_info = user_store.getPublicUserInfo(user_name)
        logging.info('user_info = ')
        logging.info(self.user_info)
        logging.info('')
        logging.info('webApiUrlPrefix = %s' % self.user_info.webApiUrlPrefix)

    def get_tags(self, tagGuids):
        tags = []
        tag_names = self.get_tag_names(tagGuids)
        for name, guid in zip(tag_names, tagGuids):
            tag = {'guid': guid, 'name': name}
            tags.append(tag)
        return tags


    def get_tag_names(self, tag_guids):
        
        if tag_guids == None:
            return []

        tag_names = []
        for tag_guid in tag_guids:
            tag = self.note_store.getTag(self.auth_token, tag_guid)
            tag_names.append(tag.name)
            #logging.info('tag = %s' % tag)

        return tag_names

    def get_tag(self, tagName):
        tags = self.note_store.listTags()
        print("Found %d tags:" % len(tags))
        for tag in tags:
            if tag.name == tagName:
                return tag

        return None

    def get_notebook(self, notebook_name):
        nb_ls = self.note_store.listNotebooks()
        count = 0
        found_nb = None
        for nb in nb_ls:
            logging.info("%s - %s" % (nb.guid, nb.name))
            if nb.name == notebook_name:
                found_nb = nb
                count += 1
        assert count <= 1, count
        return found_nb
      
    def search_notes_by_notebook(self, notebook_name): 
        nb = self.get_notebook(notebook_name)

        if nb is None:
            print('Error: Not found the notebook %s' % nb.name)
            sys.exit(0)

        print ('Found the notebook: %s - %s' % (nb.guid, nb.name))
        logging.info(nb)
        logging.info('')

        #
        # List all notes in the notebook nb.
        #

        filter = NoteStore.NoteFilter()
        filter.notebookGuid = nb.guid

        note_meta_list = self.__findAllNotes(filter)

        return note_meta_list

    def search_notes_by_title(self, title):
        
        filter = NoteStore.NoteFilter()   
        filter.words = 'intitle:%s' % title

        note_meta_list = self.__findAllNotes(filter)

        return note_meta_list

    def search_notes_by_tag(self, tag):
        
        filter = NoteStore.NoteFilter()   
        #filter.words = 'tag:%s' % tag   # [BUGBUG] This way has limit of 128 results.
        filter.tagGuids = [tag]


        note_meta_list = self.__findAllNotes(filter)

        return note_meta_list        

    def search_notes_by_year(self, year):

        year_begin = year + '0101'
        year_end = year + '1231'
        
        filter = NoteStore.NoteFilter()   
        filter.words = 'created:%s -created:%s' % (year_begin, year_end)
        logging.info('words = %s' % filter.words)

        note_meta_list = self.__findAllNotes(filter)

        return note_meta_list

    def search_created_notes_by_date(self, yyyymmdd):        
        filter = NoteStore.NoteFilter()   
        filter.words = 'created:%s' % yyyymmdd
        logging.info('words = %s' % filter.words)

        note_meta_list = self.__findAllNotes(filter)

        return note_meta_list  

    def search_updated_notes_by_date(self, yyyymmdd):        
        filter = NoteStore.NoteFilter()   
        filter.words = 'updated:%s' % yyyymmdd
        logging.info('words = %s' % filter.words)

        note_meta_list = self.__findAllNotes(filter)

        return note_meta_list               

    def get_note_content(self, guid):
        content = self.note_store.getNoteContent(self.auth_token, guid)
        return content

    def get_note(self, guid):
        note = self.note_store.getNote(
                    self.auth_token, 
                    guid, 
                    True,               # withContent
                    False,              # withResourcesData
                    False,              # withResourcesRecognition
                    False)              # withResourcesAlternateData
        return note

    def get_note2(self, guid):
        note = self.note_store.getNote(
                    self.auth_token, 
                    guid, 
                    False, 
                    False, 
                    False, 
                    False)
        return note

    def update_note(self, note):
        self.note_store.updateNote(self.auth_token, note)

    def get_resource_url(self, resource):
        res_name = resource.attributes.fileName
        res_guid = resource.guid
        res_url = '%sres/%s' % (self.user_info.webApiUrlPrefix, res_guid)
        logging.info('res_url = %s' % res_url)
        return res_url

    def download_resource(self, url):
        data = {'auth': self.auth_token}
        data = urllib.parse.urlencode(data).encode('utf-8')

        req = urllib.request.Request(url, data)
        response = urllib.request.urlopen(req)
        data = response.read() 

        return data

    #
    # Private methods
    #    

    def __findAllNotes(self, filter):    

        spec = NoteStore.NotesMetadataResultSpec()
        spec.includeTitle = True
        spec.includeTagGuids = True
        spec.includeCreated = True   
        spec.includeUpdated = True
        spec.includeNotebookGuid = True

        max_notes = 100
        all_notes = []
        idx = 0
        for i in range(10000):
            offset = i * 100
            note_list = self.note_store.findNotesMetadata(
                self.auth_token, 
                filter, 
                offset, 
                max_notes, 
                spec)
            logging.info(
                '%d, %d, %d' % (offset, max_notes, len(note_list.notes)))
            if len(note_list.notes) == 0:
                break
            for note in note_list.notes:
                all_notes.append(note)
                idx += 1
        return all_notes
