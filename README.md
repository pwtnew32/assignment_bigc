# assignment_bigc
From this assignment.<br />
![alt text](https://github.com/pwtnew32/assignment_bigc/blob/main/image/assignment.png) <br />
I choose website data for this assignment 2 websites <br />
1. BigC (link : https://www.bigc.co.th/) <br />
2. Makro (link : https://www.makro.pro/) <br />

## Workflow 

![alt text](https://github.com/pwtnew32/assignment_bigc/blob/main/image/Flow.png) <br />

### Tools
- BeautifulSoup4
- Pandas
- Sqlalchemy
- Docker
- Airflow
- Postgresql

### Workflow stept
1. Extract Data from BigC and Makro website by using BeautifulSoup4 library to get elements of product. <br />
2. Transform product elements to DataFrame by using pandas library. <br />
3. Load DataFrame to Postgresql Database which running on Docker by using Sqlalchemy library.
4. Vizualize by uisng Tableau to direct connect to Postgresql Database.
<br />

### Deployment
This workflow apply Apache Airflow by running on Docker.
1. If your PC or Vm Instance have not installed docker, Install docker as this link : https://docs.docker.com/engine/install/  <br />
as your system engine. If you have already installed docker, skip this step to next step<br />
2. I have built my custom airflow image and create things as below : 
   - Directory for project directory
   - ```Dockerfile``` to build custom image
     ```
      # defind master image
      # FROM apache/airflow:2.7.0

      FROM apache/airflow:2.7.0
      # copy local connector into container
      COPY requirement.txt /requirement.txt
      
      # upgrade pip
      RUN python -m pip install --upgrade pip
      # run pip install
      RUN pip install --requirement /requirement.txt
     ```
   - ```requirement.txt``` with list python libraries need to build custom airflow image because some python libraries were not installed in airflow image.<br />
      ```
      minio==7.1.10
      pysftp==0.2.9
      sshtunnel==0.4.0
      xlrd==1.2.0
      pandas==1.1.4
      PyMySQL==1.0.2
      paramiko==2.10.4
      sqlalchemy==1.4.46
      requests==2.31.0
      bs4==0.0.2
      ```
      and build image by run command below.<br />  <br />
     ```docker build --tag pwtnew/airflow_custom:1.1 .``` <br />  <br />
     push image to docker repo.<br />  <br />
     ```docker push pwtnew/airflow_custom:1.1```  <br />  <br />
3. After push custom image to repo, download ```docker-compose.yaml```  <br />
   download ```docker-compose.yaml```  <br />  <br />
   ```curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.7.0/docker-compose.yaml'``` <br />  <br />
   open file and change AIRFLOW_IMAGE_NAME <br />  <br />
   ```image: ${AIRFLOW_IMAGE_NAME:-pwtnew/airflow_custom:1.1}``` <br />  <br />
   then save file <br />  <br />
4. Initializing Environment for Airflow (link : https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html) by run all command as below : <br />  <br />
   - In project directory, run this command to create directory and create .env
   ```
   mkdir -p ./dags ./logs ./plugins ./config
   echo -e "AIRFLOW_UID=$(id -u)" > .env
   AIRFLOW_UID=50000
   ```
   - Initialize the database
   ```
   docker compose up airflow-init
   ```
   <br />
5. After Initializing Environment, Running Airflow by run command  <br />
   ```docker compose up```
   
## Output
In Postgresql, I create table with collect products information as below: <br />
- category : product category such as meat, water etc.
- product : product name.
- brand : product brand name such as samsung.
- price_per_unit : price per 1 unit in THB.
- unit : sale unit such as kg.
- store : store name (BigC, Makro).
- time_stamp : time stamp when data was ingested. <br /> <br />
#### Here's sample output.  <br />
![alt text](https://github.com/pwtnew32/assignment_bigc/blob/main/image/sample_output.png) <br />
