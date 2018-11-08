#!/bin/bash
function makeDir(){
static_dir=$1
if [ ! -d $static_dir ];then
mkdir $static_dir
else
echo dir exist
fi
}
function getDir()
{
for element in `ls $1`
do
echo $element
dir_or_file=$1"/"$element
if [[ $element == *".zip"* ]]
then
echo '-----------------------------------------解压' $dir_or_file 'to' $result_dir
unzip -o -d $result_dir $dir_or_file
else

rf=$result_dir/$element
echo '非zip文件' $rf
if [ -d $rf ]
then
echo "请检查"$1"文件价内存在重复的数据文件"
exit
else
cp -R $dir_or_file $result_dir
fi

fi
done
}
echo $#
if [ $# -gt 0 ]; then
echo "参数个数为$#个"
root_dir=$1
root_dir_name=${root_dir##*/}
root_dir_dir=${root_dir%/*}
result_dir=$root_dir_dir/$root_dir_name'_RESULT'
rm -r $result_dir
mkdir $result_dir
getDir $1

for element in `ls $result_dir`
do
dir_or_file=$result_dir"/"$element
echo $element
if [[ $element == *"MACOSX"* ]]
then
echo '无用文件 -' $element
else
python ./collatingSignalData.py $dir_or_file
iOS=$dir_or_file'/result/iOS'
android=$dir_or_file'/result/android'
allDataSet=$result_dir'/allDataSet'
makeDir $allDataSet
if [ -d $iOS ]
then
echo '---ios---'
for layer in `ls $iOS`
do
pl=$iOS'/'$layer
rpl=$allDataSet'/iOS/'
echo 'path'$pl $rpl
makeDir $rpl
rpl=$rpl'/'$layer
makeDir $rpl
cp -R $pl/* $rpl

done
else
echo '---not exist ios---'
fi

if [ -d $android ]
then
echo '---android---'
for layer in `ls $android`
do
pl=$android'/'$layer
rpl=$allDataSet'/android/'
echo 'path'$pl $rpl
makeDir $rpl
rpl=$rpl'/'$layer
makeDir $rpl
cp -R $pl/* $rpl
done
else
echo '---not exist android---'
fi

fi

done

else
echo "请传入根目录"
fi



