# -*- coding: utf-8 -*-
"""
@author: 98257
Date: 20200827
Version: V1.0
"""
import pandas as pd
import numpy as np

class DataAnalysis_tool(object):
    
    def SplitLine(self, str_info = "END"):
        '''
            分割线
        '''
        if str_info.upper() == "END":
            str_info = "-" * 27 + "End" + "-" * 27
            
        print(str_info + "\n")
        
    def summary_pd(self, data):
        '''
            显示pandas 类型的数据
        '''
        info = {
            "数据类型": type(data),
            "数据维度": "行数：{}\t 列数：{}".format(data.shape[0], data.shape[1]),
            "前6条记": data.head(),
            "缺失值": data.isnull().any(axis=0),
            "字段数据类型": data.dtypes    
        }
        return(info)
            
    def summary_np(self, data):
        '''
            显示 numpy 类型的信息
        '''
        info = {
            "数据类型": type(data),
            "数据维度": data.shape,
            "前6条记录": data[:5]   
        }
        return(info)

    def summary_list(self, data): 
        '''
            显示 list 类型的信息
        '''
        info = {
            "数据类型": type(data),
            "数据长度": len(data),
            "前6个键值": data[:6]
        }
        return(info)      
    
    def summary_dict(self, data):
        '''
            显示 dict 类型的信息
        '''
        info = {
            "数据类型": type(data),
            "数据长度": len(data),
            "前6个元素": list(data.keys())[:6]
        }
        return(info)
        
    def summary_other(self, data):
        '''
            显示其他的数据类型
        '''
        info = {
            "数据类型": type(data)
        }
        return(info)
    
    def Frequency(self, vector):
        '''
            计算数据出现的频率
            注意：传入的只能是向量，例如list，tuple，Series 类型数据
        '''
        v_dict = {}
        for v_i in vector:            
            if v_i in v_dict:
                v_dict[v_i] += 1
            else:
                v_dict[v_i] = 1
        
        return(v_dict)
    
    def print_analysis(self, info):
        '''
            输出需要显示的信息
        '''
        for k, v in info.items():
            self.SplitLine(k + "\n" + "-" * 30 + "\n\t" + str(v))
        self.SplitLine()

class DataAnalysis(object):
    '''
        数据集基本状态进行查看，包括：
        【1】 DataSummary：查看数据集详情
        【2】 LabelSummary：标签频率统计
    ''' 
    def LabelSummary(self, vector):
        '''
            LabelSummary 方法使用文档：
                
            （1）说明：
            |- 统计导入数据集中标签（枚举类型，或值）出现频率
            
            （2）变量：
            |- 【1】vector：输入的数据集，必须是：list、tuple、Series 类型数据
                    
            （3）返回结果：
            |- 数据集标签出现频率
            
            （4）注意：
            |- 只能传入向量，例如list，tuple，Series 类型数据
        '''
        res = self.tool.Frequency(vector)
        result = pd.DataFrame(
            {"label": list(res.keys()), "freq": list(res.values())}
        )
        return(result)
    
    def DataSummary(self, data):
        '''
            DataSummary 方法使用文档：
                
            （1）说明：
            |- 查看数据集的描述
            
            （2）变量：
            |- 【1】df：输入的数据集
                    
            （3）返回结果：
            |- 数据集的描述性结果
            
            （4）注意：
            |- 目前可以识别的数据集为：
            |- 【1】 pd.DataFrame
            |- 【2】 np.arrary
            |- 【3】 list
            |- 【4】 tuple
            |- 【5】 dict
            |- 如果是无法识别的类型，只会显示 数据类型（type） 结果
        '''
        type_group = {
            "DataFrame": self.tool.summary_pd, 
            "ndarray": self.tool.summary_np, 
            "list": self.tool.summary_list, 
            "tuple": self.tool.summary_list, 
            "dict": self.tool.summary_dict,
            "other": self.tool.summary_other
        }
        
        dt_type = type(data).__name__
        func = type_group[dt_type] if dt_type in type_group else type_group["other"]
        info = func(data)
        self.tool.print_analysis(info)

    def __init__(self):
        self.tool = DataAnalysis_tool()

DA = DataAnalysis()

if __name__ == "__main__":

    print("显示 list 类型")
    test_list = [x for x in range(10)]
    DA.DataSummary(test_list)
    
    print("显示 dict 类型")
    test_dict = dict(a = ["a", "a", "b"], b = [1, 2, 0] , c = [3, 4, 5], d = [1, 1, 2])
    DA.DataSummary(test_dict)
    
    print("显示 df 类型")
    test_df = pd.DataFrame(test_dict)
    DA.DataSummary(test_df)

    print("显示 标签频率")
    print(DA.LabelSummary(test_df))