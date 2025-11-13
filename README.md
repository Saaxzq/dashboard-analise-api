# 🛍️ Dashboard Interativo de Análise de E-commerce (ETL com API)

**Link para o Dashboard Ao Vivo:** [https://dmmqfwkneuiqrexjakw7mb.streamlit.app/](https://dmmqfwkneuiqrexjakw7mb.streamlit.app/)

Este projeto é um dashboard web interativo para análise de dados de produtos de e-commerce, construído inteiramente em Python. O aplicativo demonstra um processo completo de **ETL** (Extract, Transform, Load), buscando dados ao vivo de uma API pública.

---

## 📸 Screenshots

<div style="display: flex; flex-wrap: wrap; justify-content: center; gap: 20px;">
    <img src="https://github.com/user-attachments/assets/e54669c2-00e5-49ed-a456-79e025402ca6" alt="Dashboard View 1" style="max-width: 48%; height: auto; border: 1px solid #ddd; border-radius: 8px;">
    <img src="https://github.com/user-attachments/assets/ea40ef8c-6da0-4e2e-82c5-8c45cb1c6a40" alt="Dashboard View 2" style="max-width: 48%; height: auto; border: 1px solid #ddd; border-radius: 8px;">
</div>

</div>

---

## 🎯 Visão Geral do Projeto

O objetivo principal é demonstrar habilidades de ponta-a-ponta em um projeto de dados:
1.  **Engenharia de Dados (ETL):** Conectar a uma fonte de dados externa (API), tratar e modelar os dados.
2.  **Análise de Dados:** Agregar e resumir os dados para extrair insights (preço médio, avaliações, etc.).
3.  **Data Visualization:** Criar uma interface de usuário (UI) interativa e visualmente agradável para apresentar as descobertas.

---

## ⚙️ Processo ETL (Extract, Transform, Load)

Este projeto utiliza um pipeline ETL em tempo real cada vez que os dados são carregados:



* **(E) Extract:** Os dados são extraídos "ao vivo" da [Fake Store API](https://fakestoreapi.com/) usando a biblioteca `requests`.
* **(T) Transform:** Os dados brutos (em formato JSON) são processados e limpos usando a biblioteca `pandas`:
    * Conversão de JSON para DataFrame.
    * "Achatamento" (Flattening) de dados JSON aninhados (ex: `rating`).
    * Tradução de categorias (de inglês para português).
    * Renomeação e padronização de colunas (ex: `price` -> `Preço`).
* **(L) Load:** Os dados transformados são carregados diretamente no front-end do **Streamlit** para visualização, preenchendo os cards de métricas, gráficos e tabelas de resumo.

---

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python
* **Interface Web (UI):** Streamlit
* **Extração de Dados:** Requests (para consumir a API)
* **Manipulação e Análise (ETL):** Pandas
* **Visualização de Dados:** Altair (para gráficos interativos sem "zoom-scroll")
* **Estilização:** CSS customizado (para os "cards" das métricas)
* **Hospedagem (Deploy):** Streamlit Community Cloud

---

## 🚀 Como Executar Localmente

Se você quiser executar este projeto em sua própria máquina:

1.  **Clone o repositório:**
    ```bash
    git clone [COLOQUE A URL DO SEU REPOSITÓRIO GIT AQUI]
    cd [NOME-DA-PASTA-DO-PROJETO]
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows: venv\Scripts\activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Execute o app Streamlit:**
    ```bash
    streamlit run app.py
    ```
