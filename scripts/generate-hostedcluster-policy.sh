#!/bin/bash

DIRECTORY="/tmp/*/"
FILENAME="policy-generator-config-hostedcluster.yaml"
ROOT_DIR=$PWD
for dir in $DIRECTORY; do
    echo $dir
    if [ -n $dir ]
    then
        cd $dir
        name=$(grep "\- name:" $FILENAME | cut -d: -f2- | xargs)
        echo $name
        PolicyGenerator $FILENAME > $ROOT_DIR/deploy/acm-policies/50-GENERATED-$name.Policy.yaml
        cd $ROOT_DIR
    fi
done