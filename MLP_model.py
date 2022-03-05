#!/usr/bin/env python
# coding: utf-8

# # 다운받아야 하는 것들.
import sys

import math
import pandas as pd
import ssl
import socket
import whois
import requests
from tld import get_tld
from urllib.parse import urlparse
from dateutil.parser import parse

import torch
from torch import nn
import torch.nn.functional as F

# # *특징추출 함수들* #

# 1번 Check_IPdomain    # 1: 정상 / 0: 의심 / -1: 피싱

def Check_IPDomain(url):
    try:
        domain = urlparse(url).netloc
        check = domain.split('.')
        for i in check:
            int(i, 0)
        return -1
    
    except ValueError:
        return 1

    except:
        return 0

# 2번 Check_URLLength     # 1: 정상 / 0: 의심 / -1: 피싱

def Check_URLLength(url):
    if len(url) < 54 :
        return 1
    elif len(url) >= 54 and len(url) <= 75 :
        return 0
    else :
        return -1

# 3번 Check_Symbol   # 1: 정상 / -1: 피싱

def Check_Symbol(url):
    if '@' in url:
        return -1
    else :
        return 1

# 4번 Check_Subdomain # 1: 정상 / -1: 피싱

def Check_SubDomain(url):
    try:
        reset_url = urlparse(url).netloc
        res = get_tld(url, as_object = True)
    except:
        return -1
    
    fld = res.fld
    sub = reset_url[:(-len(fld))]
    sub_num = sub.count('.')
    
    if sub_num == 1:
        return 1
    else:
        return -1

# 5번 Check_SpecialCharacters        # 1: 정상 / -1: 피싱

def Check_SpecialCharacters(url):
    if '&' in url:
        return -1
    elif '!' in url:
        return -1
    elif '=' in url:
        return -1
    else:
        return 1

# 6번 Check_HostLength        # 1: 정상 / -1: 피싱

def Check_HostLength(url):
    try:
        URL = get_tld(url, as_object = True)
        if len(URL.fld) >22:
            return -1
        else:
            return 1
    except:
        return -1

# 7번 Check_SuspiciousWord        # 1: 정상 / -1: 피싱

def Check_SuspiciousWord(url):
    if 'signin' in url:
        return -1
    elif 'wp' in url:
        return -1
    elif 'update' in url:
        return -1
    elif 'login' in url:
        return -1
    elif 'admin' in url:
        return -1
    else:
        return 1

# 8번 Check_URLEntropy          # 1: 정상 / 0: 의심 / -1: 피싱

def entropy_matrix(url):
    try:
        url_parse = urlparse(url)
        url_split = url[len(url_parse.scheme):]
    except:
        return 0
    
    url_set = set(url_split)
    per = 1/len(url_split)
    percent = [url_split.count(i)*per for i in url_set]

    entropy = [p*math.log(p) for p in percent]
    entropy = -sum(entropy)
    
    return entropy

def Check_URLEntropy(url):
    if entropy_matrix(url) < 3.2:
        return 1
    else:
        return -1

# 9번 Check_NumRatio           # 1: 정상 / 0: 의심 / -1: 피싱

def NumRatio(url):
    try:
        url_parse = urlparse(url)
        url_split = url[len(url_parse.scheme):]
    except:
        return 0
    
    url_list = list(url_split)
    num = 0
    for i in url_list:
        try:
            if type(int(i)) is int:
                num += 1
        except:
            continue

    return num/len(url_list)

def Check_NumRatio(url):
    if NumRatio(url) > 0.17:
        return -1
    else:
        return 1

# 10번 Check_RegiLength     # 1: 정상 / 0: 의심 / -1: 피싱

def Get_RegiLength(url):
    domain_info = whois.whois(url)
    if type(domain_info.expiration_date) == list :
        expiration_date = domain_info.expiration_date[0]
    else:
        expiration_date = domain_info.expiration_date
        
    if type(domain_info.updated_date) == list :
        updated_date = domain_info.updated_date[0]
    else:
        updated_date = domain_info.updated_date

    if expiration_date == None or updated_date == None:
        return 0
    
    RegiLength = (expiration_date - updated_date).days
    return RegiLength

def Check_RegiLength(url):
    try :
        RegiLength = Get_RegiLength(url)
        if RegiLength <= 365 :
            return -1
        else:
            return 1
    except whois.parser.PywhoisError:
        return -1
    except:
        return 0

# 11번 Check_SSLnOrg   # 1 : 정상 / 0 : 의심 / -1 : 피싱

 
def https_connect(murl):
    ctx = ssl.create_default_context()
    s = ctx.wrap_socket(socket.socket(), server_hostname=murl)
    s.settimeout(30.0)                                      
    s.connect((murl, 443))
                                           
    return s

