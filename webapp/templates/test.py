from flask import Flask, request, render_template
import cPickle as pickle
#from .JamMapper.venue_event_classes import Venue, Events
with open('../../pickle_jar/names_uris_lib.pkl') as f:
    uri_dict = pickle.load(f)

with open('../../pickle_jar/uris_final_list.pkl') as f:
    events_list = pickle.load(f)

with open('../../pickle_jar/uris_final_list2.pkl') as f:
    events_list2 = pickle.load(f)

events_list.extend(events_list2)
# app = Flask(__name__)

def get_bands(text):
    bands = []
    try:
        for i in uri_dict[text][0]:
            bands.append(i)
    except (KeyError):
        print 'pick a better name'
    return bands

def get_shows(rec_band, events_list=events_list):
    shows = []
    for venue in events_list:
        for show in venue[1]:
            if [rec_band] in show[0]:
                shows.append((show[1].encode('utf-8'), venue[0]))
    return list(set(shows))

def recpage():
    error = False
    try:
        text = str(request.form['user_input'])
    except:
        error = True
    if error:
        return render_template('recs.html')
    else:
        shows = []
        rec_bands = get_bands(text)
        for rec in rec_bands:
             s = get_shows(rec)
             shows.extend(s)

        return render_template('recs.html', shows=shows[0], venues=shows[1])

if __name__ == '__main__':
    text = 'Red Hot Chili Peppers'
