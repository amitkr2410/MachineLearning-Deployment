#!/bin/bash

#to remove temp files

find . -type f \( -iname "*DS_Store" \) -delete
find . -type f \( -iname "*~" \) -delete
