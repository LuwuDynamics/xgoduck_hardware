"""Measure Gazebo model and joint motion during one experimental gait."""
import json
import math
import threading
import time
from gz.transport13 import Node
from gz.msgs10.model_pb2 import Model
from gz.msgs10.pose_v_pb2 import Pose_V
import walk_controller

samples = []
foot_heights = {"left_foot": [], "right_foot": []}
lock = threading.Lock()

def on_state(msg):
    row = {
        "x": msg.pose.position.x, "y": msg.pose.position.y, "z": msg.pose.position.z,
        "q": [msg.pose.orientation.x, msg.pose.orientation.y,
              msg.pose.orientation.z, msg.pose.orientation.w],
        "joints": {j.name: j.axis1.position for j in msg.joint},
    }
    with lock:
        samples.append(row)

def on_poses(msg):
    with lock:
        for pose in msg.pose:
            if pose.name in foot_heights:
                foot_heights[pose.name].append(pose.position.z)

def main():
    node = Node()
    node.subscribe(Model, "/world/cece_starter_room/model/cece_prototype/joint_state", on_state)
    node.subscribe(Pose_V, "/world/cece_starter_room/dynamic_pose/info", on_poses)
    time.sleep(2)
    with lock:
        if not samples:
            raise RuntimeError("No Gazebo joint-state messages")
        first = samples[-1]
        samples.clear()
        samples.append(first)
        for values in foot_heights.values():
            values.clear()
    walk_controller.main()
    time.sleep(1)
    with lock:
        rows = list(samples)
        feet = {name: list(values) for name, values in foot_heights.items()}
    final = rows[-1]
    names = walk_controller.NAMES
    result = {
        "samples": len(rows),
        "displacement_m": [final[k] - first[k] for k in ("x", "y", "z")],
        "joint_range_degrees": {
            n: math.degrees(max(r["joints"].get(n, 0) for r in rows) -
                            min(r["joints"].get(n, 0) for r in rows)) for n in names},
        "foot_frame_vertical_range_m": {
            n: max(values) - min(values) if values else None for n, values in feet.items()},
        "note": "No foot contact or physical walk is validated by this measurement."
    }
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
