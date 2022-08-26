# AWS Proton CFN Template Validation Action

This action makes it easy for you to validate changes to an AWS Proton CloudFormation/Jinja based template. Whenever a pull request is created that touches a template file, this action will:

1. Validate the template schema is valid
2. Render the template using a sample spec
3. Runs the rendered templates through `cfn-lint` 

This action can help you quickly validate that your templates are syntactically correct before registering them with AWS Proton.

## Requirements

To use this action, you have to provide a _few_ additional files in your template bundle. 

```
spec/spec.yaml
spec/sample-env-outputs.yaml [only for service templates]
```

The `spec.yaml` file needs to contain a valid spec for the template it's a part of. These values will be used to render the template.

The `sample-env-outputs.yaml` is a simple yaml file which contains a list of key/values to emulate environment outputs. This is only needed for service templates.



## Ussage 

Add the following workflow to your template repository to validate template changes during pull requests. (it's recomended you turn on branch protection so invalid changes can't be merged)

```yaml
name: Validate Template
on:
  pull_request:
    branches: [ "main" ]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@main
    # This is important as it let's the Validate action detect which templates have changed
    - name: Get changed files
      id: changed-files
      uses: tj-actions/changed-files@v29.0.0
      with:
        separator: ","
    - name: Validate changed templates
      uses: kohidave/proton-jinja-template-validation-action@main
      with: 
        changed_files: "${{steps.changed-files.outputs.all_changed_files}}"

```

### Schema files and spec directory layout

In order to render your template, this action expects a `spec/` directory in the template bundle with a sample `spec.yaml` and an `sample-env-outputs.yaml` (for Service Templates). Here's an example layout:


```
/my-template/instance_infrastructure/...
/my-template/pipeline_infrastructure/...
/my-template/schema/                        # The schema is validated and used to inject default values
/my-template/schema/schema.yaml
/my-template/spec/
/my-template/spec/spec.yaml                 # This is a real life spec, filled out. This is used to emulate a developer spec
/my-template/spec/sample-env-outputs.yaml   # This file contains a key value yaml of sample environment outputs [service templates only]
```

#### `sample-env-outputs.yaml` file

An example `sample-env-outputs.yaml` might look like this:

```yaml
SNSTopicArn: arn:aws:sns:my-cool-topic
SNSTopicName: my-cool-topic
VPCSecurityGroup: daves-cool-security-group
PrivateSubnet1: subnet-1
PrivateSubnet2: subnet-2
PublicSubnet1: public-subnet-1
PublicSubnet2: public-subnet-2
```

This will be used to fill in the values in your service template like:

```yaml
Environment:
  Variables:
    SNSTopicArn: '{{environment.outputs.SNSTopicArn}}'
Policies:
  - AWSLambdaVPCAccessExecutionRole
  - SNSPublishMessagePolicy:
      TopicName: '{{environment.outputs.SNSTopicName}}'
VpcConfig:
  SecurityGroupIds:
    - '{{environment.outputs.VPCSecurityGroup}}'
  SubnetIds:
  {% if service_instance.inputs.subnet_type == 'private' %}
      - '{{environment.outputs.PrivateSubnet1}}'
      - '{{environment.outputs.PrivateSubnet2}}'
  {% else %}
      - '{{environment.outputs.PublicSubnet1}}'
      - '{{environment.outputs.PublicSubnet2}}'
  {% endif %}
```


## Limitations

This is currently a work-in-progress, here are some things we don't currently support:

1. Environment templates
2. Pipeline templates
3. Components 
