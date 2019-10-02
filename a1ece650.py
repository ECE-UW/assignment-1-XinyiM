#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'maxinyi'


import sys
import math
import re
import copy


def generateVertices(v_list):
    '''

    :param v_list: v_list is the second group of a street input
    :return: new_v_list is an array including vertices
    '''
    v_list = str(v_list).strip()
    pattern = re.compile(r'\((\-?\d+),(\-?\d+)\)')
    v_list = pattern.findall(v_list)
    # v_list is an array of [x,y]
    new_v_list = []
    for i in v_list:
        vertex = Vertex(int(i[0]), int(i[1]))
        new_v_list.append(vertex)
    return new_v_list


def distance(va, vb):
    return math.sqrt(pow((va.x - vb.x), 2) + pow((va.y - vb.y), 2))


def input_process(command):
    if command[0] == 'a':
        G.add_st(command)
    elif command[0] == 'c':
        G.change_st(command)
    elif command[0] == 'r':
        G.remove_st(command)
    elif command[0] == 'g':
        # print("Generate a graph!...")
        G.generate_graph()
        #G.show()
    else:
        print('Error: no such command! Command must be \'c/a/g/r\' ONLY!')


vIDs = {}


def distributeVertexIDs(vertex):
    if vIDs.has_key(vertex):
        vertex.id = vIDs[vertex]
    else:
        vertex.id = len(vIDs.keys()) + 1
        vIDs[vertex] = vertex.id


def find_intersection(seg1, seg2):
        """
        :param seg1: the first segment
        :param seg2: the second segment
        :return: an intersection(Vertex) or None
        """
        # a = y0 – y1, b = x1 – x0, c = x0y1 – x1y0。
        # x = (b0*c1 – b1*c0)/D
        # y = (a1*c0 – a0*c1)/D
        # D = a0*b1 – a1*b0， (D为0时，表示两直线重合)
        a1 = seg1.v1.y - seg1.v2.y
        b1 = seg1.v2.x - seg1.v1.x
        c1 = seg1.v1.x * seg1.v2.y - seg1.v2.x * seg1.v1.y
        a2 = seg2.v1.y - seg2.v2.y
        b2 = seg2.v2.x - seg2.v1.x
        c2 = seg2.v1.x * seg2.v2.y - seg2.v2.x * seg2.v1.y
        D = a1 * b2 - a2 * b1
        # print("D is： %d" % D)
        if D == 0:
            '''
            a3 = seg1.v1.y - seg2.v2.y
            b3 = seg2.v2.x - seg1.v1.x
            c3 = seg1.v1.x * seg2.v2.y - seg2.v2.x * seg2.v2.y
            a4 = seg2.v1.y - seg1.v2.y
            b4 = seg1.v2.x - seg2.v1.x
            c3 = seg2.v1.x * seg2.v1.y - seg1.v2.x * seg1.v2.y
            D2 = a3 * b4 - a4 * b3
            if D2 == 0:
                # print("D2 is： %d" % D2)
                return "two intersections"
            else:
                print("D2 is： %d" % D2)
            '''
            return None
        else:
            inx = (b1 * c2 - b2 * c1) / D
            iny = (a2 * c1 - a1 * c2) / D
        intersection = Vertex(inx, iny)
        if seg1.liesinthesegment(intersection) and seg2.liesinthesegment(intersection):
            # print(intersection)
            return intersection
        else:
            return None


def street_name(streetname):
    for i in str(streetname):
        if not (i.isalpha()) and not (i.isspace()):
            print("Error: Street name must be alphabetical! ")
            break


class Vertex:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.id = -1
        self.isIntersection = False

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return '  %s:  (%.2f,%.2f)' % (self.id, self.x, self.y)

    def __hash__(self):
        return ('x:%s,y:%s' % (self.x, self.y)).__hash__()


