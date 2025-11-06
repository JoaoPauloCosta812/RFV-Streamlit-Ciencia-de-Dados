# Análise RFV – Segmentação de Clientes

## 📘 Descrição do Projeto
Esta aplicação interativa em **Streamlit** realiza a **análise RFV (Recência, Frequência e Valor)**, técnica essencial de marketing e CRM para segmentação de clientes com base no comportamento de compra.

Com o app, é possível **carregar uma base de dados**, calcular automaticamente as métricas **R, F e V**, e gerar uma **tabela segmentada por quartis (A, B, C, D)** — identificando os clientes mais valiosos, os regulares e os inativos.  

Além disso, o sistema sugere **ações de marketing personalizadas** e permite **baixar o resultado completo em Excel**.

---

## 🚀 Funcionalidades Principais

✅ **Upload de Arquivo (.csv ou .xlsx)**  
- Colunas esperadas: `ID_cliente`, `DiaCompra`, `CodigoCompra`, `ValorTotal`

🧮 **Cálculo Automático das Métricas RFV**
- **Recência (R):** dias desde a última compra  
- **Frequência (F):** total de compras no período  
- **Valor (V):** soma dos gastos do cliente  

🔤 **Classificação Automática por Quartis (A, B, C, D)**  
🧩 **Geração do RFV Score (ex: AAA, BCD, DDA...)**  
🎯 **Sugestões de Ações de Marketing por Perfil**  
📊 **Gráficos e Cards de Métricas Rápidas**
- Data mais recente, total gasto e número de clientes  
📥 **Download em Excel** (`RFV_resultado.xlsx`)

---

## 🖥️ Tecnologias Utilizadas

| Categoria | Ferramenta |
|------------|-------------|
| Linguagem | **Python 3.11** |
| Framework Web | **Streamlit 1.39** |
| Manipulação de Dados | **pandas**, **numpy** |
| Exportação Excel | **xlsxwriter** |
| Visualização / Layout | **Streamlit Components + CSS customizado** |
| Imagens e Gráficos | **Pillow (PIL)** |

---

## 🎨 Layout e Design
O layout foi mantido no formato clássico do Streamlit, mas com aprimoramentos de visual e usabilidade:

- Sidebar com upload e instruções  
- Cards de métricas em destaque (clientes, data, valor total)  
- Cores neutras e ícones para melhor leitura  
- Estrutura de seções por etapas:  
  **Recência → Frequência → Valor → RFV → Marketing → Download**

---

## 📈 Exemplo de Uso

1. Faça upload de um arquivo `.csv` com os dados de clientes e compras.  
2. A aplicação calcula automaticamente **Recência, Frequência e Valor**.  
3. São gerados grupos e scores RFV para cada cliente.  
4. Visualize as ações de marketing recomendadas.  
5. Baixe os resultados segmentados em Excel com um clique.
