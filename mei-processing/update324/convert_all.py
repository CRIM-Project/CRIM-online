import convert324
import argparse
import os.path
import csv

MEI_LOC = '../../crim/static/mei/'
MEI_OUT = 'output/'
METADATA = 'data/metadata.csv'

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Convert all MEI files in CRIM-Online from v3 to v4.')
  parser.add_argument('--metadata', default=METADATA, dest="metadata", help="metadata csv location")
  parser.add_argument('--mei', default=MEI_LOC, dest="mei", help="directory where MEI files are located")
  parser.add_argument('--output', default=MEI_OUT, dest="output", help="output directory")
  parser.add_argument('--meigarage', default=None, dest="garage", help="MEI Garage endpoint")
  
  options = parser.parse_args()

  if not os.path.exists(options.output):
    os.makedirs(options.output)

  with open(options.metadata, newline='') as csvfile:    
    metadata = csv.reader(csvfile)
    for [i, row] in enumerate(metadata):
      if i == 0 or row[0] == '': continue
      mei_filename = row[0]
      mei = os.path.join(options.mei, mei_filename)
      if (not os.path.exists(mei)):
        print('Could not locate ', mei)
        continue
      # Convert to MEI4 using meigarage.
      mei_v4 = convert324.convert(options.mei, mei_filename, options.garage)
      with open(os.path.join(options.output, mei_filename), 'w') as output_file:
        output_file.write(mei_v4)