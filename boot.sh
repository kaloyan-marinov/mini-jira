#!/bin/sh

source venv/bin/activate

while true; do
    echo "trying to execute the database-migration scripts"
    flask db upgrade

    if [[ "$?" == "0" ]]; then
        echo "- succeeded!"
        break
    fi

    echo "- failed; wait 5 seconds before re-trying..."
    sleep 5
done

exec gunicorn -b :5000 --access-logfile - --error-logfile - application:app
