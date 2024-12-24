import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

'''El siguiente código proporciona una herramienta para el análisis de datos y obtención de gráficas 
a partir de resultadosde área foliar remanente en un ensayo de no escogencia para evaluar el efecto
antialimentario de un extracto etanólico de Lippia alba contra Spodoptera frugiperda'''

### Procesamiento y organización de los datos
## Cargar archivo
file_name = "C:/Users/USER/Desktop/Folder/file.xlsx"  # Ruta del archivo con los datos

## Crear dataframes para el conjunto de datos del ensayo de no escogencia
df_area = pd.read_excel(file_name, sheet_name="NE")  # Areas remanentes del ensayo
df_wei = pd.read_excel(file_name, sheet_name="NE_wei")  # Peso total de las larvas
df_life = pd.read_excel(file_name, sheet_name="NE_mort")  # Número de larvas vivas
df_fed = pd.read_excel(file_name, sheet_name="NE_reg")  # Número de hojas comidas

# Renombrar las columnas para solucionar el problema de las celdas fusionadas
df_area.rename(columns={"Area foliar (cm^2)": "Control",
                         "Unnamed: 2": "Lippia",
                         "Unnamed: 3": "Insecticida"}, inplace=True)

# Eliminar las antiguas líneas de título del archivo original
df_area.drop(index=0, inplace=True)

# Crear subdataframes para separar los datos según el tiempo de lectura
df_area_0h = df_area[df_area['Tiempo'] == '0 h']
df_area_48h = df_area[df_area['Tiempo'] == '48 h']

# Transformar los subdataframes a formato largo en los casos necesarios
df_long_area_0h = df_area_0h.melt(id_vars="Muestra",                 # Dataframe de area remanente a las 0 h
                                    value_vars=["Control", "Lippia", "Insecticida"],
                                    var_name="Tratamiento",
                                    value_name="Valor")
df_long_area_48h = df_area_48h.melt(id_vars="Muestra",               # Dataframe de area remanente a las 48 h
                                      value_vars=["Control", "Lippia", "Insecticida"],
                                      var_name="Tratamiento",
                                      value_name="Valor")
df_long_life = df_life.melt(id_vars='Tiempo',                       # Dataframe de larvas vivas a lo largo del tiempo
                                    value_vars=["Control", "Lippia", "Insecticida"],
                                    var_name="Tratamiento",
                                    value_name="Numero")
df_long_fed = df_fed.melt(id_vars='Tiempo',                         # Dataframe de discos comidos a lo largo del tiempo
                                    value_vars=["Control", "Lippia", "Insecticida"],
                                    var_name="Tratamiento",
                                    value_name="Numero")

## Cálculos estadísticos
def calcular_estadisticas(df):
    resultados = {} # Diccionario con los resultados de todos los tratamientos
    for tratamiento in df['Tratamiento'].unique():
        datos = df[df['Tratamiento'] == tratamiento]['Valor'].astype(float)
        resultados[tratamiento] = {    # Crear diccionario con los estadísticos principales para cada tratamiento
            "Promedio": np.mean(datos),
            "Desviación estándar": np.std(datos),
            "Varianza": np.var(datos),
            "Mediana": np.median(datos),
            "Valores atípicos": datos[      # Cálculo de valores atípicos con la regla de 1.5*IQR
                (datos < (np.percentile(datos, 25) - 1.5 * (np.percentile(datos, 75) - np.percentile(datos, 25)))) |
                (datos > (np.percentile(datos, 75) + 1.5 * (np.percentile(datos, 75) - np.percentile(datos, 25))))]
        }
    return resultados


estadisticas_0h = calcular_estadisticas(df_long_area_0h)
estadisticas_48h = calcular_estadisticas(df_long_area_48h)

## Crear carpeta para guardar los resultados
# Crear la carpeta "resultados_ensayo" si no existe
output_dir = "resultados_ensayo"
os.makedirs(output_dir, exist_ok=True)  # Crea la carpeta si no existe


### Generación de gráficos
## Diagramas de barras de área foliar remanente promedio
tratamientos = []
medias_0h = []
medias_48h = []
for k,v in estadisticas_0h.items():
    tratamientos.append(k)
    medias_0h.append(v['Promedio'])
