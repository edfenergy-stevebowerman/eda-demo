# AWS Event Driven Architecture demos

Common technology:
- Python3.9
- Serverless Framework
- Boto3


# Pre-requisites
- AWS account with CLI access setup
- Python 3.9
- Node (suggest >14) - core Lambda code is Python, but serverless is based upon Node
- Serverless framework (```npm install serverless -g```)
- API key for PostitionStack https://positionstack.com/signup/free 

# Install
Update the serverless.yaml to add your API key for postition stack. The default config takes it from an SSM variable called ```/eda-demo/positionstack-key```
```
npm install
npm run create
```

# Use
Kick things off by uploading the demo file to the input S3 bucket:

```aws s3 cp test.csv s3://eda-demo-input-dev```

Once processing has finished, you can pull down the processed file to inspect it:

```aws s3 cp s3://eda-demo-output-dev/test.csv output.csv```

Open output.csv to see the augmented data


# Destroy
```
npm run destroy
```