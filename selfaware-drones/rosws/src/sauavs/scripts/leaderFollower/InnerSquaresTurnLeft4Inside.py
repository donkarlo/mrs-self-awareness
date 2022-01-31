from nav_msgs.msg import Odometry

class InnerSquaresTurnLeft4Inside:

    def getXyz(self, leaderOdometryNavMsg:Odometry)->(float, float, float, float):
        leaderPosition = leaderOdometryNavMsg.pose.pose.position

        followerPosX = None
        followerPosY = None
        followerPosZ = None
        followerHeading = None

        followerPosZ = leaderPosition.z

        # The heading is always constant
        followerHeading = 11

        tol = 0.5
        if leaderPosition.x < -5 and leaderPosition.x > -15 and leaderPosition.y > 5 and leaderPosition.y < 15:
            # Region 1
            followerPosX = -5
            followerPosY = 5
        elif leaderPosition.x > -5 and leaderPosition.x < 5 and leaderPosition.y < 15 + tol and leaderPosition.y > 15 - tol:
            # Region 2
            followerPosX = leaderPosition.x
            followerPosY = leaderPosition.y - 10
        elif leaderPosition.x > 5 and leaderPosition.x < 15 and leaderPosition.y > 5 and leaderPosition.y < 15:
            # Region 3
            followerPosX = 5
            followerPosY = 5

        ###############TURN INNER 4 STARTS HERE#################
        elif leaderPosition.x > 15 - tol and leaderPosition.x < 15 + tol and leaderPosition.y < 5 and leaderPosition.y > 2:
            # Region 4: going down
            followerPosX = leaderPosition.x - 10
            followerPosY = leaderPosition.y
        elif leaderPosition.x < 15 and leaderPosition.x > 11 and leaderPosition.y < 2+ tol and leaderPosition.y > 2-tol:
            # First turn left
            followerPosX = (15-leaderPosition.x)+5
            followerPosY = leaderPosition.y
        elif leaderPosition.x > 11 - tol and leaderPosition.x < 11 + tol and leaderPosition.y < 2 and leaderPosition.y >-2:
            # then go down together
            followerPosX = leaderPosition.x-2
            followerPosY = leaderPosition.y
        elif  leaderPosition.x < 15 and leaderPosition.x > 11 and leaderPosition.y < -2+ tol and leaderPosition.y > -2-tol:
            # Finaly turn right
            followerPosX = (15 - leaderPosition.x) + 5
            followerPosY = leaderPosition.y
        elif leaderPosition.x > 15 - tol and leaderPosition.x < 15 + tol and leaderPosition.y < -2 and leaderPosition.y > -5:
            # Region 4: continue down
            followerPosX = leaderPosition.x - 10
            followerPosY = leaderPosition.y
        #################################

        elif leaderPosition.x > 5 and leaderPosition.x < 15 and leaderPosition.y < -5 and leaderPosition.y > -15:
            # Region 5
            followerPosX = 5
            followerPosY = -5
        elif leaderPosition.x < 5 and leaderPosition.x > -5 and leaderPosition.y > -15 - tol and leaderPosition.y < -15 + tol:
            # Region 6
            followerPosX = leaderPosition.x
            followerPosY = leaderPosition.y + 10
        elif leaderPosition.x < -5 and leaderPosition.x > -15 and leaderPosition.y < -5 and leaderPosition.y > -15:
            # Region 7
            followerPosX = -5
            followerPosY = -5
        elif leaderPosition.x < -15 + tol and leaderPosition.x > -15 - tol and leaderPosition.y > -5 and leaderPosition.y < 5:
            # Region 8
            followerPosX = leaderPosition.x + 10
            followerPosY = leaderPosition.y

            # z position doesnt change
        return (followerPosX,followerPosY,followerPosZ,followerHeading)