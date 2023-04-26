import bs4
import arrow
from bs4 import BeautifulSoup
from common.models import *


def find_node(soup, query):
    """
    一个简单的封装，用于查找节点，如果没有找到，返回一个value为空的default节点
    """
    result = find_node(soup, query)
    return result or bs4.element.Tag(name='default', attrs={'value': ''})


def handle_court(court_node):
    """
    处理法院
    """
    court_name = find_node(court_node, 'BZFYMC').get('value')  # 法院名称
    court_code = find_node(court_node, 'FYCJM').get('value')  # 法院层级码
    court_level = find_node(court_node, 'FYJB').get('value')  # 法院层级
    court_province = find_node(court_node, 'XZQH_P').get('value')  # 行政区划——省份
    court_city = find_node(court_node, 'XZQH_C').get('value')  # 行政区划——城市

    court = Court.objects.filter(name=court_name)
    if court.exists():
        return court.first()
    else:
        return Court.objects.create(
            name=court_name, province=court_province, city=court_city, code=court_code, level=court_level)


def handle_procuratorate(soup):
    """
    处理检察院
    """
    name = find_node(soup, 'CBJG').get('value')  # 检察院名称(承办机关)
    district_code = find_node(soup, 'XZQH_CODE').get('value')  # 行政区划代码
    province = find_node(soup, 'XZQH_P').get('value')  # 行政区划——省
    city = find_node(soup, 'XZQH_C').get('value')  # 行政区划——市
    county = find_node(soup, 'XZQH_CC').get('value')  # 行政区划——区县
    level = find_node(soup, 'CBJG_LEVEL').get('value')  # 行政机关_级别

    procuratorate = Procuratorate.objects.filter(name=name)
    if procuratorate.exists():
        return procuratorate.first()
    else:
        return Procuratorate.objects.create(
            name=name, district_code=district_code, province=province, city=city, county=county, level=level)


def handle_party(party_node):
    """
    处理当事人
    """
    # 当事人信息
    name = find_node(party_node, 'SSCYR').get('value')  # 当事人名称

    if name:
        # 法院文书
        if find_node(party_node, 'SFMH').get('value') == '是':  # 当事人名称是否模糊
            name_is_fuzzy = True
        else:
            name_is_fuzzy = False
    else:
        # 检察院文书
        name = find_node(party_node, 'XM').get('value')  # 当事人名称
        name_is_fuzzy = False
    h_type = find_node(party_node, 'DSRLX').get('value')  # 当事人类型
    nationality = find_node(party_node, 'GJ').get('value')  # 国籍
    nation = find_node(party_node, 'MZ').get('value')  # 民族
    gender = find_node(party_node, 'XB').get('value')  # 性别
    birthday = find_node(party_node, 'CSRQ').get('value')  # 出生日期

    if name_is_fuzzy:
        # 直接当作新当事人处理
        return Party.objects.create(name=name, name_is_fuzzy=name_is_fuzzy, h_type=h_type,
                                    nationality=nationality, nation=nation, gender=gender, birthday=birthday)
    else:
        party = Party.objects.filter(name=name, name_is_fuzzy=name_is_fuzzy, h_type=h_type,
                                     nationality=nationality, nation=nation, gender=gender, birthday=birthday)
        if party.exists():
            return party.first()
        else:
            return Party.objects.create(name=name, name_is_fuzzy=name_is_fuzzy, h_type=h_type,
                                        nationality=nationality, nation=nation, gender=gender, birthday=birthday)


def handle_agent(agent_node, parties):
    """
    处理代理人
    """
    name = find_node(agent_node, 'SSCYR').get('value')  # 代理人名称
    h_type = find_node(agent_node, 'DSRLX').get('value')  # 当事人类型
    profession = find_node(agent_node, 'DLRBHRZYLX').get('value')  # 代理人辩护人职业类型
    a_type = find_node(agent_node, 'BHRHSSDLRLX').get('value')  # 辩护人或诉讼代理人类型

    agent = Agent.objects.filter(name=name, h_type=h_type, profession=profession, a_type=a_type)
    if agent.exists():
        agent = agent.first()
    else:
        agent = Agent.objects.create(name=name, h_type=h_type, profession=profession, a_type=a_type)

    # 被代理人
    for party in parties:
        agent.parties.add(party)


def handle_lawreference(lawreference_node):
    """
    处理法条引用
    """
    res = []
    law_name = find_node(lawreference_node, 'MC').get('value')  # 法律法条名称
    for clause in lawreference_node.findChildren('T'):  # 条
        for clause_item in clause.findChildren('K'):  # 款
            for item in clause_item.findChildren('X'):  # 项
                law_ref = LawReference.objects.filter(law_name=law_name,
                                                      clause=clause.get('value'),
                                                      clause_item=clause_item.get('value'),
                                                      item=item.get('value'))
                if law_ref.exists():
                    res.append(law_ref.first())
                else:
                    res.append(LawReference.objects.create(law_name=law_name,
                                                           clause=clause.get('value'),
                                                           clause_item=clause_item.get('value'),
                                                           item=item.get('value')))
    return res


