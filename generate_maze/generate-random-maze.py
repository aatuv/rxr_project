file_stub = open("template.txt", "r")

targetfile = open("maze.wbt", "a")

targetfile.write(file_stub.read())

with open('5x5_test4.txt') as f:
    lines = f.readlines()
    xTranslate = 0
    boxnro = 0
    for i in range(0, len(lines), 2):
        row1 = lines[i]
        zTranslate = 0
        for j in range(0, len(row1), 4):
            addHorizBlock = False
            addVertBlock = False
            if j + 4 < len(row1):
                block = row1[j:j+4]
                if block == "o---":
                    addHorizBlock = True
                elif block == "o   ":
                    addVertBlock = True
                elif block == "oggg":
                    goal = True
            else:  # last block on row1
                addVertBlock = True

            # starting positions (upper left corner)
            x = 15.5
            z = -15
            if addHorizBlock:
                object_str = ""
                object_str = object_str + "SolidBox {\n"
                object_str = object_str + "  translation " + \
                    str(x - xTranslate) + " 0.25 " + str(z + zTranslate) + "\n"
                object_str = object_str + \
                    "  name \"box_" + str(boxnro) + "\"\n"
                object_str = object_str + "  size 2.0 1.0 1.0\n"
                #object_str = object_str + "  appearance {\n"
                #object_str = object_str + "    baseColorMap NULL\n"
                #object_str = object_str + "  }\n"
                object_str = object_str + "}\n"
                targetfile.write(object_str)
                boxnro += 1
            elif addVertBlock:
                z = -15.5
                object_str = ""
                object_str = object_str + "SolidBox {\n"
                object_str = object_str + "  translation " + \
                    str(x - xTranslate) + " 0.25 " + str(z + zTranslate) + "\n"
                object_str = object_str + \
                    "  name \"box_" + str(boxnro) + "\"\n"
                object_str = object_str + "  size 1.0 1.0 1.0\n"
                object_str = object_str + "}\n"
                targetfile.write(object_str)
                boxnro += 1
            zTranslate += 2

        if i+1 < len(lines):
            row2 = lines[i + 1]
            xTranslate += 1
            zTranslate = 0
            for j in range(0, len(row2), 4):
                addVertBlock = False
                goal = False
                if j + 4 < len(row2):
                    block = row2[j:j+4]
                    if block == "|   ":
                        addVertBlock = True
                        goal = False
                    elif block == "|ggg":
                        goal = True
                else:  # last block on row2
                    addVertBlock = True

                # starting positions (upper left corner)
                x = 15.5
                z = -15.5
                if addVertBlock:
                    object_str = ""
                    object_str = object_str + "SolidBox {\n"
                    object_str = object_str + "  translation " + \
                        str(x - xTranslate) + " 0.25 " + \
                        str(z + zTranslate) + "\n"
                    object_str = object_str + \
                        "  name \"box_" + str(boxnro) + "\"\n"
                    object_str = object_str + "  size 1.0 1.0 1.0\n"
                    object_str = object_str + "}\n"
                    targetfile.write(object_str)
                    boxnro += 1
                elif goal == True:
                    object_str = ""
                    object_str = object_str + "SolidBox {\n"
                    object_str = object_str + "  translation " + \
                        str(x - xTranslate) + " 0.25 " + \
                        str(z + zTranslate) + "\n"
                    object_str = object_str + \
                        "  name \"box_" + str(boxnro) + "\"\n"
                    object_str = object_str + "  size 1.0 1.0 1.0\n"
                    object_str = object_str + "}\n"
                    targetfile.write(object_str)
                    boxnro += 1
                    object_str = ""
                    object_str = object_str + "SolidBox {\n"
                    object_str = object_str + "  translation " + \
                        str(x - xTranslate) + " -0.49 " + \
                        str(z + zTranslate + 1) + "\n"
                    object_str = object_str + \
                        "  name \"box_" + str(boxnro) + "\"\n"
                    object_str = object_str + " size 1.0 1.0 1.0\n"
                    object_str = object_str + " appearance PBRAppearance {\n"
                    object_str = object_str + " baseColor 0 1 0\n"
                    object_str = object_str + " baseColorMap NULL\n"
                    object_str = object_str + " }\n"
                    object_str = object_str + "}\n"
                    targetfile.write(object_str)
                    boxnro += 1
                zTranslate += 2
            xTranslate += 1
