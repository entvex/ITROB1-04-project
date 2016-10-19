#echo "start roscore"
#gnome-terminal --working-directory=/home/username/Desktop/CCA/
#gnome-terminal -e  /home/ubuntu/catkin_ws/src/au_crustcrawler_base/launch/base/au_crustcrawler_base base.launch
#sleep 3
#echo "start rosmeta"
#gnome-terminal -e au_crustcrawler_base meta.launch
#sleep 2
gnome-terminal -e "bash -c \"/home/ubuntu/ITROB1-04-project/catkin_ws/src/crossnballs/nodes/visionNode.py; exec bash\""
gnome-terminal -e "bash -c \"/home/ubuntu/ITROB1-04-project/catkin_ws/src/crossnballs/nodes/armControllerNode.py; exec bash\""
gnome-terminal -e "bash -c \"/home/ubuntu/ITROB1-04-project/catkin_ws/src/crossnballs/nodes/gripperNode.py; exec bash\""
echo "start game logic"
sleep 1
gnome-terminal -e "bash -c \"/home/ubuntu/ITROB1-04-project/catkin_ws/src/crossnballs/nodes/gameLogicNode.py; exec bash\""
