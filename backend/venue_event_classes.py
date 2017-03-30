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

def venue_data():
    den_venues_list = ['bluebird+theatre', 'ogden+theatre', 'beta', 'larimer', 'paramount+theatre', 'jacks', 'boulder+theater', 'macky+auditorium', 'fillmore+auditorium', 'ophelia', 'cervantes']
    names = {}
    for v in den_venues_list:
        venues = api.call('venues/search', q=v, l='denver')
        for i in venues['venues']['venue']:
            v = Venue(i)
            names[v.name] = v.id
    names['Belly Up'] = (api.call('venues/search', q='belly+up+aspen')['venues']['venue']['id'])
    names['Dazzle Restaurant & Lounge'] = (api.call('venues/search', q='dazzle+restaurant', l='denver'))['venues']['venue']['id']
    names['Gothic Theatre'] = (api.call('venues/search', q='gothic', l='denver'))['venues']['venue']['id']
    names['Red Rocks Amphitheatre'] = (api.call('venues/search', q='red+rocks+amphitheatre'))['venues']['venue']['id']
    boulder_list = ['fox', 'summit']
    for v in boulder_list:
        venues = api.call('venues/search', q=v, l='boulder')
        for i in venues['venues']['venue']:
            v = Venue(i)
            names[v.name] = v.id
    venue_names = ['Belly Up', 'Beta', 'Boulder Theater', 'Cervantes Masterpiece Ballroom', "Jazz @ Jack's", 'Larimer Lounge', 'Macky Auditorium', 'Ogden Theatre', "Ophelia's Electric Soapbox", 'Red Rocks Amphitheatre', 'The Bluebird Theater', 'The Fillmore Auditorium', 'The Fox Theatre', 'Dazzle Restaurant & Lounge']
    final = {k: names[k] for k in set(venue_names) & set(names.keys())}
    return final

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
    # venues_count = int(api.call('/venues/search', q='music', l='denver')['page_count'])
    names_ids_dict = venue_data()
    # shows_master_list = []
    # for venue, i in names_ids_dict.iteritems():
    #     v = Events(i)
    #     shows_master_list.append((venue, v.get_events()))
    # with open('shows_master_list.txt', 'w') as f:
    #     pickle.dump(shows_master_list, f)

    ##--- VENUES TO ADD: 1stbank center, paramount theatre, swallow hill music, grizzly rose, hi-dive, mishawaka, pepsi center
