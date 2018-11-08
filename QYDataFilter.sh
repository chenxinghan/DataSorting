#!/bin/bash

function getdir(){
for element in `ls $1`
do
dir_or_file=$1"/"$element
if [ -d $dir_or_file ]
then
file=${dir_or_file//$root_dir/''}
echo $file
makeDir $dst_root_dir/$file
getdir $dir_or_file
else
echo $dir_or_file
file=${dir_or_file//$root_dir/''}
dst_file=$dst_root_dir/$file
if [[ $file == *"allsensordata"* ]]
then
    echo "`grep -E ',12,|,11,|,3,|,10,' $dir_or_file`" > $dst_file
else
    echo "不包含"
    cp $dir_or_file $dst_file
fi
fi
done

}
function makeDir(){
static_dir=$1
if [ ! -d $static_dir ];then
mkdir $static_dir
else
echo dir exist
fi
}
root_dir=$1
root_dir_dir=${root_dir%/*}
root_dir_name=${root_dir##*/}
dst_root_dir=$root_dir_dir/$root_dir_name'_bak'
rm -rf $dst_root_dir
makeDir $dst_root_dir
echo $dst_root_dir
getdir $root_dir





