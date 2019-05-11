#!/bin/bash

. ./unimelb-comp90024-group-18-openrc.sh; ansible-playbook -v -i hosts -u ubuntu --key-file=~/.ssh/Group18.pem wordpress.yaml