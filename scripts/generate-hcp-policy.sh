#!/bin/bash

DIRECTORY="/tmp-hcp/*/"
FILENAME="policy-generator-config-hcp.yaml"
ROOT_DIR=$PWD
for dir in $DIRECTORY; do
    echo $dir
    if [ -n $dir ]
    then
        cd $dir
        name=$(grep "\- name:" $FILENAME | cut -d: -f2- | xargs)
        echo $name
        PolicyGenerator $FILENAME > $ROOT_DIR/deploy/acm-policies/40-GENERATED-$name.Policy.yaml
        cd $ROOT_DIR
    fi
done
