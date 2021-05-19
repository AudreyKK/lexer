from sys import argv

# remember to do error handling for {}}
# remember to review all the fail states
# remember to do documentation
# track line numbers so you can helpfully locate errors?
# review skip_blanks should they be skip_blanks(i + 1???)
# remember to implement max length of identifiers





script, filename = argv

source = open(filename, 'r')
content = source.read()
content = content.upper()

TOKENS = ['PROGRAM', 'BEGIN', 'END', 'VAR', 'FUNCTION', 'PROCEDURE',
'RESULT', 'INTEGER', 'REAL', 'ARRAY', 'OF', 'NOT', 'IF', 'THEN',
'ELSE', 'WHILE', 'DO', 'IDENTIFIER', 'INTCONSTANT', 'REALCONSTANT',
'RELOP', 'MULOP', 'ADDOP', 'ASSIGNOP', 'COMMA', 'SEMICOLON', 'COLON',
'LPAREN', 'RPAREN', 'DOUBLEDOT', 'LBRACKET', 'RBRACKET',
'UNARYMINUS', 'UNARYPLUS', 'ENDMARKER', 'ENDOFFILE', 'EMPTY']

VALID_CHAR = '''ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890
.,;:<>/*[]+-=()}{\t '''

ALPHA = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

ALPHA_NUM = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

DIGIT = '0123456789'

WHITE_SPACE = ' \t\n'

NOT_DOT = ',;:'

RELOPS = '=<>'

MULOPS = ['*', '/', 'DIV', 'MOD', 'AND']

ADDOPS = ['+', '-', 'OR']

DIVS = '[]()'



# RPAREN, RBRACKET, IDENTIFIER, INTCONSTANT, REALCONSTANT -> ADDOP
UNARY_TEST = ['IDENTIFIER', 'RPAREN', 'RBRACKET', 'INTCONSTANT', 'REALCONSTANT']

MAX_ID = 32

n = len(content)


class Token(object):

	def __init__(self, type_index, value):
		self.type = TOKENS[type_index]
		self.value = value


