# This repository contains the CF template for the infrastructure.

## Steps to recreate the infrastructure.

```bash
git clone https://github.com/cheehouhon/exercise/
```
1. Configure AWS CLI: https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html
2. Deploy VPC_RDS.yaml via Cloudformation, this will give us the VPC, and RDS.
```bash
aws cloudformation deploy --template-file VPC_RDS.yml
```
3. Grab the RDS endpoint: https://docs.aws.amazon.com/documentdb/latest/developerguide/db-instance-endpoint-find.html
4. Update the mysql host in exercise/interviewexercise/application/app.py with the RDS endpoint you created.
```bash
Example: host = "RDS-NAME.us-east-1.rds.amazonaws.com
```
5.) Build the docker image in exercise/interviewexercise/application/
```bash
cd exercise/interviewexercise/application/
docker build -t app .
```

6.) Create a repository in ECR: https://docs.aws.amazon.com/AmazonECR/latest/userguide/repository-create.html

7.) Tag and push the image to ECR
```bash
To tag
docker tag app:latest <ACCTID>.dkr.ecr.us-east-1.amazonaws.com/interviewexercise:v1.0.1
To push
docker push <ACCTID>.dkr.ecr.us-east-1.amazonaws.com/interviewexercise:v1.0.1
```
8.) Update the image in service.yaml <Line 53>
```bash
Example: Image: <ACCTID>.dkr.ecr.us-east-1.amazonaws.com/interviewexercise:v1.0.1
```

9.) Deploy ALB_RDS_ECS.yml via Cloudformation, this will give us ALB, RDS, ECS Cluster, and container task
```bash
aws cloudformation deploy --template-file ALB_SERVICE_ECS.yaml
``` 

10.) Map Alias of the output of Load Balancer to your Route 53 Record.
https://aws.amazon.com/premiumsupport/knowledge-center/route-53-create-alias-records/

# This is the one that's currently running:
http://application.cheelabs.com

11.) To cleanup, just delete all the CF stacks created in Cloudformation
https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-console-delete-stack.html

## Notes:
Since docker-compose.yml doesn’t completely work on ECS. I have to make a few changes.

1.) In app.py:
I need to create a database on RDS.
```python
# Create database
db = mysql.connect(
        host = "tiiv88mn8jz27i.cvjptpuqa6ut.us-east-1.rds.amazonaws.com",
        user = "timesheet",
        password = "timesheet",
    )
dbcur = db.cursor()
dbcur.execute("CREATE DATABASE IF NOT EXISTS timesheet")
```
2.) Hostname need to be changed to the RDS endpoint.
3.) Since docker-compose tells the host and container ports to listen on 5000, I added EXPOSE 5000 to the Dockerfile:



