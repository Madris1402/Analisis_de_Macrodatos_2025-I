#!/usr/bin/env python
# coding: utf-8

# In[1]:


rdd = spark.sparkContext.textFile("hdfs://namenode:9000/tmp/amd/contarpalabras/entrada")


# In[2]:


type(rdd)


# In[3]:


rdd.count()


# In[4]:


rdd.getNumPartitions()


# In[5]:


rdd.take(5)


# In[6]:


get_ipython().system(' pip install unidecode')


# In[7]:


import re 
from unidecode import unidecode


# Función para limpiar cada palabra
def limpiar_palabra(palabra):
    # Convertir a minúsculas
    palabra = palabra.lower()
    # Remover acentos
    palabra = unidecode(palabra)
    # Remover signos de puntuación y caracteres especiales
    palabra = re.sub(r'[^\w\s]', '', palabra)
    # Retornar la palabra limpia
    return palabra
 
# Definir un conjunto de palabras vacías (puedes añadir más)
palabras_vacias = {"", "y", "de", "la", "que", "el", "en", "los", "las", "un", "una", "a", "le", "lo"}


# In[8]:


palabras = rdd.flatMap(lambda line: line.split(" "))


# In[9]:


palabras.count()


# In[10]:


palabras.take(200)


# In[11]:


palabras_limpias = palabras.map(lambda x: limpiar_palabra(x)).filter(lambda x: x not in palabras_vacias)


# In[12]:


palabras_limpias.count()


# In[13]:


palabras_limpias.take(200)


# In[14]:


conteo = palabras_limpias.map(lambda palabra: (palabra, 1)).reduceByKey(lambda a, b: a + b)


# In[15]:


conteo.count()


# In[16]:


conteo.collect()


# In[17]:


conteo.sortBy(lambda x:x[1], ascending=False).take(30)


# In[20]:


spark.sparkContext.textFile("hdfs://namenode:9000/tmp/amd/contarpalabras/entrada").flatMap(lambda line: line.split(" "))\
.map(lambda x: limpiar_palabra(x)).filter(lambda x: x not in palabras_vacias).map(lambda palabra:(palabra, 1))\
.reduceByKey(lambda a, b: a + b).sortBy(lambda x:x[1], ascending=False).saveAsTextFile("hdfs://namenode:9000/tmp/amd/contarconspark/")


# In[ ]:




