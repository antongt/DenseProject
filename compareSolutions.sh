#!/bin/bash

# This script uses diff to print the differences between two files.

command=diff
options="--ignore-blank-lines --ignore-matching-lines=^[[:blank:]]*#"

$command $options $1 $2

