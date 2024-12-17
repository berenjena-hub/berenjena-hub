# Berenejena-hub

- Grupo 1 
- Curso escolar: 2024/2025
- Asignatura: Evolución y gestión de la configuración

## Miembros del equipo (en orden alfabético según apellido): escala de 1 al 10 con el esfuerzo hecho en el proyecto (10 mayor implicación, 1 menor implicación)

| Miembro                        | Implicación |
|--------------------------------|-------------|
| [Chen, Sheng](#)               | 9           |
| [Fernández Mota, Francisco](#) | 9           |
| [García Abadía, Enrique](#)    | 8           |
| [Giraldo Santiago, Luis](#)    | 10          |
| [Solís Agudo, Felipe](#)       | 8           |
| [Vargas Muñiz, David](#)       | 8           |


## Indicadores del proyecto

| Miembro del equipo               | Horas | Commits | LoC            | Test                                     | Issues | Work Item                                  |
|----------------------------------|-------|---------|----------------|------------------------------------------|--------|--------------------------------------------|
| [Chen, Sheng](#)                 | 75    | 29      | 4129++ y 1812--             | **6 tests Selenium**, **6 tests unitarios** | 8     | **WI: Dashboard**. Este WI implementa un tablero que muestra un resumen de las estadísticas clave del sistema: datasets sincronizados/no sincronizados, descargas, vistas y conteo dinámico de equipos. |
| [Fernández Mota, Francisco](#)   | 79    | 33      | 970            | **5 tests unitarios**, **3 tests de interfaz** | 11     | **Download in different formats**. Este WI implementa botones adicionales para que los usuarios puedan descargar tanto datasets como modelos en diferentes formatos además de los ya propuestos (UVL, Glencoe, AFM, JSON, SPLOT y CNF). |
| [García Abadía, Enrique](#)     | 66    | 19      | 1386++ y 543--             | **4 tests** (1 de ellos pair-wise)       | 6     | **WI: Advanced Filtering**. En este WI se trabaja sobre la pestaña 'explore' de la aplicación, donde se han eliminado los filtros que había y se han añadido filtros para las siguientes propiedades de los datasets: publicaction type, author, files number, total size, title y tag. |
| [Giraldo Santiago, Luis](#)      | 87    | 113     | 2.189.306++ y 2.176.010-- | **8 tests unitarios**, **3 tests selenium**, **6 tests locust** | 11     | **WI: SocialModule**. Este WI implementa un sistema de seguimiento entre usuarios, un chat para hablar entre usuarios que se han seguido mutuamente y por último una sección de comentarios en los datasets. |
| [Solís Agudo, Felipe](#)         | 70    | 30      | 1.002++ y 634-- | **2 tests Selenium**, **4 tests unitarios**  | **10** (2 de issues globales y 8 de mi WI)      | **WI: Improve UI**. En este WI se trabaja sobre la vista "view_dataset", reorganizándola y adaptándola al resto de WI de los compañeros del grupo. Además, se crea una nueva vista llamada "file_content" para gestionar archivos file.uvl de manera más sencilla. |
| [Vargas Muñiz, David](#)         | 75    | 23      | 2930++ y 884-- | **2 tests Selenium**, **4 tests unitarios**, **1 test Locust** | **12** (2 de issues globales y 10 de mi WI)     | **WI: Rate Datasets/Models.** Este WI implementa un sistema que permite calificar los distintos datasets, a través de métricas como Quality, Size y Usability, mostrando la media total para este a través del campo Overall Rating. |
| **TOTAL**                        | 452   | 274     | 2.199.823++ y 2.182.593--            | 3 tests en total (14 Selenium, 30 unitarios, 7 adicionales como Locust e interfaz)                                     | 49    | El equipo completó 49 issues divididas entre los 6 Work Items (WI), con un esfuerzo total de 452 horas. Se realizaron 247 commits que sumaron un impacto significativo en el código, con más de 2.199.823 líneas añadidas y 2.182.593 eliminadas. Las pruebas realizadas incluyen 14 tests Selenium, 30 unitarios y 7 adicionales (interfaz y carga). Estas tareas abarcaron la creación de nuevos módulos, optimización de funcionalidades existentes, y mejoras tanto en la experiencia del usuario como en la arquitectura del sistema.                         |


## Resumen Ejecutivo

### Descripcion del Sistema

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Se parte del proyecto base UVLHub, al cual se le han realizado difentes modificacion y adiciones, seleccionando diferentes WI de los propuestos para realizar. Se han seleccionado para el desarrollo 2 WI de dificultad *High* y 4 WI de dificultad *Medium*. Los WI seleccionados son los siguientes: Dashboard (*Medium*), Download in different formats (*Medium*), Rate datasets/models (*Medium*), Improved UI (*Medium*), Advanced Filtering (*High*) y Social Module (*High*). 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Centrandonos en el proyecto UVLHub en si, este proyecto nos perimite realizar la busqueda de datasets que contienen diferentes archivos uvl de una forma sencilla. Ademas de poder buscar, tambien podemos registrarnos y subir datasets propios con archivos uvl especificos. La aplicacion se compone de distintos modulos entre los que encontramos: auth, dataset, explore, featuremodel o profiles entre otros.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Para mejorar la funcionalidad de UVLHub, se usaran distintos WI como se ha comentado antes. Ademad de los anteriormente mencionados, implementaremos un WI adicional, Fakenodo. Este WI sustituira la conexion con Zenodo, una pagina donde encontramos una gran cantidad de archivos uvl de datos. Es imprescindible implementar Fakenodo paar no saturar la api de Zenodo con peticiones y asi poder obtener toda la funcionalidad de creacion de datasets en UVLHub. A continuacion se explicaran cada uno de los WI seleccionados.

#### <u>Download in different formats </u>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Para la implementacion de este WI se han modificado los módulos '*dataset*', '*flamapy*' y '*public*'. Se han añadido varios botones de descarga en la vistas como '*index*', '*view_dataset*' o '*file_content*' que permiten a los usuario descargar ficheros en el formato indicado en el botón al hacer click en él. Permite descargar dataset completos como modelos independientes. Los formatos contemplados son '*UVL*', '*Glencoe*', '*AFM*', '*SPLOT*', '*JSON*' y '*CNF*'.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;De forma adicional se han realizado tests que comprueban el correcto funcionamiento de las funciones de transformación a las que se acceden a través de rutas y el correcto funcionamiento de la interfaz para poder llevar a cabo estas descargas.

#### <u>Advanced Filtering </u>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Para la implementacion de este WI se ha modificado la pestaña '*explore*', en la que aparecen diferentes filtros para la busqueda de datasets. Se añaden filtros para publicaction type, author, files number, total size, title y tag. La forma de aplicar los filtros son desplegables con diferentes opciones que en la mayoria de los casos variaran sus valores dependiendo de los valores que se encuentren en los datasets registardos en la base de datos. Estas modificaciones se aplican directamente en el script que se acciona al inicializar la pestaña. Para que no existan errores a la hora de realizar los test, se decició añadir un boton que confirme la aplicacion de los filtros, ya que selenium no es capaz de detectar la actualizacion dinamica de los valores de los filtros y aplicarlos sin la necesidad del boton.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Ademas de las modificaciones en la pestaña '*explore*' fue necesario añadir nuevos valores a la base de datos de dataset y authors para poder comprobar bien todas las funcionalidades de los filtros, ya que los valores base de los dataset de ejemplos se quedaban cortos en cuanto a variedad de datos.

#### <u>Dashboard</u>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;La implementación del dashboard permite a los usuarios visualizar de manera clara y organizada las estadísticas clave del sistema. Este incluye:

- Total de datasets sincronizados y no sincronizados.
- Estadísticas de descargas y vistas tanto de datasets como de modelos de características.
- Conteo dinámico de equipos basado en el HTML de la sección de equipos.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;El desarrollo implicó la creación de una ruta para recopilar datos a través de servicios como `DataSetService` y `FeatureModelService`. La plantilla `dashboard.html` organiza la información en tarjetas con diseño responsivo y se realizaron pruebas con Selenium para validar su funcionalidad y aspecto visual. Adicionalmente, se utilizaron tests unitarios para asegurar la correcta integración de los datos en la plantilla.

#### <u>Improve UI </u>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Para la implementación de este WI se ha modificado la vista 'view_dataset', en la que se encuentra toda la información sobre un dataset concreto presente en la base de datos. Esta vista fue modificada y reestructurada siguiendo un esquema similar al que sigue GitHub. Además, se añadió una nueva vista,  'file_content', a la cual se puede acceder haciendo click sobre los archivos file.uvl que presenta el dataset correspondiente. Se trasladaron funcionalidades que se encontraban en la vista inicial para trabajar de manera más fácil e intuitiva sobre los archivos individuales, cosa que antes era un proceso algo menos intuitivo. Por otro lado, también se cambió la manera de ver el contenido de los archivos file.uvl que estaba en el proyecto base, siendo esta nueva manera mucho más cómoda para el usuario, con la posibilidad de volver al dataset al que dicho archivo pertenece pulsando sobre su nombre en la ruta de la parte superior de la vista, como se haría en GitHub. En esta otra vista, también existe la posibilidad de navegar sobre los archivos file.uvl de una manera más intuitiva que antes.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Se priorizó la reorganización de la vista base en función de las funcionalidades más relevantes que esta poseía. Además, también se modificó adaptándola al resto de los WI de los compañeros, los cuales muchos de ellos afectaban a la vista  'view_dataset'. En la nueva vista   'file_content' también hay funcionalidades de WI de otros compañeros.

#### <u>Rate Datasets/Models </u>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;La implementación del WI Rate Datasets/Models permite a los usuarios calificar los distintos datasets, a través de distintas métricas tales como Quality, Size y Usability, mostrando la media total para este, a través del campo Overall Rating. Además, ofrece una visualización, tanto para las medias de cada métrica, como para la media total para cada dataset.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;El desarrollo implicó:
 - La creación de la tabla ratings en la base de datos.
 - La creación del modelo Rating en models.py.
 - La adición de la class DatasetRatingRepository en repositories.py, donde se incluyen las operaciones base de la funcionalidad.
 - La adición de la class RatingService en services.py, donde se incluyen las operaciones base de la funcionalidad, referenciando el repositorio.
 - La creación de las rutas necesarias en routes.py para el manejo de la calificación de los datasets y su visualización.
 - La adición del html necesario en view_dataset.html para que sea posible el uso del backend, así como el código correspondiente al proceso en js.

 #### <u>Social Module </u>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Para la implementación de este WI se ha modificado la vista 'view_dataset' y se han creado dos nuevas, la cuales son 'other' del modulo profile y 'index' del modulo social. En la vista de 'view_dataset', se añade una sección que es la de comentarios, la cual siver para dejar tu comentario del dataset. En la vista 'other', se añade el botón para seguir a usuario. En la vista 'index', se añade la funcionalidad de chatear con personas que tu sigues y estas a su vez te siguen. Para disfrutar de estás funcionalidades tienes que ser un usuario autenticado de la página.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Para estás implementaciones se creó un nuevo módulo el cual se llamó social, en este definí dos modelos, los caules son, socail y follow. Social sirve para gestionar la parte de los mensajes entre usuarios y los comentarios y Follow sirve para el seguimiento entre personas. Para implementar estas lógica hice la funciones que están en el service y en el repositories y pará las llamadas a estas funciones desde las vistas hice el routes. Por último creé unos datos iniciales que están en seeders, para los test.

### Vision Global del Proceso de Desarrollo

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Para el desarrollo del proyecto se ha empleado una serie de procesos de desarrolo y ejecucion especificos para garantizar el buen desarrollo de proyecto y minimizar la aparicion de conflictos. Cuando ya estaban seleccionados lo WI por cada uno de los integrantes se generaron diferentes *issues* en el repositorio de github para cada uno de los WI. En estas *issues* se definirian y describiran las diferentes tareas en las que se dividirian los WI, facilitando su desarrollo y la deteccion y resolucion de errores. A cada *issue* se le asignara una *priority* la cual nos dara una vision de cuanto de importante es completarla con exactitud. Una vez que se han establecidos las *issues*, se creo un *project* de github para si poder establecer diferentes estados los cuales poder asignarle a cada *issue* dependiendo en que estapa se encuentre (Por Hacer, En Progreso, En Revision, Hecho). 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Una vez comprendido los pasos previos al desarrollo de los WI, entramos de lleno en como es el proceso de desarrollo de uno de ellos, con todos los pasos que implican. Primero, crearemos una rama para el WI, en la que trabajaremos hasta que este terminado el WI. Cuando la rama este creada, asignaremos las *issues* correspondientes a esta rama. Una vez se haya completado el desarrollo de una *issue*, se realizara un *commit* sobre esa rama, siguiendo el formato establecido en el **Acta Fundacional**. Cuando el WI este completo y se hayan realizados los testeos necesarios, se procedera a realizar una *pull request* para introducir los cambios a la rama *main*. Esta *pull request* debe ser aceptada por otro de los integrantes del grupo, que sera el encargado de revisar si existe algun conflicto que impida que se pueda proseguir con la peticion. Cuando se valide la funcionalida y apruebe la *pull request* se debera cerrar la/s *issue/s* de ese WI. 

### Entorno de Desarrollo

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

La propuesta de cambio consiste en modificar el apartado de *Related publication* de la página *home* de la aplicación y añadir a los nombres de los integrantes del grupo.

Para ello hay que seguir los siguientes pasos:
- Crear en el repositorio de github una *Issue* siguiendo la pólitica de *Issues* definida en el **Acta Fundacional**, para que la propuesta sea valorada por el equipo de desarrollo.
- La persona encargada de esa *Issue* y por lo tanto del cambio a implementar, evaluará el impacto y asignará una prioridad a la *Issue*.
- Se divide la *Issue* en otras tareas más pequeñas si el cambio es complejo.
- Para la implementación del cambio, accederemos al directorio del proyecto `cd berenjena-hub/` y se activará el entorno virtual `source venv/bin/activate`. Se creará una rama si es necesario con el comando `git checkout -b <nombre_rama>`, en caso de no tener que crear una rama, basta con hacer `git checkout <nombre_rama>`. Una vez situado en la rama, se implementarán los cambios con tests respectivos que comprueben el correcto funcionamiendo de la nueva funcionalidad.
- Una vez implementados los cambios, hacer *commit*, comandos `git add .` y `git commit -m "feat(Funcionalidad): Mensaje de commit #nº Issue"`. Es importante destacar que los *commits* según lo acordado en el **Acta Fundacional** deben ser atómicos, por lo que quizás sea necesario hacer más de un *commit*. Una vez hecho con `git push origin <nombre_rama>` los cambios se subirán a la rama remota en el repositorio de git hub.
- Tras subir los cambios al repositorio, hay que realizar una *Pull Request (PR)* para que los cambios se integren en la rama *main*, para ello es necesario seguir la política definida en el **Acta Fundacional** para esta *Pull Request (PR)*. La petición será revisada por otro integrante del grupo y será aceptada si los cambios funcionan de la forma esperada, de lo contrario se notificará y se cancelará la *Pull Request (PR)*.
- Cuando los cambios se han integrado en la rama *main*, borrar la rama si no se necesita para más implementaciones y cerrar la *Issue* de la propuesta de cambio.

### Conclusiones

El desarrollo de **Berenjena-Hub** ha permitido fortalecer habilidades tanto técnicas como de gestión de equipo, enfrentándonos a retos relacionados con la implementación de funcionalidades complejas y la integración de cambios en un entorno colaborativo. Durante el proceso, logramos los siguientes hitos clave:

1. **Funcionalidades implementadas:** 
   - Se completaron los **6 Work Items (WI)** seleccionados, abarcando tareas tanto de dificultad media como alta. Cada WI fue probado exhaustivamente para garantizar su correcta funcionalidad e integración en el sistema base, UVLHub.
   - Se incorporaron mejoras significativas como un tablero (Dashboard) interactivo, un sistema de calificación de datasets, y módulos sociales que fomentan la interacción entre usuarios.

2. **Optimización del sistema base:** 
   - UVLHub fue enriquecido con nuevas capacidades como descargas en múltiples formatos, filtros avanzados para la búsqueda de datasets, y una interfaz gráfica mejorada que hace el uso del sistema más intuitivo para los usuarios.
   - La implementación de **Fakenodo** optimizó la interacción con APIs externas, reduciendo la carga sobre servicios como Zenodo.

3. **Colaboración y gestión:** 
   - El equipo aplicó una metodología ágil, apoyándose en herramientas como GitHub Projects para la organización de tareas y la resolución de conflictos. 
   - El uso de ramas específicas para cada WI y un estricto control de calidad antes de realizar pull requests ayudó a mantener un desarrollo ordenado y sin interrupciones.

4. **Aprendizajes técnicos:** 
   - Se adquirió experiencia práctica en herramientas como Flask, SQLAlchemy, Selenium, y MariaDB, así como en la configuración de entornos de desarrollo con Docker.
   - La implementación de pruebas unitarias y de integración fue crucial para garantizar la estabilidad del sistema, cumpliendo con los estándares definidos en el **Acta Fundacional**.

### Mejoras propuestas para el futuro

Aunque se logró un sistema robusto y funcional, quedan áreas de mejora que podrían ser abordadas en futuras iteraciones del proyecto:

- **Fakenodo como parte nativa de UVLHub:** Integrar Fakenodo directamente en la arquitectura del sistema base en lugar de manejarlo como un WI adicional.
- **Base de datos más accesible:** Explorar el uso de bases de datos más ligeras y portables, como SQLite, para facilitar la configuración en entornos de desarrollo y pruebas.
- **Documentación ampliada:** Crear tutoriales o guías más detalladas para la instalación y uso del sistema, facilitando la incorporación de nuevos desarrolladores o colaboradores.

### Reflexión final

El proyecto **Berenjena-Hub** no solo cumplió con los objetivos iniciales, sino que también brindó una experiencia enriquecedora en cuanto a desarrollo de software, trabajo en equipo y resolución de problemas. Con los aprendizajes y las bases establecidas, el sistema está preparado para evolucionar en el futuro, integrando aún más funcionalidades y consolidándose como una solución robusta para la gestión de datasets en entornos colaborativos.


## Enlaces de interés:

- Enlace al repositorio: [https://github.com/berenjena-hub/berenjena-hub.git](#).
- Proyecto desplegado: [https://berenjena-hub.onrender.com/](#).