for k,v in estadisticas_48h.items():
    medias_48h.append(v['Promedio'])

# Preparar figura y subplots de área remanente promedio
fig1, axes1 = plt.subplots(1, 2, figsize=(15, 6))  # 1 fila, 2 columnas

# Gráfico 1: Área remanente promedio a las 0 h
sns.barplot(data = df_long_area_0h, x="Tratamiento",
            y="Valor",
            estimator = np.mean,
            ax=axes1[0],
            palette='colorblind')
axes1[0].set_title("Área foliar remanente promedio a las 0 horas")
axes1[0].set_xlabel("Tratamiento")
axes1[0].set_ylabel("Área foliar remanente (cm^2)")
axes1[0].plot(range(len(tratamientos)),
              medias_0h,
              color='red',
              linestyle='--',
              label='Tendencia')

# Gráfico 2: Área remanente promedio a las 48 h
sns.barplot(data = df_long_area_48h,
            x="Tratamiento",
            y="Valor",
            estimator = np.mean,
            ax=axes1[1],
            palette='colorblind')
axes1[1].set_title("Área foliar remanente promedio a las 48 horas")
axes1[1].set_xlabel("Tratamiento")
axes1[1].set_ylabel("Área foliar remanente (cm^2)")
axes1[1].plot(range(len(tratamientos)),
              medias_48h,
              color='red',
              linestyle='--',
              label='Tendencia')

# Ajustar espaciado y mostrar los gráficos
plt.tight_layout(pad=2)
plt.savefig('barplot_result.pdf', dpi= 300)
plt.show()


## Diagramas de cajas y bigores del área foliar remanente
# Preparar figura y subplots de área remanente
fig2, axes2 = plt.subplots(1, 2, figsize=(15, 6))  # 1 fila, 2 columnas

# Gráfico 1: Área remanente a las 0 h
sns.boxplot(data=df_long_area_0h,
            x="Tratamiento",
            y="Valor",
            ax=axes2[0],
            palette="Paired")
axes2[0].set_title("Área foliar remanente a las 0 horas")
axes2[0].set_xlabel("Tratamiento")
axes2[0].set_ylabel("Área foliar remanente (cm^2)")

# Gráfico 2: Área remanente a las 48 h
sns.boxplot(data=df_long_area_48h,
            x="Tratamiento",
            y="Valor",
            ax=axes2[1],
            palette="Paired")
axes2[1].set_title("Área foliar remanente a las 48 horas")
axes2[1].set_xlabel("Tratamiento")
axes2[1].set_ylabel("Área foliar remanente (cm^2)")

# Ajustar espaciado y mostrar los gráficos
plt.tight_layout(pad=2)
plt.savefig(os.path.join(output_dir, "Boxplot area remanente.pdf"), dpi= 300)
plt.show()

## Histogramas de área foliar remanente
# Preparar figura y subplots de área remanente
fig3, axes3 = plt.subplots(1, 2, figsize=(15, 6))  # 1 fila, 2 columnas

# Gráfico 1: Área remanente a las 0 h
sns.histplot(data=df_long_area_0h,
             x="Valor",
             ax=axes3[0],
             palette="Dark2",
             hue="Tratamiento",
             kde=True)
axes3[0].set_title("Área foliar remanente a las 0 horas")
axes3[0].set_ylabel("Conteo")
axes3[0].set_xlabel("Área foliar remanente (cm^2)")

# Gráfico 2: Área remanente a las 48 h
sns.histplot(data=df_long_area_48h,
             x="Valor", ax=axes3[1],
             palette="Dark2",
             hue = "Tratamiento",
             kde=True)
axes3[1].set_title("Área foliar remanente a las 48 horas")
axes3[1].set_ylabel("Conteo")
axes3[1].set_xlabel("Área foliar remanente (cm^2)")

# Ajustar espaciado y mostrar los gráficos
plt.tight_layout(pad=2)
plt.savefig(os.path.join(output_dir, "Histograma area remanente.pdf"), dpi= 300)
plt.show()

