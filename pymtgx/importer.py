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
import argparse
import csv

import pymtgx

from pyparsing import Literal, Word, alphas, nums

__author__ = 'Petter Bjelland (petter.bjelland@gmail.com)'


##
# Convert a CSV file into a Maltego .mtgx file based on a predefined format.
class Importer(object):

	STRING = alphas + nums + "_-.+ "

	INDEXED_EDGE_DEF = (Word(nums).setResultsName('from_index') + ":" 
			+ Word(alphas).setResultsName('from_type') + ">" 
			+ Word(nums).setResultsName('to_index') + ":" 
			+ Word(alphas).setResultsName('to_type') + "|" 
			+ Word(STRING).setResultsName('edge_label'))

	MAPPED_EDGE_DEF = (Word(STRING).setResultsName('from_column') + ":" 
			+ Word(alphas).setResultsName('from_type') + ">" 
			+ Word(STRING).setResultsName('to_column') + ":" 
			+ Word(alphas).setResultsName('to_type') + "|" 
			+ Word(STRING).setResultsName('edge_label'))

	##
	# Set up variables and parse input file.
	def __init__(self, input_file, format_spec_file, output_file, entity_files, delimiter, quotechar, skip_lines, map_header):		
		self.mtgx = pymtgx.Pymtgx()

		# Ensure correct output file extension.
		if output_file.endswith(".mtgx"):
			output_file = output_file[:-5]

		self.output_file = output_file

		self.number_of_edges = 0

		# Register entity specifications
		for entity_file in entity_files:
			self.mtgx.register_entities(entity_file)

		# If we are using indexed format specifications, load them right away.
		if not map_header:		
			self.format_spec = self.__load_indexed_format(format_spec_file)

		with open(input_file, 'rb') as csvfile:			
			lines = 0

			# Read lines as CSV.
			for line in csv.reader(csvfile, delimiter=delimiter, quotechar=quotechar):
				lines += 1

				if lines <= skip_lines:
					continue

				# If we are using mapped format specifications, load mapping from first
				# line that is not skipped.
				elif map_header and lines == skip_lines + 1:
					self.format_spec = self.__load_mapped_format(format_spec_file, line)
					continue
				
				# Parse the line into maltego entities and edges.
				self.number_of_edges += self._parse_line(line)			

		# Calculate the number of lines we've parsed.
		self.number_of_lines = lines - skip_lines

	##
	# Create the .mtgx archive file.
	def create(self):		
		self.mtgx.create(self.output_file)

	##
	# Load format specifications based on column index. The first column has index 0.
	def __load_indexed_format(self, format_spec_file_path):
		format_spec = []	

		with open(format_spec_file_path, 'rb') as format_spec_file:	
			for edge_definition in format_spec_file:
				definition = self.INDEXED_EDGE_DEF.parseString(edge_definition.strip())

				format_spec.append({
					'from_index': int(definition['from_index']),	
					'from_type': definition['from_type'],
					'to_index': int(definition['to_index']),
					'to_type': definition['to_type'],
					'edge_label': definition['edge_label']
				})

		return format_spec

	##
	# Load format specifications based on column name.
	def __load_mapped_format(self, format_file_path, header):
		header_map = {}

		for column in header:
			header_map[column] = len(header_map)

		format_spec = []	

		with open(format_file_path, 'rb') as format_file:	
			for edge_definition in format_file:
				definition = self.MAPPED_EDGE_DEF.parseString(edge_definition.strip())
				
				format_spec.append({
					'from_index': header_map[definition['from_column']],	
					'from_type': definition['from_type'],
					'to_index': header_map[definition['to_column']],
					'to_type': definition['to_type'],
					'edge_label': definition['edge_label']
				})

		return format_spec

	##
	# Parse a line into maltego entities and edges based on the loaded format specifications. 
	def _parse_line(self, line):
		edges = 0

		for edge_def in self.format_spec:
			has_from = line[edge_def['from_index']] != ''
			has_to = line[edge_def['to_index']] != ''

			if has_from:
				n0 = self.mtgx.add_node('maltego.' + edge_def['from_type'], line[edge_def['from_index']])

			if has_to:
				n1 = self.mtgx.add_node('maltego.' + edge_def['to_type'], line[edge_def['to_index']])

			if has_from and has_to:
				self.mtgx.add_edge(n0, n1, edge_def['edge_label'])

				edges += 1

		return edges

if __name__ == '__main__':
	parser = argparse.ArgumentParser()

	parser.add_argument("-i", "--input-file", dest="input_file",
			help="Path to file to parse", required=True)
	parser.add_argument("-f", "--format-file", dest="format_file",
			help="Path to format specification file.", required=True)
	parser.add_argument("-o", "--output-file", dest="output_file",
			help="Path to output file. Extension is added if missing.", required=True)
	parser.add_argument("-e", "--entity-files", dest="entity_files",
			help="Comma separated list of .mtz files to use.", required=True)
	parser.add_argument("-d", "--delimiter", dest="delimiter",
			help="How values are delimited. Default: ,", default=",")
	parser.add_argument("-q", "--quotechar", dest="quotechar",
			help="How values are quoted, remember escape character. Default: None")
	parser.add_argument("-s", "--skip-lines", dest="skip_lines",
			help="Number of lines to skip. Default: 0", default=0)	
	parser.add_argument("-m", "--map-header", dest="map_header",
			help="Use column names in format specification. If not, the columns in the specifications are 0-indexed.", default=False)	

	args = parser.parse_args()

	importer = Importer(input_file=args.input_file, 
		format_spec_file=args.format_file, 
		output_file=args.output_file, 
		entity_files=args.entity_files.split(','),
		delimiter=args.delimiter, quotechar=args.quotechar, 
		skip_lines=args.skip_lines, map_header=args.map_header)

	importer.create()

	print "Parsed", importer.number_of_lines, "lines. Created " + importer.output_file + ".mtgx"
