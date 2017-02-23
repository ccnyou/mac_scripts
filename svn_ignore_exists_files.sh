#!/bin/bash
svn st | grep ? | awk '{print $2"/../@"}' | xargs svn propset svn:ignore '*' 
