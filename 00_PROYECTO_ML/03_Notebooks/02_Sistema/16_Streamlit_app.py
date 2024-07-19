import streamlit as st
import cloudpickle
import pandas as pd
import matplotlib.pyplot as plt
from janitor import clean_names
from sklearn.metrics import precision_recall_curve, roc_auc_score
from yellowbrick.classifier import DiscriminationThreshold

# Definir los umbrales en un solo lugar
UMBRAL_AGRESIVO = 0.31
UMBRAL_MODERADO = 0.43
UMBRAL_EQUILIBRIO = 0.67
UMBRAL_COSTES = 0.82

# Definir las variables finales
variables_finales = [
    'household_members',
    'income',
    'mntgoldprods',
    'mntmeatproducts',
    'mntwines',
    'numcatalogpurchases',
    'numstorepurchases',
    'numwebvisitsmonth',
    'total_cmp' 
]

# Cargar el modelo
ruta_proyecto = 'C:/Users/Alfonso/OneDrive/Documentos_/Formación/Bootcamp_DS/Repo_DS/Proyect_Break_ML/Proyecto_ML/00_PROYECTO_ML'
nombre_pipe_ejecucion = 'pipe_ejecucion.pickle'
ruta_pipe_ejecucion = f'{ruta_proyecto}/04_Modelos/{nombre_pipe_ejecucion}'

with open(ruta_pipe_ejecucion, mode='rb') as file:
    pipe_ejecucion = cloudpickle.load(file)

# Función para hacer la predicción
def hacer_prediccion(datos, umbral):
    probabilidades = pipe_ejecucion.predict_proba(datos)[:, 1]
    return (probabilidades >= umbral).astype(int), probabilidades

# Función para ajustar el umbral
def ajustar_umbral(modelo, X, y):
    probabilidades = modelo.predict_proba(X)[:, 1]
    precision, recall, umbrales = precision_recall_curve(y, probabilidades)
    
    mejor_umbral_recall = umbrales[recall.argmax()]
    mejor_metrica_recall = recall.max()
    
    mejor_umbral_precision = umbrales[precision.argmax()]
    mejor_metrica_precision = precision.max()
    
    return mejor_umbral_recall, mejor_metrica_recall, mejor_umbral_precision, mejor_metrica_precision, precision, recall, umbrales

# Función para cargar y filtrar los datos
def cargar_y_filtrar_datos(ruta_csv, umbral):
    df = pd.read_csv(ruta_csv)
    df_filtrado = df[df['prediccion'] >= umbral]
    return df_filtrado

# Configuración de la página de Streamlit
st.sidebar.title("Navegación")
pagina_seleccionada = st.sidebar.radio("Ir a", ["Predicción de Marketing", "Selección de Clientes"])

