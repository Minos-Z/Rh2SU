# -*- coding:utf-8 -*-
import rhinoscriptsyntax as rs

objects = rs.GetObjects("选择要导出的物件:")
layers = rs.LayerNames()

# rhino_obj 2 blocks

selection = []
selection1 = []
block_num = 0
ob_num = len(objects)
for i in objects:
    if rs.ObjectLayer(i).find('#') != -1:
        selection1.append(i)
    else:
        block_num = block_num + 1
        rs.CurrentLayer(rs.ObjectLayer(i))
        box = rs.BoundingBox(i)
        pt = box[0]
        try:
            block = rs.AddBlock([i], pt, "block_"+str(block_num), False)
            block = rs.InsertBlock(block, pt)
        except(Exception):
            continue
        selection.append(block)

# blocks with layers
objects = selection + selection1
selection_output = []
for a in layers:
    block_list = []
    for b in objects:
        if rs.ObjectLayer(b) == a:
            block_list.append(b)
    try:
        block = rs.AddBlock(block_list, (0, 0, 0), "block_"+a)
        block = rs.InsertBlock(block, (0, 0, 0))
    except(Exception):
        continue
    selection_output.append(block)

# del insert objects
rs.UnselectAllObjects()
rs.SelectObjects(selection)
rs.DeleteObjects(rs.SelectedObjects())

# export blocks
rs.UnselectAllObjects()
PATH = rs.SaveFileName()
rs.SelectObjects(selection_output)
rs.Command("_-Export " + PATH + '.skp' + " A=Yes _Enter", echo=False)
rs.DeleteObjects(rs.SelectedObjects())
rs.Command("-Purge B=Yes D=No G=No H=No L=No I=No M=No _Enter", echo=False)
print("Job Done! Pls check"+str(PATH)+"find file.")
rs.MessageBox("导出完成！请到："+str(PATH)+"查看导出的文件。", buttons=0, title="珍爱生命，早点回家")
