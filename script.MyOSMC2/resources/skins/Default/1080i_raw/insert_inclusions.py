from glob import glob
import os
from pprint import pprint
import re
import xml.etree.ElementTree as ET

cwd = os.getcwd()
dest_folder = cwd[:-4]

include_file = 'Includes.xml'

fyles = glob('*.xml')

fyles.remove(include_file)

def get_inclusion(child):

	return "".join([ ET.tostring(e) for e in child.getchildren() ] )

tree = ET.parse(include_file)
root = tree.getroot()

inclusions = { child.attrib['name']: get_inclusion(child) for child in root}

replacement_record = {}

for fyle in fyles:

	new_fyle = os.path.join(dest_folder, fyle)

	with open(fyle, 'r') as f:

		replacement_record[fyle] = {}

		contents = ''.join(f.readlines())
		
		for include_tag, guts in inclusions.iteritems():

			string = '<include>\s*' + include_tag + '\s*</include>'

			contents, count =  re.subn(string, guts, contents, re.MULTILINE)
			
			replacement_record[fyle][include_tag] = count

	with open(new_fyle, 'w') as f:
		f.write(contents)

pprint(replacement_record)
