from flask import Flask, render_template
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
import seaborn as sns
import psycopg2
import pymongo as mongo
from dotenv import load_dotenv
import os

app = Flask(__name__)


load_dotenv(dotenv_path=".env")
# Aplicando o tema e a paleta de cores
sns.set_theme(style="whitegrid")
# Configuração de cores da paleta
palette = ["#F5A9B8", "#6BB08D", "#E34D6E", "#FFDDE5", "#F6E1A3", "#CACACA"]

# Função para executar uma query e retornar o resultado em um DataFrame
def postgresql_query(query:str,user_id:int) -> pd.DataFrame:
    try:
        conn = psycopg2.connect(os.getenv("LINK_2ANO_POSTGRESQL"))
        cursor = conn.cursor()
        
        cursor.execute(query,(user_id,))
        data = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        return pd.DataFrame(data, columns=columns)

    except Exception as e:
        print("Erro ao conectar ao banco de dados:", e)
    finally:
        cursor.close()
        conn.close()


def mongodb_query(collection:str, pipeline:list[dict], ) -> pd.DataFrame:    
    #puxando dados do mongoDB
    try:
        conn = mongo.MongoClient(os.getenv("LINK_MONGO"))
        db = conn["dbPraceando"]
        collection = db[collection]
        
        cursor = collection.aggregate(pipeline)
        return pd.DataFrame(list(cursor))
        
    except Exception as e:
        print("Erro ao conectar ao MongoDB:", e)
        return None
    finally:
        conn.close()
        
# Função para renderizar gráficos e convertê-los em imagens base64 para HTML
def render_chart(fig):
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    chart_img = base64.b64encode(buf.getvalue()).decode('utf8')
    plt.close(fig)
    return chart_img

# Função de gráfico: Big Number - Média das Notas de Todos os Eventos do Anunciante
def big_number_media_nota_total(user_id):
    pipeline = [
    {"$lookup": {
        "from": "evento",
        "localField": "cd_evento",
        "foreignField": "cd_evento",
        "as": "evento"
    }},
    {"$unwind": "$evento"},
    {"$match": {"evento.cd_anunciante": user_id}},
    {"$group": {"_id": None, "media_nota": {"$avg": "$nota"}}}
]
    
    result = mongodb_query("avaliacao", pipeline)  
    media_nota_total_value = result["media_nota"].iloc[0] if not result.empty else 0

    return media_nota_total_value

def big_number_total_eventos(user_id):
    query = """
    SELECT 
        e.id_evento,
        e.nm_evento,
        e.dt_inicio AS data_inicio,
        e.dt_fim AS data_fim,
        e.qt_interesse AS total_interesse_registrado,
        COUNT(i.id_interesse) AS total_interesse_real,
        COUNT(c.id_compra) AS total_compras
    FROM 
        evento e
    LEFT JOIN 
        interesse i ON e.id_evento = i.cd_evento
    LEFT JOIN 
        compra c ON e.id_evento = c.cd_evento
    WHERE 
        e.cd_anunciante = %s
    GROUP BY 
        e.id_evento, e.nm_evento, e.dt_inicio, e.dt_fim, e.qt_interesse
    ORDER BY 
        e.dt_inicio;
    """
    
    result = postgresql_query(query, user_id)
    return result['id_evento'].nunique()

def big_number_total_interesse(user_id):
    query = """
    SELECT 
        e.id_evento,
        e.nm_evento,
        e.dt_inicio AS data_inicio,
        e.dt_fim AS data_fim,
        e.qt_interesse AS total_interesse_registrado,
        COUNT(i.id_interesse) AS total_interesse_real,
        COUNT(c.id_compra) AS total_compras
    FROM 
        evento e
    LEFT JOIN 
        interesse i ON e.id_evento = i.cd_evento
    LEFT JOIN 
        compra c ON e.id_evento = c.cd_evento
    WHERE 
        e.cd_anunciante = %s
    GROUP BY 
        e.id_evento, e.nm_evento, e.dt_inicio, e.dt_fim, e.qt_interesse
    ORDER BY 
        e.dt_inicio;
    """
    
    result = postgresql_query(query, user_id)
    return result['total_interesse_real'].sum()

