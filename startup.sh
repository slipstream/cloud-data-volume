#!/bin/bash -e

. /root/slipstream-env/bin/activate

python /opt/slipstream/bin/mount-data.py

ss-get tcp.8888 || true

deactivate

(cd /gssc && jupyter lab --ip=0.0.0.0 --allow-root --no-browser --NodebookApp.token='') &

jupyter notebook list
