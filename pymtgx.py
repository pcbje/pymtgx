#!/usr/bin/env python
import networkx
import zipfile
import tempfile

import xml.etree.cElementTree as ElementTree
from xml.etree.cElementTree import Element, SubElement, tostring
from networkx.readwrite import graphml

default_types = {
	'maltego.Person': {"name": "person.fullname", "displayName": "Full name"},
	'maltego.EmailAddress': {"name": "email", "displayName": "Email Address"}
}

class Pymtgx(networkx.Graph):
	def __init__(self):		
		super(Pymtgx, self).__init__()
		self.node_id = 0
		self.entities = default_types

	def register_entities(self, path):
		z = zipfile.ZipFile(path, "r")

		for filename in z.namelist():			
			element = ElementTree.fromstring(z.read(filename))

			if element.tag == 'MaltegoEntity':
				self.register_entity(element)

	def register_entity(self, element):		
		baseEntity = element.find(".//BaseEntity")			
		field = element.find(".//Field")		
		
		if baseEntity != None:
			self.entities[element.attrib['id']] = {
				'baseType': baseEntity.text				
			}			
		elif field != None:
			self.entities[element.attrib['id']] = {
				'name': field.attrib['name'],
				'displayName': field.attrib['displayName'],
				'dataType': field.attrib['type']			
			}	
		
	def add_node(self, entityType, data):
		current_id = 'n' + str(self.node_id)

		self.node_id += 1		
		
		entity = self.entities[entityType]

		if 'baseType' in entity:			
			entity = self.entities[entity['baseType']]

		super(Pymtgx, self).add_node(current_id, dict(MaltegoEntity=MaltegoEntity(entityType, entity, data)))

		return current_id

	def create_mtgx(self, path, encoding='utf-8',prettyprint=True):
		writer = MaltegoWriter(encoding=encoding,prettyprint=prettyprint)
		writer.add_graph_element(self)
		
		with tempfile.NamedTemporaryFile() as temp:
			temp.write(str(writer).encode())
			temp.flush()

			zf = zipfile.ZipFile(path, mode='w')
			zf.write(temp.name, "Graphs/Graph1.graphml")
			zf.close()

class MaltegoEntity(object):
	def __init__(self, entityType, entity, value):		
		self.data = Element("data")		
		entityElement = SubElement(self.data, "mtg:MaltegoEntity")

		entityElement.attrib = {
			'xmlns:mtg': 'http://maltego.paterva.com/xml/mtgx',
			'type': entityType
		}

		propertiesElement = SubElement(entityElement, "mtg:Properties")		
		
		self.add_entity_property(propertiesElement, entity, value)

	def add_entity_property(self, parent, prop, value):				
		propertyElement = SubElement(parent, "mtg:Property")
		
		propertyElement.attrib = {
			'name': prop.get('name'),
			'displayName': prop.get('displayName'),
			'type': prop.get('dataType', 'string')
		}
		
		SubElement(propertyElement, "mtg:Value").text = value

class MaltegoWriter(graphml.GraphMLWriter):
	def add_attributes(self, scope, xml_obj, data, default):
		for k,v in data.items():
			v.data.attrib['key'] = self.get_key(k, k, scope, None)
			xml_obj.append(v.data)
		
pymtgx = Pymtgx()
pymtgx.register_entities("../../Downloads/casefile_entities.mtz")
id1 = pymtgx.add_node("maltego.Person", 'Petter Bjelland')
id2 = pymtgx.add_node("maltego.Person", 'Jon Doe')
id3 = pymtgx.add_node("maltego.Missile", 'petter.bjelland@hig.no')
pymtgx.add_edge(id1, id2)
pymtgx.add_edge(id1, id3)
pymtgx.create_mtgx("graph.mtgx")
