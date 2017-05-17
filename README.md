## Utilização de técnicas de Aprendizado de Máquina aliadas aos saberes tradicionais para apoio ao processo de inovação na produção de cachaça artesanal em Abreus - MG

___Projeto de Extensão Edital 08/2017 - IF Sudeste MG, Campus Barbacena___

__Orientador:__ <a href="http://lattes.cnpq.br/3995585094514614" target="_blank">Prof. Rafael José de Alencar Almeida</a><br />
__Bolsista:__ <a href="http://lattes.cnpq.br/4539575610533576" target="_blank">Luciano Carlos de Paiva</a>

<img align="right" width="50%" src="http://aprendizadodemaquina.com.br/grafico_aguradente.png?v=3" alt="Gráfico aprendizado de máquina aplicado à produção de cachaça">

<p>Trabalho baseado em processos de cunho científico, cultural e educativo junto à comunidade de produtores de cachaça artesanal de Abreus / MG, para o mapeamento dos fatores e parâmetros envolvidos no desenvolvimento das variedades do produto, correlacionados à sua qualidade sensorial. Estes indicadores serão utilizados no desenvolvimento de uma ferramenta de software baseada em técnicas de inteligência artificial para mapear o impacto de cada variável de produção na qualidade do produto final, e possibilitar o uso de simulações durante o desenvolvimento de novos tipos de cachaça – proporcionando orientações quantitativas a serem combinadas com os saberes tradicionais na inovação do produto, e reduzindo os custos dos processos de experimentação durante a produção.</p>

## Configuração e instalação

Passos para configurar o ambiente e executar o software:

<p>Faça o download do <a href="https://conda.io/miniconda.html" target="_blank">Miniconda</a> a partir do site oficial, de acordo com seu sistema operacional. Como o conda permite a criação de vários ambientes com versões diferente, instale a versão com o Python mais usual. A instalação é bem simples. No linux, necessita apenas adicionar permissão de execução no script e executá-lo para começar a instalação, com seguinte comando:</p>

<pre>
$ chmod +x nome_do_arquivo_instalacao.sh
$ ./nome_do_arquivo_instalacao.sh
</pre>

<p>
Clone ou baixe este repositório e descompacte na pasta:
</p>
<pre>git clone https://github.com/rafjaa/aprendizado_maquina_aguardente.git</pre>

<p>Dentro da pasta do projeto possui o arquivo “requirements.txt”, que contém a lista de pacotes necessários para execução do mesmo. O comando abaixo cria o ambiente virtual com nome ‘mla’, utilizando Python 3.5 e instala todos os pacotes listado no arquivo “requirements.txt”.</p>
<pre>
$ conda create -n mla python=3.5 --file requirements.txt
</pre>
<p>
Para utilizar o ambiente criado anteriormente, ele precisa estar ativado. Usamos o seguinte comando:
</p>
<pre>
$ source activate mla
</pre>

<p>
A partir de agora, pode se executar qualquer <i>script</i> dentro do ambiente!
</p>


