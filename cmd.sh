#!/bin/bash


export train_cmd="run.pl --max-jobs-run 3"
export decode_cmd="run.pl --max-jobs-run 3"
export mkgraph_cmd="run.pl --max-jobs-run 3"

if [[ "$HOSTNAME" == *"sharc"* ]]; then
    export train_cmd="queue.pl --mem 6G"
    export decode_cmd="queue.pl --mem 8G"
fi
