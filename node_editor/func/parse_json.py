import json
from .tree import Tree


def write_json_file(data, file_path) -> None:
    try:
        with open(file_path, 'w', encoding="utf-8") as json_file:
            json.dump(data, json_file, indent=4, ensure_ascii=False)
        print("JSON file created successfully.")
    except Exception as e:
        print(f"Error: {e}")


def read_json_file(file_path) -> dict:
    try:
        with open(file_path, 'r', encoding="utf-8") as file:
            json_data = json.load(file)
            return json_data
    except FileNotFoundError as e:
        print(f"File not found: {e}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")


def get_links(connections):
    links = []
    alph_uuid = {}
    link_conn = {}

    counter = 97  # char(97) = a

    for c in connections:
        if c['start_pin'][:2] != '::' or c['end_pin'][:2] != '::':
            for uuid in [c['start_uuid'], c['end_uuid']]:
                if uuid not in alph_uuid:
                    alph_uuid[uuid] = chr(counter)
                    counter += 1

            link_str = alph_uuid[c['end_uuid']] + ' ' + alph_uuid[c['start_uuid']]
            if link_str not in links:
                links.append(link_str)
                link_conn[link_str] = c
            elif c['start_pin'][:2] != "::" or c['end_pin'][:2] != "::":
                link_conn[link_str] = c

    return links, link_conn


def test(number):
    json_data = number

    nodes = json_data.get('nodes')
    connections = json_data.get('connections')

    if not nodes or not connections:
        return

    uuid_id = {}

    for n in nodes:
        metadata = n['metadata']
        if 'id' in metadata:
            uuid_id[n['uuid']] = metadata['id']
        elif 'value' in metadata:
            if metadata['value']:
                uuid_id[n['uuid']] = 'true'
            else:
                uuid_id[n['uuid']] = 'false'
        else:
            uuid_id[n['uuid']] = n['name']

    print('types', uuid_id.values())

    links, link_conn = get_links(connections)

    Tree.printForest(links)
    exe, on_event = Tree.getRequestsData(uuid_id, links, link_conn)

    out = {'id': 1, 'commands': []}

    for i in range(len(exe)):
        d = {'on_event': on_event[i], 'exe': exe[i], 'id': out['id']}
        out['commands'].append(d)

    write_json_file(out, f'test_exit.json')
    return out["commands"]
