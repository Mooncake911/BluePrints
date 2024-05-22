import json
import os
from .tree import *


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


def get_links(conns, types):
    links = []
    alph_uuid = {}
    link_conn = {}

    counter = 97
    for c in conns:
        if c['start_uuid'] not in alph_uuid:
            alph_uuid[c['start_uuid']] = chr(counter)
            counter += 1
        if c['end_uuid'] not in alph_uuid:
            alph_uuid[c['end_uuid']] = chr(counter)
            counter += 1

        if isinstance(types[c['start_uuid']], int) and types[c['end_uuid']] == 'Branch_Node' and \
                c['start_pin'][:2] == "::" and c['end_pin'][:2] == "::":
            continue
        else:
            link_str = alph_uuid[c['end_uuid']] + ' ' + alph_uuid[c['start_uuid']]
            if link_str not in links:
                links.append(link_str)
                link_conn[link_str] = c
            elif not c['start_pin'][:2] == "::" or not c['end_pin'][:2] == "::":
                link_conn[link_str] = c

    return links, link_conn


def test(json_data):
    nodes = json_data['nodes']
    conns = json_data['connections']

    uuid_id = {}
    timer_indexes = {}
    for n in nodes:
        if n['name'][:5] == 'Timer':
            timer_indexes[n['uuid']] = n['metadata']['index']

        if 'id' in n['metadata']:
            uuid_id[n['uuid']] = n['metadata']['id']
        elif 'value' in n['metadata']:
            if n['metadata']['value'] == 'True':
                uuid_id[n['uuid']] = 'true'
            elif n['metadata']['value'] == 'False':
                uuid_id[n['uuid']] = 'false'
            else:
                uuid_id[n['uuid']] = n['metadata']['value']
        else:
            uuid_id[n['uuid']] = n['name']

    print('types', uuid_id)

    links, link_conn = get_links(conns, uuid_id)

    Tree.printForest(links)
    exe, on_event, ids = Tree.getRequestsData(uuid_id, links, link_conn, timer_indexes)

    outs = []
    for i in range(len(exe)):
        out = {'type': 'config',
               'message':
                   {
                       'id': 1,
                       'event': '',
                       'text': ''
                   }
               }

        if len(ids) == 0:
            id, _ = map(str, on_event[i].split('.'))
            id = int(id[2:])
        else:
            id = ids[i]

        out['message']['id'] = id
        out['message']['event'] = on_event[i]
        out['message']['text'] = exe[i]

        outs.append(json.dumps(out, ensure_ascii=False))

        # json_out = json.dumps(out)
        # json_string_to_file(json_out, f'test{test}.{i}_exit.json')

    return outs
