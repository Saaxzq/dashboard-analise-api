import streamlit as st
import pandas as pd
import requests
import altair as alt


def load_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"Arquivo CSS '{file_name}' não encontrado.")


@st.cache_data
def carregar_dados():
    url = "https://fakestoreapi.com/products"

    try:
        response = requests.get(url)

        if response.status_code == 200:
            dados_json = response.json()

            dados_df = pd.DataFrame(dados_json)
            dados_df['rating_rate'] = dados_df['rating'].apply(lambda x: x['rate'])
            dados_df['rating_count'] = dados_df['rating'].apply(lambda x: x['count'])

            mapa_categorias = {
                "electronics": "Eletrônicos",
                "jewelery": "Joias",
                "men's clothing": "Roupas Masculinas",
                "women's clothing": "Roupas Femininas"
            }

            dados_df['Categoria'] = dados_df['category'].map(mapa_categorias)
            dados_df = dados_df.drop(['rating', 'image', 'category'], axis=1)

            dados_df.rename(columns={
                'id': 'ID',
                'title': 'Produto',
                'price': 'Preco',
                'description': 'Descricao',
                'rating_rate': 'Avaliacao',
                'rating_count': 'Contagem_Avaliacoes'
            }, inplace=True)

            dados_df.set_index('ID', inplace=True)

            return dados_df

        else:
            st.error(f"Erro ao buscar dados da API. Código: {response.status_code}")
            return None

    except Exception as e:
        st.error(f"Ocorreu um erro na requisição: {e}")
        return None


st.set_page_config(
    page_title="Dashboard de E-commerce",
    page_icon="🛍️",
    layout="wide"
)

load_css("style.css")

st.title("🛍️ Dashboard de Análise de E-commerce (ETL com API)")
st.markdown("Análise de produtos da *Fake Store API*.")

df = carregar_dados()

if df is not None:

    st.sidebar.header("Filtros")

    st.sidebar.subheader("Filtrar por Categoria")

    categorias_unicas = df['Categoria'].unique()
    categorias_selecionadas_map = {}

    for cat in categorias_unicas:
        categorias_selecionadas_map[cat] = st.sidebar.checkbox(cat, value=True)

    categorias_para_filtrar = [
        cat for cat, selecionado in categorias_selecionadas_map.items() if selecionado
    ]

    st.sidebar.subheader("Filtrar por Preço")
    preco_max = int(df['Preco'].max())
    preco_min = int(df['Preco'].min())

    preco_range = st.sidebar.slider(
        "Selecione o Range de Preço (R$)",
        min_value=preco_min,
        max_value=preco_max,
        value=(preco_min, preco_max)
    )

    df_filtrado = df[df['Categoria'].isin(categorias_para_filtrar)]

    df_filtrado = df_filtrado[
        (df_filtrado['Preco'] >= preco_range[0]) &
        (df_filtrado['Preco'] <= preco_range[1])
        ]

    st.header("Métricas Principais (Baseado nos Filtros)")

    if not df_filtrado.empty:
        total_produtos = df_filtrado.shape[0]
        preco_medio = df_filtrado['Preço'].mean()
        avaliacao_media = df_filtrado['Avaliação'].mean()

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(label="📦 Produtos Encontrados", value=total_produtos)

        with col2:
            st.metric(label="💵 Preço Médio", value=f"R$ {preco_medio:,.2f}")

        with col3:
            st.metric(label="⭐ Avaliação Média", value=f"⭐ {avaliacao_media:,.2f}")

        st.header("Resumo por Categoria (Baseado nos Filtros)")

        df_resumo_categoria = df_filtrado.groupby('Categoria').agg(
            Numero_de_Produtos=('Produto', 'count'),
            Preco_Medio=('Preço', 'mean'),
            Avaliacao_Media=('Avaliação', 'mean')
        ).reset_index()

        st.dataframe(
            df_resumo_categoria,
            hide_index=True,
            column_config={
                "Categoria": st.column_config.TextColumn("Categoria"),
                "Numero_de_Produtos": st.column_config.NumberColumn("Qtd. Produtos"),
                "Preco_Medio": st.column_config.NumberColumn(
                    "Preço Médio", format="R$ %.2f"
                ),
                "Avaliacao_Media": st.column_config.NumberColumn(
                    "Avaliação Média", format="⭐ %.2f"
                ),
            },
            use_container_width=True
        )

        st.header("Visualizações (Baseado nos Filtros)")

        st.subheader("Preço por Produto")
        df_grafico_preco = df_filtrado[['Produto', 'Preço']].sort_values(by='Preço', ascending=False).reset_index()
        chart = alt.Chart(df_grafico_preco).mark_bar(color="#588157").encode(
            x=alt.X('Produto', sort=None),
            y=alt.Y('Preço'),
            tooltip=['Produto', 'Preço']

        ).interactive(
            bind_y=False
        )
        st.altair_chart(chart, use_container_width=True)

        st.subheader("Avaliação vs. Popularidade (Contagem)")
        if not df_filtrado.empty:
            scatter_chart = alt.Chart(df_filtrado).mark_circle(size=60).encode(
                x=alt.X('Avaliação'),
                y=alt.Y('Contagem_Avaliações'),
                color=alt.Color('Categoria'),
                tooltip=['Produto', 'Categoria', 'Avaliação', 'Contagem_Avaliações']

            ).interactive(
                bind_x=False,
                bind_y=False
            )
            st.altair_chart(scatter_chart, use_container_width=True)

        # (A TABELA ANTIGA DE DADOS BRUTOS FOI REMOVIDA DAQUI)

    else:
        st.warning("Nenhum produto encontrado para os filtros selecionados.")
else:
    st.error("Falha ao carregar os dados. O dashboard não pode ser exibido.")