for i in $(squeue -u mep22dku -p compute-16-64   -h  -t PD -o %i)

do

    scontrol update jobid=$i partition=compute-24-128

    echo $i

done
