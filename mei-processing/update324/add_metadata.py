import csv
import sys
import os.path
from copy import deepcopy
from datetime import date
import xml.etree.ElementTree as ET

MEI_LOC = 'output/'
MEI_OUTPUT = 'output/metadata'
METADATA_MASSES = os.path.join('data', 'metadata-masses.csv')
METADATA_MODELS = os.path.join('data', 'metadata-models.csv')

MEINSURI = 'http://www.music-encoding.org/ns/mei'
MEINS = '{%s}' % MEINSURI
XINSURI = 'http://www.w3.org/2001/XInclude'
XINS = '{%s}' % XINSURI
ET._namespace_map.update({MEINSURI: '', XINSURI: 'xi'})
ISODATE = date.today().strftime("%Y-%m-%d")
MEIDECLS= """<?xml version="1.0" encoding="UTF-8"?>
<?xml-model href="https://music-encoding.org/schema/4.0.1/mei-CMN.rng" type="application/xml" schematypens="http://relaxng.org/ns/structure/1.0"?>
<?xml-model href="https://music-encoding.org/schema/4.0.1/mei-CMN.rng" type="application/xml" schematypens="http://purl.oclc.org/dsdl/schematron"?>
"""

def apply_model_metadata(mei, metadata):
  mei_doc = ET.parse(mei)
  root = mei_doc.getroot()

  # Revert staffDef/label to staffDef/@label
  staffDefs = root.findall(f'{MEINS}music//{MEINS}staffDef')
  for staffDef in staffDefs:
    label = staffDef.find(f'{MEINS}label').text
    if label:
      staffDef.set('label', label)

  head_el = root.find(f'{MEINS}meiHead')
  fileDesc_el = head_el.find(f'{MEINS}fileDesc')

  # title
  titleStmt_el = fileDesc_el.find(f'{MEINS}titleStmt')
  titleStmt_el.clear()
  title_el = ET.SubElement(titleStmt_el, 'title')
  title_el.text = metadata[5]

  respStmt_el = ET.SubElement(titleStmt_el, 'respStmt')

  # composer
  composer_el = ET.Element('persName', {
    'role': 'composer',
    'auth': 'VIAF',
    'auth.uri': metadata[3]
  })
  composer_el.text = metadata[2]
  respStmt_el.append(composer_el)

  # editors
  editors = metadata[18].split('|')
  for editor in editors:
    ET.SubElement(respStmt_el, 'persName', {
    'role': 'editor'
  }).text = editor.strip()
  # pubStmt  
  pubStmt_el = fileDesc_el.find(f'{MEINS}pubStmt')
  pubStmt_el.clear()
  pubStmt_el.append(ET.fromstring("""<publisher>
      Citations: The Renaissance Imitation Mass Project
  </publisher>"""))
  for distributor in metadata[25].split('|'):
    pubStmt_el.append(ET.fromstring(f'<distributor>{distributor}</distributor>'))
  pubStmt_el.append(ET.fromstring(f'<date isodate="{ISODATE}"/>'))
  pubStmt_el.append(ET.fromstring(f'<availability>{metadata[24]}</availability>'))

  # appInfo
  appInfo_el = head_el.find(f'{MEINS}encodingDesc/{MEINS}appInfo')
  application = """<application version="1.0.0">
      <name>add_metadata.py</name>
  </application>"""
  appInfo_el.append(ET.fromstring(application))

  # work data
  worklist_el = head_el.find(f'{MEINS}workList')
  work_el = worklist_el.find(f'{MEINS}work')
  work_el.remove(work_el.find(f'{MEINS}incip'))
  work_el.find(f'{MEINS}title').text = metadata[5]
  ET.SubElement(work_el, 'composer').append(deepcopy(composer_el))
  classification = f'<classification><termList><term>{metadata[7].strip()}</term></termList></classification>'
  work_el.append(ET.fromstring(classification))

  # source data
  manifestation = f"""  <manifestationList xmlns="{MEINSURI}" xml:id="manifestationList">
      <manifestation>
        <identifier type="RISM">{metadata[20]}</identifier>
        <titleStmt>
          <title>{metadata[5]}</title>
        </titleStmt>
        <pubStmt>
          <publisher>
            <persName auth="VIAF" auth.uri="{metadata[12]}">{metadata[11]}</persName>
          </publisher>
          <date/>
        </pubStmt>
        <physLoc>
          <repository>
            <corpName>{metadata[22]}</corpName>
            <settlement>{metadata[21]}</settlement>
          </repository>
          <identifier type="shelfmark"> {metadata[23]} </identifier>
        </physLoc>
      </manifestation>
    </manifestationList>
  """
  manifestation_el = ET.fromstring(manifestation)
  head_el.append(manifestation_el)

  if (len(metadata[14].strip()) > 1):
    # add second publisher
    manifestation_el.find(f'{MEINS}manifestation//{MEINS}publisher').append(
      ET.fromstring(f'<persName auth="VIAF" auth.uri="{metadata[15]}">{metadata[14]}</persName>')
    )

  # pub date
  date_el = manifestation_el.find(f'{MEINS}manifestation/{MEINS}pubStmt/{MEINS}date')
  if len(metadata[17].strip()) == 4:
    date_el.attrib['isodate'] = metadata[17].strip()
  else:
    date_el.text = metadata[17]

  return ET.tostring(root, encoding='unicode')

