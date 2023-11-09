import datetime
import pdb

from evernote_wrapper import EvernoteWrapper

def main():

    #
    # Create an Evernote Wrapper object
    #

    ew = EvernoteWrapper()

    #
    # Specify user name and token for the Evernote.
    #

    user_name = 'Your name'
    auth_token = "Your token"
    
    #
    # Connect Evernote service
    #

    ew.connect(user_name, auth_token)

    #
    # Search notebook "C1 - Auto"
    #
    
    nb = ew.get_notebook("C1 - Auto")

    #
    # Search nodes by created date.
    #

    note_meta_list = ew.search_created_notes_by_date('20220719')
    for note_meta in note_meta_list:
        created = note_meta.created // 1000
        created_dt = datetime.datetime.fromtimestamp(created)
        created_str = created_dt.strftime("%Y/%m/%d %H:%M")
        print("%s: [%s]" % (created_dt, note_meta.title))

if __name__ == '__main__':
    main()