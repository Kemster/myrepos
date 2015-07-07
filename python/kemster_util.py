from pprint import pprint
import arrow
import re
import json


def get_request_type(json):
    
    try:
        request = json['request']
        querystring = request['queryString']
        for t in querystring:
            if t['name'] == u't':
                return t['value']
            if t['name'] == u'utmt':
                return t['value']
            if t['name'] == u'utmp':
                return t['value']
            
        return 'Not found'
    except KeyError:
        return 'N/A'
    
def get_request_account(json):
    
    try:
        request = json['request']
        querystring = request['queryString']
        for t in querystring:
            if t['name'] == u'utmac':
                return t['value']
            if t['name'] == u'tid':
                return t['value']
            
        return 'Not found'
    except KeyError:
        return 'N/A'
    
def get_request_hit_time(json):
    
    try:
        request = json['request']
        querystring = request['queryString']
        for t in querystring:
            if t['name'] == u'utmht':
                return t['value']
            
        return 'Not found'
    except KeyError:
        return 'N/A'
    
def get_request_label(json):
    
    try:
        for t in json['request']['queryString']:
            if t['name'] == u'utme':
                return t['value']
            
        return 'Not found'
    except KeyError:
        return 'N/A'

def parse_har_file(har, pattern):
    '''
        returns parsed har file for Beamly GA accounts
            [{'<account_num>: 'UA123456-2', 'account_name': 'Beamly Insight GA', 'data': []},
            {'<account_num>: 'UA9876543-1', 'account_name': 'Beamly Reach GA', 'data': []}]
    '''

    result = []
    for p in har['log']['entries']:
        if 'google-analytics' in p['request']['url']:
            if exclude_request(p):
                # check exclusion list to see if we want to process this google-analytics request
                continue
            ga_account = get_request_account(p)
            if ga_account not in ['UA-26141997-1']:
                print 'Excluding request for GA account {0}'.format(ga_account)
                continue
                
            url = p['request']['url']
            method = p['request']['method']
            started_date_time = p['startedDateTime']
            request_type = get_request_type(p)
            event_label = get_request_label(p)
            event_data = parse_event_label(event_label)
            hit_time = get_request_hit_time(p)
            res = {'startedDateTime': started_date_time,  'ga_account': ga_account, 'request_type': request_type, 'method': method, 
                    'hit_time': hit_time}
            res.update(event_data)
            result.append(res)
    return result



def exclude_request(har_record):
    if 'url' in har_record['request'].keys():
        url = har_record['request']['url']
        if url.endswith('/ga.js') or url.endswith('/analytics.js') or url.endswith('.com/p/__utm.gif'):
            print 'Excluding {0}'.format(url)
            return True

    return False

def get_event_label_details(event_label):
    '''
    '''
    el_dict = {}
    if 'id' in event_label.keys(): el_dict.update({'id':event_label['id'] })
    if 'ityp' in event_label.keys(): el_dict.update({'ityp':event_label['ityp']})
    if 'loc' in event_label.keys(): el_dict.update({'loc':event_label['loc']} )
    if 'zt' in event_label.keys(): el_dict.update({'zt':event_label['zt']} )
    if 'tvc' in event_label.keys(): el_dict.update({'tvc':event_label['tvc']} )
    if 'typ' in event_label.keys(): el_dict.update({'typ':event_label['typ']} )
    if 'ft' in event_label.keys(): el_dict.update({'ft':event_label['ft']} )
    if 'token' in event_label.keys(): el_dict.update({'token':event_label['token']} )
    if 'parent' in event_label.keys(): el_dict.update({'parent':event_label['parent']} )
    #if 'url' in event_label.keys(): el_dict.update({'url':event_label['url']} )
    if 'val' in event_label.keys(): el_dict.update({'val':event_label['val']} )
    if 'action' in event_label.keys(): el_dict.update({'action':event_label['action']} )
    if 'platforms' in event_label.keys(): el_dict.update({'platforms':event_label['platforms']})
    if 'entity_id' in event_label.keys(): el_dict.update({'entity_id':event_label['entity_id']})       
        
    return el_dict
 


def parse_event_label(event_label):
    if len(event_label)== 0 or event_label == 'Not found' : return {}
    
    split = re.split('\(([^)]+)\)', event_label)
    cust_vars = [[],[],[]]
    result = {}
    for i in split:
        if len(i) > 8:
            if i.find('{')> 0 and i.find('}')> 0:
                el_json =  i[i.find('{'):i.rfind('}')+ 1]
                event_category = i[0:i.find('{')].split('*')[0]
                event_action = i[0:i.find('{')].split('*')[1]
                result.update({'event_category': event_category, 'event_action': event_action, 'event_action': event_action, 'json': el_json})
            else:
                counter = 0
                data = i.split('*')
                for j in data:
                    cust_vars[counter].append(data[counter])
                    counter += 1
    for cv in cust_vars:
        result.update({cv[0]: cv[1]})

        
    if 'json' in result.keys():
        json_el = json.loads(result['json'])
        result.pop('json')
        if 'items' in json_el.keys():
            # then we have an array of event label data
            el_items = []
            for i in json_el['items']:
                el_items.append(get_event_label_details(i))
            
            
            if len(el_items) > 1:
                result.update({'items': el_items})
            elif len(el_items) == 1:
                result.update(el_items[0])
            
            json_el.pop('items')
        result.update(get_event_label_details(json_el))
    return result

    
