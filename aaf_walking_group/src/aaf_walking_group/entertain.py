#!/usr/bin/env python

import rospy
import smach
from std_msgs.msg import String
import strands_webserver.client_utils
from aaf_walking_group.msg import EmptyActionGoal


class Entertain(smach.State):
    def __init__(self, display_no, gaze, image_client):
        smach.State.__init__(
            self,
            outcomes=['key_card', 'killall'],
            input_keys=['current_waypoint'],
            output_keys=['current_waypoint']
        )
        self.display_no = display_no
        self.card = False
        self.sub = None
        self.gaze = gaze
        self.image_client = image_client

    def execute(self, userdata):
        self.gaze.people()
        self.image_client.send_goal(EmptyActionGoal())
        self.card = False
        self.sub = rospy.Subscriber("/socialCardReader/commands", String, callback=self.callback)
        rospy.loginfo("Showing entertainment interface.")
        strands_webserver.client_utils.display_relative_page(self.display_no, "entertainment.html")
        rospy.loginfo("I am at: " + userdata.current_waypoint)
        while not self.card and not rospy.is_shutdown() and not self.preempt_requested():
            rospy.sleep(1)
        self.gaze.preempt()
        self.image_client.cancel_all_goals()
        if self.preempt_requested():
            self.sub.unregister()
            self.sub = None
            return 'killall'
        return 'key_card'

    def callback(self, data):
        rospy.loginfo("got card: " + str(data.data))
        if data.data == "PAUSE_WALK":
            self.card = True
            self.sub.unregister()
            self.sub = None