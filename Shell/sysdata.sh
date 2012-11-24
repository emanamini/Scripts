#!/bin/bash 

# CALCULATE VARIABLES
CORES=4
oldBRecived=0
oldBTransmited=0
netInterface=/proc/net/dev

# FUNCTIONS
function getRamInfo
{
    totalMemory=$(free -m | grep "Mem:" | awk '{printf( "%.2f", $2/1024)}' )
    usedMemory=$(free -m | grep "buffers/cache" | awk '{printf( "%.2f", $3/1024)}')
    memInPercent=$(echo "$totalMemory $usedMemory" | awk '{printf( "%.0f", $2/($1/100)) }')
}
function getNetBytes
{
    Brecived=$(cat $netInterface | grep "eth0" | awk '{print($2)}')
    Btransmited=$(cat $netInterface | grep "eth0" | awk '{print($10)}')
}
function getCpuInfo()
{
    CORE=$1
    addr="^cpu${CORE}"
    local CPU=(`cat /proc/stat | grep $addr`) # Get the total CPU statistics.
    unset CPU[0]                                # Discard the "cpu" prefix.
    local IDLE=${CPU[4]}                        # Get the idle CPU time.

    # Calculate the total CPU time.
    local TOTAL=0
    for VALUE in "${CPU[@]}"; do
	let "TOTAL=$TOTAL+$VALUE"
    done

    # Catch current cores last state
    PREV_IDLE=$(eval echo \PREV_IDLE$CORE)
    PREV_TOTAL=$(eval echo \PREV_TOTAL$CORE)
    
    # Calculate the CPU usage since we last checked.
    let "DIFF_IDLE=$IDLE-$PREV_IDLE"
    let "DIFF_TOTAL=$TOTAL-$PREV_TOTAL"
    let "DIFF_USAGE=(1000*($DIFF_TOTAL-$DIFF_IDLE)/$DIFF_TOTAL+5)/10"

    eval \PREV_TOTAL$CORE="$TOTAL"
    eval \PREV_IDLE$CORE="$IDLE"
}

# GENERATE OUTPUT
while true;
do
    getNetBytes
    getRamInfo
    for (( COUNT=0; COUNT < $CORES; COUNT++ ));do
	getCpuInfo $COUNT
	eval \cpu$COUNT=$DIFF_USAGE
    done
    # Date and time: Tue 2012.11.06 10:49
    date=$(date +"%a %Y.%m.%d %H:%M")
    
    dlSpeed=$(echo $(( $Brecived-$oldBRecived )) | awk '{printf( "%.2f", $1/1024)}')
    upSpeed=$(echo $(( $Btransmited-$oldBTransmited )) | awk '{printf( "%.2f", $1/1024)}')
    traffic=$(echo "$Brecived $Btransmited" | awk '{printf( "%.2f", ($1+$2)/1024/1024 )}')

    printf \
	"CPU: %3s,%3s,%3s,%3s | RAM: %sG/%sG (%s%%) | LAN: ↓: %5sk ↑: %5sk T↕: %6s | %s  \n" \
	"$cpu0" "$cpu1" "$cpu2" "$cpu3" "$usedMemory" \
	"$totalMemory" "$memInPercent" "$dlSpeed" \
	"$upSpeed" "$traffic" "$date"
    oldBRecived=$Brecived
    oldBTransmited=$Btransmited
    sleep 1
done
