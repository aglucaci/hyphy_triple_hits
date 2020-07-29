#!/bin/bash

clear

echo ""
echo "# ###"
echo ""


BASEDIR="/Users/user/Documents/EmpiricalDatasets"

# Available online at
# https://github.com/veg/hyphy/blob/master/res/TemplateBatchFiles/SelectionAnalyses/BUSTED.bf
# https://github.com/veg/hyphy-analyses/blob/master/BUSTED-MH/BUSTED-MH.bf

BUSTEDS=$BASEDIR"/hyphy-develop/res/TemplateBatchFiles/SelectionAnalyses/BUSTED.bf"
BUSTEDSMH=$BASEDIR"/hyphy-analyses/BUSTED-MH/BUSTED-MH.bf"
HYPHY=$BASEDIR"/hyphy-develop/hyphy"
res=$BASEDIR"/hyphy-develop/res"

echo "# Settings"
echo "BASEDIR: "$BASEDIR
echo "HYPHY: "$HYPHY
echo "Resources: "$res
echo "BUSTEDS batch file: "$BUSTEDS
echo "BUSTEDS-MH batch file: "$BUSTEDSMH
echo ""

echo "# File checks"

# File checks
if [ -f "$HYPHY" ]; then
    echo "$HYPHY exists."
else
    echo "$HYPHY does not exist."
fi

if [ -f "$BUSTEDS" ]; then
    echo "$BUSTEDS exists."
else
    echo "$BUSTEDS does not exist."
fi

if [ -f "$BUSTEDSMH" ]; then
    echo "$BUSTEDSMH exists."
else
    echo "$BUSTEDSMH does not exist."
fi
# End file checks
echo ""


echo "Starting to process files..."

for file in $BASEDIR/11-datasets/*.nex; do
    echo "Processing: "$file
    
    #Does the nexus file exist and is not empty?
    if [ -s "$file" ]; then
        echo "    $file data exists and is not empty"
        
        # [1] Process it for BUSTEDS
        CHECK=$file".BUSTEDS.json"
        if [ -s "$CHECK" ]
        then
           echo "    BUSTEDS file exists and is not empty "
        else
           echo "    BUSTEDS file does not exist, or is empty "
           echo $HYPHY $BUSTEDS LIBPATH=$res --alignment $file --output $file".BUSTEDS.json"
        fi
    
        CHECK=$file".BUSTEDS-MH.json"
        # [2] Process it for BUSTEDS-MH
        if [ -s "$CHECK" ]
        then
           echo "    BUSTEDS-MH file exists and is not empty "
        else
           echo "    BUSTEDS-MH file does not exist, or is empty "
           echo $HYPHY $BUSTEDSMH LIBPATH=$res --alignment $file --output $file".BUSTEDS-MH.json"
        fi
    else
        echo "    $file does not exist or is empty"
    fi
    
    #$HYPHY $BUSTEDS --alignment $file --output $file".BUSTEDS.json"
    
    #$HYPHY $BUSTEDSMH --alignment $file --output $file".BUSTEDS-MH.json"
done


# Mitochondrial dataset
echo ""
echo "# Trying - Mitochondrial dataset "
for file in $BASEDIR/11-datasets/*.mtnex; do
    echo "Processing (mt nexus): "$file
    #Does the nexus file exist and is not empty?
    if [ -s "$file" ]; then
        echo "    $file data exists and is not empty"
        
        # [1] Process it for BUSTEDS
        CHECK=$file".BUSTEDS.json"
        if [ -s "$CHECK" ]
        then
           echo "    BUSTEDS file exists and is not empty "
        else
           echo "    BUSTEDS file does not exist, or is empty "
           #Vertebrate-mtDNA
           #Invertebrate-mtDNA
           $HYPHY $BUSTEDS LIBPATH=$res --alignment $file --output $file".BUSTEDS.json" --code Vertebrate-mtDNA
        fi
    
        CHECK=$file".BUSTEDS-MH.json"
        # [2] Process it for BUSTEDS-MH
        if [ -s "$CHECK" ]
        then
           echo "    BUSTEDS-MH file exists and is not empty "
        else
           echo "    BUSTEDS-MH file does not exist, or is empty "
           $HYPHY $BUSTEDSMH LIBPATH=$res --alignment $file --output $file".BUSTEDS-MH.json" --code Vertebrate-mtDNA
        fi
    else
        echo "    $file (mt nexus) data does not exist or is empty"
    fi
    
done

