
import cloudpickle
import pandas as pd

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
ruta_proyecto = 'C:/Users/Alfonso/OneDrive/Documentos_/Formación/Bootcamp_DS/Repo_DS/Proyect_Break_ML/00_PROYECTO_ML'
nombre_pipe_ejecucion = 'pipe_ejecucion.pickle'
ruta_pipe_ejecucion = f'{ruta_proyecto}/04_Modelos/{nombre_pipe_ejecucion}'

with open(ruta_pipe_ejecucion, mode='rb') as file:
    pipe_ejecucion = cloudpickle.load(file)

# Función para solicitar los datos del usuario
def solicitar_datos():
    datos = {}
    for variable in variables_finales:
        valor = float(input(f"Ingrese el valor para {variable}: "))
        datos[variable] = [valor]
    return pd.DataFrame(datos)

# Función para hacer la predicción
def hacer_prediccion(datos):
    scoring = pipe_ejecucion.predict_proba(datos)[:, 1]
    return scoring[0]

# Programa principal
if __name__ == "__main__":
    print("Ingrese los datos para las siguientes variables:")
    datos_nuevos = solicitar_datos()
    prediccion = hacer_prediccion(datos_nuevos)
    print(f"La predicción es: {prediccion}")