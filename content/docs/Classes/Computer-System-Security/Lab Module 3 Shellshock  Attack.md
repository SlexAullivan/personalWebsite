---
title: Shell Shock Attack
date: 3/04/2021
---



# Lab Module 3: Shellshock  Attack

Alexander Sullivan  
3/04/21

## Part One: Overview

Learning Objective: get first hand experience with the shellshock vulnerability.

We will be experimenting with the actual shellshock attack in this lab. The Shellshock attack was first developed on September 24, 2014, and was a vulnerability within the Bash program.

## Part Two: Lab Tasks

### 2.1 Experimenting with Bash function

Bash within Ubuntu 16.04 has already been patched to fix the vulnerability, so the creators of the SEED VM have included a vulnerable version of the Bash program inside the /bin folder, known as  `bash_shellshock`

We will design an experiment that will verify that the `bash_shellshock` program is indeed vulnerable to the shell shock attack and then try the attack on the regular Bash program.

![exportingfoo](/images/exportingfoo.png)

Above we can see the exploit that makes bash vulnerable to a shellshock attack, because of a function called `parse_and_execute()` within the bash code when a new shell is created the line `echo "malicious code"` was executed rather than copied as part of the environment variable. This is because environment variables need to be passed from parent to child process. 

Below you can see that I changed my shell to one vulnerable to the shellshock attack, and then used a similar exploit as explained during class to get the root shell. I'm not completely sure how this works, but I believe it has something to do with the fact that when you export your `foo` environment variable, then run our program `a.out`  uses the `system()` function to create a child process. When that child process is created it incorrectly parses the `foo` environment variable and executes the shell program. Then because `a.out` is a `setuid` program with root privileges the resulting shell is opened as root.

![bash_shellshock](images/bash_shellshock.png)

![gettingRoot](/images/gettingRoot.png)

### 2.2 Setting up CGI programs

In this task we set up a cgi program and then viewed the resulting page at `localhost/gi/bin/myprog.cgi`

​							 ![cgi-setup](/images/cgi-setup.png)

![cgi-setup](/images/curlcgi.png)

Then above you can see the page with the curl command.

### 2.3 Passing Data to Bash via Environment variable

In this task we changed the CGI program to display the environment variables  using  `strings /proc/$$/environ`

Seen using the curl command here:![cgiEnvVariables](/images/cgiEnvVariables.png)

This data could potentially be present from a remote server serving the web page. Here the info is from local host because we are running the web-server on our own machine.

### 2.4 Launching the Shellshock Attacks

So this gave me access to the root shell but I'm not sure if this attack was done correctly. First of all I changed the a.out program to the following

```c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void main(){

        setuid(geteuid());
        system("curl http://localhost/cgi-bin/myprog.cgi");

}

```

Then I changed the resulting binary of the program above to be a `setuid` program, and exported another `foo` environment variable like this:

`export foo='() { echo "hello"; }; /bin/sh`' 

The following is the result:

![cgishellshock](/cgishellshock.png)

### 2.5 Getting a Reverse Shell via Shellshock Attack

In this task we were supposed to be able to get a reverse shell from the web server to our own shell. I figured this out after watching the lecture from Wenliang Du on you tube. He goes over how to listen on a port using the `nc` command and how to redirect the std out and std in back to another shell process. 

Combining this with the shellshock attack and I was able to open a reverse shell within the web server. Some environment variables are passed from the client process to the server process, so you can user the shellshock attack in a similar way as earlier. I did this using two terminals on the same machine like so:

On one terminal I used `nc` to listen to port 9090:

![nccommand](/images/nccommand.png)

Then in another terminal I used a curl command and a shellshock attack to inject the reverse shell.

![curlReverseShell](/images/curlReverseShell.png)

Back on the first  terminal where I was listening I received the following:

![reverseShell](/images/reverseShell.png)

### 2.6 Using the Patched Bash

Running the same vulnerabilities as before I could no longer get the attacks to work. The shellshock injection has been patched so that the following commands are no longer executed.