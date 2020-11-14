
def file_to_str(path):
	f = open(path, 'r')
	s = f.read()
	f.close()
	return s

def str_to_file(s, path):
	f = open(path, 'w')
	f.write(s)
	f.close()
