from flask import Flask, request, render_template
import cPickle as pickle
import os
import eventful
api = eventful.API(os.environ["EVENTFUL_ID"])
import datetime
from fuzzywuzzy import fuzz, process

with open('../pickle_jar/names_uris_lib.pkl') as f:
    uri_dict = pickle.load(f)
with open('../pickle_jar/uris_master_list1.pkl') as f:
    events_list = pickle.load(f)
with open('../pickle_jar/shows_dict.pkl', 'r') as f:
    shows_dict = pickle.load(f)
with open('../pickle_jar/images2.pkl') as f:
    images = pickle.load(f)
choices = uri_dict.keys()
# events_list.extend(events_list2)

app = Flask(__name__)

def get_bands(text):
    band = process.extract(text, choices, limit=1)[0][0]
    return uri_dict[band], band

def get_shows(rec_band, events_list=events_list):
    shows = []
    for venue in events_list:
        for show in venue[1]:
            year, month, day = (int(d) for d in show[3][:10].split('-'))
            time = datetime.datetime(year, month, day, 23)
            if rec_band in show[0] and time > datetime.datetime.now():
                shows.append((show[1], venue[0], show[2], show[3]))
    return list(set(shows))

@app.route('/')
def homepage():

    return render_template('main.html')

@app.route('/about')
def aboutpage():

    return render_template('about.html')

@app.route('/contact')
def contactpage():

    return render_template('contact.html')

@app.route('/recs', methods=['GET','POST'])
def recpage():
    error = False
    try:
        text = str(request.form['user_input'].encode('utf-8'))
    except:
        error = True
    if error:
        return render_template('recs.html')
    else:
        try:
            shows = []
            rec_bands, band = get_bands(text)
            for rec in rec_bands:
                 s = get_shows(str(rec.encode('utf-8')))
                 shows.extend(s)
            shows = set(shows)
            titlelist = [show[0].encode('utf-8') for show in shows]
            venuelist = [show[1].encode('utf-8') for show in shows]
            idslist = [show[2].encode('utf-8') for show in shows]
            datelist = [show[3].encode('utf-8') for show in shows]
            l = sorted(zip(titlelist, venuelist, idslist, datelist), key = lambda x: x[3])
            return render_template('recs.html', shows=l, band=band)
        except:
            band = (text)
            return render_template('recs.html', band=band)

@app.route('/recs/event/<activity_id>', methods=['GET', 'POST'])
def eventpage(activity_id):
    event = api.call('events/get', id=activity_id.encode('utf-8'))
    start=event['start_time']
    year, month, day = (int(d) for d in start[:10].split('-'))
    weekday = datetime.date(year, month, day)
    time, date = start[10:], start[:10]
    return render_template('event.html', title=event['title'], address=event['address'], venue=event['venue_name'], city=event['city'], region=event['region'], time=time, weekday=weekday.strftime("%A"), date=date, start=event['start_time'], venue_id=event['venue_id'], price=event['price'], photo=images[event['venue_id']])

@app.route('/venues/<activity_id>', methods=['GET', 'POST'])
def venuepage(activity_id):
    v = api.call('venues/get', id=activity_id.encode('utf-8'))
    dumps = shows_dict[v['name']]
    return render_template('venues.html', name=v['name'], dump=dumps)


@app.route('/careers')
def careerspage():

    return render_template('careers.html')

if __name__ == "__main__":
    app.run(debug=True, threaded=True)
