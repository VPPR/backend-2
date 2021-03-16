#!/usr/bin/env bash

function run_cmd() {
    ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null prk@$SERVER_IP "$*"
}

eval $(ssh-agent)
ssh-add - <<< $SSH_KEY
run_cmd "git -C backend fetch origin main"
run_cmd "git -C backend reset --hard origin/main"
run_cmd "sudo systemctl restart backend"
eval $(ssh-agent -k)