from ctumrs.topics.Plot3dColsFromTextFile import PlotFromCtuMrsTopicTextFile

plot = PlotFromCtuMrsTopicTextFile(
    "/home/donkarlo/Dropbox/projs/research/data/self-aware-drones/ctumrs/two-step/uav1-odometry-odom_gps.txt",
    ["field.pose.pose.position.x", "field.pose.pose.position.y", "field.pose.pose.position.z"])

plot.plot()
