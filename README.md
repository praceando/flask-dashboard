# Flask Dashboard

## Objetivo
Este repositório contém uma API desenvolvida em Flask que, ao receber o ID de um usuário, gera um relatório estilo dashboard BI, apresentando dados sobre eventos e interações do usuário em uma página HTML. O dashboard exibe métricas gerais e gráficos que ajudam a visualizar os dados de forma intuitiva.

## Tecnologias 
O dashboard personalizado  utiliza as seguintes tecnologias:

- **Python**: Linguagem de programação, utilizada para ligar os dados com o front-end e responsável por criar os gráficos
- **HTML e CSS**: Conjunto de ferramentas utilizadas para estruturar e estilizar o site
- **PostgreSQL**: Utilizado para o armazenamento de dados relacionais, garantindo consistência e suporte a transações complexas.
- **MongoDB**: Empregado para o armazenamento de dados não relacionais, como documentos JSON, permitindo maior flexibilidade na estruturação das informações.

## Funcionalidades do Dashboard

O dashboard exibe as seguintes informações:

- **Métricas Principais**:
  - Total de Eventos
  - Total de Interesse
  - Total de Compras
  - Média de Notas

- **Gráficos**:
  - Top 5 eventos com maior número de avaliações
  - Distribuição de faixa etária dos consumidores
  - Distribuição de gênero dos consumidores
  - Eventos por categoria
  - Média de notas por evento

## Como Utilizar

1. **Clone o repositório**:

```bash
   git clone https://github.com/praceando/flask-dashboard.git
   cd flask-dashboard
 ```

2. Instalar as bibliotecas listadas no arquivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

3. **Configure as variáveis de ambiente**:
Crie um arquivo `.env` para armazenar informações de conexão com o banco de dados, se necessário.

4. **Execute a aplicação**:

 ```bash
 python app.py
 ```

5. **Acesse o dashboard**:
No navegador, vá para `http://ec2-52-204-64-214.compute-1.amazonaws.com:5001/dashboard/<user_id>`, substituindo `<user_id>` pelo ID do anunciante que deseja visualizar.

## Exemplo de Dashboard
<div align="center">
<img src="https://github.com/praceando/flask-dashboard/blob/dev/exemplo_dashboard.jpg" width="300">
</div>

---
Enviando nossos melhores insights com 95% de confiança - equipe de dados🎲!
- [Fernanda Leão](https://github.com/fernandaleaoleita)
- [Guilherme Barbosa](https://github.com/guii-barbosa)
