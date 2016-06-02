#!/bin/bash
svn st | grep !M | awk '{print $2"@"}' | xargs svn revert
