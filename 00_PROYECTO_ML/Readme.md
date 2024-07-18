
## **ALCANCE DEL PROYECTO**
Se ha ralizado un proyecto de machine learning de clusterización y clasificación sobre un dataset del ámbito del marketing cogido de la página de kaggle ([enlace_kaggle](https://www.kaggle.com/datasets/rodsaldanha/arketing-campaign)).

### Sobre el dataset
El dataset contiene información de 4 tipos:
- Información personal de los clientes (edad, estado civil, nivel de educación...)
- Información relacionada con las cantidades de compra por tipo de producto (vino, carne, dulces...)
- Información relacionada con el número de compras realizados por diferentes medios (tienda, online, descuentos,...)
- Información relacionada con el resultado de campañas de marketing anteriores. En total, se muestran 5 campañas de marketing.

### Sobre sus datos
- Contiene 29 variables de partida
- Un total de 2240 filas

### Sobre la variable target
- La variable target sobre la que realizar la clasificación es 'Response'.
- Se encuentra muy desbalanceada (85% (0) vs 15% (1)).

### Objetivos de negocio:
    - Mejora del ROI de las acciones de marketing a través de:
        - Conocimiento profundo de los clientes y de sus hábitos de compra.
        - Conocimiento profundo de las ventas por productos y tipo de cliente.
        - Implementación de un sistema de predicción funcional

### Problemas a resolver:
    - Realizar una segmentación de clientes efectiva que pueda ser útil para el departamento de marketing, tanto a nivel de cliente, como de productos y de medios de compra.
    - Establecer la predicción sobre la probabilidad de que acepten una nueva camapaña de marketing o no.
    - Dotar de herramientas útiles para que puedan ponerlo en práctica cuanto antes.

## **ESTRUCTURA DEL PROYECTO**
La carpeta RAIZ del proyecto es `00_PROYECTO`.    
Dentro de la misma están:    
    
    - 01_Documentos    
        - Contiene los archivos del entorno y requisitos del sistema con el que ha sido creado el proyecto. 

    - 02_Datos    
        - Contiene tres carpetas:
            - 01_Originales: donde se encuentra en dataset original
            - 02_Validacion: donde se encuentra el apartado del dataset para testear
            - 03_Trabajo: contiene los diferentes dataset que se han ido creando a lo largo del proyecto.

    - 03_Notebooks
        - Contiene dos carpetas:  
            - 01_Desarrollo. Con un total de 13 notebooks donde se ha realizado el grueso del proyecto además de un archivo .py con las funciones.
            - 02_Sistema: Contiene los archivos .py con los códigos de ejecución, reentrenamiento así como el archivo para la app.

    - 04_Modelos
        - Contiene los diferentes modelos que se han realizado para la clasificación así como para la preparación del código para los archivos de ejedución y reentrenamiento.

    - 05_Resultados  
        - Contiene las varaibles seleccionadas  

    - 06_Otros    
        - Archivo de 'cajón de sastre' donde se han incluido imágenes y un archivo de powerBI con un dashboard para el personal de marketing.

## Resultados del proyecto:

### Clusterización
- Se han realizado dos propuestas, una con 2 cluster y otra con 3, tratando de incluir solo aquellas variables para las que se podía observar una diferencia clara.
- De las 35 variables finales del modelo, la clusterización se ha realizado con 19. Se podría haber reducido más, pero se ha entendido que con esas 19 el modelo ganaba en explicabilidad.
- Se ha creado un dashboard powerBI para hacer más accesible y visual al equipo de marketing la información en función de cada cláster.
La elección de los clúster finales dependerá del equipo de marketing.


### Clasificación
- La modelización se ha realizado con una dataset reducido a 9 variables para tratar de aumentar la explicabilidad y funcionalidad del modelo en producción.    
- Los valores de recall y precision de la clase positiva han sido muy parecidos a los obtenidos al entrenar el modelo con todas las variables.
- Aunque el modelo se ha entrenado para maximizar el recall de la clase positiva, posteriormente, en producción, se han dado 4 umbrales de corte correspondiente a diferentes objetivos de negocio:
    - Modelo agresivo de captación de clientes
    - Modelo más moderado
    - Modelo más equilibrado entre captación y costes
    - Modelo para maximizar los costes en campañas en las que el coste de la misma sea elevado.
- Se ha implementado una app para el equipo de marketing con dos páginas:    
    - En la primera se pueden introducir los datos sobre las variables con las que ha sido entrenado el modelo y da la probabilidad en función de la elección del objetivo de negocio.
    - En la segunda, se ha enlazado el dataset original para que puedan acceder a los datos de los clientes actuales a los que lanzar la campaña. Al igual que antes, pueden seleccionar entre los diferentes objetivos de negocio.
- Se ha dejado preparado el código de reentrenamiento así como los requisitos del entorno con el que ha sido creado el modelo por si en un futuro hubiera que reentrenarlo.



