import networkx

from xml.etree.cElementTree import Element, SubElement, ElementTree, tostring
from networkx.utils import make_str
from networkx.readwrite import graphml

types = {
	'maltego.Person': {
		"name": "person.fullname",
		"displayName": "Full name"
	}
}

class Pymtgx(networkx.Graph):
	def __init__(self):		
		super(Pymtgx, self).__init__()
		self.node_id = 0

	def add_node(self, type, data):
		current_id = 'n' + str(self.node_id)
		super(Pymtgx, self).add_node(current_id, dict(MaltegoEntity=MaltegoEntity(type, data)))
		self.node_id += 1		
		return current_id

	def add_edge(self, sourceId, targetId):
		super(Pymtgx, self).add_edge(sourceId, targetId)

class MaltegoEntity(object):
	def __init__(self, type, value):		
		self.data = Element("data")		
		entity = SubElement(self.data, "mtg:MaltegoEntity")
		entity.attrib['xmlns:mtg'] = 'http://maltego.paterva.com/xml/mtgx'
		entity.attrib['type'] = type

		propertiesElement = SubElement(entity, "mtg:Properties")		
		
		self.add_entity_property(propertiesElement, types[type], value)

	def add_entity_property(self, parent, prop, value):				
		propertyElement = SubElement(parent, "mtg:Property")
		
		propertyElement.attrib['name'] = prop.get('name', 'unknown')		
		propertyElement.attrib['displayName'] = prop.get('displayName', 'Unknown')
		propertyElement.attrib['hidden'] = prop.get('hidden', 'false')
		propertyElement.attrib['nullable'] = prop.get('nullable', 'true')
		propertyElement.attrib['readonly'] = prop.get('readonly', 'false')
		propertyElement.attrib['type'] = prop.get('type', 'string')

		SubElement(propertyElement, "mtg:Value").text = value

class MaltegoWriter(graphml.GraphMLWriter):
	def __init__(self, encoding, prettyprint):		
		super(MaltegoWriter, self).__init__(encoding=encoding,prettyprint=prettyprint)

	def add_attributes(self, scope, xml_obj, data, default):
		for k,v in data.items():
			v.data.attrib['key'] = self.get_key(k, k, scope, None)
			xml_obj.append(v.data)
			
def write_graphml(G, path, encoding='utf-8',prettyprint=True):
	writer = MaltegoWriter(encoding=encoding,prettyprint=prettyprint)
	writer.add_graph_element(G)
	writer.dump(path)

pymtgx = Pymtgx()
id1 = pymtgx.add_node("maltego.Person", 'Petter Bjelland')
id2 = pymtgx.add_node("maltego.Person", 'Jon Doe')
pymtgx.add_edge(id1, id2)

write_graphml(pymtgx, open('Graph1.graphml', 'wb'))