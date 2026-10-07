import maya.cmds as cmds

selection = cmds.ls(sl=True)

for item in selection:
    objName = "{}".format(item)
    
    # 0:Center, 1:Left, 2:Right
    sideNum = 0
    if "Left" in objName: sideNum = 1
    if "Right" in objName: sideNum = 2
    attrSide = "{}.side".format(item)
    cmds.setAttr(attrSide, sideNum)
    
    # 18:Other
    attrType = "{}.type".format(item)
    cmds.setAttr(attrType, 18)

    otherType = "{}.otherType".format(item)
    boneName = (
        objName.replace("Left", "")
               .replace("Right", "")
               .replace("_JNT", "")
    )
    cmds.setAttr(otherType, boneName, type="string")
    
    