#!/bin/bash
openssl pkcs12 -in $1 -out $1.pem -nodes