import sys, math

class Huffman:
	def __init__(self, s):
		self.s = s
		self.word_to_time = {}
		self.word_to_code = {}
		self.code_to_word = {}
		self.node_to_sons = {}
		self._make_code()

	
	def _make_code(self):
		for word in self.s:
			if word not in self.word_to_time:
				self.word_to_time[word] = 0
			self.word_to_time[word] += 1

		node_to_time = {}
		self.node_to_sons = {}
		for word in self.word_to_time:
			node_to_time[(word,)] = self.word_to_time[word]
			self.node_to_sons[(word,)] = []
		node_to_time[('EOF',)] = 1
		self.node_to_sons[('EOF',)] = []

		while len(node_to_time) > 1:
			min1 = min2 = math.inf
			node1 = node2 = ()
			for node in node_to_time:
				time = node_to_time[node]
				if time < min1:
					node2, min2 = node1, min1
					node1, min1 = node, time
				elif time < min2:
					node2, min2 = node, time

			new_node, new_time = node1 + node2, min1 + min2
			node_to_time[new_node] = new_time
			self.node_to_sons[new_node] = [node1, node2]

			del node_to_time[node1]
			del node_to_time[node2]

		self._assign_code(list(node_to_time.keys())[0], '')


	def _assign_code(self, node, code):
		if len(self.node_to_sons[node]) == 0:
			self.word_to_code[node[0]] = code
			self.code_to_word[code] = node[0]
		else:
			assert(len(self.node_to_sons[node]) == 2)
			self._assign_code(self.node_to_sons[node][0], code + '0')
			self._assign_code(self.node_to_sons[node][1], code + '1')


	def c(self, x):
		return self.word_to_code[x]


	def dc(self, cx):
		return self.code_to_word[cx]

'''
# Using the Huffman Code above
def c(x):
	# x -> C(x)
	# may replaced by any coding scheme
	return x

def dc(cx):
	# C(x) -> x
	return cx
'''

class LZ78:
	def __init__(self, s):
		self.s = s
		self.encoding = []
		self.entry_to_index = {(): -1}
		self.huffman_code = Huffman(self.s)

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
				self.encoding.append((last_index, self.huffman_code.c(cur_byte)))
				self.entry_to_index[tp] = len(self.encoding) - 1
				break

			cur_byte = self.s[cur]
			buffer.append(cur_byte)
			tp = tuple(buffer)

			if tp in self.entry_to_index:
				cur += 1
				continue

			last_index = self.entry_to_index[tp[:-1]]
			self.encoding.append((last_index, self.huffman_code.c(cur_byte)))
			self.entry_to_index[tp] = len(self.encoding) - 1
			buffer.clear()
			cur += 1

	def _find_entry(self, last_index, codeword):
		rs = [self.huffman_code.dc(codeword)]
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

	file = open('Introduction to Data Compression.txt', 'r')
	s = file.read()
	file.close()

	encoder = LZ78(s)
	encoder.encode()
	
	print('----- Statistics -----')
	print('Original file size:', len(s), 'bytes')
	print('# Encoding entries:', len(encoder.encoding), '\n')

	compression_size = 0
	for _, codeword in encoder.encoding:
		compression_size += math.log(len(encoder.encoding), 2) + len(codeword)

	print('Size after compression (bit base):', math.ceil(compression_size / 8), 'bytes')
	print('Compression rate:', math.ceil(compression_size / 8) / len(s))

	new_s = encoder.decode()

	file = open('test_LZ78.txt', 'w')
	file.write(new_s)
	file.close()
