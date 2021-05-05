# Environment Variables (Reading)

[Link to Reading](https://www.digitalocean.com/community/tutorials/how-to-read-and-set-environmental-and-shell-variables-on-linux)

**Environment:**

An area that the shell builds every time that it starts a session, that contains variables that define system properties.

Every time a shell spawns a process gathers and compiles information that should be available to the shell process and any children, from files and settings on the system.

Environment is implemented as key value pairs, if there are multiple values they are separated by colons :

`KEY = value1: value2`

if there is white space: 

` KEY = "value  with spaces  " `

**Environment Variables:** variables defined for the current shell, inherited by any child shells. used to pass information into processes that are spawned from the shell.

**Shell Variables:** variables contained only in the shell that they were defined in, used for ephemeral data for example the working directory

print variables with:

`printenv`

`env` lets you modify the environment that programs run ion by passing a set of variable definitions into a command line

`set` : get a list of all shell variables, environment variables, local variables, and shell functions

- Environment variables are only passed to the child processes. so if a new environment variable is made within a child process the variable is destroyed when we return to the parent process.

To make environment variables persistent even after the process, is closed so they do not need to be set every time bash is started, is more difficult than it seems due to the fact that bash starts in different ways depending on how the process is opened.

**Login vs non-Login shells**

- **login:** begins by authenticating the user, via terminal or ssh and authenticate
    - will read details from /etc/profile first, then look for the first login shell configuration file in the users home directory.
    - reads the first file within  ~/.bash_profile, ~/.bash_login, and ~/.profile
    - doesn't read any further files in the above
- **non-login:** starting a shell within an authenticated session, for example calling bash within terminal. we were not asked for authentication details
    - will read /etc/bash.bashrc, then the user specified ~/.bashrc to build environment

**interactive and non interactive:**

- **interactive:** shell session attached to a terminal
    - normal session that begins with ssh
- **non interactive:** not attached to a terminal session
    - script run from command line: non interactive, non log in
    - read the environmental variable called BASH_ENV, and read the file specified to define the new environment
- shell sessions can be any combo of interactive, non interactive, login and non login

**Implementing Environment Variables:**

- Usually we want our settings to be available both within the login and non login shells, so we define variables within the `~/.bashrc` file
- new environment variables can be placed anywhere within the file
- if system wide variables are needed then you need to think about adding them to `/etc/profile`, `/etc/bash.bashrc` , `/etc/environment`