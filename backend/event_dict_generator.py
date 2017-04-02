import pickle
import eventful
import os
api = eventful.API(os.environ["EVENTFUL_ID"])
with open('../pickle_jar/shows_master_list.pkl', 'r') as f:
    shows_master_list = pickle.load(f)

###want app to import venues_dict###
###{venue: {show: [date, title, price, id]}}

def event_gen(venues_dict):
    venue_ids = []
    for k, v in venues_dict.iteritems():
        venue_ids.append(k)
    events_d = {}
    for i in venue_ids:
        for z in shows_master_list:
            if i == z[0]:
                event_listing = [x[1] for x in z[1]]
                dates, titles, prices, ids = [], [], [], []
                for event in event_listing:
                    e = api.call('events/get', id=event.encode('utf-8'))
                    dates.append(e['start_time'])
                    titles.append(e['title'])
                    prices.append(e['price'])
                    ids.append(event.encode('utf-8'))
                events_d[i] = sorted(set(zip(dates,titles,prices,ids)), key=lambda x: x[0])
    return events_d

if __name__ == '__main__':
    v_dict = {'Belly Up Aspen': 'V0-001-001496614-6',
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
    'The Fox Theatre': 'V0-001-000164037-2','1st Bank Center':'V0-001-000362189-4', 'Pepsi Center':'V0-001-000105138-3', 'Grizzly Rose Saloon and Dance Emporium':'V0-001-000268840-3', 'Swallow Hill Music Hall':'V0-001-001131295-5', 'Hi-Dive':'V0-001-000170025-8', 'Paramount Theatre':'V0-001-000198697-3'}
    shows_dict = event_gen(v_dict)
    with open('../pickle_jar/shows_dict.pkl', 'w') as f:
        pickle.dump(shows_dict, f)
