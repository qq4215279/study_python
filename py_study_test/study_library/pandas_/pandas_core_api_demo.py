#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Pandas 核心 API 综合示例
展示 pandas 库的主要功能和最佳实践
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 设置显示选项
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)


def demo_basic_concepts():
    """1. 基础概念与数据结构"""
    print("=" * 50)
    print("1. 基础概念与数据结构")
    print("=" * 50)
    
    """
    创建 Series
    pandas.Series(data=None, index=None, dtype=None, name=None, copy=False, fastpath=False)
    参数说明：
        data：Series 的数据部分，可以是列表、数组、字典、标量值等。如果不提供此参数，则创建一个空的 Series。
        index：Series 的索引部分，用于对数据进行标记。可以是列表、数组、索引对象等。如果不提供此参数，则创建一个默认的整数索引。
        dtype：指定 Series 的数据类型。可以是 NumPy 的数据类型，例如 np.int64、np.float64 等。如果不提供此参数，则根据数据自动推断数据类型。
        name：Series 的名称，用于标识 Series 对象。如果提供了此参数，则创建的 Series 对象将具有指定的名称。
        copy：是否复制数据。默认为 False，表示不复制数据。如果设置为 True，则复制输入的数据。
        fastpath：是否启用快速路径。默认为 False。启用快速路径可能会在某些情况下提高性能。
    """
    print("\n--- 1.1 创建 Series ---")
    print("Series 示例:")
    series_data = pd.Series([1, 3, 5, np.nan, 6, 8], name='数字序列')
    print(series_data)

    # 查看基本信息
    print("数据类型：", series_data.dtype)
    print("索引：", series_data.index)
    print(f"索引.tolist(): {series_data.index.tolist()}")
    print("数据：", series_data.values)
    print("前两行数据：", series_data.head(2))


    """
    创建 DataFrame
    pandas.DataFrame(data=None, index=None, columns=None, dtype=None, copy=False)
        参数说明：
        data：DataFrame 的数据部分，可以是字典、二维数组、Series、DataFrame 或其他可转换为 DataFrame 的对象。如果不提供此参数，则创建一个空的 DataFrame。
        index：DataFrame 的行索引，用于标识每行数据。可以是列表、数组、索引对象等。如果不提供此参数，则创建一个默认的整数索引。
        columns：DataFrame 的列索引，用于标识每列数据。可以是列表、数组、索引对象等。如果不提供此参数，则创建一个默认的整数索引。
        dtype：指定 DataFrame 的数据类型。可以是 NumPy 的数据类型，例如 np.int64、np.float64 等。如果不提供此参数，则根据数据自动推断数据类型。
        copy：是否复制数据。默认为 False，表示不复制数据。如果设置为 True，则复制输入的数据。
    """

    print("\n--- 1.2 创建 DataFrame ---")
    data = {
        '姓名': ['张三', '李四', '王五', '赵六', '钱七'],
        '年龄': [25, 30, 35, 28, 32],
        '部门': ['技术部', '市场部', '技术部', '人事部', '财务部'],
        '薪资': [15000, 22000, 18000, 12000, 16000],
        '入职日期': pd.date_range('2020-01-01', periods=5, freq='6ME')
    }
    
    df = pd.DataFrame(data)
    print("DataFrame 示例:")
    print(df)
    print(f"\n形状: {df.shape}")
    print(f"列名: {df.columns.tolist()}")
    print(f"索引: {df.index.tolist()}")


def demo_data_io():
    """2. 数据读写操作"""
    print("\n" + "=" * 50)
    print("2. 数据读写操作")
    print("=" * 50)
    
    # 创建示例数据用于保存
    sample_data = pd.DataFrame({
        '产品': ['手机', '电脑', '平板', '耳机', '手表'],
        '销量': [100, 80, 60, 120, 90],
        '价格': [3000, 8000, 2500, 500, 2000],
        '地区': ['北京', '上海', '广州', '深圳', '杭州']
    })
    
    # 保存为不同格式（实际运行时需要相应文件）
    print("\n--- 2.1 数据写入示例 ---")
    print("# 保存为 CSV 格式")
    print("sample_data.to_csv('sales_data.csv', index=False, encoding='utf-8')")
    
    print("\n# 保存为 Excel 格式")
    print("sample_data.to_excel('sales_data.xlsx', index=False, sheet_name='销售数据')")
    
    print("\n# 保存为 JSON 格式")
    print("sample_data.to_json('sales_data.json', orient='records', force_ascii=False)")
    
    # 读取数据的常用参数
    print("\n--- 2.2 数据读取参数 ---")
    print("""
    # 读取 CSV 的常用参数：
    df = pd.read_csv('data.csv',
                     encoding='utf-8',      # 编码格式
                     sep=',',               # 分隔符
                     header=0,              # 标题行位置
                     index_col=0,           # 将某列作为索引
                     usecols=['A', 'B'],    # 只读取指定列
                     skiprows=2,            # 跳过前2行
                     nrows=1000,            # 只读前1000行
                     na_values=['N/A', 'NULL'],  # 指定缺失值标识
                     parse_dates=['date_column'],  # 解析日期列
                     dtype={'column': 'str'})     # 指定列数据类型
    """)