def apply_metadata(mei, metadata):
  mass_name = "_".join(metadata[0].split('_')[0:3])
  mei_doc = ET.parse(mei)
  root = mei_doc.getroot()

  # Revert staffDef/label to staffDef/@label
  staffDefs = root.findall(f'{MEINS}music//{MEINS}staffDef')
  for staffDef in staffDefs:
    label = staffDef.find(f'{MEINS}label').text
    staffDef.set('label', label)

  # set mdiv's id to "movement"
  mdiv_el = root.find(f'{MEINS}music//{MEINS}mdiv')
  del mdiv_el.attrib['{http://www.w3.org/XML/1998/namespace}id']
  mdiv_el.set('xml:id', 'section')

  head_el = root.find(f'{MEINS}meiHead')
  fileDesc_el = head_el.find(f'{MEINS}fileDesc')

  titleStmt_el = fileDesc_el.find(f'{MEINS}titleStmt')
  title_el = titleStmt_el.find(f'{MEINS}title')
  title_el_id = title_el.get('{http://www.w3.org/XML/1998/namespace}id')
  titleStmt_el.set('xml:id', title_el_id+'-ts')
  title_el.clear()
  title_el.set('xml:id', title_el_id)
  title_el.text = metadata[1]

  respStmt_el = ET.SubElement(titleStmt_el, 'respStmt')
  # composer
  ET.SubElement(respStmt_el, 'persName', {
    'role': 'composer',
    'auth': 'VIAF',
    'auth.uri': metadata[5]
  }).text = metadata[4]
  # editors
  editors = metadata[8].split('|')
  for editor in editors:
    ET.SubElement(respStmt_el, 'persName', {
    'role': 'editor'
  }).text = editor.strip()
  # pubStmt  
  pubStmt_el = fileDesc_el.find(f'{MEINS}pubStmt')
  pubStmt_el.clear()
  pubStmt_el.append(ET.fromstring("""<publisher>
      Citations: The Renaissance Imitation Mass Project
  </publisher>"""))
  for distributor in metadata[22].split('|'):
    pubStmt_el.append(ET.fromstring(f'<distributor>{distributor}</distributor>'))
  pubStmt_el.append(ET.fromstring(f'<date isodate="{ISODATE}"/>'))
  pubStmt_el.append(ET.fromstring(f'<availability>{metadata[21]}</availability>'))
  # appInfo
  appInfo_el = head_el.find(f'{MEINS}encodingDesc/{MEINS}appInfo')
  application = """<application version="1.0.0">
      <name>add_metadata.py</name>
  </application>"""
  appInfo_el.append(ET.fromstring(application))

  # get rid of incipit  
  head_el.remove(head_el.find(f'{MEINS}workList'))

  # XPointers to work-level metadata
  encodingDesc_pos = head_el.getchildren().index(head_el.find(f'{MEINS}encodingDesc'))
  head_el.insert(
    encodingDesc_pos + 1,
    ET.Element(f'{XINS}include', {
      'href': f'{mass_name}.mei',
      'xpointer': 'workList'
    })
  )
  head_el.insert(
    encodingDesc_pos + 2,
    ET.Element(f'{XINS}include', {
      'href': f'{mass_name}.mei',
      'xpointer': 'manifestationList'
    })
  )

  return ET.tostring(root, encoding='unicode')

