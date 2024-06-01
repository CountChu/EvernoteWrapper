#
# FILENAME.
#       eve_util.py - Evernote Utility Python Module.
#
# FUNCTIONAL DESCRIPTION.
#       The module provides utility API.
#
# NOTICE.
#       Author: visualge@gmail.com (CountChu)
#       Created on 2024/4/7
#       Updated on 2024/4/9
#

import os
import hashlib
import binascii

import evernote.edam.type.ttypes as ttypes

from Count import cnt_util

def build_note(ew, nb, title, body, res_ls=None):
    content = ''
    content += '<?xml version="1.0" encoding="UTF-8"?>'
    content += '<!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">'
    content += '<en-note>'  
    content += body
    content += '</en-note>'          

    #
    # Create note_obj
    #

    note_obj = ttypes.Note()
    note_obj.title = title
    note_obj.content = content
    note_obj.notebookGuid = nb.guid
    if res_ls != None:
        note_obj.resources = res_ls

    createdNote = ew.note_store.createNote(note_obj)
    print("Successfully created a new note with GUID: ", createdNote.guid)

    return createdNote.guid

#
# Build viewLink
# evernote:///view/[userId]/[shardId]/[noteGuid]/[noteGuid]/
# evernote:///view/19792815/s172/640f0459-f271-a6f7-22fe-f02588dcf55b/48aa7d36-8a0d-4ba0-b85a-ff3591138f04/"
#    

def build_a_href(ew, nb_guid, guid, title):
    link = 'evernote:///view/%d/%s/%s/%s/' % (
        ew.user_info.userId, 
        ew.user_info.shardId,
        guid, 
        nb_guid)
    out = '<a href="%s">%s</a>' % (link, title)
    return out

def build_open_link(natives, dn, bn):
    out = ''
    out += '<div>'

    out += '<code><span style="font-size: 14px;">'    
    out += '%s' % bn
    out += '</span></code>'

    for native in natives:
        path = os.path.join(native['path'], dn, bn)    
        path = path.replace('%', '%25')

        if 'prefix' in native:
            path = native['prefix'] + path  
            
        out += ' [<a href="%s">%s</a>]' % (path, native['name'])      

    out += '</div>'
    return out

def build_open_link_2(natives, dn):
    out = ''

    for native in natives:
        path = os.path.join(native['path'], dn)    
        path = path.replace('%', '%25')

        if 'prefix' in native:
            path = native['prefix'] + path  
            
        out += ' [<a href="%s">%s</a>]' % (path, native['name'])      

    return out

def build_open_link_3(natives, title):
    out = ''

    out += '<div>'
    out += '<code><span style="font-size: 14px;">'
    
    #fileName = fileName.replace('&', '%26')
    out += title
    
    out += '</span></code>'

    for native in natives:
        url = native['path']
        #url = url.replace('&', '%26')
        out += '&nbsp;[<a href="%s">%s</a>]' % (url, native['name'])

    out += '</div>'

    return out

def _build_image(image_fn):
    f = open(image_fn, 'rb')
    image_data = f.read()
    f.close()

    md5 = hashlib.md5()
    md5.update(image_data)
    image_hash = md5.digest()

    image_hash_hex = binascii.hexlify(image_hash)
    image_hash_str = image_hash_hex.decode("UTF-8")

    data = ttypes.Data()
    data.size = len(image_data)
    data.bodyHash = image_hash
    data.body = image_data  

    image_resource = ttypes.Resource()
    image_resource.mime = "image/jpeg"
    image_resource.data = data
    image_resource.attributes = ttypes.ResourceAttributes(fileName=image_fn)    

    return image_resource, image_hash_str           

def build_image(fn, alt, width, resources):
    image_resource, image_hash_str = _build_image(fn)
    if width == None:
        out = f'<en-media type="image/jpeg" hash="{image_hash_str}" alt="{alt}"/>'
    else:
        out = f'<en-media type="image/jpeg" hash="{image_hash_str}" alt="{alt}"  width="%dpx"/>' % width

    resources.append(image_resource)
    return out

def update_res_fn(ew, res_fn, new_notes):

    #
    # If res_fn exists, delete the old note.
    #

    res = cnt_util.load_yaml(res_fn, {'generatedNotes': []})
    for note in res['generatedNotes']:
        ew.note_store.deleteNote(ew.auth_token, note['guid'])
        print(f'Successfully deleted the old note of GUID: {note["guid"]}')

    #
    # Save res_fn
    #

    res = {'generatedNotes': new_notes}
    cnt_util.save_yaml(res, res_fn)







