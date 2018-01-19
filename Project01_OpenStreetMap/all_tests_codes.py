# 03_mapparser.py
# !/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint


def count_tags(filename):
    # YOUR CODE HERE
    tags = {}
    for event, elem in ET.iterparse(filename):
        if elem.tag not in tags:
            tags[elem.tag] = 1
        else:
            tags[elem.tag] += 1
    return tags


def test():

    tags = count_tags('example.osm')
    pprint.pprint(tags)
    assert tags == {'bounds': 1,
                    'member': 3,
                    'nd': 4,
                    'node': 20,
                    'osm': 1,
                    'relation': 1,
                    'tag': 7,
                    'way': 1}


if __name__ == "__main__":
    test()

############################################################

# 07_tags.py
# !/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re


lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')


def key_type(element, keys):
    if element.tag == "tag":
        # YOUR CODE HERE
        if lower.search(element.attrib['k']):
            keys['lower'] += 1
        elif lower_colon.search(element.attrib['k']):
            keys['lower_colon'] += 1
        elif problemchars.search(element.attrib['k']):
            keys['problemchars'] += 1
        else:
            keys['other'] += 1

    return keys


def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)

    return keys


def test():
    keys = process_map('example.osm')
    pprint.pprint(keys)
    assert keys == {'lower': 5, 'lower_colon': 0, 'other': 1, 'problemchars': 1}


if __name__ == "__main__":
    test()

############################################################

# 08_users.py
# !/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re


def get_user(element):

    return


def process_map(filename):
    users = set()
    for _, element in ET.iterparse(filename):
        if 'uid' in element.attrib:
            users.add(element.attrib['uid'])

    return users


def test():

    users = process_map('example.osm')
    pprint.pprint(users)
    assert len(users) == 6


if __name__ == "__main__":
    test()

############################################################

# 11_audit.py
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "example.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)


expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place",
            "Square", "Lane", "Road", "Trail", "Parkway", "Commons"]

# UPDATE THIS VARIABLE
mapping = {"St": "Street",
           "St.": "Street",
           "Ave": "Avenue",
           "Rd.": "Road"
           }


def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    osm_file.close()
    return street_types


def update_name(name, mapping):

    # YOUR CODE HERE
    m = street_type_re.search(name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            name = re.sub(street_type_re, mapping[street_type], name)

    return name


def test():
    st_types = audit(OSMFILE)
    assert len(st_types) == 3
    pprint.pprint(dict(st_types))

    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_name(name, mapping)
            print name, "=>", better_name
            if name == "West Lexington St.":
                assert better_name == "West Lexington Street"
            if name == "Baldwin Rd.":
                assert better_name == "Baldwin Road"


if __name__ == '__main__':
    test()

############################################################

# 12_data.py
import xml.etree.ElementTree as ET
import pprint
import re
import codecs
import json


lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
non_chinese_name = re.compile(r'[A-Za-z]+')  # 非中文字符
include_space = re.compile(r'^\s|\s$')  # 开头末尾有空格，不符合标准

CREATED = ["version", "changeset", "timestamp", "user", "uid"]


def fix_values(element):
    # 修补空格
    for tag in element.iter("tag"):
        if tag.attrib['k'] == 'name':
            if include_space.search(tag.attrib['v']):
                tag.attrib['v'] = tag.attrib['v'].strip()
    # 统一电话号码格式
        if tag.attrib['k'] == 'phone':
            if len(tag.attrib['v'].split(',')) < 2:
                tag.attrib['v'] = '+86-021-' +\
                    str(tag.attrib['v']).replace(' ', '')[-8:]
            else:
                new_list = []
                for i in (tag.attrib['v'].split(',')):
                    new_list.append('+86-021-' + str(i).replace(' ', '')[-8:])
                tag.attrib['v'] = ', '.join(new_list)


# xml转json
def shape_element(element):
    fix_values(element)
    node = {}
    if element.tag == "node" or element.tag == "way":
        # YOUR CODE HERE
        node['type'] = element.tag

        for a in element.attrib:
            if a in CREATED:
                if 'created' not in node:
                    node['created'] = {}
                node['created'][a] = element.attrib[a]

            elif a in ['lat', 'lon']:
                if 'pos' not in node:
                    node['pos'] = [None, None]
                if a == 'lat':
                    node['pos'][0] = float(element.attrib[a])
                else:
                    node['pos'][1] = float(element.attrib[a])

            else:
                node[a] = element.attrib[a]

        for tag in element.iter("tag"):
            if not problemchars.search(tag.attrib['k']):
                if lower_colon.search(tag.attrib['k']):

                    if tag.attrib['k'].find('addr') == 0:
                        if 'address' not in node:
                            node['address'] = {}

                        sub_attr = tag.attrib['k'].split(':', 1)
                        node['address'][sub_attr[1]] = tag.attrib['v']

                    else:
                        node[tag.attrib['k']] = tag.attrib['v']

                elif tag.attrib['k'].find(':') == -1:
                    node[tag.attrib['k']] = tag.attrib['v']

            for nd in element.iter("nd"):
                if 'node_refs' not in node:
                    node['node_refs'] = []
                node['node_refs'].append(nd.attrib['ref'])

        return node
    else:
        return None


def process_map(file_in, pretty=False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2) + "\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data


def test():
    data = process_map('example.osm', True)
    # pprint.pprint(data)

    correct_first_elem = {
        "id": "261114295",
        "visible": "true",
        "type": "node",
        "pos": [41.9730791, -87.6866303],
        "created": {
            "changeset": "11129782",
            "user": "bbmiller",
            "version": "7",
            "uid": "451048",
            "timestamp": "2012-03-28T18:31:23Z"
        }
    }
    assert data[0] == correct_first_elem
    assert data[-1]["address"] == {
        "street": "West Lexington St.",
        "housenumber": "1412"
    }
    assert data[-1]["node_refs"] == ["2199822281", "2199822390", "2199822392",
                                     "2199822369", "2199822370",
                                     "2199822284", "2199822281"]


if __name__ == "__main__":
    test()