def demo_data_exploration():
    """3. 数据查看与探索"""
    print("\n" + "=" * 50)
    print("3. 数据查看与探索")
    print("=" * 50)
    
    # 创建示例数据
    df = pd.DataFrame({
        '姓名': ['张三', '李四', '王五', '赵六', '钱七', '孙八', '周九', '吴十'],
        '年龄': [25, 30, 35, 28, 32, 27, 33, 29],
        '部门': ['技术部', '市场部', '技术部', '人事部', '财务部', '技术部', '市场部', '人事部'],
        '薪资': [15000, 22000, 18000, 12000, 16000, 17000, 20000, 13000],
        '绩效评分': [4.2, 3.8, 4.5, 3.2, 4.0, 4.1, 3.9, 3.5],
        '入职年份': [2019, 2020, 2018, 2021, 2019, 2020, 2018, 2022]
    })
    
    print("--- 3.1 基本查看方法 ---")
    print("前3行:")
    print(df.head(3))
    
    print("\n后3行:")
    print(df.tail(3))
    
    print("\n随机2行:")
    print(df.sample(2))
    
    print("\n--- 3.2 数据信息 ---")
    print("数据基本信息:")
    print(df.info())
    
    print("\n数值列统计摘要:")
    print(df.describe())
    
    print("\n分类列统计:")
    print(df.describe(include=['object']))
    
    print("\n--- 3.3 统计分析 ---")
    print(f"平均薪资: {df['薪资'].mean():.2f}")
    print(f"薪资中位数: {df['薪资'].median()}")
    print(f"薪资标准差: {df['薪资'].std():.2f}")
    print(f"最高薪资: {df['薪资'].max()}")
    print(f"最低薪资: {df['薪资'].min()}")
    print(f"薪资四分位数:")
    print(df['薪资'].quantile([0.25, 0.5, 0.75]))


def demo_data_selection():
    """4. 数据筛选与选择"""
    print("\n" + "=" * 50)
    print("4. 数据筛选与选择")
    print("=" * 50)
    
    df = pd.DataFrame({
        'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
        'age': [25, 30, 35, 28, 32],
        'department': ['IT', 'Marketing', 'IT', 'HR', 'Finance'],
        'salary': [50000, 60000, 55000, 45000, 52000],
        'experience': [2, 5, 7, 3, 4]
    })
    
    print("--- 4.1 列选择 ---")
    print("选择单列（返回 Series）:")
    print(df['name'])
    
    print("\n选择多列（返回 DataFrame）:")
    print(df[['name', 'salary']])
    
    print("\n使用 loc 选择列:")
    print(df.loc[:, 'name':'department'])
    
    print("\n使用 iloc 选择列（位置索引）:")
    print(df.iloc[:, [0, 3]])  # 第1列和第4列
    
    print("\n--- 4.2 行选择 ---")
    print("按标签选择行:")
    print(df.loc[0:2])  # 标签0到2（包含2）
    
    print("\n按位置选择行:")
    print(df.iloc[0:3])  # 位置0到2（不包含3）
    
    print("\n选择特定行:")
    print(df.loc[[0, 2, 4]])
    
    print("\n--- 4.3 条件筛选 ---")
    print("基础条件筛选:")
    high_salary = df[df['salary'] > 52000]
    print(high_salary)
    
    print("\n复合条件筛选（AND）:")
    it_senior = df[(df['department'] == 'IT') & (df['experience'] >= 5)]
    print(it_senior)
    
    print("\n复合条件筛选（OR）:")
    young_or_high_paid = df[(df['age'] < 30) | (df['salary'] > 55000)]
    print(young_or_high_paid)
    
    print("\n使用 isin 方法:")
    specific_depts = df[df['department'].isin(['IT', 'Finance'])]
    print(specific_depts)
    
    print("\n使用 query 方法:")
    result = df.query('salary > 50000 and age < 35')
    print(result)


