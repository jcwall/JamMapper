import os
import eventful
api = eventful.API(os.environ["EVENTFUL_ID"])
import pickle

class Venue():
    def __init__(self, venue):
        self.name = venue['name']
        self.address = venue['address']
        self.city = venue['city_name']
        self.zip = venue['postal_code']
        self.id = venue['id']
        self.lat = venue['latitude']
        self.long = venue['longitude']
        self.url = venue['url']

class Events():
    def __init__(self, venueid):
        self.id = venueid
    def get_events(self):
        events = api.call('events/search', l=self.id)
        pages = int(events['page_count'])
        shows = []
        print self.id, '-----------'
        #print 'this venue has {} pages of events'.format(pages)
        for p in range(1, pages+1):
            page = api.call('events/search', l=self.id, page_number=p)
            for i in page['events']['event']:
                #shows[i['title']] = i['id']
                shows.append((i['title'].encode('utf-8'), i['id']))
        return shows

if __name__ == '__main__':
    names_ids_dict = {'Belly Up': 'V0-001-001496614-6',
    'Beta': 'V0-001-000216537-3',
    'Boulder Theater': 'V0-001-001461242-1',
    'Cervantes Masterpiece Ballroom': 'V0-001-000458762-1',
    'Dazzle Restaurant & Lounge': 'V0-001-000339274-3',
    "Jazz @ Jack's": 'V0-001-000212352-6',
    'Larimer Lounge': 'V0-001-001711423-0',
    'Macky Auditorium': 'V0-001-001224313-9',
    'Ogden Theatre': 'V0-001-001154846-2',
    "Ophelia's Electric Soapbox": 'V0-001-008853052-6',
    'Red Rocks Amphitheatre': 'V0-001-001417416-1',
    'The Bluebird Theater': 'V0-001-001524792-3',
    'The Fillmore Auditorium': 'V0-001-001308294-2',
    'The Fox Theatre': 'V0-001-000164037-2','1stbank':'V0-001-000362189-4', 'Pepsi Center':'V0-001-000105138-3', 'Grizzly Rose':'V0-001-000268840-3', 'Swallow Hill':'V0-001-001131295-5', 'Hi-dive':'V0-001-000170025-8', 'Paramount Theatre':'V0-001-000198697-3'}
    shows_master_list = []
    for venue, i in names_ids_dict.iteritems():
        e = Events(i)
        shows_master_list.append((venue, e.get_events()))
    with open('../pickle_jar/shows_master_list.pkl', 'w') as f:
        pickle.dump(shows_master_list, f)
    with open('../pickle_jar/venues_dict.pkl', 'w') as f:
        pickle.dump(names_ids_dict, f)