class Segment:
    '''
    Segment: v1 and v2 are vertices and v1 appears before v2
    '''
    def __init__(self, v1, v2):
        # Generate Segment in order
        if v1.id > v2.id:
            v3 = v2
            v2 = v1
            v1 = v3
        self.v1 = v1
        self.v2 = v2

    def __eq__(self, other):
        return self.v1 == other.v1 and self.v2 == other.v2

    # Override not equal function
    def __ne__(self, other):
        return self.v1 != other.v1 or self.v2 != other.v2

    def __hash__(self):
        return self.__str__().__hash__()

    def __str__(self):
        return '  <%s,%s>' % (self.v1.id, self.v2.id)

    def endofsegment(self, vx):
        return self.v1 == vx or self.v2 == vx

    def liesinthesegment(self,vx):
        d1 = distance(self.v1, vx)
        d2 = distance(vx, self.v2)
        d3 = distance(self.v1, self.v2)
        # print("d1 : %s\nd2 : %s\nd3 : %s" % (d1, d2, d3))
        return d3 >= d1 and d3 >= d2



class Street:
    def __init__(self, name, vertices):
        self.name = name
        self.vertices_list= []
        self.segment_list = []
        # self.initSegmentsinStreet(vertices)
        if len(vertices) >= 2:
            self.vertices_list = vertices
            for i in range(len(vertices) - 1):
                self.segment_list.append(Segment(vertices[i], vertices[i + 1]))
        else:
            print("Error: a street must have 2 vertices or more!")


    def insertPointintoSegment(self, segment, vp):
        # 1.判断vp是不是segment的End_vertex
        if segment.endofsegment(vp):
            if segment.v1 == vp:
                segment.v1.isIntersection = True
            if segment.v2 == vp:
                segment.v2.isIntersection = True
            return None
        # insert函数只用在插入交点时，所以vp必须是交点，判断vp是否是segment的端点，
        # 如果是，则将端点的isIntersection值设为True

        # 2.把原有的segment分为两个
        seg_a = Segment(segment.v1, vp)
        seg_b = Segment(vp, segment.v2)
        new_segs = []
        new_vertices = []
        for i in range(len(self.segment_list)):
            if self.segment_list[i] != segment:
                # print("%s != %s " % (self.segment_list[i], segment))
                new_segs.append(self.segment_list[i])
            else:
                new_segs.append(seg_a)
                new_segs.append(seg_b)

        self.segment_list = new_segs


        # 3.在原有的vertices列表中插入新的vertex
        for i in range(len(self.vertices_list)):
            new_vertices.append(self.vertices_list[i])
            if self.vertices_list[i] == segment.v1:
                # Attention：一定要插入在v1的后面！！！！！！！
                # 不能直接判断不是vp就append
                if new_vertices.count(vp) == 0:
                    new_vertices.append(vp)
        self.vertices_list = new_vertices


