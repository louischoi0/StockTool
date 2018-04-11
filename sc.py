import pandas as  pd
import sys

def get_list(idx) :
    res = pd.DataFrame()

    for i in range(1, idx+1) :
        pagesrc = "http://finance.naver.com/fund/fundDailyQuoteList.nhn?fundCd=K55301B73758&page="
        pagesrc += str(i)
        res = res.append(pd.read_html(pagesrc)[0])

    return res

a = get_list(int(sys.argv[1]))
a.to_csv('list.csv')
