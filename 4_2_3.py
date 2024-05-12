"""
# new:      20231018
# edit:     syz
# handin due:   20231025
# 根据mrtb_data.xlsx文件中的数据绘制堆叠柱状图
"""

import matplotlib.pyplot as plt
import pandas as pd

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来设置字体样式以正常显示中文标签（黑体）
plt.rcParams['axes.unicode_minus'] = False  # 正确输出负数
df = pd.read_excel('mrtb_data.xlsx')

df1 = df.groupby('类别')['性别'].value_counts().to_frame().unstack()
df1.columns = ['女', '男']
# print(df1.index.values)  # Index(['V1会员', 'V2会员', '图书', '明日高级VIP', '编程词典'], dtype='object', name='类别')
# print(df1.columns)    # MultiIndex([('性别', '女'), ('性别', '男')], names=[None, '性别'])

# fig, ax = plt.subplots()

p1 = df1.plot.bar(stacked=True, alpha=0.5, rot=45)
plt.ylabel("男女分布")
plt.legend()
plt.bar_label(p1, label_type='center')

plt.savefig('4_2_3_result.png')  # 图表输出到本地
plt.show()
