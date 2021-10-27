# Welcome to the Unified Makerspace Project

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization
process also creates a virtualenv within this project, stored under the .env
directory.  To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.

To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .env
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .env/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .env\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

You must now ensure that you are signed into AWS CLI:

Instructions for configuring AWS CLI: 
- https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html

Sign in instructions for AWS Educate accounts:
- Navigate to awseducate.com and sign in
- Go to "My Classrooms" and select go to classroom for the class' account you wish to deploy to
- Select "Account Details" and "Show" next to AWS CLI
- Copy and paste the block code that is shown into ~/.aws/credentials

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

If the synth is successful, you can then deploy to the AWS account you are currently signed into

```
$ cdk deploy
```

If you are updating an existing CloudFormation Stack, you will be met with a changelog which you can then review and hit "y" to approve

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!

## Generating a component diagram

The components of this system are described in [`makerspace.dot`](./makerspace.dot). You can re-generate the PNG using the below command:

```
dot makerspace.dot -Tpng > makerspace.png
```