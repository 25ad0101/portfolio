import maya.cmds as cmds

# 1. シーン内のすべてのジョイントを取得
all_joints = cmds.ls(type="joint")
joints_to_select = []

for jt in all_joints:
    # --- 【改良】除外フィルターの適用 ---
    
    # フィルターA: 親が存在するか確認（親がいない＝ルートジョイントなので除外）
    parent = cmds.listRelatives(jt, parent=True)
    if not parent:
        continue # ルートはスキップして次のジョイントへ
        
    # フィルターB: 親が持っている子供（自分の一族）の数を調べる
    # parent[0] は自分の直上の親の名前
    siblings = cmds.listRelatives(parent[0], children=True, type="joint")
    if siblings and len(siblings) >= 2:
        continue # 兄弟（枝分かれ）がいる場合はスキップして次のジョイントへ
        
    # ----------------------------------

    # 2. アトリブートからTranslate X, Y, Z の値を取得
    tx = cmds.getAttr(f"{jt}.translateX")
    ty = cmds.getAttr(f"{jt}.translateY")
    tz = cmds.getAttr(f"{jt}.translateZ")
    
    # 3. 0ではない軸の数をカウント (絶対値で判定)
    non_zero_count = 0
    if abs(tx) > 0.001: non_zero_count += 1
    if abs(ty) > 0.001: non_zero_count += 1
    if abs(tz) > 0.001: non_zero_count += 1
    
    # 4. 2軸以上に入っていればリストに追加
    if non_zero_count >= 2:
        joints_to_select.append(jt)

# 5. 条件に一致したジョイントを【一括で】選択する
if joints_to_select:
    cmds.select(joints_to_select, replace=True)
    print(f"【成功】エラーの可能性があるジョイントを {len(joints_to_select)} 個選択しました。")
else:
    cmds.select(clear=True)
    print("問題のあるジョイント（単一チェイン内で複数軸に値があるもの）は見つかりませんでした！")
