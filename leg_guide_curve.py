import maya.cmds as cmds

# ３つのジョイントを順番に選択してもらう（大腿、膝、足首の順）
selection = cmds.ls(sl=True, type="joint")
if len(selection) != 3:
    cmds.error("大腿、膝、足首、の３つのジョイントを順番に選択してください。")
else:
    thigh_jnt = selection[0]
    knee_jnt = selection[1]
    ankle_jnt = selection[2]
    
    # カーブの始点と終点のワールド座標値を取得する。
    # queryオプションにすることで、値の読み取りモードになる。
    pos_thigh = cmds.xform(thigh_jnt, query=True, translation=True, worldSpace=True)
    pos_ankle = cmds.xform(ankle_jnt, query=True, translation=True, worldSpace=True)
    
    # カーブを生成。degree=1により、直線になる。
    guide_curve = cmds.curve(degree=1, point=[pos_thigh, pos_ankle])
    
    # 
    cmds.insertKnotCurve(guide_curve, addKnots=1, parameter=0.5, insertBetween=True, replaceOriginal=True)
    
    # 追加した中点のワールド座標を取得。エディットポイントの番号が再割り当てで、ep[1]が中点である。
    # 膝を移動したあとに足首がずれたのを戻すために、ガイドカーブの終点座標も取得しておく。
    mid_points_pos = cmds.pointPosition(f"{guide_curve}.ep[1]", world=True)
    end_points_pos = cmds.pointPosition(f"{guide_curve}.ep[2]", world=True)
    
    # 膝のジョイントを、直線の中点にスナップさせる（ジョイントを中点の位置に移動）
    # 膝の後で、足首を移動する。（元の位置にもどす）
    cmds.xform(knee_jnt, translation=mid_points_pos, worldSpace=True)
    cmds.xform(ankle_jnt, translation=end_points_pos, worldSpace=True)
    
    # カーブを選択して終わる
    cmds.select(guide_curve)
    print(f"成功：{guide_curve}を作成し、{knee_jnt}を平面上の直線にスナップしました。")
    