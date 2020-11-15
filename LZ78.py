from util import *
import sys

def c(x):
	# x -> C(x)
	# may replaced by any coding scheme
	return x

def dc(cx):
	# C(x) -> x
	return cx

class LZ78:
	def __init__(self, s):
		self.s = s
		self.encoding = []
		self.entry_to_index = {(): -1}

	def encode(self):
		cur = 0
		MAX_LEN = len(self.s)
		buffer = []

		while True:
			if cur == MAX_LEN:
				cur_byte = 'EOF'
				buffer.append(cur_byte)
				tp = tuple(buffer)
				last_index = self.entry_to_index[tp[:-1]]
				self.encoding.append((last_index, c(cur_byte)))
				self.entry_to_index[tp] = len(self.encoding) - 1
				break

			cur_byte = self.s[cur]
			buffer.append(cur_byte)
			tp = tuple(buffer)

			if tp in self.entry_to_index:
				cur += 1
				continue

			last_index = self.entry_to_index[tp[:-1]]
			self.encoding.append((last_index, c(cur_byte)))
			self.entry_to_index[tp] = len(self.encoding) - 1
			buffer.clear()
			cur += 1

	def _find_entry(self, last_index, codeword):
		rs = [dc(codeword)]
		if last_index == -1:
			return rs

		prev_last_index, prev_codeword = self.encoding[last_index]
		rs += self._find_entry(prev_last_index, prev_codeword)
		return rs


	def decode(self):
		s = []
		for last_index, codeword in self.encoding:
			tmp = self._find_entry(last_index, codeword)
			tmp.reverse()
			s += tmp
		return ''.join(s[:-1])


	def save_file(self, path):
		file = open(path, 'w')
		for last_index, codeword in self.encoding:
			file.write(str(last_index) + ' ' + str(codeword) + '\n')
		file.close()


if __name__ == '__main__':

	s = file_to_str('Introduction to Data Compression.txt')
	encoder = LZ78(s)
	encoder.encode()
	
	#encoder.save_file('compressed.txt')
	print(len(encoder.encoding))
	#print(len(encoder.entry_to_index))
	#print(list(encoder.entry_to_index.keys())[:200])

	new_s = encoder.decode()
	str_to_file(new_s, 'test_LZ78.txt')