if pagina_seleccionada == "Predicción de Marketing":
    st.title("Predicción de Marketing")
    st.write("Ingrese los datos para las siguientes variables:")

    # Cargar los datos de validación
    nombre_fichero_datos = 'validacion.csv'
    ruta_completa = ruta_proyecto + '/02_Datos/02_Validacion/' + nombre_fichero_datos
    df = pd.read_csv(ruta_completa, index_col=0)

    # Preprocesar los datos si es necesario
    df = (clean_names(df).drop_duplicates())
    df['status_members'] = df['marital_status'].map({
        'Together': 2,  
        'Divorced': 1,  
        'Married': 2,   
        'Single': 1,    
        'Widow': 1,     
        'OTROS': 1      
    })
    df['household_members'] = df['status_members'] + df['kidhome'] + df['teenhome']
    df['total_cmp'] = df.filter(like='accepted').apply(pd.to_numeric, errors='coerce').sum(axis=1)
    train_set_numeric = df.filter(like='cmp').apply(pd.to_numeric, errors='coerce')
    df['total_%_cmp'] = df['total_cmp'] / len(train_set_numeric.columns)
    df['total_amount'] = df.filter(like='mnt').sum(axis=1)
    df = df.drop(columns=['status_members'])

    # Crear un formulario para que el usuario ingrese los datos
    with st.form(key='prediction_form'):
        # Dividir las entradas en dos columnas
        col1, col2 = st.columns(2)
        datos = {}
        for i, variable in enumerate(variables_finales):
            with col1 if i % 2 == 0 else col2:
                datos[variable] = st.number_input(f"Ingrese el valor para {variable}:", value=0.0)
        
        submit_button = st.form_submit_button(label='Hacer Predicción')

    # Sección para seleccionar el modelo
    st.write("Seleccione el modelo que desea utilizar:")
    modelo_seleccionado = st.radio(
        "Opciones de modelo:",
        ('Modelo agresivo captación clientes', 'Modelo moderado captación de clientes', 
         'Equilibrio entre captación y costes', 'Maximizando los costes')
    )

    # Asignar el umbral basado en la selección del usuario
    umbral = UMBRAL_AGRESIVO  # Valor por defecto
    if modelo_seleccionado == 'Modelo agresivo captación clientes':
        umbral = UMBRAL_AGRESIVO
    elif modelo_seleccionado == 'Modelo moderado captación de clientes':
        umbral = UMBRAL_MODERADO
    elif modelo_seleccionado == 'Equilibrio entre captación y costes':
        umbral = UMBRAL_EQUILIBRIO
    elif modelo_seleccionado == 'Maximizando los costes':
        umbral = UMBRAL_COSTES

    if submit_button:
        df_nuevo = pd.DataFrame([datos])
        X = df[variables_finales]  # Características del conjunto de datos
        y = df['response']  # Etiquetas verdaderas

        mejor_umbral_recall, mejor_metrica_recall, mejor_umbral_precision, mejor_metrica_precision, precision, recall, umbrales = ajustar_umbral(pipe_ejecucion, X, y)
        
        prediccion, probabilidad = hacer_prediccion(df_nuevo, umbral)
        
        st.write(f"La predicción es: {'Cliente potencial' if prediccion[0] == 1 else 'No cliente potencial'}")
        st.write(f"Este cliente tiene una probabilidad del {probabilidad[0] * 100:.2f}% de ser un cliente potencial.")
        st.write(f"El mejor umbral para recall es: {mejor_umbral_recall:.2f}")
        st.write(f"El mejor umbral para precisión es: {mejor_umbral_precision:.2f}")
        st.write(f"El valor del AUC-ROC es: {roc_auc_score(y, pipe_ejecucion.predict_proba(X)[:, 1]):.2f}")

elif pagina_seleccionada == "Selección de Clientes":
    st.title("Selección de Clientes")

    # Selección del umbral
    st.write("Seleccione el modelo que desea utilizar:")
    modelo_seleccionado = st.radio(
        "Opciones de modelo:",
        ('Modelo agresivo captación clientes', 'Modelo moderado captación de clientes', 
         'Equilibrio entre captación y costes', 'Maximizando los costes')
    )

    # Asignar el umbral basado en la selección del usuario
    umbral = UMBRAL_AGRESIVO  # Valor por defecto
    if modelo_seleccionado == 'Modelo agresivo captación clientes':
        umbral = UMBRAL_AGRESIVO
    elif modelo_seleccionado == 'Modelo moderado captación de clientes':
        umbral = UMBRAL_MODERADO
    elif modelo_seleccionado == 'Equilibrio entre captación y costes':
        umbral = UMBRAL_EQUILIBRIO
    elif modelo_seleccionado == 'Maximizando los costes':
        umbral = UMBRAL_COSTES

    # Ruta del archivo CSV
    nombre_df_final = 'df_predict_final.csv'
    ruta_df_final = f'{ruta_proyecto}/02_Datos/03_Trabajo/{nombre_df_final}'
   
    # Cargar y filtrar los datos
    df_filtrado = cargar_y_filtrar_datos(ruta_df_final, umbral)

    # Mostrar los resultados
    st.write("Clientes seleccionados:")
    st.dataframe(df_filtrado.head(15))  # Mostrar las primeras 15 filas

    # Botón para descargar el archivo CSV
    st.download_button(
        label="Descargar datos filtrados",
        data=df_filtrado.to_csv(index=False).encode('utf-8'),
        file_name='clientes_filtrados.csv',
        mime='text/csv'
    )











