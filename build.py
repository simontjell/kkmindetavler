"""Bygger index.html og mindetavler-kbh.kml ud fra data/tavler.txt og data/coords.txt.
Kør: python3 build.py"""
import json, os, re
from xml.sax.saxutils import escape

W = os.path.dirname(os.path.abspath(__file__)) + '/'
coords = {}
for line in open(W + 'data/coords.txt', encoding='utf-8'):
    line = line.strip()
    if not line:
        continue
    p = line.split('|')
    lat, lon = p[1].split(',')
    coords[int(p[0])] = (float(lat), float(lon), len(p) > 2 and p[2] == '~')

locs = {}
order = []
n = 0
for line in open(W + 'data/tavler.txt', encoding='utf-8'):
    line = line.rstrip('\n')
    if not line:
        continue
    i, d, a, t, o = line.split('|')
    i = int(i)
    n += 1
    if i not in locs:
        lat, lon, approx = coords[i]
        locs[i] = {'d': d, 'a': a, 'lat': lat, 'lon': lon, 'x': 1 if approx else 0, 't': [], 'o': []}
        order.append(i)
    locs[i]['t'].append(t if a == locs[i]['a'] else a + ': ' + t)
    locs[i]['o'].append(o)

WAR = re.compile(r'besættelse|modstand|dræbt|faldt|faldet|frihedsk|Gestapo|Shellhuset|henrettet|skudt|194[0-5]', re.I)
data = []
for i in order:
    L = locs[i]
    L['w'] = 1 if all(WAR.search(t) for t in L['t']) else 0
    data.append(L)

print('tavler', n, 'steder', len(data), 'omtrentlige', sum(L['x'] for L in data), 'besættelse', sum(L['w'] for L in data))
bad = [L['a'] for L in data if not (55.60 < L['lat'] < 55.76 and 12.43 < L['lon'] < 12.67)]
print('uden for området:', bad)

tpl = open(W + 'template.html', encoding='utf-8').read()
out = tpl.replace('/*DATA*/', json.dumps(data, ensure_ascii=False, separators=(',', ':')))
out = out.replace('{{N}}', str(n)).replace('{{S}}', str(len(data)))
open(W + 'index.html', 'w', encoding='utf-8').write(out)

k = ['<?xml version="1.0" encoding="UTF-8"?>', '<kml xmlns="http://www.opengis.net/kml/2.2"><Document>',
     '<name>Mindetavler i København</name>',
     '<description>Kilde: Københavns Biblioteker, bibliotek.kk.dk/din/bag-om-kobenhavn/mindetavler</description>']
cur = None
for L in data:
    if L['d'] != cur:
        if cur is not None:
            k.append('</Folder>')
        cur = L['d']
        k.append('<Folder><name>%s</name>' % escape(cur))
    desc = '<br><br>'.join(escape(t) + ('<br><i>' + escape(o) + '</i>' if o else '') for t, o in zip(L['t'], L['o']))
    if L['x']:
        desc += '<br><i>Placering omtrentlig</i>'
    k.append('<Placemark><name>%s</name><description><![CDATA[%s]]></description><Point><coordinates>%s,%s</coordinates></Point></Placemark>'
             % (escape(L['a']), desc, L['lon'], L['lat']))
k.append('</Folder></Document></kml>')
open(W + 'mindetavler-kbh.kml', 'w', encoding='utf-8').write('\n'.join(k))
