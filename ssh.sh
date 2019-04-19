#!/bin/sh
ssh -4 -L 5432:cisdb.cis.uab.edu:5432 $1@moat.cs.uab.edu
