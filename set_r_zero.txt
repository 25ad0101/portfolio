import maya.cmds as cmds

selection = cmds.ls(sl=True)

for obj in selection:
    cmds.xform(obj, rotation=[0, 0, 0])
