plotBase=$1

echo $plotBase
input1="inputRootFiles/DUMMYFILENAME_RU.root"
input2="inputRootFiles/DUMMYFILENAME_UF.root"
#plotdir1="~/public_html/2017/20171203_cscSeg/ME11/"
#plotdir2="~/public_html/2017/20171203_cscSeg/nonME11/"
plotdir1=${plotBase}"ME11/"
plotdir2=${plotBase}"nonME11/"
mkdir -p $plotdir1 $plotdir2
cp /home/mhl/public_html/index.php $plotdir1
cp /home/mhl/public_html/index.php $plotdir2

plotfile1="tmpRootPlots/CSCresults_RU_ME11.root"
plotfile2="tmpRootPlots/CSCresults_UF_ME11.root"
plotfile3="tmpRootPlots/CSCresults_RU_nonME11.root"
plotfile4="tmpRootPlots/CSCresults_UF_nonME11.root"
t1="RU"
t2="UF"

python compareTwoSmallTree.py --input1 ${input1} --input2 ${input2} --doME11 --plotdir ${plotdir1}
python compareTwoSmallTree.py --input1 ${input1} --input2 ${input2} --plotdir ${plotdir2}

python runSelector.py --inputfile ${input1} -t "RU_nonME11"
python runSelector.py --inputfile ${input1} --doME11 -t "RU_ME11"
python runSelector.py --inputfile ${input2} -t "UF_nonME11"
python runSelector.py --inputfile ${input2} --doME11 -t "UF_ME11"
python makeplots.py --plotfile1 ${plotfile1} --plotfile2 ${plotfile2} --t1 ${t1} --t2 ${t2} --plotdir ${plotdir1}
python makeplots.py --plotfile1 ${plotfile3} --plotfile2 ${plotfile4} --t1 ${t1} --t2 ${t2} --plotdir ${plotdir2}

