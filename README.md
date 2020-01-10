# Hello World FaaS with OpenWhisk

This README serves as documentation for getting OpenWhisk to run on a virtual machine (VM). OpenWhisk is an open source project that provides a framework for deploying so-called "serverless" functions, also known as functions as a service (FaaS). Hopefully this README will allow the user to quickly get OpenWhisk up and running on a VM and then using and deploying some example hello world functions.


#### Table of Contents

- [Building and Running OpenWhisk on Vagrant VM](#building-and-running-openwhisk-on-vagrant-vm)
  * [Setting up OpenWhisk Environment on Vagrant VM](#setting-up-openwhisk-environment-on-vagrant-vm)
- [Building and Running OpenWhisk through Docker](#building-and-running-openwhisk-through-docker)
- [Deploy some FaaS](#deploy-some-faas)
    + [Building a FaaS action](#building-a-faas-action)
    + [Building Chained FaaS actions](#building-chained-faas-actions)
    + [Useful FaaS links](#useful-faas-links)


## Building and Running OpenWhisk on Vagrant VM

The first step to deploying serverless functions through OpenWhisk is to get the framework constructed on a Vagrant VM. Therefore, the first step that is required is to get Vagrant.

```bash
$ sudo apt-get update
$ sudo apt-get install VirtualBox
$ sudo apt-get install Vagrant
```

If you aren't working on a linux machine, I would suggest using a VM software for your operating system to do the following instructions. OpenWhisk is an open source project, but it isn't immediately clear to me how much development is done to keep the project functional on many different OS's. Therefore, it is probably easiest to work from a *nix based machine. Thus, if running from Windows, my current best suggestion is to use a Windows VM software to create a VM to log into, and from there execute these README instructions.

Now that you have the necessary machinery to make the VM, lets get OpenWhisk to build one for you.

```bash
$ git clone --depth=1 https://github.com/apache/openwhisk.git openwhisk
$ cd openwhisk/tools/vagrant
```

Nominally this is where the OpenWhisk instructions tell you to run the script `./hello` which builds the VM for you. However, I found that the script does not work out of the box and needs some tweaks. Please make the following changes to the `Vagrantfile` in the `openwhisk/tools/vagrant` directory. The Vagrantfile controls the properties of the VM.

1. Open up the `Vagrantfile` in your favorite text editor and search for the line `source all.sh oracle`. Find this line, and delete `oracle` so that it only reads `source all.sh`

2. Next, search for the line `# Build and Deploy`. Underneath this comment, you will find some lines that look like:
```bash
set -e
set -x
HOME=/home/vagrant
source /etc/environment
```
Add the following lines under `source /etc/environment`:
```bash
sudo apt-get install -y npm
curl -sL https://deb.nodesource.com/setup_13.x | sudo -E bash - 
sudo apt-get install -y nodejs
```



After you have made these changes, save the file and exit your text editor. You should now be able to run `./hello` without an issue. Note that it takes a while (e.g. 10-15 minutes) as the script builds a pretty good sized memory machine. You will know that the setup script finished successfully when you see the following:

```bash
default: ok: whisk API host set to 192.168.33.16
default: Swagger UI URL: https://192.168.33.16/api/v1/docs/index.html?url=/api/v1/api-docs
default: ++ echo 'Swagger UI URL: https://192.168.33.16/api/v1/docs/index.html?url=/api/v1/api-docs'
default: ++ wsk action invoke /whisk.system/utils/echo -p message hello --result
default: {
default:     "message": "hello"
default: }
default: +++ date
default: ++ echo 'Mon Dec 16 16:46:39 UTC 2019: build-deploy-end'
```

You should now be able to log in to the VM by typing at the CLI
```
$ vagrant ssh
```

### Setting up OpenWhisk Environment on Vagrant VM

Now you should be in the VM and be able to use the OpenWhisk command `wsk`. For example, try to run the hello world command

```bash
vagrant@ubuntu-xenial:$ wsk action invoke /whisk.system/utils/echo -p message hello --result
```
which should return

```
{
    "message": "hello"
}
```

So that OpenWhisk knows where to deploy your serverless functions, create a file in your home directory:

```
vagrant@ubuntu-xenial:$ emacs ~/.wskprops
```

If the file is not already filled with the following information, copy the following into `~/.wskprops` :
```
AUTH=23bc46b1-71f6-4ed5-8c54-816aa4f8c502:123zO3xZCLrMN6v2BKK1dXYFpXlPkccOFqm12CdAsMgRU4VrNZ9lyGVCGuMDGIwP
APIHOST=192.168.33.16
```

These are the default authorization and IP address that OpenWhisk will deploy functions with/to. Note that you should now be able to actually go to `http://192.168.33.16` and see the OpenWhisk default JSON data.



## Building and Running OpenWhisk through Docker

The OpenWhisk dev team recently deleted all of the Vagrant capabilties, since apparently the community does not use the Vagrant option. They suggest running through a Docker container, which basically does the same thing as the Vagrant machine except that now your functions will be deployed through a container instead of through the Vagrant VM.

A useful [link](http://jamesthom.as/blog/2018/01/19/starting-openwhisk-in-sixty-seconds/) explains how to get started in 60 seconds. I basically followed these instructions, with some additional tweaks. The full setup list of instructions is documented below. The following instructions are assuming you already have docker desktop [installed](https://docs.docker.com/install/) for your OS.

Clone the repository and run the Makefile quick-start option:

```bash
git clone https://github.com/apache/openwhisk-devtools.git
cd openwhisk-devtools/docker-compose
sudo make quick-start
```

This builds the docker containers and builds the OpenWhisk source for you to be able to use. After this is finished running, you should see an example print to the console screen of Hello World, which is how you know it has completed correctly.

Now you need to get the CLI API functional. The `make quick-start` creates a `.wskprops` file for you, I would just copy this to your home directory since this is where OpenWhisk looks for it by default:

```
cp .wskprops ~/.wskprops
WSK_CONFIG_FILE=~/.wskprops
```

Next, to get the CLI API functional you need to access the binary file that was installed by the Makefile. It is placed by default in `openwhisk-devtools/docker-compose/openwhisk-src/bin/wsk`. So I do:


```bash
alias wsk=~/git/openwhisk-devtools/docker-compose/openwhisk-src/bin/wsk
```

Now you should be able to use the CLI and access web actions. For example, if you follow the instructions to deploy a hello world function below, you should be able to follow the web url and trigger a FaaS. Note that in the case of the docker container, Whisk complains that it is unable to validate a certificate. You can bypass this by adding the `-i` flag to any `wsk` command that you run, which stands for insecure. In my case, I just added this to the `alias` command above. This might be a bug (feature?) of the docker container deployment. When Serverless (the API, not the generic name) interfaces with Whisk, it requires that you set a flag in the YAML file to `ignore_certs`. So there is precedence from Serverless that, for whatever reason, when deploying FaaS locally through the docker container you have to ignore the certification that is normally required by Whisk.

The default IP address that I get for the docker container is `https://160.91.45.8` but this may not be static like the Vagrant machine IP address is static. You can always check by deploying a hello world function and then grabbing the url via `wsk action get helloWorld --url`. 

## Deploy some FaaS

Now you should be in good shape to actually try to deploy some FaaS. Here are several links that I found useful for learning how to use Whisk and how to write some basic functions.




#### Building a FaaS action

You can deploy your FaaS by using some of the hello world examples in this repository. One easy example is to trigger a function with a URL that makes a decision and triggers some other functions based on a string parameter given in the URL. Clone this repository first:
```bash
vagrant@ubuntu-xenial:$ git clone https://github.com/osbornjd/HelloWorldOpenWhisk.git
```

We will use the python files `webRedirectAction.py`, `hello.py`, and `goodbye.py`. Lets create a package to work in first:
```bash
vagrant@ubuntu-xenial:$ wsk package create pythondemo
```
Next create your hello and goodbye actions:

```bash
vagrant@ubuntu-xenial:$ wsk action create pythondemo/hello hello.py --web true
vagrant@ubuntu-xenial:$ wsk action create pythondemo/goodbye goodbye.py --web true
vagrant@ubuntu-xenial:$ wsk action create pythondemo/redirectAction webRedirectAction.py --web true
```

`--web true` tells OpenWhisk to deploy the function with an attached URL. We could first try to run the hello world `hello.py` web action by executing:

```bash
vagrant@ubuntu-xenial:$ wsk action get pythondemo/hello --url
```

and then entering the returned URL into the browser, e.g. (with "Joe" changed to whatever you like your string to be)

```bash
https://192.168.33.16/api/v1/web/guest/pythondemo/hello?name=Joe
```

The same can be done for the web redirect action

```bash
vagrant@ubuntu-xenial:$ wsk action get pythondemo/redirectAction --url
```

then type in the URL at the browser
```
https://192.168.33.16/api/v1/web/guest/default/webRedirectAction?name=Joe
```

You can adjust the length of the name to see the web redirect in action (e.g. by using "Joseph" instead of "Joe")


#### Building Chained FaaS actions

You can also chain FaaS together directly within OpenWhisk without e.g. just redirecting a bunch of URLs. As an example, let's chain four functions together which each do different tasks. We will chain together `helloSequence.js`,`/whisk.system/utils/split`,`/whisk.system/utils/sort`, and `final.js`.

First create a package to keep the actions in

```bash
vagrant@ubuntu-xenial:$ wsk package create htmlSequence
```


Then create the actions:

```bash
vagrant@ubuntu-xenial:$ wsk action create htmlSequence/hello helloSequence.js
vagrant@ubuntu-xenial:$ wsk action create htmlSequence/final final.js
vagrant@ubuntu-xenial:$ wsk action create htmlSequence/htmlSequence --sequence htmlSequence/hello,/whisk.system/utils/split,/whisk.system/utils/sort,htmlSequence/final --web true
vagrant@ubuntu-xenial:$ wsk action get htmlSequence/htmlSequence --url
```
Then type the URL into your browser with a string to parse and a character with which to parse the string, for example:
```
https://192.168.33.16/api/v1/web/guest/htmlSequence/htmlSequence?name=Joe%20likes%20to%20eat%20clementines&separator=%20
```
This parses the phrase "Joe likes to eat clementines" by the space character and prints it to to an html page (I didn't know this, but apparently %20 is the space character in URL language).





#### Useful FaaS links
-[OpenWhisk Default README](https://github.com/apache/openwhisk/blob/master/README.md)
-[blog post about how to deploy hello world javascript function and then call it via browser URL](https://horeaporutiu.com/blog/openwhisk-web-actions-and-rest-api-calls/)
-[API Gateway README](https://github.com/apache/openwhisk/blob/master/docs/apigateway.md)
-[packages README](https://github.com/apache/openwhisk/blob/master/docs/packages.md)
-[Web actions README](https://github.com/apache/openwhisk/blob/master/docs/webactions.md#web-actions)
-[Using REST APIs with OpenWhisk README](https://github.com/apache/openwhisk/blob/master/docs/rest_api.md)
-[OpenWhisk Workshop exercises and READMEs](https://github.com/apache/openwhisk-workshop/tree/master/exercises)
-[Example FaaS included by default in OpenWhisk Catalog](https://github.com/apache/openwhisk-catalog/tree/master/packages/utils)
-[OpenWhisk actions README](https://github.com/apache/openwhisk/blob/master/docs/actions.md)
























