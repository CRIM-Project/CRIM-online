import convert324
import argparse
from os import listdir
import os.path

MEI_LOC = '../../crim/static/mei/'
MEI_OUT = 'output/'

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Convert all MEI files in CRIM-Online from v3 to v4.')
  parser.add_argument('--mei', default=MEI_LOC, dest="mei", help="directory where MEI files are located")
  parser.add_argument('--output', default=MEI_OUT, dest="output", help="output directory")
  parser.add_argument('--meigarage', default=None, dest="garage", help="MEI Garage endpoint")
  
  options = parser.parse_args()

  if not os.path.exists(options.output):
    os.makedirs(options.output)

  mei_files = [f for f in listdir(options.mei) if os.path.isfile(os.path.join(options.mei, f))]

  for mei_filename in mei_files:
    mei = os.path.join(options.mei, mei_filename)
    if (not os.path.exists(mei)):
      print('Could not locate ', mei)
      continue
    # Convert to MEI4 using meigarage.
    mei_v4 = convert324.convert(options.mei, mei_filename, options.garage)
    with open(os.path.join(options.output, mei_filename), 'w') as output_file:
      output_file.write(mei_v4)