from urllib.request import urlopen
from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from io import StringIO
from io import open

def readPDF(pdfFile):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)

    process_pdf(rsrcmgr, device, pdfFile)
    device.close()

    content = retstr.getvalue()
    retstr.close()
    return content

'''
#####################################
dashujr_复杂网络策略_命中示例权重分
#####################################
'''

pdfFile = open("C:\\Users\\T\\Downloads\\dashujr_复杂网络策略_命中示例权重分.pdf",'rb')
outputString = readPDF(pdfFile)
print(outputString)
pdfFile.close()

#提取规则编号
import re
import pandas as pd

pattern1=re.compile('[0-9]{8}')
col1=pattern1.findall(outputString)

#提取权重分
pattern2=re.compile('[0-9]\.[0-9]')
col2=pattern2.findall(outputString)

#提取规则名称
pattern3=re.compile('[手机号|设备命|身份证].+')
col3=pattern3.findall(outputString)
col3=col3[1:]
pattern4=re.compile('.*_50[a-z]{4}')
col4=pattern4.findall(outputString)
col5=list(map(lambda x,y:x+y,col3,col4))

#导出数据
data=pd.DataFrame()
data['规则编号']=col1
data['规则名称']=col5
data['权重分']=col2
data.to_csv('C:\\Users\\T\\Downloads\\dashujr_复杂网络策略_命中示例权重分.csv',index=False)
