export XOS_DIR=/opt/xos
nohup python computenode-synchronizer.py  -C $XOS_DIR/synchronizers/computenode/computenode_synchronizer_config > /dev/null 2>&1 &
