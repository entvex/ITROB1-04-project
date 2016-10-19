echo "killing all the things"
sleep 1
ps -ef | grep visionNode | grep -v grep | awk '{print $2}' | xargs kill
ps -ef | grep armControllerNode | grep -v grep | awk '{print $2}' | xargs kill
ps -ef | grep gripperNode | grep -v grep | awk '{print $2}' | xargs kill
ps -ef | grep gameLogicNode | grep -v grep | awk '{print $2}' | xargs kill
