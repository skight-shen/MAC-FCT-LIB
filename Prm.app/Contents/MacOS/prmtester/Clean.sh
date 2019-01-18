base_folder=$(dirname $0)
find $base_folder -name "*.pyc" -exec rm {} \;
find $base_folder -name "*.log" -exec rm {} \;