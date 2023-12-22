import streamlit as st
import requests
import streamlit_echarts
from bs4 import BeautifulSoup
from pyecharts.charts import Bar, Pie, Line, WordCloud, Scatter, Funnel,Boxplot
from pyecharts import options as opts
from collections import Counter
import re

from pyecharts.globals import ThemeType
from pyecharts.render import make_snapshot


def process(url):
    # 添加侧边栏
    chart_type = st.sidebar.selectbox("请选择图型", ["词云图", "柱状图", "饼图", "折线图", "散点图","条形图" , "漏斗图"])
    url = str(url)
    data = requests.get(url).content
    soup = BeautifulSoup(data, 'html.parser')
    soup = soup.get_text()
    # 使用正则表达式去除HTML标签
    soup = re.sub(r'<.*?>', '', soup)
    # 去除标点符号和多余空格
    soup = re.sub(r'[^\w\s]', '', soup)
    words = soup.split()

    word_freq = Counter(words)
    wordcloud_data = [(word, freq) for word, freq in word_freq.items()]
    topword = word_freq.most_common(20)
    categories = [word[0] for word in topword]
    values = [word[1] for word in topword]

    # 词云图
    wordcloud = (
        WordCloud()
        .add("", wordcloud_data, word_size_range=[20, 100], shape="diamond")
    )

    # 柱状图
    bar = (
        Bar()
        .add_xaxis(categories)
        .add_yaxis("频率", values)
    )

    # 饼图
    pie = (
        Pie()
        .add("", topword)
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    )

    # 折线图
    line = (
        Line()
        .add_xaxis(categories)
        .add_yaxis("Word_freq", values)
    )



    # 散点图
    scatter = (
        Scatter()
        .add_xaxis(categories)
        .add_yaxis("频率", values)
    )

    #条形图
    bar2 = (
          Bar()
          .add_xaxis(categories)
          .add_yaxis("频率", values)
          .reversal_axis()  # 反转 x 轴和 y 轴
    )

    # 漏斗图
    funnel = (
        Funnel()
        .add("", wordcloud_data)
    )


    return wordcloud, bar, pie, line, scatter, bar2, funnel, chart_type


def main():
    st.title("文本分析应用")
    url = st.text_input("请输入文章URL")
    if st.button("分析") or url:
        if url:
            wordcloud, bar, pie, line, scatter,bar2, funnel , chart_type= process(url)

            if chart_type == "词云图":
                streamlit_echarts.st_pyecharts(
                    wordcloud,
                    theme=ThemeType.DARK
                )
            elif chart_type == "柱状图":
                streamlit_echarts.st_pyecharts(
                    bar,
                    theme=ThemeType.DARK
                )
            elif chart_type == "饼图":
                streamlit_echarts.st_pyecharts(
                    pie,
                    theme=ThemeType.DARK
                )
            elif chart_type == "折线图":
                streamlit_echarts.st_pyecharts(
                    line,
                    theme=ThemeType.DARK
                )
            elif chart_type == "散点图":
                streamlit_echarts.st_pyecharts(
                    scatter,
                    theme=ThemeType.DARK
                )
            elif chart_type == "条形图":
                streamlit_echarts.st_pyecharts(
                    bar2,
                    theme=ThemeType.DARK
                )
            # elif chart_type == "条形图":
            #      streamlit_echarts.st_pyecharts(
            #          bar,
            #          theme=ThemeType.DARK
            #      )
            elif chart_type == "漏斗图":
                streamlit_echarts.st_pyecharts(
                    funnel,
                    theme=ThemeType.DARK
                )




if __name__ == '__main__':
    main()