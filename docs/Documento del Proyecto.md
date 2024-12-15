# Berenejena-hub

- Grupo 1 
- Curso escolar: 2024/2025
- Asignatura: Evolución y gestión de la configuración

## Miembros del equipo (en orden alfabético según apellido): escala de 1 al 10 con el esfuerzo hecho en el proyecto (10 mayor implicación, 1 menor implicación)

| Miembro                        | Implicación |
|--------------------------------|-------------|
| [Fernández Mota, Francisco](#)  | [1-10]      |
| [García Abadía, Enrique](#)     | [1-10]      |
| [Giraldo Santiago, Luis](#)    | [1-10]      |
| [Sheng Chen](#)                | [1-10]      |
| [Solís Agudo, Felipe](#)        | [1-10]      |
| [Vargas Muñiz, David](#)        | [1-10]      |

## Indicadores del proyecto

| Miembro del equipo               | Horas | Commits | LoC | Test | Issues | Work Item         |
|----------------------------------|-------|---------|-----|------|--------|-------------------|
| [Fernández Mota, Francisco](#)   | HH    | XX      | YY  | ZZ   | II     | Descripción breve |
| [García Abadía, Enrique](#)     | HH    | XX      | YY  | **4 tests** (1 de ellos pair-wise)   | II     | **WI: Advanced Filtering**. En este WI se trabaja sobre la pestaña 'explore' de la aplicacion, donde se han eliminado los filtros que habia y se han añadido filtros para las siguientes propiedades de los dataset: publicaction type, author, files number, total size, title y tag. |
| [Giraldo Santiago, Luis](#)      | HH    | XX      | YY  | ZZ   | II     | Descripción breve |
| [Sheng Chen](#)                  | HH    | XX      | YY  | **6 tests Selenium**, **6 tests unitarios**   | II     | **WI: Dashboard**. Este WI implementa un tablero que muestra un resumen de las estadísticas clave del sistema: datasets sincronizados/no sincronizados, descargas, vistas y conteo dinámico de equipos. |
| [Solís Agudo, Felipe](#)         | HH    | XX      | YY  | ZZ   | II     | Descripción breve |
| [Vargas Muñiz, David](#)         | HH    | XX      | YY  | ZZ   | II     | Descripción breve |
| **TOTAL**                        | tHH   | tXX     | tYY | tZZ  | tII    | Descripción breve |

## Resumen Ejecutivo

### Descripcion del Sistema

**BORRAR CUANDO SE TERMINE LA SECCION** 
*Se explicará el sistema desarrollado desde un punto de vista funcional y arquitectónico. Se hará una descripción tanto funcional como técnica de sus componentes y su relación con el resto de subsistemas. Habrá una sección que enumere explícitamente cuáles son los cambios que se han desarrollado para el proyecto.*

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Se parte del proyecto base UVLHub, al cual se le han realizado difentes modificacion y adiciones, seleccionando diferentes WI de los propuestos para realizar. Se han seleccionado para el desarrollo 2 WI de dificultad *High* y 4 WI de dificultad *Medium*. Los WI seleccionados son los siguientes: Dashboard (*Medium*), Download in different formats (*Medium*), Rate datasets/models (*Medium*), Improved UI (*Medium*), Advanced Filtering (*High*) y Social Module (*High*). 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Centrandonos en el proyecto UVLHub en si, este proyecto nos perimite realizar la busqueda de datasets que contienen diferentes archivos uvl de una forma sencilla. Ademas de poder buscar, tambien podemos registrarnos y subir datasets propios con archivos uvl especificos. La aplicacion se compone de distintos modulos entre los que encontramos: auth, dataset, explore, featuremodel o profiles entre otros.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Para mejorar la funcionalidad de UVLHub, se usaran distintos WI como se ha comentado antes. Ademad de los anteriormente mencionados, implementaremos un WI adicional, Fakenodo. Este WI sustituira la conexion con Zenodo, una pagina donde encontramos una gran cantidad de archivos uvl de datos. Es imprescindible implementar Fakenodo paar no saturar la api de Zenodo con peticiones y asi poder obtener toda la funcionalidad de creacion de datasets en UVLHub. A continuacion se explicaran cada uno de los WI seleccionados.

#### <u>Advanced Filtering </u>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Para la implementacion de este WI se ha modificado la pestaña '*explore*', en la que aparecen diferentes filtros para la busqueda de datasets. Se añaden filtros para publicaction type, author, files number, total size, title y tag. La forma de aplicar los filtros son desplegables con diferentes opciones que en la mayoria de los casos variaran sus valores dependiendo de los valores que se encuentren en los datasets registardos en la base de datos. Estas modificaciones se aplican directamente en el script que se acciona al inicializar la pestaña. Para que no existan errores a la hora de realizar los test, se decició añadir un boton que confirme la aplicacion de los filtros, ya que selenium no es capaz de detectar la actualizacion dinamica de los valores de los filtros y aplicarlos sin la necesidad del boton.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Ademas de las modificaciones en la pestaña '*explore*' fue necesario añadir nuevos valores a la base de datos de dataset y authors para poder comprobar bien todas las funcionalidades de los filtros, ya que los valores base de los dataset de ejemplos se quedaban cortos en cuanto a variedad de datos.

#### <u>Dashboard</u>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;La implementación del dashboard permite a los usuarios visualizar de manera clara y organizada las estadísticas clave del sistema. Este incluye:

- Total de datasets sincronizados y no sincronizados.
- Estadísticas de descargas y vistas tanto de datasets como de modelos de características.
- Conteo dinámico de equipos basado en el HTML de la sección de equipos.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;El desarrollo implicó la creación de una ruta para recopilar datos a través de servicios como `DataSetService` y `FeatureModelService`. La plantilla `dashboard.html` organiza la información en tarjetas con diseño responsivo y se realizaron pruebas con Selenium para validar su funcionalidad y aspecto visual. Adicionalmente, se utilizaron tests unitarios para asegurar la correcta integración de los datos en la plantilla.

### Vision Global del Proceso de Desarrollo

**BORRAR CUANDO SE TERMINE LA SECCION** *Debe dar una visión general del proceso que ha seguido enlazándolo con las herramientas que ha utilizado. Ponga un ejemplo de un cambio que se proponga al sistema y cómo abordaria todo el ciclo hasta tener ese cambio en producción. Los detalles de cómo hacer el cambio vendrán en el apartado correspondiente.*

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Para el desarrollo del proyecto se ha empleado una serie de procesos de desarrolo y ejecucion especificos para garantizar el buen desarrollo de proyecto y minimizar la aparicion de conflictos. Cuando ya estaban seleccionados lo WI por cada uno de los integrantes se generaron diferentes *issues* en el repositorio de github para cada uno de los WI. En estas *issues* se definirian y describiran las diferentes tareas en las que se dividirian los WI, facilitando su desarrollo y la deteccion y resolucion de errores. A cada *issue* se le asignara una *priority* la cual nos dara una vision de cuanto de importante es completarla con exactitud. Una vez que se han establecidos las *issues*, se creo un *project* de github para si poder establecer diferentes estados los cuales poder asignarle a cada *issue* dependiendo en que estapa se encuentre (Por Hacer, En Progreso, En Revision, Hecho). 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Una vez comprendido los pasos previos al desarrollo de los WI, entramos de lleno en como es el proceso de desarrollo de uno de ellos, con todos los pasos que implican. Primero, crearemos una rama para el WI, en la que trabajaremos hasta que este terminado el WI. Cuando la rama este creada, asignaremos las *issues* correspondientes a esta rama. Una vez se haya completado el desarrollo de una *issue*, se realizara un *commit* sobre esa rama, siguiendo el formato establecido en el **Acta de Constitucion**. Cuando el WI este completo y se hayan realizados los testeos necesarios, se procedera a realizar una *pull request* para introducir los cambios a la rama *main*. Esta *pull request* debe ser aceptada por otro de los integrantes del grupo, que sera el encargado de revisar si existe algun conflicto que impida que se pueda proseguir con la peticion. Cuando se valide la funcionalida y apruebe la *pull request* se debera cerrar la/s *issue/s* de ese WI. 

### Entorno de Desarrollo

**BORRAR CUANDO SE TERMINE LA SECCION** *Debe explicar cuál es el entorno de desarrollo que ha usado, cuáles son las versiones usadas y qué pasos hay que seguir para instalar tanto su sistema como los subsistemas relacionados para hacer funcionar el sistema al completo. Si se han usado distintos entornos de desarrollo por parte de distintos miembros del grupo, también debe referenciarlo aquí.*
El desarrollo del proyecto se realizó utilizando un conjunto robusto de herramientas y configuraciones que permitieron implementar y probar las funcionalidades requeridas. A continuación, se describen los aspectos clave del entorno utilizado:

El desarrollo del proyecto se realizó utilizando un entorno bien estructurado para garantizar la eficacia y la reproducibilidad del sistema. A continuación, se describen los aspectos clave:

#### **Sistema Operativo y Configuración Base**
- **Sistema Operativo:** Ubuntu 22.04 LTS.
- **Lenguaje de Programación:** Python 3.10+.
- **Framework Principal:** Flask 3.0.3.
- **Base de Datos:** MariaDB, con las bases de datos `uvlhubdb` y `uvlhubdb_test`.
- **Gestión de Dependencias:** Uso del archivo `requirements.txt` para mantener la consistencia.

#### **Configuración de MariaDB**
MariaDB fue instalada y configurada con los siguientes pasos:
1. Instalación del servidor:
   ```bash
   sudo apt install mariadb-server -y
   sudo systemctl start mariadb
   ```
2. Configuración inicial con `mysql_secure_installation` y creación de usuarios y bases de datos:
   ```sql
   CREATE DATABASE uvlhubdb;
   CREATE DATABASE uvlhubdb_test;
   CREATE USER 'uvlhubdb_user'@'localhost' IDENTIFIED BY 'uvlhubdb_password';
   GRANT ALL PRIVILEGES ON uvlhubdb.* TO 'uvlhubdb_user'@'localhost';
   GRANT ALL PRIVILEGES ON uvlhubdb_test.* TO 'uvlhubdb_user'@'localhost';
   FLUSH PRIVILEGES;
   ```

#### **Pasos para Configurar el Sistema**
1. **Clonar el Repositorio del Proyecto:**
   ```bash
   git clone git@github.com:<YOUR_GITHUB_USER>/uvlhub_practicas.git
   cd uvlhub_practicas
   ```

2. **Crear y Activar un Entorno Virtual:**
   ```bash
   sudo apt install python3.12-venv
   python3.12 -m venv venv
   source venv/bin/activate
   ```

3. **Instalar las Dependencias:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Configurar Variables de Entorno:**
   Crear un archivo `.env` basado en el archivo de ejemplo:
   ```bash
   cp .env.local.example .env
   ```

5. **Ignorar el Módulo Webhook:**
   Evitar problemas en desarrollo agregando `webhook` a `.moduleignore`:
   ```bash
   echo "webhook" > .moduleignore
   ```

6. **Aplicar Migraciones y Poblar la Base de Datos:**
   ```bash
   flask db upgrade
   rosemary db:seed
   ```

7. **Ejecutar el Servidor de Desarrollo:**
   ```bash
   flask run --host=0.0.0.0 --reload --debug
   ```
   Esto iniciará la aplicación en el puerto 5000, accesible desde [http://localhost:5000](http://localhost:5000).

#### **Herramientas Clave**
- **Flask y Extensiones:** Para el desarrollo backend.
- **SQLAlchemy:** Gestión ORM de la base de datos.
- **pytest y Selenium:** Pruebas unitarias e integradas.
- **Rosemary:** CLI para facilitar tareas de desarrollo.
- **Docker:** Soporte opcional para pruebas de integración.

Estas configuraciones aseguran un entorno de desarrollo sólido y replicable, facilitando la colaboración entre los miembros del equipo.
#### **Sistema Operativo y Configuración Base**
- **Sistema Operativo:** Ubuntu 22.04 LTS.
- **Lenguaje de Programación:** Python 3.10+.
- **Framework Principal:** Flask 3.0.3.
- **Base de Datos:** SQLite para el desarrollo local y soporte para MySQL en caso de despliegue.
- **Gestión de Dependencias:** Utilización del archivo `requirements.txt` para garantizar consistencia en las instalaciones.

#### **Entornos Utilizados por los Miembros del Equipo**
- **Ubuntu 22.04:** Todos los miembros utilizaron este sistema operativo para garantizar compatibilidad y reproducibilidad en las configuraciones.
- **Entornos Virtuales:** Se usaron entornos virtuales (`venv`) para aislar las dependencias y evitar conflictos entre proyectos.

#### **Librerías y Herramientas Clave**
El proyecto hizo uso de una variedad de librerías y herramientas, incluyendo:
- **Librerías de Backend:**
  - `Flask` y sus extensiones (`Flask-Login`, `Flask-WTF`, `Flask-SQLAlchemy`) para el desarrollo del servidor.
  - `SQLAlchemy` para la gestión ORM de la base de datos.
  - `BeautifulSoup` para el procesamiento de HTML.
- **Librerías de Testing:**
  - `pytest` y `pytest-cov` para pruebas unitarias e integración.
  - `selenium` para pruebas de interfaz gráfica automatizadas.
- **Otras Herramientas:**
  - `docker` y `docker-compose` (en caso de pruebas de integración).
  - `flake8` para análisis estático del código.
### Ejercicio de Propuesta de Cambio

**BORRAR CUANDO SE TERMINE LA SECCION** *Se presentará un ejercicio con una propuesta concreta de cambio en la que a partir de un cambio que se requiera, se expliquen paso por paso (incluyendo comandos y uso de herramientas) lo que hay que hacer para realizar dicho cambio. Debe ser un ejercicio ilustrativo de todo el proceso de evolución y gestión de la configuración del proyecto.*

### Conclusiones

**BORRAR CUANDO SE TERMINE LA SECCIÓN** *Se enunciarán algunas conclusiones y se presentará un apartado sobre las mejoras que se proponen para el futuro (curso siguiente) y que no han sido desarrolladas en el sistema que se entrega*

## Enlaces de interés:

- Enlace al repositorio: [https://github.com/berenjena-hub/berenjena-hub.git](#).
- Proyecto desplegado: [https://berenjena-hub.onrender.com/](#).
- [Cualquier otro enlace de interés](#).
