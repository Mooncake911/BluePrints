import json
import os
from tree import *



def json_string_to_file(json_string, file_path):
    try:
        # Parse the JSON string into a Python object
        json_data = json.loads(json_string)
        
        # Write the Python object to a JSON file
        with open(file_path, 'w') as json_file:
            json.dump(json_data, json_file, indent=4)
            
        print("JSON file created successfully.")
    except Exception as e:
        print(f"Error: {e}")


def read_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            json_data = json.load(file)
            return json_data
    except FileNotFoundError:
        print("File not found.")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None
    

def get_links(conns):
    links = []
    alph_uuid = {}
    link_conn = {}

    counter = 97
    for i in range(len(conns)):
        if conns[i]['start_pin'][:8] != '::Ex Out' or conns[i]['end_pin'][:7] != '::Ex In':
            if conns[i]['start_uuid'] not in alph_uuid:
                alph_uuid[conns[i]['start_uuid']] = chr(counter)
                counter += 1
            if conns[i]['end_uuid'] not in alph_uuid:
                alph_uuid[conns[i]['end_uuid']] = chr(counter)
                counter += 1

            link_str = alph_uuid[conns[i]['end_uuid']] + ' ' + alph_uuid[conns[i]['start_uuid']]
            if link_str not in links:
                links.append(link_str)
                link_conn[link_str] = conns[i]
            elif not conns[i]['start_pin'][:2] == "::" or not conns[i]['end_pin'][:2] == "::":
                link_conn[link_str] = conns[i]
    
    return links, link_conn


def test(test):
    json_data = read_json_file(f'projects/test{test}/test{test}.json')

    nodes = json_data['nodes']
    conns = json_data['connections']

    uuid_id = {}
    for i in range(len(nodes)):
        if 'id' in nodes[i]['metadata']:
            uuid_id[nodes[i]['uuid']] = nodes[i]['metadata']['id']
        elif 'value' in nodes[i]['metadata']:
            if nodes[i]['metadata']['value']:
                uuid_id[nodes[i]['uuid']] = 'true'
            else:
                uuid_id[nodes[i]['uuid']] = 'false'
        else:
            uuid_id[nodes[i]['uuid']] = nodes[i]['name']

    print('types', uuid_id)
    
    links, link_conn = get_links(conns)

    Tree.printForest(links)
    exe, on_event = Tree.getRequestsData(uuid_id, links, link_conn)

    id = 1
    #for i in range(len(exe)):
        
    
    out = {}
    out['id'] = id
    out['commands'] = []

    for i in range(len(exe)):
        out['commands'].append({
            'on_event': on_event[i],
            'exe': exe[i]
        })

    json_out = json.dumps(out)
    json_string_to_file(json_out, f'test{test}_exit.json')
    

test(0)
test(1)
test(2)
test(3)
test(4)















