#!/bin/bash

IPADDR=$(ifconfig | grep 'inet ' | awk '{print $2}' | grep -v '127.0.0.1')
echo 'export IPADDR="'$IPADDR'"' >> ~/.bashrc
exec $SHELL