def big_number_total_compras(user_id):
    query = """
    SELECT 
        e.id_evento,
        e.nm_evento,
        e.dt_inicio AS data_inicio,
        e.dt_fim AS data_fim,
        e.qt_interesse AS total_interesse_registrado,
        COUNT(i.id_interesse) AS total_interesse_real,
        COUNT(c.id_compra) AS total_compras
    FROM 
        evento e
    LEFT JOIN 
        interesse i ON e.id_evento = i.cd_evento
    LEFT JOIN 
        compra c ON e.id_evento = c.cd_evento
    WHERE 
        e.cd_anunciante = %s
    GROUP BY 
        e.id_evento, e.nm_evento, e.dt_inicio, e.dt_fim, e.qt_interesse
    ORDER BY 
        e.dt_inicio;
    """
    
    result = postgresql_query(query, user_id)
    return result['total_compras'].sum()


# Função de gráfico: Ranking dos Eventos com Maior Número de Avaliações
def grafico_eventos_populares(user_id):
    
    pipeline = [
        {"$lookup": {
            "from": "evento",
            "localField": "cd_evento",
            "foreignField": "cd_evento",
            "as": "evento"
        }},
        {"$unwind": "$evento"},
        {"$match": {"evento.cd_anunciante": user_id}},
        {"$group": {
            "_id": "$cd_evento",
            "total_avaliacoes": {"$sum": 1},
            "nome_evento": {"$first": "$evento.nm_evento"},
            "media_nota": {"$avg": "$nota"}
        }},
        {"$sort": {"total_avaliacoes": -1}},
        {"$limit": 5}
    ]
    
    result = mongodb_query("avaliacao", pipeline)

    if result.empty:
        print("DataFrame df_eventos_populares está vazio.")
        return None
    
    # Certifique-se de que os campos estão no tipo correto
    result['nome_evento'] = result['nome_evento'].astype(str)
    result['total_avaliacoes'] = result['total_avaliacoes'].astype(int)

    fig, ax = plt.subplots()
    sns.barplot(data=result, x='total_avaliacoes', y='nome_evento', ax=ax, palette=palette)
    ax.set_xlabel("Total de Avaliações")
    ax.set_ylabel("Nome do Evento")    
    fig.patch.set_alpha(0)  # Remover o fundo
    ax.set_facecolor("none")  # Remover o fundo do eixo
    
    return render_chart(fig)


# Função de gráfico: Média de Notas por Evento
def grafico_media_notas_evento(user_id):
    
    pipeline = [
    {"$lookup": {
        "from": "evento",
        "localField": "cd_evento",
        "foreignField": "cd_evento",
        "as": "evento"
    }},
    {"$unwind": "$evento"},
    {"$match": {"evento.cd_anunciante": user_id}},
    {"$group": {"_id": "$cd_evento", "media_nota": {"$avg": "$nota"}}},
    {"$sort": {"media_nota": -1}}
]
    
    result = mongodb_query("avaliacao", pipeline)
    
    fig, ax = plt.subplots()
    sns.barplot(data=result, x='media_nota', y='_id', ax=ax, palette=palette)
    ax.set_xlabel("Média de Nota")
    ax.set_ylabel("ID do Evento")
    fig.patch.set_alpha(0)  # Remove o fundo da figura
    ax.set_facecolor("none")  # Remove o fundo do eixo
    return render_chart(fig)

# Gráfico: Faixa Etária dos Consumidores
def grafico_faixa_etaria_pizza(user_id):
    
    query = """
    SELECT 
        CASE 
            WHEN DATE_PART('year', AGE(c.dt_nascimento)) BETWEEN 0 AND 10 THEN '0-10'
            WHEN DATE_PART('year', AGE(c.dt_nascimento)) BETWEEN 11 AND 20 THEN '11-20'
            WHEN DATE_PART('year', AGE(c.dt_nascimento)) BETWEEN 21 AND 30 THEN '21-30'
            WHEN DATE_PART('year', AGE(c.dt_nascimento)) BETWEEN 31 AND 40 THEN '31-40'
            WHEN DATE_PART('year', AGE(c.dt_nascimento)) BETWEEN 41 AND 50 THEN '41-50'
            WHEN DATE_PART('year', AGE(c.dt_nascimento)) BETWEEN 51 AND 60 THEN '51-60'
            WHEN DATE_PART('year', AGE(c.dt_nascimento)) BETWEEN 61 AND 70 THEN '61-70'
            WHEN DATE_PART('year', AGE(c.dt_nascimento)) > 70 THEN '71+'
            ELSE 'Desconhecida'
        END AS faixa_etaria,
        COUNT(*) AS total_consumidores
    FROM 
        consumidor c
    INNER JOIN 
        interesse i ON c.id_consumidor = i.cd_consumidor
    INNER JOIN 
        evento e ON i.cd_evento = e.id_evento
    WHERE 
        e.cd_anunciante = %s
    GROUP BY 
        faixa_etaria
    ORDER BY 
        faixa_etaria;
    """
    
    result = postgresql_query(query,user_id)
    
    fig, ax = plt.subplots()
    ax.pie(
        result['total_consumidores'], 
        labels=result['faixa_etaria'], 
        autopct='%1.1f%%', 
        startangle=90, 
        colors=palette[:len(result)]
    )
    fig.patch.set_alpha(0)  # Remove o fundo da figura
    return render_chart(fig)

