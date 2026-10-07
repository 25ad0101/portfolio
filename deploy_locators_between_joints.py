import maya.cmds as cmds

def deploy_locators_between_joints():
    
    selection = cmds.ls(sl=True, type="joint")
    
    if len(selection) != 2:
        cmds.warning("２つのジョイントを選択してから実行してください。")
        return
        
    joint_a = selection[0]
    joint_b = selection[1]
    
    pos_a = cmds.xform(joint_a, q=True, ws=True, t=True)
    pos_b = cmds.xform(joint_b, q=True, ws=True, t=True)
    
    created_locators = []
    for i in range(1, 4):
        weight = i * 0.25
        
        x = pos_a[0] + (pos_b[0] - pos_a[0]) * weight
        y = pos_a[1] + (pos_b[1] - pos_a[1]) * weight
        z = pos_a[2] + (pos_b[2] - pos_a[2]) * weight
        
        loc = cmds.spaceLocator(name=f"between_loc_{i:02d}")[0]
        cmds.xform(loc, ws=True, t=(x, y, z))
        created_locators.append(loc)
        
    cmds.select(created_locators)
    print(f"成功：{joint_a} と {joint_b} の間に３つのロケータを配置しました。")
    
    
deploy_locators_between_joints()
