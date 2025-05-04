🛍️ Web Scraper - Desafio Commercia
Este projeto é um web scraper desenvolvido para extrair informações detalhadas de um produto em uma página HTML do desafio da Infosimples. Os dados extraídos são salvos no formato JSON.

📁 Estrutura do Projeto
bash
Copiar
Editar
TESTE_ESTÁGIO/
├── src/
│   └── json_exporter/
│       ├── __pycache__/
│       └── write_json.py         # Classe responsável por salvar e estruturar o JSON
├── produto.json                  # Arquivo de saída com os dados extraídos
├── web_scrape.py                 # Script principal com o web scraping

⚙️ Como Funciona
web_scrape.py
Este é o script principal que:

Acessa a URL do produto

Utiliza BeautifulSoup para fazer o parsing do HTML

Extrai:

Título e marca do produto

Categorias e descrição

Lista de SKUs com preços e disponibilidade

Tabela de propriedades técnicas

Avaliações de clientes (nome, data, nota e texto)

Nota média geral

URL da página

Os dados são organizados em um dicionário e salvos em produto.json

write_json.py
Contém a classe Json, responsável por:

Estruturar um dicionário com os campos desejados

Salvar o dicionário em um arquivo .json no diretório raiz do projeto

▶️ Como Executar
1. Instale os pacotes necessários
Certifique-se de que você tem o Python instalado (>=3.8) e instale as dependências:

bash
Copiar
Editar
pip install requests beautifulsoup4
2. Execute o script de scraping
No terminal, rode o script web_scrape.py:

bash
Copiar
Editar
python web_scrape.py
