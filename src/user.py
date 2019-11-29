import json

class User():

	login = ''
	status = False
	dir_corrente='$ '
	dir_padrao='home/'

	def __init__(self, login='user', status=False, dir_corrente='$ ', \
		dir_padrao='$ ', grupo_root=False):

		self.login = login
		self.status = status
		self.dir_corrente = dir_corrente
		self.dir_padrao = dir_padrao
		self.grupo_root = grupo_root

	# Converte as informações do usuário para JSON.
	def usuario_json(self):
		
		data = {}
		data['login'] = self.login
		data['status'] = self.status
		data['dir_corrente'] = self.dir_corrente
		data['dir_padrao'] = self.dir_padrao
		data['grupo_root'] = self.grupo_root
		return json.dumps(data)
	
	def json_loads(self, arquivo):

		data = json.loads(arquivo)
		usuario = User(data['login'], data['status'], data['dir_corrente'], \
			data['dir_padrao'], data['grupo_root'])
		return usuario