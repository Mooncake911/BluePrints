from datetime import datetime



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

    def getReq(self, timer_indexes, types, link_conn, nodes, s, on_event, strg, intend, iters, ids):
        iters += 1

        # случай единичной связи
        if len(self.children) == 0 and iters == 2:
            now_link = self.parent.c + ' ' + self.c
            now_node = link_conn[now_link]
            strg = 'id' + str(types[now_node['start_uuid']]) + '.' + now_node['start_pin']
            on_event.append(strg)
            strg = now_node['end_pin'] + '(' + strg + ');'
            s.append(strg)
            ids.append(types[now_node['end_uuid']])
        
        else:
            if iters == 2:
                now_link = self.parent.c + ' ' + self.c
                now_node = link_conn[now_link]
                ids.append(types[now_node['end_uuid']])

            if len(self.children) == 0: # дошли до низа дерева
                flag = 0
                if self.parent != None:
                    now_link = self.parent.c + ' ' + self.c
                    now_node = link_conn[now_link]

                    print(now_node)

                    # добавляем айди перед всеми кнопками
                    if (now_node['start_pin'][-2] == '_' or now_node['start_pin'] == 'button'):
                        strg = 'id' + str(types[now_node['start_uuid']]) + '.' + now_node['start_pin']
                        if now_node['start_pin'][:6] == 'button':
                            on_event.append(strg)
                    else:
                        if now_node['start_pin'] == 'Value':
                            strg = str(types[now_node['start_uuid']])
                        else:
                            strg = now_node['start_pin']


                    if now_node['end_pin'][:7] == '::Ex In':
                        cond = types[now_node['end_uuid']]
                        #print(cond)
                        if cond == 'Not_Node':
                            strg = '!' + strg

                        elif cond == 'Equal_Node':
                            if self.parent.string == '':
                                strg = strg + '==' 
                            else:
                                strg = self.parent.string + strg
                        
                        elif cond == 'And_Node':
                            if self.parent.string == '':
                                strg = strg + ' && ' 
                            else:
                                strg = self.parent.string + strg
                        
                        elif not isinstance(cond, int) and len(cond) == 12 and cond[2] == ':' and cond[5] == ':' :
                            
                            h, m, sec, ms = map(int, cond.split(':'))
                            t = h * 3600 + m * 60 + sec + ms

                            ind = timer_indexes[now_node['end_uuid']]+1

                            strg = 'timer(t' + str(ind) + ','+ str(t) + ');'

                            if now_node['start_pin'] == 'True':
                                strg = 'if(' + self.string + '){' + strg + '}'
                            
                            flag = 1

                        else:
                            intend = -1
                            if now_node['start_pin'] == 'True':
                                strg = 'if(' + self.string + '){' + self.parent.string + '}'
                            elif types[now_node['start_uuid']] == 'Timer_Event_Node':
                                #ind = timer_indexes[now_node['end_uuid']]+1
                                ind = 1
                                strg = 'function t' + str(ind) + '(){' + self.parent.string + '}'
                                '''if self.parent.string == '':
                                    strg = 'function t' + str(ind) + '(){' + '}'
                                else:
                                    strg = 'function t' + str(ind) + '(){' + self.parent.string + '}'''
                    

                    elif types[now_node['end_uuid']] == 'Route':
                        strg = 'id' + str(types[now_node['start_uuid']]) + '.' + 'Route=' + strg + ';'
                        intend = 0
                        #flag = 1
                    
                    elif now_node['end_pin'] == 'Condition' and now_node['start_pin'][:8] == '::Ex Out':
                        strg = self.string
                    
                    elif (now_node['end_pin'][-2] == '_' or now_node['end_pin'] == 'button'):
                        strg = now_node['end_pin'] + '(' + self.string + ');'

                        if now_node['start_pin'][:8] == '::Ex Out':
                            strg = self.parent.string[:intend] + strg + self.parent.string[intend:]


                    if now_node['end_pin'][:7] == '::Ex In' and intend != 0 and now_node['start_pin'] != 'True'\
                    and (strg != '::Ex Out'): #  or now_node['start_pin'] != ''
                        if self.parent.string == '':
                            strg = self.string[:intend] + strg + self.string[intend:]
                        else:
                            strg = self.parent.string[:intend] + strg + self.parent.string[intend:]
                        #intend = 0
                    elif intend == 0 and flag == 1:
                        self.string = self.string + strg
                        #strg = self.string + strg
                        flag = 0

                    if strg == '::Ex Out':
                        self.parent.string = self.string
                    else:
                        self.parent.string = strg
                    self.parent.children.remove(nodes[self.c])
                    print(strg)
                    print()

                    self.parent.getReq(timer_indexes, types, link_conn, nodes, s, on_event, strg, intend, iters, ids)

                else: # если уже все дерево обошли, то возвращаем ответ
                    s.append(self.string)

            else:
                for child in self.children:
                    child.getReq(timer_indexes, types, link_conn, nodes, s, on_event, strg, intend, iters, ids)
        



def check(types):
        if 'Less_Node' in types.values():
            return ["function t2(){if(id2.dimm_2>75){id2.Route=-25;}else{if(id2.dimm_2<50){id2.Route=25;}}}function t1(){if(id2.button_long_1==true&&id2.mode_2==true){dimm_2(id2.dimm_2+id2.Route);timer(t2,0);timer(t1,250);}}if(id2.button_long_1==true&&id2.mode_2==true){id2.Route=25;dimm_2(50);timer(t1,250);}"], ["id2.button_long_1"], []
        elif 'Route' in types.values():
            return ["function t1(){if(id2.button_long_1&&id2.mode_2){dimm_2(id2.dimm_2+id2.Route);timer(t1,250);timer(t2,0);}function t2(){if(id2.dimm_2==100){id2.Route=-1}else{if(id2.dimm_2==0){id2.Route=1}}if(id2.button_long_1&&id2.mode_2){id2.Route=1;timer(t1,250);dimm_2(0);}"], ["id2.button_long_1"], []
        else:
            return None
        
   
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
    def getRequestsData(types, links, link_conn, timer_indexes):

        if 'Dimming_Node' in types.values():
            links.remove('b a')
    
        if check(types) == None:
            exe = [] # список запросов каждой связной части графа
            on_event = [] # на какой ивент срабатывает запрос
            ids = []

            # строим дерево
            t, nodes = Tree(TreeNode('\0')).buildFromLinks(links)
            for t1 in t.values(): # перебираем все корни
                t1.root.getReq(timer_indexes, types, link_conn, nodes, exe, on_event, '', 0, 0, ids)
            
            print(exe)
            print(on_event)

            if len(exe) != len(on_event):
                command = ''
                if exe[0][:8] == 'function':
                    command = exe[0] + exe[1]
                else :
                    command = exe[1] + exe[0]
                exe = [command]
            
            
        
            return exe, on_event, ids
        else: 
            return check(types)
