# Face Recognition using a PaaS-based application

## Group Members

- Prasidh Aggarwal (paggar10)
- Revanth (rbangal5)
- Shriya (ssrin103)

## Tasks

### Prasidh Aggarwal

Main responsibility was to setup the entire infrastructure.

- Efficiently executed the tasks of setting up the project infrastructure.
- Created an AWS account and defined IAM users with appropriate permissions, ensuring secure access to the required resources.
- Configured user roles for the Lambda function, establishing the necessary privileges for seamless operation.
- Proceeded to set up S3 buckets and DynamoDB, creating a solid data storage and retrieval foundation.
- Established a private Elastic Container Registry (ECR) for secure image storage.
- Successfully loaded the DynamoDB with relevant data.
Built a customized Docker image containing essential libraries and tools.
- Deployed the Lambda function using the Docker image to AWS.
- Completed assigned responsibilities and enabled the project to progress efficiently.

### Shriya

Main responsibility was to do frame extraction and perform face recognition.

- Wrote a Lambda function to process video files and extract frames, ensuring efficient input data handling.
- Integrated the Python face recognition library, enabling accurate identification of individuals in the extracted frames.
- Developed code to generate output CSV files containing student information derived from the face recognition process.
- Tested the Lambda function locally throughout the development process to validate its functionality and optimize performance.
- Contributed to the project's progress by delivering a robust solution for processing and analyzing video files.

### Revanth

Main responsibility was to do the testing and evaluation and debug core issues wherever necessary.

- Configured the Lambda trigger on the input S3 bucket to enable automatic execution of the Lambda function upon receiving new files.
- Tested the Lambda function using the provided workload generator to evaluate its performance and reliability under simulated real-world scenarios.
- Verified the correctness of the output CSV files and assessed processing times to ensure all requests were completed within a reasonable timeframe.
- Identified and resolved various issues during testing, such as architecture mismatch and permission issues.
- Further refined the solution to deliver optimal results.
- Diligently executed each task and contributed to the project's success, ensuring a robust and efficient system for processing and analyzing input data.

Apart from these individual tasks, every team member was involved in designing, implementing, developing, and testing the application.

## Architecture

![Application Architecture](./extras/images/application_arch.jpg "Complete application architecture")

## AWS Credentials

AWS credentials were not required by any specific AWS services in this project. Considering it is not a good practice to provide credentials on github, we won't be doing so.

## S3 Bucket Names

- serverlesspresso-input-us-west-1
- serverlesspresso-output-us-west-1

## Other AWS resources

- Lambda function --> face-recog-lambda-serverlesspresso
- Private ECR  --> cse546-serverlesspresso
- Lambda user role --> face-recognition-lambda-role

## Project working and Architecture

Please click [here](./reports/ServerlessPresso_Group_Report.pdf) to read a detailed report of the working of the application.
For individual member reports use the below links:

- [Prasidh](./reports/Prasidh_Aggarwal_Individual_Report.pdf)
- [Shriya](./reports/Shriya_Srinivasan_Individual_Report.pdf)
- [Revanth](./reports/Revanth_Suresha_Individual_Report.pdf)

## How to get started?

1. Clone the repo.

2. In the handler.py modify the input and output bucket names if required.

3. Build the docker image using  

    ```bash
    docker build -t <image-name> .
    ```

4. Login to the private ECR.

    ``` bash
    aws ecr get-login-password --region us-west-1 | docker login --username AWS --password-stdin <ecr-url>
    ```

5. Tag the image to push to the ECR.

    ```bash
    docker tag <image-name> <ecr-url>/<ecr-name>:<image-tag>
    ```

6. Push the docker image to the ECR.

    ```bash
    docker push <ecr-url>/<ecr-name>:<image-tag>
    ```

7. From the workload generator directory, run the below command.

    ```bash
    python3 workload.py
    ```

8. Check the output bucket for the csv files with the student data.
