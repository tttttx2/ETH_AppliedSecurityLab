#!/bin/bash

# split development compose setup into vms
csplit -z ../docker-compose.yml /#------/ {*}

echo 'version: "3.9"' > version
echo 'services: ' > version
for file in xx*; do
    newName=$(egrep -o '# VM [0-9]{2}' $file)
    newFile=${newName:5}/docker-compose.yml
    mkdir -p ${newName:5}
    cat version $file > $newFile
    rm $file
    
done

rm -rf 99
rm version

# modify network settings
for vm in 0*; do

    filename=$vm/docker-compose.yml

    csplit -z $filename '/#+++/' {*}

    for file in xx*; do

        ip=$(cat $file | grep "ipv4_address:" | egrep -o '([0-9]+\.*){4}')
        build=$(cat $file | grep "build:" | egrep -o '\./.*$'| sed 's/ *$//' | sed 's|\./||')

        # add host IP to port
        sed -i -e 's/80:80/"'$ip':80:80"/g' $file
        sed -i -e 's/443:443/"'$ip':443:443"/g' $file
        sed -i -e 's/514:514/"'$ip':514:514"/g' $file
        sed -i -e 's/1601:1601/"'$ip':1601:1601"/g' $file
        sed -i -e 's/3306:3306/"'$ip':3306:3306"/g' $file
        sed -i -e 's/#EXPOSETHIS/- "'$ip':443:443"/g' $file
        sed -i -e 's/.*- 10.*$//g' $file
        # remove int network
        sed -n '/networks:/q;p' $file > tmp
        mv tmp $file
    done
    #combine multi services
    for file in xx*; do
    cat $file >> tmp
    rm $file
    done
    mv tmp $filename
    
    # remove comments and newlines
    cat $filename | tr -s '\n' > tmp
    mv tmp $filename

    sed -i -e 's/.*#.*$//g' $filename
    
    cp -r ../$build $vm/$build

done
exit
