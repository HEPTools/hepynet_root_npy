docker run -it --rm \
    -v $(git rev-parse --show-toplevel):/work \
    -v /net/s3_datae/yangz:/data \
    -w /work \
    starp/hepynet_root_npy:v0 bash