def demo_data_cleaning():
    """5. 数据处理与清洗"""
    print("\n" + "=" * 50)
    print("5. 数据处理与清洗")
    print("=" * 50)
    
    # 创建包含缺失值的数据
    df_dirty = pd.DataFrame({
        'name': ['Alice', 'Bob', None, 'David', 'Eve', None],
        'age': [25, np.nan, 35, 28, np.nan, 32],
        'salary': [50000, 60000, np.nan, 45000, 52000, 48000],
        'department': ['IT', 'Marketing', 'IT', None, 'Finance', 'HR']
    })
    
    print("--- 5.1 缺失值处理 ---")
    print("原始数据:")
    print(df_dirty)
    
    print("\n检查缺失值:")
    print(df_dirty.isnull())
    
    print("\n每列缺失值统计:")
    print(df_dirty.isnull().sum())

    """
    Pandas 清洗空值
        如果我们要删除包含空字段的行，可以使用 dropna() 方法，语法格式如下：
            df.dropna(axis=0, how='any', thresh=None, subset=None, inplace=False)
        参数说明：
            axis：默认为 0，表示逢空值剔除整行，如果设置参数 axis＝1 表示逢空值去掉整列。
            how：默认为 'any' 如果一行（或一列）里任何一个数据有出现 NA 就去掉整行，如果设置 how='all' 一行（或列）都是 NA 才去掉这整行。
            thresh：设置需要多少非空值的数据才可以保留下来的。
            subset：设置想要检查的列。如果是多个列，可以使用列名的 list 作为参数。
            inplace：如果设置 True，将计算得到的值直接覆盖之前的值并返回 None，修改的是源数据。
    """
    print("\n删除包含缺失值的行:")
    print(df_dirty.dropna())
    print("\n删除包含缺失值的列:")
    print(df_dirty.dropna(axis=1))

    #  fillna() 方法来替换一些空字段：
    print("\n填充缺失值（用0）:")
    print(df_dirty.fillna(0))
    
    print("\n填充缺失值（用均值）:")
    numeric_cols = df_dirty.select_dtypes(include=[np.number]).columns
    df_filled_mean = df_dirty.copy()
    df_filled_mean[numeric_cols] = df_dirty[numeric_cols].fillna(df_dirty[numeric_cols].mean())
    print(df_filled_mean)
    
    print("\n向前填充:")
    print(df_dirty.ffill())
    
    # 处理重复数据
    print("\n--- 5.2 重复值处理 ---")
    df_dup = pd.DataFrame({
        'A': [1, 2, 2, 3, 4, 4],
        'B': ['x', 'y', 'y', 'z', 'w', 'w']
    })
    
    print("包含重复值的数据:")
    print(df_dup)


    """
    Pandas 清洗重复数据
        df.dropna()	删除包含缺失值的行或列；
        df.fillna(value)	将缺失值替换为指定的值；
        df.replace(old_value, new_value)	将指定值替换为新值；
        df.duplicated()	检查是否有重复的数据；
        df.drop_duplicates()	删除重复的数据。
    """
    print("\n标记重复行:")
    print(df_dup.duplicated())
    
    print("\n删除重复行:")
    print(df_dup.drop_duplicates())
    
    print("\n基于特定列去重:")
    print(df_dup.drop_duplicates(subset=['A']))
    
    # 数据类型转换
    print("\n--- 5.3 数据类型转换 ---")
    df_types = pd.DataFrame({
        'string_col': ['1', '2', '3', '4'],
        'mixed_col': ['100', '200.5', 'invalid', '300']
    })
    
    print("原始数据类型:")
    print(df_types.dtypes)
    
    print("\n安全转换为数值（错误转为 NaN）:")
    df_types['numeric_safe'] = pd.to_numeric(df_types['mixed_col'], errors='coerce')
    print(df_types)
    
    # 列重命名
    print("\n--- 5.4 列重命名 ---")
    df_rename = df_dirty.copy()
    df_rename_renamed = df_rename.rename(columns={
        'name': '姓名',
        'age': '年龄',
        'salary': '薪资'
    })
    print("重命名后的列:")
    print(df_rename_renamed.columns.tolist())


