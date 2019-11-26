## Software para simular um servidor de arquivos ftp com utilização de python RPC e criptografia em comunicações.


### Instalação - Serão instalados os softwares virtualenv e rpyc
#### Para configurar o ambiente execute o arquivos config.sh
$ ./config.sh

### Para colocar em funcionamento, primeiro deve-se ativar o ambiente virtual.
$ source ambiente/bin/activate

### Para ativar o servidor de arquivos.
$ python3 src/arquivos.py

### Para ativar o servidor de autenticação.
$ python3 src/autenticação.py

### Para ativar o servidor de conexões.
$ python3 src/conexoes.py

### Para ativar o cliente

### Criar usuário ROOT. Para criar o usuário root deve-se executar o seguinte comando.
$ python3 src/autenticacao.py root password
