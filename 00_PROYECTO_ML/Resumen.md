# Resumen del proyecto de ML

### Objetivos de negocio:
    - Mejora del ROI de las acciones de marketing a través de:
        - Conocimiento profundo de los clientes y de sus hábitos de compra.
        - Conocimiento profundo de las ventas por productos y tipo de cliente.
        - Implementación de un sistema de predicción funcional

## Alcance del proyecto
- Realizar una clusterización para segmentar a los clientes.
- Realizar una clasificación para predecir los clientes con más probabilidad de aceptar ofertas comerciales en base a una target dada por negocio.

## Partes del proyecto
El proyecto se puede dividir en cuatro partes:
- Primera parte: en la que se realiza el cargado, exploración, limpieza, tratamiento de datos y preselección de variables.
- Segunda parte: en la que se lleva a cabo la modelización para la clasificación.
- Tercera parte: en la que se realiza la modelización para la cluserización.
- Cuarte parte: en la que se prepara el código para producción.

### Sobre la variable target
- La variable target sobre la que realizar la clasificación es 'Response'.
- Se encuentra muy desbalanceada (85% (0) vs 15% (1)).

## Características de los clientes y su relación con las ventas y la variable target.
- La mayor parte de los clientes son casados ('married') y graduados ('graduation'), seguidos de doctores ('PhD') y en pareja ('Together'). 
- El importe de ventas totales también se corresponde con esta distribución.
- En cuanto a los miembros totales de un hogar, el 40% son de 3 personas y el 34% de 2 personas.
- El importe de las ventas sin embargo es mayor para hogares con 2 miembros que con 3 miembros.
- La proporción de 'unos' en la variable target ('response') del valor 'PhD' de la variable 'education' sugiere que son más propensos a las ofertas.
- La proporción de 'unos' en la variable target ('response') del valor 'Single', 'Divorced' y 'Widow' sugiere que son más propensos a las ofertas vs el valor 'Together' que sugiere lo contrario.
- A pesar de esto, el elevado número de clientes que son casados y graduados, tienen el mayor % de aceptación de ofertas.
- La edad no es representativa de ninguna clase, ni de la aceptación o no de las ofertas.
- En cuanto a los ingresos, a mayor nivel de formación mayor cantidad de ingreso, mientras que a menor número de miembros en el hogar, mayor es la mediana del ingreso.
- Existe una correlación entre el nivel de ingresos elevado y un menor número de miembros en el hogar con el importe de ventas final.
- Las variables que tienen una correlación lineal mayor a 20 con la variable target ('response'), son 'recency_mms', 'mntwines_mms', 'mntmeatproducts_mms',  'numcatalogpurchases_mms', 'acceptedcmp3','acceptedcmp5', 'acceptedcmp1'.


## Contribución a las ventas
- La mayor parte de las ventas vienen de productos de vino y de carne, con una diferencia muy considerable con el resto de productos. 

## Medios de compra
- La mayor parte de las ventas provienen del store seguido muy de cerca por las ventas a través de la web.

## Variables relevantes
### Clusterización
- Aunque los medios de estimación del mejor número de clúster daban como resultado unánime el de 2 clúster, también se ha realizado la segmentación y análisis sobre 3 clúster dado que permitía aislar a aquellos que tenían una mayor concentracíon de unos en la variable target 'response'.
- Se ha tomado como referencia para realizar la clusterización aquellas variables que permitían una clara diferenciación entre clúster (al hacerlo sobre dos clúster).
response,	income_mms,	mntwines_mms,	mntfruits_mms,	mntmeatproducts_mms,	kidhome_mms,	teenhome_mms, mntfishproducts_mms, mntsweetproducts_mms,	mntgoldprods_mms,	numwebpurchases_mms,	numcatalogpurchases_mms,	
numstorepurchases_mms,	numwebvisitsmonth_mms,	household_members_mms,	total_amount_mms,	total_purchase_mms, median_amount_purchase_mms,	total_cmp_mms.
- Se puede observar las características de cada clúster en el dashboard del powerBI.

### Clasificación
- Como ya se ha comentado la variable target se encontraba muy desbalanceada.
- Para hacer funcional el modelo se ha trabajado en la selección de las mínimas variables que ofrecían unos resultados similares a entrenar el modelo con todas las variables.
- Las variables seleccionadas han sido (en orden de importancia para el modelo):
    - total_cmp_mms
    - household_members_mms
    - mntmeatproducts_mms
    - numwebvisitsmonth_mms
    - numstorepurchases_mms
    - mntgoldprods_mms
    - mntwines_mms
    - numcatalogpurchases_mms
    - income_mms

- El modelo final elegido para pasar a producción ha sido el LGBClassifier.
- Los resultados del modelo ofrecen un predicción del 77% para el total de potenciales clientes que aceptan la oferta, si bien, el porcentaje de predicción si un cliente va a aceptar o no es del orden del 40%.
- Se ha diseñado las métricas del algoritmo teniendo en cuenta el llegar al mayor número de potenciales clientes a pesar de incluir algunos que no vayan a aceptar la oferta, con la idea de que los costes de las campañas tienen un ROI elevado y pueden compensar el lanzarselas a clientes que puedan decir que no, pero de esta manera nos aseguramos llegar al mayor número de clientes potenciales posible.
- A pesar de entrenar el algoritmo así, de cara a la producción, se han implementado cuatro umbrales de corte que permiten predecir a los clientes en base a diferentes objetivos de campaña como son:
    - Modelo agresivo de captación de clientes
    - Modelo más moderado
    - Modelo más equilibrado entre captación y costes
    - Modelo para maximizar los costes en campañas en las que el coste de la misma sea elevado.



