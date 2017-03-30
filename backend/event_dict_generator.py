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
