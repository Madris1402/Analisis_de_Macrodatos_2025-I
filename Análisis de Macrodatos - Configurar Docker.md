### Cargar Imágenes

Abrir la terminal en la carpeta donde se encuentren las imágenes
```
docker load -i .\namenode-image.tar

docker load -i .\resourcemanager-image.tar

docker load -i .\dnnm-image.tar

docker load -i .\pyspark-notebook.tar
```

### Contenedores Temporales

``` docker
docker network create hadoop-net

docker container run --rm --init --detach --name namenode --network=hadoop-net --hostname namenode -p 9870:9870 namenode-image

docker container run --rm --init --detach --name resourcemanager --network=hadoop-net --hostname resourcemanager -p 8088:8088 resourcemanager-image

docker container run --rm --init --detach --name dnnm1 --network=hadoop-net --hostname dnnm1 dnnm-image

docker container run --rm --init --detach --name dnnm2 --network=hadoop-net --hostname dnnm2 dnnm-image

docker container run --rm --init --detach --name dnnm3 --network=hadoop-net --hostname dnnm3 dnnm-image

docker stop dnnm1 dnnm2 dnnm3 namenode resourcemanager 
```

### Crear Contenedores

``` docker
docker network create hadoop-net

docker container run --init --detach --name namenode --network=hadoop-net --hostname namenode -p 9870:9870 namenode-image

docker container run --init --detach --name resourcemanager --network=hadoop-net --hostname resourcemanager -p 8088:8088 resourcemanager-image 

docker container run --init --detach --name dnnm1 --network=hadoop-net --hostname dnnm1 dnnm-image

docker container run --init --detach --name dnnm2 --network=hadoop-net --hostname dnnm2 dnnm-image 

docker container run --init --detach --name dnnm3 --network=hadoop-net --hostname dnnm3 dnnm-image

docker run --init --detach --name jupyter-pyspark --network=hadoop-net -p 8888:8888 -p 4040:4040 pyspark-notebook
```
### Comandos Docker

Iniciar Contenedores
``` docker
docker start namenode resourcemanager jupyter-pyspark dnnm1 dnnm2 dnnm3
```

Detener Contenedores
``` docker
docker stop dnnm3 dnnm2 dnnm1 jupyter-pyspark resourcemanager namenode
```

Para entrar a la terminal del name node y ejecutar comandos.
``` docker
docker exec -it namenode /bin/bash
```

### Hadoop

`hdfs` Hadoop File System, sirve para acceder a los archivos del sistema de nombre de nodos.
`hadoop` Administra el cluster, mientras que `hdfs` accede al cluster
`hdfs dfs -ls /` Muestra el contenido de todo el cluster de Hadoop
`hdfs version` Detalles de la version
`hadoop fs -ls /` Muestra el contenido de todo el cluster de Hadoop
`hdfs getconf -namenodes`	Muestra la configuración de los nodos (no mostró nada)
`hdfs dfsadmin -report`		Muestra la configuración de los nodos
`hdfs dfs -mkdir /tmp/amd` Crea una carpeta en `tmp` llamada `amd`
`hdfs dfs -ls -r /tmp` Lista los elementos dentro de `tmp`
`dd if=/dev/urandom bs=1M count=250 | hdfs dfs -put - /tmp/amd/arch250M` Crea un archivo de 250MiB en la carpeta `amd`	
`hdfs getconf -confKey df.blocksize` Muestra el tamaño de los bloques de Hadoop
`hdfs dfs -head /tmp/amd/arch250M` Muestra las primeras 10 líneas del archivo random
`hdfs dfs -rm /tmp/amd/arch250M` Borra el archivo random
`dd if=/dev/urandom bs=1M count=250 | hdfs dfs -put - /tmp/amd/ejbloque/arch250M.rnd` Crea un archivo random

`hdfs dfs -chmod -r 777 /tmp` Dar permisos de Lectura y Escritura a Jupyter

### S00 Archivo Random

``` hdfs
hdfs dfs -mkdir /tmp/amd

hdfs dfs -ls -r /tmp

hdfs dfs -chmod -r 777 /tmp

dd if=/dev/urandom bs=1M count=250 | hdfs dfs -put - /tmp/amd/ejbloque/arch250M.rnd

hdfs dfs -ls -r /tmp/amd/ejbloque

hdfs dfs -head /tmp/amd/ejbloque/arch250M.rnd

```

### S01 Conteo de Palabras

##### Descargar Libros

```hdfs
curl -L https://raw.githubusercontent.com/omarmendoza564/datos/main/datos/libros/evangelio_segun_marcos.txt | hdfs dfs -put -f - /tmp/amd/contarpalabras/entrada/evangelio_segun_marcos.txt

curl -L https://raw.githubusercontent.com/omarmendoza564/datos/main/datos/libros/la_biblioteca_de_babel.txt | hdfs dfs -put -f - /tmp/amd/contarpalabras/entrada/la_biblioteca_de_babel.txt

curl -L https://raw.githubusercontent.com/omarmendoza564/datos/main/datos/libros/funes_el_memorioso.txt | hdfs dfs -put -f - /tmp/amd/contarpalabras/entrada/funes_el_memorioso.txt
```

### S04 Spark Data Frame de Locatel

##### Descargar Datos de Locatel

```hdfs
curl -L https://datos.cdmx.gob.mx/dataset/529aac27-d1c1-426f-8c45-fd76fba43bf4/resource/44913088-806d-4f80-acca-1409a8225e9c/download/locatel0311-2024.csv | hdfs dfs -put -f - /tmp/amd/locatel0311/locatel0311-2024.csv

curl -L https://datos.cdmx.gob.mx/dataset/529aac27-d1c1-426f-8c45-fd76fba43bf4/resource/1ece1ddf-3e82-44f4-9435-486b1b9167f5/download/locatel0311-2023.csv | hdfs dfs -put -f - /tmp/amd/locatel0311/locatel0311-2023.csv

curl -L https://archivo.datos.cdmx.gob.mx/suac/locatel0311-2022.csv | hdfs dfs -put -f - /tmp/amd/locatel0311/locatel0311-2022.csv

curl -L https://archivo.datos.cdmx.gob.mx/suac/locatel0311-2021.csv | hdfs dfs -put -f - /tmp/amd/locatel0311/locatel0311-2021.csv

curl -L https://archivo.datos.cdmx.gob.mx/suac/locatel0311-2020.csv | hdfs dfs -put -f - /tmp/amd/locatel0311/locatel0311-2020.csv

curl -L https://archivo.datos.cdmx.gob.mx/suac/locatel0311-2019.csv | hdfs dfs -put -f - /tmp/amd/locatel0311/locatel0311-2019.csv

curl -L https://github.com/omarmendoza564/datos/raw/refs/heads/main/datos/CPdescarga.txt | iconv -f ISO-8859-1 -t UTF-8 | hdfs dfs -put -f - /tmp/amd/sepomex/CPdescarga.txt
```