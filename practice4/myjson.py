import json
with open('sample_data.json','r') as file:
    sample_data=json.load(file)
attributes=sample_data['imdata'][0]['l1PhysIf']['attributes']
print(attributes['dn'])
print(attributes['descr'])
print(attributes['speed'])
print(attributes['mtu'])