import json
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

    counter = 94
    for c in conns:
        # if c['start_pin'][:8] != '::Ex Out' or c['end_pin'][:7] != '::Ex In':
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
            # if not (isinstance(types[c['start_uuid']], int) and types[c['end_uuid']] == 'Branch_Node'):
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
    for n in nodes:
        if 'id' in n['metadata']:
            uuid_id[n['uuid']] = n['metadata']['id']
        elif 'value' in n['metadata']:
            if n['metadata']['value'] == True:
                uuid_id[n['uuid']] = 'true'
            elif n['metadata']['value'] == False:
                uuid_id[n['uuid']] = 'false'
            else:
                uuid_id[n['uuid']] = n['metadata']['value']
        else:
            uuid_id[n['uuid']] = n['name']

    print('types', uuid_id)

    links, link_conn = get_links(conns, uuid_id)

    Tree.printForest(links)
    exe, on_event = Tree.getRequestsData(uuid_id, links, link_conn)

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

        id, _ = map(str, on_event[i].split('.'))
        out['message']['id'] = id[2:]
        out['message']['event'] = on_event[i]
        out['message']['text'] = exe[i]

        outs.append(out)

        json_out = json.dumps(out)
        return json_out