# Gráfico: Gênero dos Consumidores
def grafico_genero(user_id):
    
    query = """
    SELECT 
        c.id_consumidor,
        c.nm_nickname AS nickname_consumidor,
        DATE_PART('year', AGE(c.dt_nascimento)) AS idade,
        g.ds_genero AS genero,
        COUNT(i.id_interesse) AS total_eventos_interessados
    FROM 
        interesse i
    INNER JOIN 
        consumidor c ON i.cd_consumidor = c.id_consumidor
    INNER JOIN 
        usuario u ON c.id_consumidor = u.id_usuario
    LEFT JOIN 
        genero g ON u.cd_genero = g.id_genero
    INNER JOIN 
        evento e ON i.cd_evento = e.id_evento
    WHERE 
        e.cd_anunciante = %s
    GROUP BY 
        c.id_consumidor, c.nm_nickname, c.dt_nascimento, g.ds_genero
    ORDER BY 
        idade;
    """
    
    result = postgresql_query(query,user_id)
    
    genero_counts = result['genero'].value_counts()
    fig, ax = plt.subplots()
    genero_counts.plot(kind='pie', ax=ax, autopct='%1.1f%%', colors=palette[:len(genero_counts)])
    ax.set_ylabel("")
    fig.patch.set_alpha(0)
    ax.set_facecolor("none")
    return render_chart(fig)

def grafico_eventos_categoria(user_id):
    
    query = """
    SELECT 
        t.ds_categoria AS categoria_evento,
        t.nm_tag AS tag,
        COUNT(et.id_evento_tag) AS total_eventos_com_tag
    FROM 
        evento_tag et
    INNER JOIN 
        evento e ON et.cd_evento = e.id_evento
    INNER JOIN 
        tag t ON et.cd_tag = t.id_tag
    WHERE 
        e.cd_anunciante = %s
    GROUP BY 
        t.ds_categoria, t.nm_tag
    ORDER BY 
        total_eventos_com_tag DESC;
    """
    
    result = postgresql_query(query,user_id)
    
    fig, ax = plt.subplots()
    sns.barplot(data=result, x='total_eventos_com_tag', y='tag', ax=ax, palette=palette)
    ax.set_title("Eventos por Categoria")
    ax.set_xlabel("Número de Eventos")
    ax.set_ylabel("Categoria")
    fig.patch.set_alpha(0)
    ax.set_facecolor("none")
    return render_chart(fig)


@app.route('/dashboard/<int:user_id>', methods=['GET'])
def index_page(user_id:int):
    # Big Numbers
    total_eventos = big_number_total_eventos(user_id)
    total_interesse = big_number_total_interesse(user_id)
    total_compras = big_number_total_compras(user_id)
    media_nota_total = big_number_media_nota_total(user_id)

    # Gráficos SQL
    faixa_etaria_img = grafico_faixa_etaria_pizza(user_id)
    genero_img = grafico_genero(user_id)
    categoria_img = grafico_eventos_categoria(user_id)

    # Gráficos MongoDB
    
    eventos_populares_img =  grafico_eventos_populares(user_id)
    media_notas_evento_img = grafico_media_notas_evento(user_id)

    return render_template(
        'index.html',
        total_eventos=total_eventos,
        total_interesse=total_interesse,
        total_compras=total_compras,
        media_nota_total=media_nota_total,
        faixa_etaria_img=faixa_etaria_img,
        genero_img=genero_img,
        categoria_img=categoria_img,
        eventos_populares_img=eventos_populares_img,
        media_notas_evento_img=media_notas_evento_img
    )

if __name__ == '__main__':
    app.run(debug=False,port=5001, host='0.0.0.0')