def demo_data_transformation():
    """6. 数据转换与计算"""
    print("\n" + "=" * 50)
    print("6. 数据转换与计算")
    print("=" * 50)
    
    df = pd.DataFrame({
        '姓名': ['张三', '李四', '王五', '赵六', '钱七'],
        '年龄': [25, 30, 35, 28, 32],
        '部门': ['技术部', '市场部', '技术部', '人事部', '财务部'],
        '基本工资': [12000, 18000, 15000, 10000, 13000],
        '奖金': [3000, 4000, 3500, 2000, 3000]
    })
    
    print("--- 6.1 添加新列 ---")
    # 基本运算
    df['总薪资'] = df['基本工资'] + df['奖金']
    df['年薪'] = df['总薪资'] * 12
    
    # 条件赋值
    df['薪资等级'] = np.where(df['总薪资'] >= 18000, '高级',  np.where(df['总薪资'] >= 15000, '中级', '初级'))
    
    # 使用 cut 进行分箱
    df['年龄组'] = pd.cut(df['年龄'], bins=[20, 28, 35, 40], labels=['青年', '中年', '资深'])
    
    print("添加新列后的数据:")
    print(df[['姓名', '总薪资', '年薪', '薪资等级', '年龄组']])
    
    print("\n--- 6.2 应用函数 ---")
    # 自定义函数
    def salary_category(total_salary):
        if total_salary >= 20000:
            return 'S级'
        elif total_salary >= 16000:
            return 'A级'
        elif total_salary >= 12000:
            return 'B级'
        else:
            return 'C级'
    
    df['薪资级别'] = df['总薪资'].apply(salary_category)
    print("\n使用 apply 应用自定义函数:")
    print(df[['姓名', '总薪资', '薪资级别']])
    
    # Lambda 函数
    df['姓名长度'] = df['姓名'].apply(lambda x: len(x))
    df['奖金比例'] = df['奖金'] / df['基本工资']
    print("\n使用 lambda 函数:")
    print(df[['姓名', '姓名长度', '奖金比例']])
    
    print("\n--- 6.3 分组聚合 ---")
    # 基础分组
    dept_stats = df.groupby('部门')['总薪资'].agg(['mean', 'min', 'max', 'count'])
    print("各部门薪资统计:")
    print(dept_stats)
    
    # 多列分组
    age_dept_stats = df.groupby(['年龄组', '部门'], observed=True).agg({
        '总薪资': ['mean', 'sum'],
        '姓名': 'count'
    }).round(2)
    print("\n年龄组和部门组合统计:")
    print(age_dept_stats)
    
    # 自定义聚合函数
    def salary_range(series):
        return series.max() - series.min()
    
    custom_agg = df.groupby('部门').agg({
        '总薪资': ['mean', salary_range],
        '年龄': 'mean'
    }).round(2)
    print("\n自定义聚合函数结果:")
    print(custom_agg)


def demo_data_merge():
    """7. 数据合并与连接"""
    print("\n" + "=" * 50)
    print("7. 数据合并与连接")
    print("=" * 50)
    
    # 创建示例数据
    employees = pd.DataFrame({
        '员工ID': [1, 2, 3, 4, 5],
        '姓名': ['张三', '李四', '王五', '赵六', '钱七'],
        '部门ID': [101, 102, 101, 103, 102]
    })
    
    departments = pd.DataFrame({
        '部门ID': [101, 102, 103, 104],
        '部门名称': ['技术部', '市场部', '人事部', '财务部'],
        '部门经理': ['王经理', '李经理', '张经理', '赵经理']
    })
    
    salaries = pd.DataFrame({
        '员工ID': [1, 2, 3, 4, 6],  # 注意：员工ID=6不存在于employees中
        '基本工资': [15000, 22000, 18000, 12000, 20000],
        '奖金': [3000, 4000, 3500, 2000, 5000]
    })
    
    print("--- 7.1 Merge 连接操作 ---")
    print("左表（员工信息）:")
    print(employees)
    print("\n右表（部门信息）:")
    print(departments)
    print("\n薪资表:")
    print(salaries)
    
    # 内连接（只保留两边都有的记录）
    inner_result = pd.merge(employees, departments, on='部门ID', how='inner')
    print("\n内连接结果:")
    print(inner_result)
    
    # 左连接（保留左边所有记录）
    left_result = pd.merge(employees, departments, on='部门ID', how='left')
    print("\n左连接结果:")
    print(left_result)
    
    # 外连接（保留两边所有记录）
    outer_result = pd.merge(employees, salaries, on='员工ID', how='outer')
    print("\n外连接结果:")
    print(outer_result)
    
    # 多表连接
    multi_merge = pd.merge(
        pd.merge(employees, departments, on='部门ID'),
        salaries, on='员工ID', how='left'
    )
    print("\n三表连接结果:")
    print(multi_merge)
    
    print("\n--- 7.2 Concat 拼接操作 ---")
    df1 = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
    df2 = pd.DataFrame({'A': [5, 6], 'B': [7, 8]})
    df3 = pd.DataFrame({'C': [9, 10], 'D': [11, 12]})
    
    print("垂直拼接（增加行）:")
    vertical_concat = pd.concat([df1, df2], ignore_index=True)
    print(vertical_concat)
    
    print("\n水平拼接（增加列）:")
    horizontal_concat = pd.concat([df1, df3], axis=1)
    print(horizontal_concat)


