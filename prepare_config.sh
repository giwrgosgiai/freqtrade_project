#!/bin/bash

# Έλεγχος αν έχει οριστεί το SERVICE_NAME
if [ -z "$SERVICE_NAME" ]; then
    echo "Το SERVICE_NAME δεν έχει οριστεί"
    exit 1
fi

# Αντιγραφή του κατάλληλου config
cp "/freqtrade/user_data_${SERVICE_NAME}/config.json" "/freqtrade/user_data/config.json"

# Εκτέλεση της αρχικής εντολής
exec "$@" 