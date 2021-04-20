from ctumrs.topics.DumpedTextFile import DumpedTextFile
from ctumrs.topics.ThreeDPositionToVelocityObsSerieBuilderFromDumpedTextFile import \
    ThreeDPositionToVelocityObsSerieBuilderFromDumpedTextFile

dumpedTextFile = DumpedTextFile(
    "/home/donkarlo/Dropbox/projs/research/data/self-aware-drones/ctumrs/two-step/uav1-odometry-odom_gps.txt")

threeDMaker = ThreeDPositionToVelocityObsSerieBuilderFromDumpedTextFile(dumpedTextFile,
                                                                        ["field.pose.pose.position.x"
                                                                            , "field.pose.pose.position.y"
                                                                            , "field.pose.pose.position.z"],
                                                                        5000)
threeDMaker.saveToFileWithoutTime(
    "/home/donkarlo/Dropbox/projs/research/data/self-aware-drones/ctumrs/two-step/manip/pos-vel-obs-from-gps.txt"
    , ",")
