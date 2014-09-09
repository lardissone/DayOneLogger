import os
import sys

def get_icloud_path():
    mobile_docs = os.path.expanduser('~/Library/Mobile Documents')
    dayone_path = [s for s in os.listdir(mobile_docs) if 'dayoneapp' in s]

    if not dayone_path:
        print 'Error: Day One not syncing to iCloud'
        sys.exit()

    return '%s/%s/Documents/Journal_dayone/entries/' % (
        mobile_docs,
        dayone_path[0])

def get_dropbox_path():
    return os.path.expanduser('~/Dropbox/Apps/Day One/Journal.dayone/entries')
