
def file_to_bytes(path):
	# return the file in bytes format
	# can be seen as an array of ints ranging 0 -- 255
	f = open(path, 'rb')
	bs = f.read()
	f.close()
	return bs

def bytes_to_file(bs, path):
	f = open(path, 'wb')
	f.write(bs)
	f.close()
