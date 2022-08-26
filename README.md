# AWS Proton Template Rendering Validation

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

## Limitations

This is currently a work-in-progress, here are some things we don't currently support:

1. Environment templates
2. Components 