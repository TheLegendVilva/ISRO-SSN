from typing import Tuple
from netCDF4 import Dataset
import Graph_builder
import Safe_passage
from Graph_builder import GraphBuilder,Node
from Safe_passage import Safe_path

class Graph_searchagent:
    def __init__(self,start,dest,path,graph,pathfinder,view_range):
        self.start= start
        self.destination= dest
        self.view_range= view_range
        self.old_pos= start
        self.new_pos= start
        self.path=path
        self.graph=graph
        self.pathfinder=pathfinder


    def in_viewrange(self,coord:Tuple[int,int]):
        if(abs(coord[0]-self.new_pos[0])<=self.view_range):
            if(abs(coord[1]-self.new_pos[1])<=self.view_range):
                return True
        return False

    def updation(self,inp=[]):
        inrange_changed_nodes=[]
        """
        store the changes... which are not in the viewrange
        [(x,y,{hs:new_hs,...}),...]
        """
        for i in inp:
            lat,lon,parameters=i
            changed_node=self.graph.get_node((lat,lon))
            if changed_node==None:
                #print("not a valid node to change")
                continue
            changed_node.hs[1]=parameters
        
        a=self.new_pos[0]
        b=self.new_pos[1]
        c=self.view_range
        for i in range(a-c,a+c+1):
            for j in range(b-c,b+c+1):
                if(i==a and j==b):
                    continue
                node=self.graph.get_node((i,j))
                if node==None:
                    #print("not a valid node to change")
                    continue 
                if(node.hs[0]!=node.hs[1]):#monitoring one param
                    inrange_changed_nodes.append(node)
        
        return inrange_changed_nodes
    
    def parser(self,inp):
        if inp ==None: return []
        if inp[0]=="[" and inp[-1]=="]":
            type=list #check format

        inp=inp[1:-1]
        tuple_list=inp.split(';')
        li=[]
        for i in tuple_list:
            if inp[0]=="(" and inp[-1]==")":
                type=tuple #check format
            i=i[1:-1]
            lat,lon,hs=[int(i) for i in i.split(',')]
            li.append((lat,lon,hs))
        return li
    
    def run(self):
        
        # global fig
        # global plot_handle
        while 1:
            """
            To change a coord x,y
            input must be a list of tuple containing
            coordinates and dictionary of changed parameters
            i.e
            [(x,y,{hs:new_hs,...});...]
            [(x,y,hs);] =>present format
            print(self.path)
            
            lat=[]
            lon=[]
            for i in self.path:
                lat.append(i[0])
                lon.append(i[1])
            x, y = mp(lon, lat)
            plot_handle.set_ydata(y)
            plot_handle.set_xdata(x)
            fig.canvas.draw()
            """
            
            #fig.canvas.flush_events()
            
            #plt.rcParams["figure.figsize"] = (50,50)
            #plt.show(block=False)
            inp = input('enter q to quit \n'
                        'enter list of changed coords to make changes in map\n'
                        'enter space to continue \n'
                        ': ')
            
            if (inp=='q'): break
            if (inp==" " or inp=="[]"): inp=None
            if not inp :  #next position
                self.new_pos=self.path[1] #this must be possible when there are no inrange changes for the old pos
            inp=self.parser(inp)
            inrange_changes=self.updation(inp) #changed inrange nodes
            self.pathfinder.changednodes=inrange_changes
            self.path=self.pathfinder.move_and_replan(self.new_pos)
            self.old_pos=self.new_pos
            
            if (self.old_pos==self.destination): 
                print("reached destination", self.destination)
                break

            return self.path
            

def main_search(source,destination,gtype="full",ntype=1,path=[]):
    if gtype=="part":
        graph=GraphBuilder(gtype,ntype,path).graph
        # print("part")
        # sys.exit()
    else:
        graph=GraphBuilder(gtype,ntype).graph

    pathfinder=Safe_path(source,destination,graph)
    path=pathfinder.move_and_replan(source) 
    """
    just to see how computation is reduced
    after plotting this,
    make sure to remove the all_vertices variable from
    priority queue , releases the memory
    """
    """
    explored= list(pathfinder.open.all_vertices)
    path.append(explored)
    """
    #uncomment this for getting basemap plots
    # filepath  = r"C:\Users\91807\Downloads\data_iiit-varoda\data_iiit-varoda\ww3_fcs_glo_1.0.nc"
    # fh=Dataset(filepath,mode="r")
    # data=env_factors()
    # fh=data.file
    # lons = fh.variables['lon'][40:91]
    # lats = fh.variables['lat'][70:101]
    # waveheight = fh.variables['hs'][:]
    # fig=plt.figure()
    # mp = Basemap(projection ='merc',llcrnrlon=40,llcrnrlat=0,urcrnrlon =90,urcrnrlat=30,resolution = "i")
    # lon,lat = np.meshgrid(lons,lats)
    # x,y = mp(lon,lat)
    # c_scheme=mp.pcolor(x,y,np.squeeze(waveheight[0,70:101,40:91]),cmap='ocean')

    # mp.drawcoastlines(color='white',linewidth=1)
    # mp.bluemarble()
    # fig.canvas.draw()

    # cbar = mp.colorbar(c_scheme,location='right',pad='10%')
    # lat=[]
    # lon=[]
    # path=[(10, 83), (10, 82), (10, 81), (10, 80), (9, 79), (8, 78), (8, 77), (9, 76), (10, 76), (11, 75), (12, 74), (13, 73), (14, 72), (15, 71), (16, 70)]

    # for i in path:
    #     lat.append(i[0])
    #     lon.append(i[1])
    # x, y = mp(lon, lat)
    # plot_handle, = mp.plot(x, y,marker='.',linewidth=2,color='white')
    # fig.canvas.draw()
    # plt.show(block=False)
    
    # rework is needed in how we are goin to pause and continue the operataion of the d star lite
    # so as of now , just returning the path for sake of output and integration
    #  
    #graphsearch=Graph_searchagent(source,destination,path,graph,pathfinder,view_range=2)
    #graphsearch.run()
    return path
    #graphsearch call
    #loops till it reaches destination

#PARSER
import sys
source_coords=tuple([int(i) for i in sys.argv[1].split(',')])
destination_coords= tuple([int(i) for i in sys.argv[2].split(',')])
gtype="full" #default
ntype=1      #default
path=[]      #default
try:
    ntype=int(sys.argv[4]) #so like if u have provided a ntype, and didnt provide gtype.. then it will still work
    gtype=sys.argv[3]      #by defaulting gtype to full, so for higher ntypes,it will take lot of time
except:
    1    
#print(source_coords,destination_coords, type(source_coords),type(destination_coords))
if(gtype=="part"):#by default the graph will be built on the path which is obtained by having 8neighbours
    path=main_search(source_coords,destination_coords,"full",1,[])

#main_search(source_coords,destination_coords,gtype,ntype,path)
print(main_search(source_coords,destination_coords,gtype,ntype,path))
#2.28s =>ntype1
#5.09s =>ntype2
#27.39s =>ntype=3
#46.63 =>type=4