#!/bin/bash

cd /kaptnn-financial-calculator-api/

git fetch origin

LOCAL=$(git rev-parse @)
REMOTE=$(git rev-parse @{u})

if [ "$LOCAL" != "$REMOTE" ]; then
    echo "New updates detected. Applying updates..."
    git reset --hard HEAD
    git pull origin production

    pm2 restart apisempoa
else
    echo "No updates detected."
fi