class Graph:
    def __init__(self):
        # Graph:  Streets = {} V = {} E = {}
        # vertices_final:
        # 1) intersections
        # 2) end-points of segments that one of the vertex is intersection

        # edges :
        # 1) one of the vertices is intersection
        # 2) both of the vertices are on the same street
        # 3) one is reachable from another without traversing another vertex
        self.Streets = {}
        self.edges = {}
        self.vertices_f = {}
        # vertices_f : {Vertex1 : 1....}

    def add_vertex(self, vertex):
        if not self.vertices_f.has_key(vertex):
            distributeVertexIDs(vertex)
            # print(vertex.id)
            self.vertices_f[vertex] = vertex

    def add_edge(self, edge):
        if not(self.edges.has_key(edge)) and edge.v1 != edge.v2:
            self.edges[edge] = edge

    def add_st(self, command):
        pattern = r'a\s+\"(.+?)\"(( ?\(\-?\d+,\-?\d+\))+)\s*$'
        matching = re.match(pattern, command)
        if matching:
            street = str(matching.group(1).upper())
            street_name(street)
            # print(str(street))
            if self.Streets.has_key(street):
                print("Error: the street name does exist!")
                return
            vertexList = generateVertices(matching.group(2))
            # vertexList = generateVertices(vertexList)
            self.Streets[street] = Street(street, vertexList)
        else:
            print("Error: wrong input! ")

    def change_st(self, command):
        pattern = r'c\s+\"(.+?)\"(( ?\(\-?\d+,\-?\d+\))+)\s*$'
        matching = re.match(pattern, command)
        if matching:
            street = str(matching.group(1).upper())
            street_name(street)
            if self.Streets.has_key(street):
                vertexList = matching.group(2)
                vertexList = generateVertices(vertexList)
                self.Streets[street] = Street(street, vertexList)
                # print("change %s successfully!" % street)
            else:
                print ("Error: this street doesn't exist!")
        else:
            print ("Error: Wrong input!")

    def remove_st(self, command):
        pattern = r'r \"(.+?)\"'
        matching = re.match(pattern, command)
        if matching:
            street = str(matching.group(1).upper())
            street_name(street)
            if self.Streets.has_key(street):
                del self.Streets[street]
            else:
                print("Error: This street doesn't exist!")
        else:
            print("Error: Wrong input!")

    def generate_graph(self):
        new_G = copy.deepcopy(G)
        streetsName = new_G.Streets.keys()

        # generate all the intersections, mark them as inter, and insert them into segments
        '''
        for st1 in streets:
            for st2 in streets:
                for seg1 in segments in st1:
                    for seg2 in segments in st2:
                        intersection = find_intersection(seg1, seg2)
                        if intersection exists:
                            insert point into seg1,st1
                            insert point into seg2,st2
        '''
        for i in range(len(streetsName) - 1):
            # 遍历所有街道
            for j in range(i + 1, len(streetsName)):
                # new_G.Street is a dict, use []
                st1 = new_G.Streets[streetsName[i]]
                # segs1 = st1.segment_list
                st2 = new_G.Streets[streetsName[j]]
                # segs2 = st2.segment_list
                for s1 in st1.segment_list:
                    # Error: s1 in segs1
                    for s2 in st2.segment_list:
                        # Error: s2 in segs2
                        intersection = find_intersection(s1, s2)
                        if intersection:
                            # print("交点存在，为 %s " % str(intersection))
                            intersection.isIntersection = True  # mark as intersection
                            st1.insertPointintoSegment(s1, intersection)
                            st2.insertPointintoSegment(s2, intersection)
                            # st1，st2中的segment要实时更新
                            new_G.Streets[streetsName[i]] = st1
                            new_G.Streets[streetsName[j]] = st2

        # generate edges: segments including at least one intersection
        # generate vertices (distribute IDs for the vertices) :
        # intersections / vertices adjacent to the intersections
        '''
        for st in all the streets:
            for vertex in all the vertices in this street:
                if this vertex is intersection:
                    add this vertex into vertices_list
                        if vertex's previous vertex exists:
                            add this one into vertices_list 
                            make edge by these two vertices 
                            add the edge into edge_list
                        if vertex's next vertex exists:
                            add this one into vertices_list
                            make edge by these two vertices 
                            add edge into the edge_list
        '''
        # 遍历第一个到最后一个street
        for i in range(len(streetsName)):
            st = new_G.Streets[streetsName[i]] # 遍历st上的每一个vertex
            for j in range(len(st.vertices_list)):
                # print(st.vertices_list[j].intersection)
                if st.vertices_list[j].isIntersection:
                    # print("%s is intersection" % st.vertices_list[j])
                    new_G.add_vertex(st.vertices_list[j])
                    if j - 1 >= 0:
                        new_G.add_vertex(st.vertices_list[j - 1])
                        # 错误示范：edge = Segment(st.vertices_list[j - 1], st.vertices_list[j])
                        edge = Segment(new_G.vertices_f[st.vertices_list[j - 1]], new_G.vertices_f[st.vertices_list[j]])
                        # vertices_f是一个字典，用一个key，由于遍历的是st.vertices_list 所以传入的vertex都要是vertices_list中的j-1和j
                        # Segment(Vertex1,Vertex2) 传入两个Vertex 第一个
                        # print(edge)
                        new_G.add_edge(edge)
                    if j + 1 < len(st.vertices_list):
                        # 这里是小于，不是小于等于
                        # print("not distributed vertex: %s " % st.vertices_list[j + 1])
                        new_G.add_vertex(st.vertices_list[j + 1])
                        # 错误示范：edge = Segment(st.vertices_list[j], st.vertices_list[j + 1])
                        edge = Segment(new_G.vertices_f[st.vertices_list[j]], new_G.vertices_f[st.vertices_list[j + 1]])
                        # print (edge)
                        new_G.add_edge(edge)
        print("V = {")
        for v in new_G.vertices_f:
            print(v)
        print("}")
        print("E = { ")
        count = 0
        for e in new_G.edges:
            count += 1
            if count < len(new_G.edges):
                print(str(e) + ',')
            else:
                print(str(e))
        print('}')


G = Graph()


def main():
    while True:
        try:
            args = raw_input()
            input_process(args)
        except EOFError:
            sys.exit(0)


if __name__ == '__main__':
    main()


