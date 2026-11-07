"""Refresh public-only metrics. Network/API failures leave committed assets intact."""
import argparse
from collections import Counter
from datetime import datetime, timezone
import json
import os
from pathlib import Path
from urllib.request import Request, urlopen
from visuals import panel, text, OUT

ROOT = Path(__file__).resolve().parents[1]
USER = 'abhisheksureshnair'

def fetch(path):
    headers = {'Accept': 'application/vnd.github+json', 'User-Agent': 'shadow-monarch-profile', 'X-GitHub-Api-Version': '2022-11-28'}
    if os.getenv('GH_TOKEN'):
        headers['Authorization'] = 'Bearer ' + os.environ['GH_TOKEN']
    with urlopen(Request('https://api.github.com/' + path, headers=headers), timeout=30) as response:
        return json.load(response)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--fixture-dir', type=Path, help='Directory containing public API responses for offline regeneration')
    parser.add_argument('--render', action='store_true', help='Rebuild visuals without changing the timestamp if values are unchanged')
    args = parser.parse_args()
    if args.fixture_dir:
        repos = json.loads((args.fixture_dir / 'profile-repos.json').read_text())
        events = json.loads((args.fixture_dir / 'profile-events.json').read_text())
    else:
        repos = []
        page = 1
        while True:
            batch = fetch(f'users/{USER}/repos?type=owner&per_page=100&page={page}')
            if not isinstance(batch, list):
                raise ValueError('Repository API did not return a list')
            repos.extend(batch)
            if len(batch) < 100:
                break
            page += 1
        events = fetch(f'users/{USER}/events/public?per_page=100')
    if not isinstance(repos, list) or not isinstance(events, list):
        raise ValueError('Invalid API response; existing snapshot retained')
    repos = [r for r in repos if not r['private'] and r['owner']['login'].lower() == USER]
    original = [r for r in repos if not r['fork']]
    langs = Counter(r['language'] for r in original if r.get('language'))
    stars = sum(r['stargazers_count'] for r in original)
    latest = max((e['created_at'] for e in events if e.get('public')), default=None)
    values = {'public_repositories':len(repos),'non_fork_repositories':len(original),'stars_on_non_forks':stars,'primary_languages':dict(langs),'latest_returned_public_event':latest}
    previous_path = OUT / 'activity.json'
    previous = json.loads(previous_path.read_text()) if previous_path.exists() else {}
    unchanged = all(previous.get(key) == value for key,value in values.items())
    if unchanged and not args.render:
        print('Public metrics unchanged; retaining snapshot and timestamp.')
        return
    timestamp = previous['snapshot_timestamp_utc'] if unchanged else datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    date = timestamp[:10]
    body = text(32, 42, '05 / GITHUB SNAPSHOT', 18, '#22D3EE', 700) + text(32, 76, f'{date} UTC • Public API data', 18)
    for x, value, label in [(32,len(repos),'PUBLIC REPOSITORIES'),(345,stars,'STARS / NON-FORK REPOS')]:
        body += text(x, 142, value, 48, '#F8FAFC', 700) + text(x, 174, label, 15)
    body += text(32, 225, 'PRIMARY LANGUAGES / NON-FORK REPOSITORIES', 16, '#22D3EE', 700)
    for i,(lang,count) in enumerate(langs.most_common(5)):
        body += text(32, 263+i*32, f'{lang}  /  {count}', 20, '#F8FAFC')
        body += f'<rect x="290" y="{249+i*32}" width="{max(4,count/max(langs.values())*560)}" height="12" rx="6" fill="#7C3AED"/>'
    bottom = 290 + min(5,len(langs))*32
    body += text(32,bottom, f'Latest returned public event: {latest[:10] if latest else "none available"}',18)
    body += text(32,bottom+30,'Snapshot, not live telemetry. Full scope and source links below.',16)
    # All data is collected and validated before any output changes.
    panel('activity',body,920,bottom+58,'Dated public GitHub repository and activity snapshot')
    mobile=text(24,36,'05 / GITHUB SNAPSHOT',17,'#22D3EE',700)+text(24,68,f'{date} UTC',18)
    mobile+=text(24,114,f'{len(repos)} public repositories',27,'#F8FAFC',700)+text(24,153,f'{stars} stars on non-fork repositories',20)
    mobile+=text(24,202,'PRIMARY LANGUAGES / REPO COUNT',15,'#22D3EE',700)
    for i,(lang,count) in enumerate(langs.most_common(5)):
        mobile+=text(24,238+i*32,f'{lang} / {count}',20,'#F8FAFC')
    y=262+min(5,len(langs))*32
    mobile+=text(24,y,'Latest returned public event:',17)+text(24,y+28,latest[:10] if latest else 'None available',20,'#F8FAFC')
    panel('activity-mobile',mobile,440,y+52,'Dated public GitHub snapshot')
    for slug,value,label,scope in [('repositories',len(repos),'PUBLIC REPOSITORIES','Owned / including forks'),('stars',stars,'GITHUB STARS','Owned public non-forks'),('projects',len(original),'NON-FORK REPOSITORIES','Owned / public only')]:
        tile=text(22,38,label,14,'#22D3EE',700)+text(22,103,value,48,'#F8FAFC',700)+text(22,137,scope,16)+text(22,163,date+' UTC',14)
        panel(slug,tile,300,185,label+' — dated public API snapshot')
    data = {'snapshot_date_utc':date,'snapshot_timestamp_utc':timestamp,**values}
    (OUT/'activity.json').write_text(json.dumps(data,indent=2)+'\n')
    lines = [f'# GitHub snapshot — {date} UTC', '', f'Last changed snapshot: **{timestamp}**. Daily checks with unchanged values do not modify files or this timestamp.', '', f'- Public owned repositories: **{len(repos)}** (including forks).',f'- Non-fork public repositories: **{len(original)}**.',f'- Stars received by those non-fork repositories: **{stars}**.',f'- Latest event returned by the public events API: **{latest or "none available"}**.','', '## Primary languages', '', 'Counts of non-fork repositories by GitHub’s primary-language field. Repositories with no language are excluded; this is not a byte share, skill rating or professional experience measure.','']
    lines += [f'- {lang}: {count}' for lang,count in langs.most_common()]
    lines += ['', '## Sources and limits', '', f'[Public repositories API](https://api.github.com/users/{USER}/repos?type=owner&per_page=100) · [Public events API](https://api.github.com/users/{USER}/events/public?per_page=100)', '', 'Repository results are paginated. Events are a limited recent feed, not complete contribution history. Private work, commit totals and streaks are not counted. No synthetic heatmap is displayed. A failed refresh keeps the last successful dated snapshot. The workflow may be delayed or disabled by GitHub.','']
    (ROOT/'docs'/'activity.md').write_text('\n'.join(lines))

if __name__ == '__main__':
    main()
