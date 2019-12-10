# Instalando o virual env
pip3 install --user virtualenv
# Criando o ambiente virtual
virtualenv ambiente
# Ativando o ambiente virtual
source ambiente/bin/activate
# Instalando o rpyc
pip3 install rpyc
# Criando diretório e arquivo para base de dados de login.
#mkdir -p banco/
#touch banco/logins.txt
# Criando diretório base para as homes dos usuários.
#mkdir -p home/root
