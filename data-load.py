
import os
import sys

# def iterate(path, command):
#   if os.path.isfile(path) and path.endswith('.json'):
#     command(path)
#   elif os.path.isdir(path):
#     for filename in os.listdir(path):
#       iterate(os.path.join(path, filename), command)



# def load_data(file):
#   command = f'python3 ./manage.py loaddata {file}'
#   # print(command)
#   os.system(f'python3 ./manage.py loaddata {file}')

if __name__ == '__main__':
  # if len(sys.argv) < 2:
  #   print("usage: data-load.py <path>")
  #   sys.exit(-1)

  # path = sys.argv[1]
  # iterate(path, load_data)

  path = 'crim/fixtures/data-2022-fresh'
  items = [ 'genre.json',
            'mass.json',
            'piece.json',
            'part.json',
            'phrase.json',
            'voice.json',
            'treatise.json',
            'source.json',
            'person.json',
            'roletype.json',
            'role.json',
            'definition.json',
            'observation.json',
            'relationship.json',
          ]
  for filename in items:
    file = os.path.join(path, filename)
    os.system('python3 ./manage.py makemigrations')
    os.system('python3 ./manage.py migrate')
    os.system(f'python3 ./manage.py loaddata {file}')
    # if os.system(f'python3 ./manage.py loaddata {file}') != 0:
    #   sys.exit(-1)
