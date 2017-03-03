import os
import eventful
api = eventful.API(os.environ["EVENTFUL_ID"])
import pickle
from venue_event_classes import Venue, Events

if __name__ == '__main__':
    shows_master_list = []
    venue_ids = {'1stbank':'V0-001-000362189-4', 'Pepsi Center':'V0-001-000105138-3', 'Grizzly Rose':'V0-001-000268840-3', 'Swallow Hill':'V0-001-001131295-5', 'Hi-dive':'V0-001-000170025-8', 'Paramount Theatre':'V0-001-000198697-3'}
    for venue, i in venue_ids.iteritems():
        e = Events(i)
        shows_master_list.append((venue, e.get_events()))

    #******saved as shows_master_list.txt
# ['Belly Up', 'Beta', 'Boulder Theater', 'Cervantes Masterpiece Ballroom', "Jazz @ Jack's", 'Larimer Lounge', 'Macky Auditorium', 'Ogden Theatre', "Ophelia's Electric Soapbox", 'Red Rocks Amphitheatre', 'The Bluebird Theater', 'The Fillmore Auditorium', 'The Fox Theatre', 'Dazzle Restaurant & Lounge']



#1st bank 'V0-001-000362189-4'
#pepsi center 'V0-001-000105138-3'
#grizzlyrose 'V0-001-000268840-3'
#swallow hill
    #'V0-001-007281175-8'
    #'V0-001-008371841-1'
    # 'V0-001-001131295-5'
    # 'V0-001-005738721-2'
    # 'V0-001-005629643-6'
#hidive
    # 'V0-001-000170025-8'
    # 'V0-001-007238256-6'
#paramount
    #'V0-001-001908397-0'
    # 'V0-001-000198697-3'
    # 'V0-001-010733387-9'
