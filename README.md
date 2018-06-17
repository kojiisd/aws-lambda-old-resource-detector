# aws-lambda-old-resource-detector
This script detect old lambda functions. And if the functions are connected to CloudFormation Stacks, this script will show the relationships.

# Prepare
## Install pytz

```
$ mkdir lib
$ pip install pytz -t ./lib
```

## Modify serverless.yml

```
custom:
    environment:
      DURATION_DAYS: 7
```

Environment of "DURATION_DAYS" should be changed by your own desire.

# Deploy

```
$ sls deploy
```