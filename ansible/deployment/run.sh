#!/bin/bash

. ./unimelb-comp90024-group-18-openrc.sh; ansible-playbook -u ubuntu --ask-become-pass --key-file=~/.ssh/Group18.pem deploy.yaml