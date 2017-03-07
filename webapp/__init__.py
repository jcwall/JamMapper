from flask import Flask, request, render_template
import cPickle as pickle
import os
import eventful
api = eventful.API(os.environ["EVENTFUL_ID"])
import datetime

with open('../pickle_jar/names_uris_lib.pkl') as f:
    uri_dict = pickle.load(f)
with open('../pickle_jar/uris_final_list.pkl') as f:
    events_list = pickle.load(f)
with open('../pickle_jar/uris_final_list2.pkl') as f:
    events_list2 = pickle.load(f)
with open('../pickle_jar/images2.pkl') as f:
    images = pickle.load(f)

events_list.extend(events_list2)

app = Flask(__name__)

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
            if rec_band in show[0]:
                shows.append((show[1].encode('utf-8'), venue[0], show[2]))
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
        shows = []
        rec_bands = get_bands(text)
        for rec in rec_bands:
             s = get_shows(str(rec.encode('utf-8')))
             shows.extend(s)
        shows = set(shows)
        titlelist = [show[0].encode('utf-8') for show in shows]
        venuelist = [show[1].encode('utf-8') for show in shows]
        idslist = [show[2].encode('utf-8') for show in shows]
        l = zip(titlelist, venuelist, idslist)

        return render_template('recs.html', shows=l)

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
    shows = []
    for venue in events_list:
        if venue[0] == v['name']:
            shows.extend(venue[1])
    events = [event[2] for event in shows]
    dates, titles, prices, ids = [], [], [], []
    for i, event in enumerate(events):
        e = api.call('events/get', id=event.encode('utf-8'))
        if e['title'] not in titles and e['start_time'] not in dates:
            dates.append(e['start_time'])
            titles.append(e['title'])
            prices.append(e['price'])
            ids.append(event.encode('utf-8'))
    dump = zip(dates,titles,prices,ids)
    dumps = sorted(set(dump), key=lambda x: x[0])
    return render_template('venues.html', name=v['name'], dump=dumps)


@app.route('/careers')
def careerspage():

    return render_template('careers.html')

if __name__ == "__main__":
    app.run(debug=True, threaded=True)
