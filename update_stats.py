import json
import urllib.request
from pathlib import Path
from datetime import datetime, timezone

URL = 'https://api.pota.app/stats/user/TA1CCM'
req = urllib.request.Request(URL, headers={'User-Agent': 'TA1CCM-Stats-Dashboard/1.0', 'Accept': 'application/json'})
with urllib.request.urlopen(req, timeout=30) as response:
    data = json.load(response)
if data.get('callsign', '').upper() != 'TA1CCM':
    raise ValueError('Unexpected callsign from POTA API')
for key in ('activator', 'hunter'):
    if not isinstance(data.get(key), dict):
        raise ValueError(f'Missing {key} statistics')
output = {
    'callsign': 'TA1CCM',
    'updated_utc': datetime.now(timezone.utc).isoformat(timespec='seconds'),
    'activator': {k: data['activator'].get(k, 0) for k in ('activations', 'parks', 'qsos')},
    'attempts': {k: data.get('attempts', {}).get(k, 0) for k in ('activations', 'parks', 'qsos')},
    'hunter': {k: data['hunter'].get(k, 0) for k in ('parks', 'qsos')},
    'awards': data.get('awards', 0),
    'endorsements': data.get('endorsements', 0),
}
Path('stats.json').write_text(json.dumps(output, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('Updated POTA statistics:', output['activator'])