## Diagrama de barras de peso total de las larvas
# Preparar figura y subplots de peso total
fig4, axes4 = plt.subplots(1, 2, figsize=(15, 6))  # 1 fila, 2 columnas

# Gráfico 1: Peso total de las 30 larvas a las 0 h
sns.barplot(data = df_wei,
            x="Tratamiento",
            y="Peso total 0 h",
            palette='colorblind',
            ax=axes4[0])
axes4[0].set_title("Peso total de las larvas a las 0 h")
axes4[0].set_xlabel("Tratamiento")
axes4[0].set_ylabel("Peso total de las 30 larvas (g)")
axes4[0].plot(range(len(df_wei['Tratamiento'])),
              df_wei['Peso total 0 h'],
              color='red',
              linestyle='--',
              label='Tendencia')

# Gráfico 2: Peso total de las 30 larvas a las 48 h
sns.barplot(data = df_wei,
            x="Tratamiento",
            y="Peso total 48 h",
            palette='colorblind',
            ax=axes4[1])
axes4[1].set_title("Peso total de las larvas a las 48 h")
axes4[1].set_xlabel("Tratamiento")
axes4[1].set_ylabel("Peso total de las 30 larvas (g)")
axes4[1].plot(range(len(df_wei['Tratamiento'])),
              df_wei['Peso total 48 h'],
              color='red',
              linestyle='--',
              label='Tendencia')

# Ajustar espaciado y mostrar los gráficos
plt.tight_layout(pad=2)
plt.savefig(os.path.join(output_dir, "Peso total de larvas.pdf"), dpi= 300)
plt.show()

## Diagrama de líneas de larvas vivas
# Preparar figura de larvas comidas

sns.lineplot(data = df_long_life,
             x="Tiempo",
             y="Numero",
             hue = 'Tratamiento',
             palette='colorblind',
             markers=True)
sns.scatterplot(data = df_long_life,
                x="Tiempo",
                y="Numero",
                hue = 'Tratamiento',
                palette='colorblind',
                markers=True,
                legend=None)
plt.title("Número de larvas vivas a lo largo del tiempo")
plt.xlabel("Tiempo")
plt.ylabel("Número de larvas vivas")

# Ajustar espaciado y mostrar los gráficos
plt.tight_layout(pad=2)
plt.savefig(os.path.join(output_dir, "No. larvas vivas.pdf"), dpi= 300)
plt.show()

## Diagrama de líneas de discos comidos
# Preparar figura de discos comidos
sns.lineplot(data = df_long_fed,
             x="Tiempo",
             y="Numero",
             hue = 'Tratamiento',
             palette='colorblind',
             markers=True)
sns.scatterplot(data = df_long_fed,
                x="Tiempo",
                y="Numero",
                hue = 'Tratamiento',
                palette='colorblind',
                markers=True,
                legend=None)
plt.title("Número de discos comidos")
plt.xlabel("Tiempo")
plt.ylabel("Número de discos comidos")

# Ajustar espaciado y mostrar los gráficos
plt.tight_layout(pad=2)
plt.savefig(os.path.join(output_dir, 'No. discos comidos.pdf'), dpi= 300)
plt.show()

### Generar archivo de texto con resultados
output_file = "resultados_ensayo/resultados_estadisticos.txt"
with open(output_file, "w") as f:
    f.write("Resultados estadísticos del experimento\n")
    f.write("=======================================\n\n")

    f.write("Resultados a las 0 horas:\n")
    for tratamiento, stats in estadisticas_0h.items():
        f.write(f"{tratamiento}:\n")
        for key, value in stats.items():
            if isinstance(value, pd.Series):  # Para valores atípicos
                value = list(value)
            f.write(f"  {key}: {value}\n")
        f.write("\n")

    f.write("Resultados a las 48 horas:\n")
    for tratamiento, stats in estadisticas_48h.items():
        f.write(f"{tratamiento}:\n")
        for key, value in stats.items():
            if isinstance(value, pd.Series):  # Para valores atípicos
                value = list(value)
            f.write(f"  {key}: {value}\n")
        f.write("\n")

print(f"Archivo de resultados generado: {output_file}")




