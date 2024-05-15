class TreeNode:
    def __init__(self, c):
        self.c = c
        self.parent = None
        self.children = []
        self.string = ''

    def addChild(self, n, p):
        n.parent = p
        self.children.append(n)

    def addParent(self, n):
        self.parent = n

    def printTreeIdented(self, indent):
        print(indent + "-->" + self.c)
        for child in self.children:
            child.printTreeIdented(indent + "   |")

    def getReq(self, types, link_conn, nodes, s, on_event, strg, intend):
        if len(self.children) == 0:  # дошли до низа дерева
            if self.parent is not None:
                now_link = self.parent.c + ' ' + self.c
                now_node = link_conn[now_link]

                print(now_node)

                # добавляем айди перед всеми кнопками
                if now_node['start_pin'][-2] == '_' or now_node['start_pin'] == 'button':
                    strg = str(types[now_node['start_uuid']]) + '.' + now_node['start_pin']
                    if now_node['start_pin'][:6] == 'button':
                        on_event.append(strg)
                else:
                    if now_node['start_pin'] == 'Value':
                        strg = str(types[now_node['start_uuid']])
                    else:
                        strg = now_node['start_pin']

                if (now_node['start_pin'][-2] == '_' or now_node['start_pin'] == 'button') \
                        and now_node['end_pin'][-2] == '_':
                    strg = now_node['end_pin'] + '(' + strg + ');'
                    s.append(strg)
                    return

                if now_node['end_pin'][:7] == '::Ex In':
                    cond = types[now_node['end_uuid']]
                    if cond == 'Not_Node':
                        strg = '!' + strg
                    elif cond == 'Equal_Node':
                        if self.parent.string == '':
                            strg = strg + ' == '
                        else:
                            strg = self.parent.string + strg
                    else:
                        if now_node['start_pin'] == 'True':
                            strg = 'if( ' + self.string + ' ){ ' + self.parent.string + ' }'
                            intend = -1

                elif now_node['end_pin'] == 'Condition' and now_node['start_pin'][:8] == '::Ex Out':
                    strg = self.string

                elif now_node['end_pin'][-2] == '_' or now_node['end_pin'] == 'button':
                    strg = now_node['end_pin'] + '(' + self.string + ');'

                    if now_node['start_pin'][:8] == '::Ex Out':
                        strg = self.parent.string[:intend] + strg + self.parent.string[intend:]

                self.parent.string = strg
                self.parent.children.remove(nodes[self.c])
                print(strg)
                print()

                self.parent.getReq(types, link_conn, nodes, s, on_event, strg, intend)

            else:  # если уже все дерево обошли, то возвращаем ответ
                s.append(self.string)

        else:
            for child in self.children:
                child.getReq(types, link_conn, nodes, s, on_event, strg, intend)


class Tree:
    def __init__(self, root):
        self.root = root

    def buildFromLinks(self, links):
        nodes = {}
        forest = {}

        for link in links:
            # If start of link not seen before, add it two both arrays
            if link[0] not in nodes:
                nodes[link[0]] = TreeNode(link[0])
                forest[link[0]] = Tree(nodes[link[0]])

            # If end of link is not seen before, add it to the nodes array
            if link[2] not in nodes:
                nodes[link[2]] = TreeNode(link[2])

            # If end of link is seen before, remove it from forest 
            elif link[2] in forest:
                forest.pop(link[2])

            # Establish Parent-Child Relationship between Start and End
            nodes[link[0]].addChild(nodes[link[2]], nodes[link[0]])

        return forest, nodes

    @staticmethod
    def printForest(links):
        t, _ = Tree(TreeNode('\0')).buildFromLinks(links)
        for t1 in t.values():
            t1.root.printTreeIdented("")
            print()

    @staticmethod
    def getRequestsData(types, links, link_conn):
        exe = []  # список запросов каждой связной части графа
        on_event = []  # на какой ивент срабатывает запрос

        # строим дерево
        t, nodes = Tree(TreeNode('\0')).buildFromLinks(links)
        for t1 in t.values():  # перебираем все корни
            t1.root.getReq(types, link_conn, nodes, exe, on_event, '', 0)

        return exe, on_event
