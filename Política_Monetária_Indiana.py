# Importando packs
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sb

# Carregando os dados
df = pd.read_csv('/content/Global Dataset of Inflation.csv', encoding='latin-1')


# Verificando informações
df.info()

df_india = df.loc[df['Country']=='India']

df_india.head()

# 1. Filtre o DataFrame
filtered_df = df[(df['Country'] == 'India') & (df['Series Name'] == 'Headline Consumer Price Inflation')]

# 2. Selecione as colunas apropriadas
filtered_df = filtered_df[['Country'] + [str(year) for year in range(2012, 2023)]]

# 3. Use a função melt para transformar as colunas de anos em linhas
melted_df = filtered_df.melt(id_vars=['Country'], var_name='Year', value_name='Inflation_Rate')

# 4. Defina os nomes de coluna
melted_df = melted_df.rename(columns={'Country': 'Country', 'Year': 'Year', 'Inflation_Rate': 'Inflation_Rate'})

# Resetando o índice
melted_df = melted_df.reset_index(drop=True)

# Visualize o resultado
print(melted_df)
melted_df.info()

# Carregando novos dados
Interest_Rate = pd.read_csv('/content/India_Interest_Rate.csv')
Nominal_Product_Rate = pd.read_csv('/content/Nominal_Domestic_Product_India.csv')
Real_Product_Rate = pd.read_csv('/content/Real_Domestic_Product_India.csv')

# Converta a coluna 'INDIR3TIB01STQ' para o tipo float
Interest_Rate['INDIR3TIB01STQ'] = pd.to_numeric(Interest_Rate['INDIR3TIB01STQ'], errors='coerce')
Nominal_Product_Rate['NGDPNSAXDCINQ'] = pd.to_numeric(Nominal_Product_Rate['NGDPNSAXDCINQ'], errors='coerce')
Real_Product_Rate['NGDPRNSAXDCINQ'] = pd.to_numeric(Real_Product_Rate['NGDPRNSAXDCINQ'], errors='coerce')

# Extraindo os 4 primeiros caracteres da coluna "DATE"
Interest_Rate['DATE'] = Interest_Rate['DATE'].str[:4]
Nominal_Product_Rate['DATE'] = Nominal_Product_Rate['DATE'].str[:4]
Real_Product_Rate['DATE'] = Real_Product_Rate['DATE'].str[:4]

# Renomeando colunas
Interest_Rate.rename(columns={'DATE':'Year', 'INDIR3TIB01STQ' : 'Interest Rate'}, inplace = True)
Nominal_Product_Rate.rename(columns={'DATE':'Year', 'NGDPNSAXDCINQ' : 'Nominal Product Rate'}, inplace = True)
Real_Product_Rate.rename(columns={'DATE':'Year', 'NGDPRNSAXDCINQ' : 'Real Product Rate'}, inplace = True)

# Mesclando tabelas
Monetary_Agregate_df = pd.merge(melted_df, Interest_Rate[['Year', 'Interest Rate']], on = 'Year', how = 'left')
Monetary_Agregate_df = pd.merge(Monetary_Agregate_df, Nominal_Product_Rate[['Year', 'Nominal Product Rate']], on = 'Year', how = 'left')
Monetary_Agregate_df = pd.merge(Monetary_Agregate_df, Real_Product_Rate[['Year', 'Real Product Rate']], on = 'Year', how = 'left')

Monetary_Agregate_df.head()

# A partir de DataFrame chamado Monetary_Agregate_df:

# Filtrando os dados a partir do ano-base (2012)
df = Monetary_Agregate_df[Monetary_Agregate_df['Year'] >= '2011']

# Calculando as taxas de crescimento da Nominal Product Rate e da Real Product Rate
df['Nominal Product Rate Growth'] = ((df['Nominal Product Rate'] - df['Nominal Product Rate'].shift(1)) / df['Nominal Product Rate'].shift(1)) * 100
df['Real Product Rate Growth'] = ((df['Real Product Rate'] - df['Real Product Rate'].shift(1)) / df['Real Product Rate'].shift(1)) * 100

# Criand o gráfico
plt.figure(figsize=(10, 6))
plt.plot(df['Year'], df['Nominal Product Rate Growth'], label='Nominal Product Rate Growth', marker='o')
plt.plot(df['Year'], df['Real Product Rate Growth'], label='Real Product Rate Growth', marker='s')

# Definindo os rótulos dos eixos e o título do gráfico
plt.xlabel('Year')
plt.ylabel('Rate Growth (%)')
plt.title('Variação Anual da Taxa de Crescimento do Produto Nominal e do Produto Real\n (Ano Base: 2012)')
plt.legend()

# Exibindo o gráfico
plt.grid(True)
plt.show()

# Defina os dados que você deseja plotar
years = Monetary_Agregate_df['Year']
interest_rate = Monetary_Agregate_df['Interest Rate']
inflation_rate = Monetary_Agregate_df['Inflation_Rate']

# Calcule as médias das taxas
average_interest_rate = interest_rate.mean()
average_inflation_rate = inflation_rate.mean()

# Crie o gráfico
plt.figure(figsize=(10, 6))
plt.plot(years, interest_rate, label='Interest Rate', marker='o')
plt.plot(years, inflation_rate, label='Inflation Rate', marker='s')

# Adicione as linhas pontilhadas para as médias
plt.axhline(y=average_interest_rate, color='b', linestyle='--', label=f'Média Interest Rate ({average_interest_rate:.2f})')
plt.axhline(y=average_inflation_rate, color='r', linestyle='--', label=f'Média Inflation Rate ({average_inflation_rate:.2f})')

# Defina os rótulos dos eixos e o título do gráfico
plt.xlabel('Year')
plt.ylabel('Rate Absolut Value')
plt.title('Evolução da Interest Rate e Inflation Rate por Ano')
plt.legend()  # Adicione a legenda para identificar as curvas e as médias

# Exiba o gráfico
plt.grid(True)
plt.show()

df.head(11)

# Carregando Dados
gdp = pd.read_csv("/content/gdp.csv")
juro = pd.read_csv("/content/taxa_de_juro.csv")
precos = pd.read_csv("/content/variação_precos.csv")
preco_futuro = pd.read_csv("/content/preco_futuro.csv")
producao_industrial = pd.read_csv("/content/produção_industrial.csv")
balanca = pd.read_csv("/content/balanca_comercial.csv")
desemprego = pd.read_csv("/content/india-unemployment-rate.csv")

# Mesclando Tabelas para os dados trimestrais
df_trimestral = pd.merge(gdp, juro[["DATE","INTDSRINM193N"]], on = "DATE", how = "left")
df_trimestral = pd.merge(df_trimestral, precos[["DATE","CPALTT01INQ659N"]], on = "DATE", how = "left")
df_trimestral = pd.merge(df_trimestral, producao_industrial[["DATE","INDPRINTO01GYSAM"]], on = 'DATE', how="left")
df_trimestral = pd.merge(df_trimestral,balanca[["DATE","XTEITT01INQ156S"]], on="DATE", how='left')

# Renomeando colunas
df_trimestral.rename(columns={'NAEXKP01INQ657S':'%_GDP', 'INTDSRINM193N' : 'Taxa_de_Juro', 'CPALTT01INQ659N':'%_CPI', 'INDPRINTO01GYSAM': '%_Production', 'XTEITT01INQ156S': 'Exports/Imports'}, inplace = True)

# Visualizando
df_trimestral.head(60)
