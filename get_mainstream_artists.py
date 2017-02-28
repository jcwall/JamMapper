import requests

def get_uris(artistname):
    url = 'https://api.spotify.com/v1/search?q={}&type=artist'.format(artistname)
    res = requests.get(url)
    #return res['artists']['items'][0]['uri'].encode('utf-8')
    return res.json()['artists']['items'][0]['uri'].encode('utf-8')
if __name__ == '__main__':
    res_list = []
    mainstream = ['daft+punk', 'beyonce', 'the+beatles', 'kendrick+lamar', 'radiohead', 'luke+bryan']
    for i in mainstream:
        res_list.append(get_uris(i))
