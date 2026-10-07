# 記憶したTRSを別のオブジェクトに適用する（ペースト動作）

import maya.cmds as cmds

global saved_trs_data

if "saved_trs_data" in globals() and saved_trs_data:
    selected = cmds.ls(sl=True)
    if selected:
        for obj in selected:
            cmds.setAttr(f"{obj}.t", *saved_trs_data["t"])
            cmds.setAttr(f"{obj}.r", *saved_trs_data["r"])
            cmds.setAttr(f"{obj}.s", *saved_trs_data["s"])
        cmds.inViewMessage(amg="TRS値をペーストしました。", pos="midCenter", bkc=0x00000000, fade=True)
    else:
        cmds.warning("ペースト先のオブジェクトが選択されていません。")
else:
    cmds.warning("コピーされたTRSデータがありません。先にコピーを実行してください。")
    
