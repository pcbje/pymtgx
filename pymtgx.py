#!/usr/bin/env python
"""
This work is made available under the Apache License, Version 2.0.

You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
License for the specific language governing permissions and limitations under
the License.
"""
import networkx
import zipfile
import tempfile

import xml.etree.cElementTree as ElementTree
from xml.etree.cElementTree import Element, SubElement, tostring
from networkx.readwrite import graphml

default_types = {
  'maltego.Person': {"name": "person.fullname"},
  'maltego.Alias': {"name": "alias"},
  'maltego.EmailAddress': {"name": "email"},
  'maltego.IPv4Address': {"name": "ipv4-address"},
  'maltego.URL': {"name": "short-title"},
  'maltego.MobileComputer': {"name": "device"}
}

class Pymtgx(networkx.DiGraph):
  def __init__(self):		
    super(Pymtgx, self).__init__()
    self.positions = {}
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
        'dataType': field.attrib['type']
      }	
		
  def add_node(self, entityType, data):
    current_id = 'n' + str(self.node_id)

    self.node_id += 1		
		
    entity = self.entities[entityType]

    if 'baseType' in entity:			
      entity = self.entities[entity['baseType']]

    renderer = EntityRenderer()

    self.positions[current_id] = renderer

    super(Pymtgx, self).add_node(current_id, dict(MaltegoEntity=MaltegoEntity(entityType, entity, data), EntityRenderer=renderer))

    return current_id

  def layout(self, layout='spring_layout', space=100):
    layout_func = getattr(networkx, layout)

    scale = len(self.nodes()) * space

    positions = layout_func(self, scale=scale)

    for pos in positions:
      self.positions[pos].position.attrib = {
        'x': str(int(positions[pos][0])),
        'y': str(int(positions[pos][1]))
      }

  def create(self, path, encoding='utf-8',prettyprint=True):    
    writer = MaltegoWriter(encoding=encoding,prettyprint=prettyprint)
    
    writer.add_graph_element(self)

    writer.xml.find('.//key[@attr.name="EntityRenderer"]').set('yfiles.type', "nodegraphics")
		
    with tempfile.NamedTemporaryFile() as temp:
      temp.write(str(writer).encode())
      temp.flush()

      zf = zipfile.ZipFile(path + '.mtgx', mode='w')
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
      'type': prop.get('dataType', 'string')
    }
		
    SubElement(propertyElement, "mtg:Value").text = value

class EntityRenderer(object):
  def __init__(self):    
    self.data = Element("data")   

    entityRendererElement = SubElement(self.data, "mtg:EntityRenderer")

    entityRendererElement.attrib['xmlns:mtg'] = 'http://maltego.paterva.com/xml/mtgx'

    self.position = SubElement(entityRendererElement, "mtg:Position")   

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