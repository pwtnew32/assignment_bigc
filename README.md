# assignment_bigc
From this assignment.<br />
![alt text](https://github.com/pwtnew32/assignment_bigc/blob/main/image/assignment.png) <br />
I choose website data for this assignment 2 websites <br />
1. BigC (link : https://www.bigc.co.th/) <br />
2. Makro (link : https://www.makro.pro/) <br />
<br />
## Workflow <br />
![alt text](https://github.com/pwtnew32/assignment_bigc/blob/main/image/Flow.png) <br />
### Tools
- BeautifulSoup4
- Pandas
- Sqlalchemy
- Docker
- Airflow
- Postgresql
<br />
### Workflow step
1. Extract Data from BigC and Makro website by using BeautifulSoup4 library to get elements of product. <br />
2. Transform product elements to DataFrame by using pandas library. <br />
3. Load DataFrame to Postgresql Database which running on Docker by using Sqlalchemy library.
4. Vizualize by uisng Tableau to direct connect to Postgresql Database.
<br />

### Deployment
This workflow apply Apache Airflow by running on Docker.
1. If your PC or Vm Instance have not installed docker, Install docker as this link : https://docs.docker.com/engine/install/  <br />
as your system engine. If you have already installed docker, skip this step to next step<br />
2. Create directory to apply as airflow project dir and download ```docker-compose.yaml``` in this repo to this directory.
