#!/usr/bin/env bash

#SBATCH --time=24:00:00
#SBATCH --mem=32G
#SBATCH --job-name=count_africa
#SBATCH --partition=dali
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=12
#SBATCH --mail-type=END
#SBATCH --mail-user=yichia3@illinois.edu
#SBATCH --mail-type=FAIL
#SBATCH --output=%x-%j.out

. /projects/dali/spack/share/spack/setup-env.sh
spack env activate dali

python3 calculate_class_dist_South_Africa.py
