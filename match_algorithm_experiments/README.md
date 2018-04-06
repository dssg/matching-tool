# Running Matching Algorithm Experiments

Tuning the matching algorithm requires trying many combinations of parameters to see which produces the best matches. Rather than running each combination and then checking the results, it is easier to run many combinations of parameters at once and then compare all of the results at the end. The files in this repository are intended to help with this.

The procedure for running these experiments is roughly:

1. Create a distinct `docker-compose.yml` for each combination of parameters you want to try. 
2. Upload each of these to a directory on S3.
3. For each file, launch an EC2 instance that downloads the file and runs the specified matching algorithm.



