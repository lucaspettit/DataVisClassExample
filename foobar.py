from argparse import ArgumentParser

if __name__ == '__main__':
  parser = ArgumentParser()
  parser.add_argument('-v', '--value', choices=['foo', 'bar'], help='You say "foo", i say "bar". Or visa-versa')
  v = parser.parse_args().value

  if v == 'foo':
    print('bar!')
  else:
    print('foo!')