class Lexer(object):

	def __init__(self):
		return
		#self.tokens = []

	def not_valid(self, index):
		return not (content[index] in VALID_CHAR)

	def is_notdot(self, index):
		return (content[index] in NOT_DOT)

	def is_blank(self, index):
		return (
			content[index] == ' ' or
			content[index] == '\t' or
			content[index] == '\n'
		)

	def skip_blank(self, index):
		while index < n and self.is_blank(index):
			index += 1
		return index

	def is_comment(self, index):
		return (
			content[index] == '{'
		)

	def skip_comment(self, index):
		while index < n and not(content[index] == '}'):
			# while loop has to run until the end of the file or until it finds }
			index += 1
		if index == n:
			print'ERROR: unmatched \'{\''
			quit()
		elif index < n:
			index += 1  # to skip the final bracket
		return index

	def is_alpha(self, index):
		return (content[index] in ALPHA)

	def is_alphanum(self, index):
		return (content[index] in ALPHA_NUM)

	def is_digit(self, index):
		return (content[index] in DIGIT)

	def is_PROGRAM(self, temp):
		return temp == 'PROGRAM'

	def is_BEGIN(self, temp):
		return temp == 'BEGIN'

	def is_END(self, temp):
		return temp == 'END'

	def is_VAR(self, temp):
		return temp == 'VAR'

	def is_FUNCTION(self, temp):
		return temp == 'FUNCTION'

	def is_PROCEDURE(self, temp):
		return temp == 'PROCEDURE'

	def is_RESULT(self, temp):
		return temp == 'RESULT'

	def is_INTEGER(self, temp):
		return temp == 'INTEGER'

	def is_REAL(self, temp):
		return temp == 'REAL'

	def is_ARRAY(self, temp):
		return temp == 'ARRAY'

	def is_OF(self, temp):
		return temp == 'OF'

	def is_NOT(self, temp):
		return temp == 'NOT'

	def is_IF(self, temp):
		return temp == 'IF'

	def is_THEN(self, temp):
		return temp == 'THEN'

	def is_ELSE(self, temp):
		return temp == 'ELSE'

	def is_WHILE(self, temp):
		return temp == 'WHILE'

	def is_DO(self, temp):
		return temp == 'DO'


	def GetNextToken(self):

		# initialize variables
		i = 0
		last_token = Token(36, 'n/a')

		# q0 start state
		while i < n:
		
		    # if content[i] == \n then increment line count

			#q1 blank or valid char
			i = self.skip_blank(i)
			if i < n and self.not_valid(i):
				# failstate
				print'ERROR: invalid character found '

			# q3 encountering a { beginning of comment
			elif i < n and self.is_comment(i):
				i = self.skip_comment(i)

			# q4 through 22. All 17 keywords and IDENTIFIER as else case
			elif i < n and self.is_alpha(i):
				temp = ''
				while i < n and self.is_alphanum(i) and len(temp) <= MAX_ID:
					# TODO: check for appropriate spacers are present around keywords
					# TODO: at i + 1 to the arguments of skip_blanks
					temp = temp + content[i]
					if self.is_PROGRAM(temp):
						#self.tokens.append(Token(0, 'None'))
						last_token = Token(0, 'None')
						yield last_token
						temp = ''
						i = self.skip_blank(i + 1)
					elif self.is_BEGIN(temp):
						#self.tokens.append(Token(1, 'None'))
						last_token = Token(1, 'None')
						yield last_token
						temp = ''
						i = self.skip_blank(i + 1)
					elif self.is_END(temp):
						#self.tokens.append(Token(2, 'None'))
						last_token = Token(2, 'None')
						yield last_token
						temp = ''
						i = self.skip_blank(i + 1)
					elif self.is_VAR(temp):
						#self.tokens.append(Token(3, 'None'))
						last_token = Token(3, 'None')
						yield last_token
						temp = ''
						i = self.skip_blank(i + 1)
					elif self.is_FUNCTION(temp):
						#self.tokens.append(Token(4, 'None'))
						last_token = Token(4, 'None')
						yield last_token
						temp = ''
						i = self.skip_blank(i + 1)
					elif self.is_PROCEDURE(temp):
						#self.tokens.append(Token(5, 'None'))
						last_token = Token(5, 'None')
						yield last_token
						temp = ''
						i = self.skip_blank(i + 1)
					elif self.is_RESULT(temp):
						#self.tokens.append(Token(6, 'None'))
						last_token = Token(6, 'None')
						yield last_token
						temp = ''
						i = self.skip_blank(i + 1)
					elif self.is_INTEGER(temp):
						#self.tokens.append(Token(7, 'None'))
						last_token = Token(7, 'None')
						yield last_token
						temp = ''
						i = self.skip_blank(i + 1)
					elif self.is_REAL(temp):
						#self.tokens.append(Token(8, 'None'))
						last_token = Token(8, 'None')
						yield last_token
						temp = ''
						i = self.skip_blank(i + 1)
					elif self.is_ARRAY(temp):
						#self.tokens.append(Token(9, 'None'))
						last_token = Token(9, 'None')
						yield last_token
						temp = ''
						i = self.skip_blank(i + 1)
					elif self.is_OF(temp):
						#self.tokens.append(Token(10, 'None'))
						last_token = Token(10, 'None')
						yield last_token
						temp = ''
						i = self.skip_blank(i + 1)
					elif self.is_NOT(temp):
						#self.tokens.append(Token(11, 'None'))
						last_token = Token(11, 'None')
						yield last_token
						temp = ''
						i = self.skip_blank(i + 1)
					elif self.is_IF(temp):
						#self.tokens.append(Token(12, 'None'))
						last_token = Token(12, 'None')
						yield last_token
						temp = ''
						i = self.skip_blank(i + 1)
					elif self.is_THEN(temp):
						#self.tokens.append(Token(13, 'None'))
						last_token = Token(13, 'None')
						yield last_token
						temp = ''
						i = self.skip_blank(i + 1)
					elif self.is_ELSE(temp):
						#self.tokens.append(Token(14, 'None'))
						last_token = Token(14, 'None')
						yield last_token
						temp = ''
						i = self.skip_blank(i + 1)
					elif self.is_WHILE(temp):
						#self.tokens.append(Token(15, 'None'))
						last_token = Token(15, 'None')
						yield last_token
						temp = ''
						i = self.skip_blank(i + 1)
					elif self.is_DO(temp):
						#self.tokens.append(Token(16, 'None'))
						last_token = Token(16, 'None')
						yield last_token
						temp = ''
						i = self.skip_blank(i + 1)
					elif i < n:
						i += 1

				# IDENTIFIER accept state
				if i < n + 1 and (0 < len(temp) <= MAX_ID):
					#self.tokens.append(Token(17, temp))
					last_token = Token(17, temp)
					yield last_token
					temp = ''
					i = self.skip_blank(i)

			# q23
			elif i < n and self.is_digit(i):
				temp = ''

				# q23
				while i < n and self.is_digit(i):
					temp = temp + content[i]
					i += 1

					# INTC accept state
					if i < n and (self.is_comment(i) or self.is_blank(i) or
						content[i] in ADDOPS or content[i] in MULOPS or
						content[i] in RELOPS or self.is_notdot(i)):
						#self.tokens.append(Token(18, temp))
						last_token = Token(18, temp)
						yield last_token
						temp = ''
						i = self.skip_blank(i)

					# q24
					elif i < n and content[i] == '.':
						dot_temp = ''
						dot_temp = content[i]
						i += 1

						# accept state DOUBLEDOT and INTCONSTANT
						if i < n and content[i] == '.':
							#self.tokens.append(Token(18, temp))
							last_token = Token(18, temp)
							yield last_token
							#self.tokens.append(Token(29, 'None'))
							last_token = Token(29, 'None')
							yield last_token
							temp = ''
							i += 1

						# q25
						elif i < n and self.is_digit(i):
							temp = temp + dot_temp
							while i < n and self.is_digit(i):
								temp = temp + content[i]
								i += 1

							# REALC accept state
							if i < n and (self.is_comment(i) or self.is_blank(i) or
							content[i] in ADDOPS or content[i] in MULOPS or
							content[i] in RELOPS or self.is_notdot(i)):
									#self.tokens.append(Token(19, temp))
									last_token = Token(19, temp)
									yield last_token
									temp =''
									i = self.skip_blank(i)

							# q26
							elif i < n and content[i] == 'E':
								temp = temp + content[i]
								i += 1

								# q27
								if i < n and (content[i] == '+' or content[i] == '-'):
									temp = temp + content[i]
									i += 1

									# q28
									if i < n and self.is_digit(i):
										while i < n and self.is_digit(i):
											temp = temp + content[i]
											i += 1

										# REALC accept state
										if i < n and (self.is_blank(i) or
										self.is_comment(i) or self.is_notdot(i) or
										content[i] in ADDOPS or
										content[i] in MULOPS or
										content[i] in RELOPS):
											#self.tokens.append(Token(19, temp))
											last_token = Token(19, temp)
											yield last_token
											temp = ''
											i = self.skip_blank(i)

										# REALC fail state
										else:
											print'ERROR: REALC fail state bad character'
											quit()

									elif i < n and not(self.is_digit(i)):
										last_token = Token(19, temp)
										yield last_token
										temp = ''
										i = self.skip_blank(i)
								# q28
								elif i < n and self.is_digit(i):
									while i < n and self.is_digit(i):
										temp = temp + content[i]
										i += 1

									# REALC accept state
									if i < n and (self.is_blank(i) or
									self.is_comment(i) or self.is_notdot(i) or
									content[i] in ADDOPS or
									content[i] in MULOPS or
									content[i] in RELOPS):
										#self.tokens.append(Token(19, temp))
										last_token = Token(19, temp)
										yield last_token
										temp = ''
										i = self.skip_blank(i)

									# fail state
									else:
										print'ERROR: REALC fail state bad character'
										quit()
								else:
									print'ERROR: REALC fail state bad character'
									quit()
						# fail state dot
						else:
							print'bad character index: %r' % i

					# q26
					elif i < n and content[i] == 'E':
						temp = temp + content[i]
						i += 1

						# q27
						if i < n and (content[i] == '+' or content[i] == '-'):
							temp = temp + content[i]
							i += 1

							# q28
							if i < n and self.is_digit(i):
								while i < n and self.is_digit(i):
									temp = temp + content[i]
									i += 1

								# REALC accept state
								if i < n and (self.is_blank(i) or self.is_comment(i) or
								self.is_notdot(i) or content[i] in ADDOPS or
								content[i] in MULOPS or content[i] in RELOPS):
									last_token = Token(19, temp)
									yield last_token
									temp = ''
									i = self.skip_blank(i)

								# fail state
								else:
									print'ERROR: REALC fail state bad character'

							# REALC accept state
							elif i < n and self.is_alpha(i):
								last_token = Token(19, temp)
								yield last_token
								temp = ''
								i = self.skip_blank(i)
						# q28
						elif i < n and self.is_digit(i):
							while i < n and self.is_digit(i):
								temp = temp + content[i]
								i += 1

							# REALC accept state
							if i < n and (self.is_blank(i) or self.is_comment(i) or
							self.is_notdot(i) or content[i] in ADDOPS or
							content[i] in MULOPS or content[i] in RELOPS):
								#self.tokens.append(Token(19, temp))
								last_token = Token(19, temp)
								yield last_token
								temp = ''
								i = self.skip_blank(i)

							# fail state
							else:
								print'ERROR: REALC fail state bad character'
								quit()

						elif i < n and not(self.is_digit(i)):
							last_token = Token(19, temp)
							yield last_token
							temp = ''
							i = self.skip_blank(i)

			elif i < n and content[i] in RELOPS:
				rel_temp = ''

				# RELOP accept state 1
				if i < n and content[i] == '=':
					last_token = Token(20, 1)
					yield last_token
					i = self.skip_blank(i + 1)

				# q29
				elif i < n and content[i] == '<':
					i += 1

					# RELOP accept state 2
					if i < n and content[i] == '>':
						last_token = Token(20, 2)
						yield last_token
						i = self.skip_blank(i + 1)

					# RELOP accept state 5
					elif i < n and content[i] == '=':
						last_token = Token(20, 5)
						yield last_token
						i = self.skip_blank(i + 1)

					# RELOP accept state 3
					else:
						last_token = Token(20, 3)
						yield last_token
						i = self.skip_blank(i)

				# q30
				elif i < n and content[i] == '>':
					i += 1

					# RELOP accept state 6
					if i < n and content[i] == '=':
						last_token = Token(20, 6)
						yield last_token
						i = self.skip_blank(i)

					# RELOP accept state 4
					else:
						last_token = Token(20, 4)
						yield last_token
						i = self.skip_blank(i)

			elif i < n and content[i] in MULOPS:
				if i < n and content[i] == '*':
					last_token = Token(21, 1)
					yield last_token
					i = self.skip_blank(i + 1)
				elif i < n and content[i] == '/':
					last_token = Token(21, 2)
					yield last_token
					i = self.skip_blank(i + 1)
				elif i < n and content[i] == 'DIV':
					last_token = Token(21, 3)
					yield last_token
					i = self.skip_blank(i + 1)
				elif i < n and content[i] == 'MOD':
					last_token = Token(21, 4)
					yield last_token
					i = self.skip_blank(i + 1)
				elif i < n and content[i] == 'AND':
					last_token = Token(21, 5)
					yield last_token
					i = self.skip_blank(i + 1)

			elif i < n and content[i] in ADDOPS:
				if i < n and content[i] == '+':

					# ADDOP 1 accept state
					if i < n and last_token.type in UNARY_TEST:
						last_token = Token(22, 1)
						yield last_token
						i = self.skip_blank(i + 1)

					# UNARYPLUS accept state
					else:
						last_token = Token(33, 'None')
						yield last_token
						i = self.skip_blank(i + 1)
				elif i < n and content[i] == '-':

					# ADDOP 2 accept state
					if i < n and last_token.type in UNARY_TEST:
						last_token = Token(22, 2)
						yield last_token
						i = self.skip_blank(i + 1)

					# UNARYMINUS accept state
					else:
						last_token = Token(32, 'None')
						yield last_token
						i = self.skip_blank(i + 1)
				elif i < n and content[i] == 'OR':

					# ADDOP 3 accept state
					last_token = Token(32, 'None')
					yield last_token
					i = self.skip_blank(i + 1)

			elif i < n and self.is_notdot(i):

				if i < n and content[i] == ':':
					i += 1

					# ASSIGNOP accept state
					if i < n and content[i] == '=':
						last_token = Token(23, 'None')
						yield last_token
						i = self.skip_blank(i + 1)

					# COLON accept state
					else:
						last_token = Token(26, 'None')
						yield last_token
						i = self.skip_blank(i)

				# COMMA accept state
				elif i < n and content[i] == ',':
					last_token = Token(24, 'None')
					yield last_token
					i = self.skip_blank(i + 1)

				# SEMICOLON accept state
				elif i < n and content[i] == ';':
					last_token = Token(25, 'None')
					yield last_token
					i = self.skip_blank(i + 1)

			elif i < n and content[i] in DIVS:
				if i < n and content[i] == '(':
					last_token = Token(27, 'None')
					yield last_token
					i = self.skip_blank(i + 1)

				# RPAREN accept state
				elif i < n and content[i] == ')':
					last_token = Token(28, 'None')
					yield last_token
					i = self.skip_blank(i + 1)

				# LBRACKET accept state
				elif i < n and content[i] == '[':
					last_token = Token(30, 'None')
					yield last_token
					i = self.skip_blank(i + 1)

				# RBRACKET accept state
				elif i < n and content[i] == ']':
					last_token = Token(31, 'None')
					yield last_token
					i = self.skip_blank(i + 1)

			elif i < n and content[i] == '.':
				i += 1
				if i < n and content[i] == '.':
					last_token = Token(29, 'None')
					yield last_token
					i = self.skip_blank(i + 1)
				else:
					# ENDMARKER accept state
					last_token = Token(34, 'None')
					yield last_token
					i = self.skip_blank(i)

			elif i < n and content[i] == '}':
				print'ERROR: unmatched \'}\''
				quit()

		last_token = Token(35, 'None')
		yield last_token




# def run_lexer():
# 	lexer = Lexer()
#
# 	for token in lexer.GetNextToken():
# 		print '(%r, %r)' % (token.type, token.value)
#
#
#
# def main():
#     run_lexer()
#
#
# main()
