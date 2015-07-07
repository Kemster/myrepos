from pprint import pprint
import arrow
for p in resp['log']['entries']:
    if 'google-analytics' in p['request']['url']:
        url = p['request']['url']
        method = p['request']['method']
        started_date_time = p['startedDateTime']
        request_type = get_request_type(p)
        event_label = get_request_label(p)
        ga_account = get_request_account(p)
        hit_time = get_request_hit_time(p)
        res = {'startedDateTime': started_date_time,  'ga_account': ga_account, 'request_type': request_type, 'method': method, 'url': url, 'event_label': event_label, 'hit_time': hit_time}
        
        pprint(res)
        #pprint(p)