def Check_SSLnOrg(url):    
    try:
        murl = urlparse(url).netloc
        s = https_connect(murl)
    except:                       
        return -1
    cert = s.getpeercert()
    issuer = dict(x[0] for x in cert['issuer'])
    issued_by = issuer['organizationName']

    data = pd.read_csv('./dataset/trust_organization.csv')
    trust_orglist = data['0']

    for trusted_issuer in trust_orglist:
        if trusted_issuer == issued_by:
            break
    else :
        return 0
 
    notAfter = cert['notAfter']
    notBefore = cert['notBefore']
    init_date = parse(notBefore)
    expiration_date = parse(notAfter)
    total_days = (expiration_date.date() - init_date.date()).days
    if total_days >= 365 :
        return 1
    else :
        return 0
    
# 12번 Check_IsHttps           # 1: 정상 / 0: 의심 / -1: 피싱

def Check_IsHttps(url):
    scheme = urlparse(url).scheme
    if scheme == 'https':
        return 1
    elif scheme == 'http':
        return -1
    else:
        return 0

# 13번 Check_Shortening       # 1: 정상 / 0: 의심/ -1: 피싱

def Check_Shortening(url):
    try:
        http_status = requests.get(url, timeout = 30).history  #read timout설정
        for i in http_status:  
            if i.status_code//100 == 3:
                return -1
        else:
            return 1
    except:
        return 0



# # Google Extension #

# ### 1. 받은 URL을 특징별로 분류하기 ###

def parse_url(url):
    func = []
    func.append(Check_IPDomain)
    func.append(Check_URLLength)
    func.append(Check_Symbol)
    func.append(Check_SubDomain)   
    func.append(Check_SpecialCharacters)
    func.append(Check_HostLength)
    func.append(Check_SuspiciousWord)
    func.append(Check_URLEntropy)
    func.append(Check_NumRatio)
    func.append(Check_RegiLength)
    func.append(Check_SSLnOrg)
    func.append(Check_IsHttps)

    parse = []
    for i in range(len(func)):
        try:
            parse.append(func[i](url))
        except:
            parse.append(0)

    return parse


# ### 2. 모델 불러오기 ###

class MLP(nn.Module):
  def __init__(self, feature_size, hidden1, hidden2, hidden3):
    super().__init__()

    self.feature = feature_size
    self.hidden_dim1 = hidden1
    self.hidden_dim2 = hidden2
    self.hidden_dim3 = hidden3

    self.layer1 = nn.Sequential(
        nn.Linear(self.feature, self.hidden_dim1),
        nn.ReLU()
    )
    self.layer2 = nn.Sequential(
        nn.Linear(self.hidden_dim1, self.hidden_dim2),
        nn.ReLU()
    )
    self.layer3 = nn.Sequential(
        nn.Linear(self.hidden_dim2, self.hidden_dim3),
        nn.ReLU()
    )
    self.output = nn.Sequential(
        nn.Linear(self.hidden_dim3, 1),
        nn.Sigmoid()
    )
  def forward(self, x):
    x = self.layer1(x)
    x = self.layer2(x)
    x = self.layer3(x)
    x = self.output(x)
    return x

  def accuracy_fn(self, x, y):
    result = x
    for i in range(len(result)):
      if result[i][0] >= 0.5:
        result[i][0] = 1
      else:
        result[i][0] = 0
    n_correct = torch.eq(result, y).sum().item()
    accuracy = (n_correct/len(x)) *100
    return accuracy


# ### 3. 학습한 머신러닝 알고리즘으로 결과 추측하기 ###


def IsPhishing(_url):
    parsed = parse_url(_url)                #list
    parsed_toTensor = torch.Tensor(parsed)  #tensor

    func_name = []
    func_name.append('"Check_IPDomain"')
    func_name.append('"Check_URLLength"')
    func_name.append('"Check_Symbol"')
    func_name.append('"Check_SubDomain"')   
    func_name.append('"Check_SpecialCharacters"')
    func_name.append('"Check_HostLength"')
    func_name.append('"Check_SuspiciousWord"')
    func_name.append('"Check_URLEntropy"')
    func_name.append('"Check_NumRatio"')
    func_name.append('"Check_RegiLength"')
    func_name.append('"Check_SSLnOrg"')
    func_name.append('"Check_IsHttps"') 

    isphish = float(model(parsed_toTensor))  #result

    if isphish >= 0.5:
      result = '"isbenign": 1,'
    else:
      result = '"isbenign": -1,'

    for i in range(len(parsed)):
        result = result + func_name[i] + ': ' + str(parsed[i]) + ',' 
    result = result[:-1] + '}'


    print(result)

# return 1이면 정상, 0이면 거짓

if __name__ == '__main__':
    hidden_dim1 = 10
    hidden_dim2 = 10
    hidden_dim3 = 5
    feature_size = 12

    model = MLP(feature_size, hidden_dim1, hidden_dim2, hidden_dim3)
    model.load_state_dict(torch.load('./savedmodel/MLP_statedict.pt'))
    
    IsPhishing(sys.argv[1])

