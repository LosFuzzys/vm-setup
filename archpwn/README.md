# Docker Containers

To build one of the containers, just use ```sudo docker build -t $name ./$name```


## Container Security

Remember: containers don't contain. Never run untrusted binaries as root in the 
container. If you need to do something scary, set up a VM and use the containers 
inside this VM. Hopefully this repo will contain a script to do that for you.


## archpwn

[archpwn](archpwn/) is a container that contains some useful tools for pwning
stuff during CTFs, so that you don't have to install or update everything before
the start of a CTF.

Building:
```sudo docker build -t archpwn ./archpwn```
Running:
```sudo docker run -t -i -v /path/to/you/ctf/folder:/ctf:z archpwn```

TODO:
  * Add more intersting tools
  * Can we install/use GUI applications?
  * Any other fancy configs to make shell usage easier?
  * Can we use the install scripts from [ctf-tools](https://github.com/LosFuzzys/ctf-tools)

