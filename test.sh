
PROGRESS=$(cat ./progress.log 2>/dev/null)
echo "$PROGRESS"
echo "1" > ./progress.log
echo