def create_mass_mei(mass_name, metadata):
  '''
  Populate template as much as possible right away, then complete metadata with DOM operations.
  '''

  mei_doc = ET.fromstring(f"""<?xml version="1.0" encoding="UTF-8"?>
<?xml-model href="https://music-encoding.org/schema/4.0.1/mei-CMN.rng" type="application/xml" schematypens="http://relaxng.org/ns/structure/1.0"?>
<?xml-model href="https://music-encoding.org/schema/4.0.1/mei-CMN.rng" type="application/xml" schematypens="http://purl.oclc.org/dsdl/schematron"?>
<mei xmlns="http://www.music-encoding.org/ns/mei" xmlns:xi="http://www.w3.org/2001/XInclude" xml:id="{mass_name}">
  <meiHead xmlns="http://www.music-encoding.org/ns/mei" xml:id="CRIM_MASS-0001">
    <altId>{mass_name}</altId>
    <fileDesc>
      <titleStmt>
        <title>{metadata[2]}</title>
        <respStmt>
          <persName role="composer" auth="VIAF" auth.uri="{metadata[5]}">{metadata[4]}</persName>
        </respStmt>
      </titleStmt>
      <pubStmt>
        <publisher> Citations: The Renaissance Imitation Mass Project </publisher>
        <distributor> Centre d'Études Supérieures de la Renaissance </distributor>
        <distributor>Haverford College</distributor>
        <date isodate="{ISODATE}"/>
        <availability>{metadata[21]}</availability>
      </pubStmt>
    </fileDesc>
    <encodingDesc>
      <appInfo>
        <application version="1.0.0">
          <name>add_metadata.py</name>
        </application>
      </appInfo>
    </encodingDesc>
    <workList xml:id="workList">
      <work>
        <title>{metadata[2]}</title>
        <composer>
          <persName role="composer" auth="VIAF" auth.uri="{metadata[5]}">{metadata[4]}</persName>
        </composer>
        <contents></contents>
      </work>
    </workList>
    <manifestationList xml:id="manifestationList">
      <manifestation>
        <identifier type="RISM">{metadata[17]}</identifier>
        <titleStmt>
          <title>{metadata[2]}</title>
        </titleStmt>
        <pubStmt>
          <publisher>
            <persName auth="VIAF" auth.uri="{metadata[14]}">{metadata[13]}</persName>
          </publisher>
          <date isodate="{metadata[16]}"/>
        </pubStmt>
        <physLoc>
          <repository>
            <corpName>{metadata[19]}</corpName>
            <settlement>{metadata[18]}</settlement>
          </repository>
          <identifier type="shelfmark"> {metadata[20]} </identifier>
        </physLoc>
      </manifestation>
    </manifestationList>
  </meiHead>
  <music><body></body></music>
</mei>""")
  respStmt_el = mei_doc.find(f'{MEINS}meiHead/{MEINS}fileDesc//{MEINS}respStmt')
  editors = metadata[8].split('|')
  for editor in editors:
    ET.SubElement(respStmt_el, 'persName', {
    'role': 'editor'
  }).text = editor.strip()
  return mei_doc

def add_mass_metadata(mei_doc, metadata):
  # Contents
  contents_el = mei_doc.find(f'{MEINS}meiHead/{MEINS}workList/{MEINS}work/{MEINS}contents')
  ET.SubElement(contents_el, 'contentItem').text =metadata[3]
  # XPointers to mdivs
  body_el = mei_doc.find(f'{MEINS}music/{MEINS}body')
  ET.SubElement(body_el, f'{XINS}include', {
    'href': f'{metadata[0]}',
    'xpointer': 'section'
  })
  return mei_doc

# MAIN

if not os.path.exists(MEI_OUTPUT):
  os.makedirs(MEI_OUTPUT)

# Deal with masses first.
updated_masses = {}

with open(METADATA_MASSES, newline='') as csvfile:
  csv_data = csv.reader(csvfile)
  metadata = list(csv_data)
  for [i, row] in enumerate(metadata):
    if i == 0 or row[0] == '': continue
    mei_filename = row[0]
    mei = os.path.join(MEI_LOC, mei_filename)
    if (not os.path.exists(mei)):
      print('Could not locate ', mei)
      continue
    # If a mass file hasn't been created yet, create it.
    mass_name = "_".join(mei_filename.split('_')[0:3])
    if (not mass_name in updated_masses.keys()):
      mass_doc = create_mass_mei(mass_name, row)
      updated_masses[mass_name] = mass_doc
    else:
      mass_doc = updated_masses[mass_name]
    updated_masses[mass_name] = add_mass_metadata(mass_doc, row)
    # If this is the last row about this mass, write out.
    next_row = list(metadata)[i+1]
    next_mass_name = "_".join(next_row[0].split('_')[0:3])
    if (not next_mass_name == mass_name):      
      with open(os.path.join(MEI_LOC, mass_name+'.mei'), 'w') as mass:
        mass.write(MEIDECLS)
        mass.write(ET.tostring(mass_doc, encoding='unicode'))
    # Add metadata to section file
    with open(os.path.join(MEI_OUTPUT, mei_filename), 'w') as mei_output:
      mei_output.write(MEIDECLS)
      mei_output.write(apply_metadata(mei, row))

# Now deal with models

with open(METADATA_MODELS, newline='') as csvfile:
  csv_data = csv.reader(csvfile)
  metadata = list(csv_data)

  for [i, row] in enumerate(metadata):
    if i == 0 or row[0] == '': continue
    mei_filename = row[0]
    mei = os.path.join(MEI_LOC, mei_filename)
    if (not os.path.exists(mei)):
      print('Could not locate ', mei)
      continue
    with open(os.path.join(MEI_OUTPUT, mei_filename), 'w') as mei_output:
      mei_output.write(MEIDECLS)
      mei_output.write(apply_model_metadata(mei, row))