def demo_advanced_features():
    """8. 高级功能"""
    print("\n" + "=" * 50)
    print("8. 高级功能")
    print("=" * 50)
    
    # 时间序列处理
    print("--- 8.1 时间序列处理 ---")
    dates = pd.date_range('2023-01-01', periods=12, freq='ME')
    ts_data = pd.DataFrame({
        '日期': dates,
        '销售额': np.random.randint(10000, 50000, 12),
        '访问量': np.random.randint(1000, 5000, 12)
    })
    
    print("时间序列数据:")
    print(ts_data.head())
    
    print(f"\n数据类型: {ts_data['日期'].dtype}")
    print(f"日期范围: {ts_data['日期'].min()} 到 {ts_data['日期'].max()}")
    
    # 数据透视表
    print("\n--- 8.2 数据透视表 ---")
    sales_data = pd.DataFrame({
        '销售员': ['张三', '李四', '张三', '李四', '王五', '张三'],
        '产品类别': ['电子产品', '服装', '电子产品', '服装', '电子产品', '服装'],
        '季度': ['Q1', 'Q1', 'Q2', 'Q2', 'Q1', 'Q2'],
        '销售额': [15000, 8000, 18000, 12000, 22000, 9000]
    })
    
    pivot_table = sales_data.pivot_table(
        values='销售额',
        index='销售员',
        columns='产品类别',
        aggfunc='sum',
        fill_value=0
    )
    print("数据透视表:")
    print(pivot_table)
    
    # 交叉表
    crosstab = pd.crosstab(
        sales_data['销售员'],
        sales_data['产品类别'],
        values=sales_data['销售额'],
        aggfunc='sum'
    ).fillna(0)
    print("\n交叉表:")
    print(crosstab)
    
    # 排序和排名
    print("\n--- 8.3 排序和排名 ---")
    df_sort = pd.DataFrame({
        '姓名': ['张三', '李四', '王五', '赵六'],
        '数学': [85, 92, 78, 88],
        '英语': [90, 85, 95, 82]
    })
    
    print("按数学成绩排序:")
    print(df_sort.sort_values('数学', ascending=False))
    
    print("\n按总分排序:")
    df_sort['总分'] = df_sort['数学'] + df_sort['英语']
    print(df_sort.sort_values('总分', ascending=False))
    
    print("\n添加排名:")
    df_sort['数学排名'] = df_sort['数学'].rank(ascending=False)
    df_sort['总分排名'] = df_sort['总分'].rank(ascending=False)
    print(df_sort)


def main():
    """主函数 - 运行所有示例"""
    print("🐼 Pandas 核心 API 综合示例 🐼")
    print("本示例展示了 pandas 库的主要功能和使用方法\n")
    
    try:
        demo_basic_concepts()
        demo_data_io()
        demo_data_exploration()
        demo_data_selection()
        demo_data_cleaning()
        demo_data_transformation()
        demo_data_merge()
        demo_advanced_features()
        
        print("\n" + "=" * 50)
        print("✅ 所有示例演示完成！")
        print("=" * 50)
        print("\n💡 学习建议:")
        print("1. 从基础概念开始，熟练掌握 DataFrame 和 Series")
        print("2. 重点练习数据读写、筛选和清洗操作")
        print("3. 掌握分组聚合是数据分析的关键技能")
        print("4. 多表连接在实际工作中非常常用")
        print("5. 实践是最好的学习方式，多动手练习")
        
    except Exception as e:
        print(f"❌ 运行出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()