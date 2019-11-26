class User():

	login = ''
	status = False
	dir_corrente='$ '

	def __init__(login='user', status=False, dir_corrente='$ '):

		self.login = login
		self.status=status
		self.dir_corrente=dir_corrente