def handle_judge(judge_node):
    """
    处理法官
    """
    name = find_node(judge_node, 'FGRYXM').get('value')  # 法官人员姓名
    full_name = find_node(judge_node, 'FGRYWZ').get('value')  # 法官人员完整

    judge = Judge.objects.filter(full_name=full_name)
    if judge.exists():
        return judge.first()
    else:
        return Judge.objects.create(name=name, full_name=full_name)


def handle_document(soup: bs4.BeautifulSoup):
    """
    处理其他文书(通知书, 起诉状, 只有一个的‘暂予监外执行案例’）
    """
    # 仅存储基本信息
    agency = find_node(soup, 'WSZZDW').get('value')  # 文书制作单位
    doc_name = find_node(soup, 'WSMC').get('value')  # 文书名称
    doc_type = find_node(soup, 'WSZL').get('value')  # 文书种类
    full_text = find_node(soup, 'QW').get('value')  # 文书内容

    return Document.objects.create(agency=agency, doc_name=doc_name, doc_type=doc_type, full_text=full_text)


def handle_judgment(soup: bs4.BeautifulSoup):
    """
    处理判决书(裁定书/调解书)
    """
    # 文书基本信息
    document = handle_document(soup)

    # 判决书基本信息
    case_number = find_node(soup, 'AH').get('value')  # 案号
    case_type = find_node(soup, 'AJLB').get('value')  # 案件类别
    judgment_date_str = find_node(soup, 'CPSJ').get('value')
    judgment_date = arrow.get(judgment_date_str, 'YYYY年M月D日').date()  # 裁判时间

    # 法院信息
    court_node = find_node(soup, 'JBFY')
    court = handle_court(court_node)

    # 创建文书
    judgment = Judgment.objects.create(document=document,
                                       case_number=case_number,
                                       case_type=case_type,
                                       judgment_date=judgment_date,
                                       court=court)
    judgment.save()

    # 当事人信息
    plaintiff_node_list = soup.find_all('QSF')  # 原告(起诉方)
    for plaintiff_node in plaintiff_node_list:
        judgment.plaintiff.add(handle_party(plaintiff_node))

    defendant_node_list = soup.find_all('YSF')  # 被告(被诉方)
    for defendant_node in defendant_node_list:
        judgment.defendant.add(handle_party(defendant_node))

    # 代理人信息
    agent_node_list = soup.find_all('DLR')
    for agent_node in agent_node_list:
        parties = []  # 代理人代理的当事人
        for party_node in agent_node.find_all('DLDX'):
            parties.append(judgment.plaintiff.filter(name=party_node.get('value')).first())  # 用名字查找当事人
            parties.append(judgment.defendant.filter(name=party_node.get('value')).first())
        judgment.agent.add(handle_agent(agent_node, parties))

    # 法条引用
    lawreference_node_list = soup.find_all('FLFTFZ')
    for lawreference_node in lawreference_node_list:
        for lawreference in handle_lawreference(lawreference_node):  # handle_lawreference返回的是一个法条列表
            judgment.lawreference.add(lawreference)

    # 法官信息
    judge_node_list = soup.find_all('CUS_FGCY')
    for judge_node in judge_node_list:
        judgment.judge.add(handle_judge(judge_node))


def handle_prosecution(soup: bs4.BeautifulSoup):
    """
    处理起诉书
    """
    # 文书基本信息
    document = handle_document(soup)

    # 起诉书基本信息
    case_number = find_node(soup, 'AH').get('value')  # 案号
    case_type = find_node(soup, 'AJLB').get('value')  # 案件类别

    # 诉至法院
    court_name = find_node(soup, 'SZFY').get('value')  # 诉至法院名称

    if court_name:
        p_date_str = find_node(soup, 'QSRQ').get('value')  # 起诉日期
    else:
        p_date_str = find_node(soup, 'BQSRQ').get('value')  # 不起诉日期
    p_date = arrow.get(p_date_str, 'YYYY年M月D日').date()

    # 检察院信息
    procuratorate = handle_procuratorate(soup)

    # 创建文书
    prosecution = Prosecution.objects.create(document=document,
                                             case_number=case_number,
                                             case_type=case_type,
                                             p_date=p_date,
                                             procuratorate=procuratorate)
    prosecution.save()

    # 当事人信息
    if court_name:
        defendant_node_list = soup.find_all('CUS_BGRXX')  # 被告人信息
    else:
        defendant_node_list = soup.find_all('CUS_BBQSRXX')  # 被不起诉人信息
    for defendant_node in defendant_node_list:
        prosecution.defendant.add(handle_party(defendant_node))
