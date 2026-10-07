# 選択したオブジェクトのTRSを記憶する（コピーペーストのコピー動作）
# （シーンを跨げる。Mayaを閉じるまで保持される。）

import maya.cmds as cmds

global saved_trs_data
saved_trs_data = {}

selected = cmds.ls(sl=True)
if selected:
    obj = selected[0]

    saved_trs_data['t'] = cmds.getAttr(f"{obj}.t")[0]
    saved_trs_data['r'] = cmds.getAttr(f"{obj}.r")[0]
    saved_trs_data['s'] = cmds.getAttr(f"{obj}.s")[0]

    cmds.inViewMessage(amg=f"<color=yellow>{obj}</color> のTRSをコピーしました。", pos='midCenter', bkc=0x00000000, fade=True)
else:
    cmds.warning("オブジェクトが選択されていません。")


print(saved_trs_data)
