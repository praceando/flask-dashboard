Aqui está o template ajustado para o seu projeto de dashboard com Flask:

---

## ✨ O que foi feito?

Desenvolvida uma API em Flask que, ao receber o ID do usuário, gera um dashboard estilo BI em HTML. O dashboard exibe dados agregados e gráficos baseados nas interações e eventos do usuário.

- [X] 📝 Criação/Atualização de funcionalidade
- [ ] 🐛 Correção de bug
- [ ] 🛠 Refatoração de código

## 📝 Descrição detalhada

- Criação de endpoints para receber o ID do usuário e gerar o relatório correspondente.
- Implementação de visualizações de dados (gráficos e métricas) no HTML, utilizando os dados processados.
- Adição de gráficos que representam:
  - Top 5 eventos com maior número de avaliações
  - Distribuição de faixa etária e gênero dos consumidores
  - Eventos por categoria
  - Média de notas por evento

## 🔍 Como testar?

- Passos para testar:
  1. Clone o repositório e navegue até a branch `main`
  2. Instale as dependências com `pip install -r requirements.txt`
  3. Execute `python app.py`
  4. Abra o navegador e acesse `http://ec2-52-204-64-214.compute-1.amazonaws.com:5001/dashboard/<user_id>`, substituindo `<user_id>` pelo ID do usuário que deseja visualizar.

## ⚠ Informações adicionais

Nenhuma informação adicional.

## 📸 Screenshot (opcional)
<div align="center">
<img src="https://github.com/praceando/flask-dashboard/blob/main/exemplo_dashboard.jpg" width="300">
</div>


## ✅ Checklist

- [X] Testes foram criados/adaptados.
- [X] O código está de acordo com o guia de estilo do projeto.
- [ ] A documentação foi atualizada, se necessário.

## 🎯 Issue relacionada

<!-- Se houver, link da issue associada ao PR. -->

## 💬 Comentários

Verificar se as visualizações e as métricas estão de acordo com os dados retornados pela API para garantir a precisão do dashboard.