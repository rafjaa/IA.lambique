## Utilização de técnicas de Aprendizado de Máquina aliadas aos saberes tradicionais para apoio ao processo de inovação na produção de cachaça artesanal em Abreus - MG

___Projeto de Extensão Edital 08/2017 - IF Sudeste MG, Campus Barbacena___

__Orientador:__ <a href="http://lattes.cnpq.br/3995585094514614" target="_blank">Prof. Rafael José de Alencar Almeida</a><br />
__Bolsistas:__
- <a href="http://lattes.cnpq.br/4539575610533576" target="_blank">Luciano Carlos de Paiva</a>
- <a href="http://lattes.cnpq.br/1080835313733221" target="_blank">Érika Cristina Santos de Assis</a>

<img align="right" width="50%" src="http://aprendizadodemaquina.com.br/grafico_aguradente.png?v=3" alt="Gráfico aprendizado de máquina aplicado à produção de cachaça">

<p>Trabalho baseado em processos de cunho científico, cultural e educativo junto à comunidade de produtores de cachaça artesanal de Abreus / MG, para o mapeamento dos fatores e parâmetros envolvidos no desenvolvimento das variedades do produto, correlacionados à sua qualidade sensorial. Estes indicadores serão utilizados no desenvolvimento de uma ferramenta de software baseada em técnicas de inteligência artificial para mapear o impacto de cada variável de produção na qualidade do produto final, e possibilitar o uso de simulações durante o desenvolvimento de novos tipos de cachaça – proporcionando orientações quantitativas a serem combinadas com os saberes tradicionais na inovação do produto, e reduzindo os custos dos processos de experimentação durante a produção.</p>

## Configuração e instalação 
<p>Caso ainda não tenha, instale a versão do Python3 disponível em https://www.python.org/downloads, de acordo com sua distribuição.</p> 
<p>Vamos utilizar o <a href=https://virtualenv.pypa.io/en/stable/>virtualenv</a>, onde será possível a instalação de todas as dependências utilizadas no programa em um ambiente virtual. No linux, em distribuições baseada no Debian,  o Virtualenv pode ser instalado com o comando:</p>
<pre>$ sudo apt-get install virtualenv</pre>

Clone ou baixe este repositório e descompacte na pasta:
<pre>$ git clone https://github.com/rafjaa/aprendizado_maquina_aguardente.git </pre>

Entre na pasta do projeto e crie um ambiente virtual com virtualenv, especificando a versão utilizada do Python:
<pre>$ virtualenv env --python=python3</pre>

Após a criação é necessário ativar o ambiente, o mesmo pode ser realizado com o comando:
<pre>$ source ./env/bin/activate</pre>

Com o ambiente virtual ativado, instale as dependências, listadas no arquivo "requirements.txt":
<pre>(env)$ pip install -r ./requirements.txt</pre>

Com o ambiente configurado, entre na pasta "/app" e execute o arquivo "server.py". Após, abra o navegador e vá para o endereço: http://127.0.0.1:5000:
<pre>(env)$ python server.py</pre>

