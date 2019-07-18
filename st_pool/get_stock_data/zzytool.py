#encoding=utf-8
import os


'''
递归文件夹, 找到文件所在的路径
'''
def findfile(dir,filename):
    filelist = os.listdir(dir)
    # print filelist
    # print filelist
    filepath =''
    j =0;
    for i in filelist:
        # print i
        j= j+1
        # print j
        fullfile = os.path.join(dir, i)

        # print fullfile
        if not os.path.isdir(fullfile):
            if i == filename:                    #1.txt为你所查找的文件名
                print  fullfile





        else:
             findfile(fullfile,filename)






if __name__ == '__main__':
    dir = '/Users/zzy/百度云同步盘/09_同步 mac/2017计划/06_康明集团/windows 资料/DKM/11月10-集群配置文件/'
    filename = 'configuration.xsl'
    st =  findfile(dir,filename)
    print'st', st

    # fr(dir)

