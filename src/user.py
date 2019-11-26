class User():

	login = ''
	status = False
	dir_corrente='$ '
	dir_padrao='home/'

	def __init__(self, login='user', status=False, dir_corrente='$ ', \
		grupo_root=False):

		self.login = login
		self.status = status
		self.dir_corrente = dir_corrente
		self.dir_padrao += dir_corrente
		self.grupo_root = grupo_root