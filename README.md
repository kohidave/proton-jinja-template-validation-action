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
spec/sample-outputs.yaml [only for service templates]
```

The `spec.yaml` file needs to contain a valid spec for the template it's a part of. These values will be used to render the template.

The `sample-outputs.yaml` is a simple yaml file which contains a list of key/values to emulate environment and service outputs. This is only needed for service templates (service instances and pipelines).



## Ussage 

Add the following workflow to your template repository to validate template changes during pull requests. (it's recomended you turn on branch protection so invalid changes can't be merged)

```yaml
name: Validate Template
on:
  pull_request:
    branches: [ "main" ]
jobs:
  TemplateChecker:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
      with:
        fetch-depth: 0
    - name: Get changed files
      id: changed-files
      uses: tj-actions/changed-files@v34
      with:
        separator: ","
    - name: Run action
      # Put your action repo here
      uses: kohidave/proton-jinja-template-validation-action@main
      with: 
        changed_files: "${{steps.changed-files.outputs.all_changed_files}}"
```

### Schema files and spec directory layout

In order to render your template, this action expects a `spec/` directory in the template bundle with a sample `spec.yaml` and an `sample-outputs.yaml` (for Service Templates). Here's an example layout:


```
/my-template/instance_infrastructure/...
/my-template/pipeline_infrastructure/...
/my-template/schema/                        # The schema is validated and used to inject default values
/my-template/schema/schema.yaml
/my-template/spec/
/my-template/spec/spec.yaml                 # This is a real life spec, filled out. This is used to emulate a developer spec
/my-template/spec/sample-outputs.yaml       # This file contains a key value yaml of sample environment and service outputs [service templates only]
```

#### `sample-outputs.yaml` file

An example `sample-outputs.yaml` might look like this:

```yaml
environment:
  SNSTopicArn: arn:aws:sns:my-cool-topic
  SNSTopicName: my-cool-topic
  VPCSecurityGroup: daves-cool-security-group
  PrivateSubnet1: subnet-1
  PrivateSubnet2: subnet-2
  PublicSubnet1: public-subnet-1
  PublicSubnet2: public-subnet-2
service:
  LambdaRuntime: ruby2.7
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

And your pipeline template like this:

```yaml
Environment:
  Variables:
    Runtime: '{{service_instances[0].outputs.LambdaRuntime}}'
```

The service and environment outputs will be used for every service instance and environment in your template. 

## Limitations

This is currently a work-in-progress, here are some things we don't currently support:

1. Components 
2. Schemas defining `default` values must use a lower-cased `default`. 
3. Error handling when a sample output is not available to template has somewhat cryptic error messaging. 

## CFN Lint Errors

By default, this action will run all CFN Lint rules for all regions. If this is not what you want, you can add [CFN Overrides](https://github.com/aws-cloudformation/cfn-lint#template-based-metadata) to your template. 

As an example:

```
Metadata:
  cfn-lint:
    config:
      regions:
        - us-east-1
        - us-east-2
      ignore_checks:
        - E2530
```        