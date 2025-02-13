#!/bin/env bash

for RC in `find . -type f -regex \\.+RC`
do
    FINAL=${RC%.*}
    echo "Finalizing $RC into $FINAL"
    mv $FINAL ./history/
    mv $RC $FINAL
done
