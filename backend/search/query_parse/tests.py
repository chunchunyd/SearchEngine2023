from .views import *
from django.test import TestCase


# 测试parse_query
class QueryParseTestCase(TestCase):
    """
    测试parse_query
    """

    def test_split_into_tokens(self):
        """
        测试split_into_tokens
        """
        query = 'aa & (bb | cc & ee) - dd'
        tokens = split_into_tokens(query)
        self.assertEqual(tokens, ['aa', '&', '(', 'bb', '|', 'cc', '&', 'ee', ')', '-', 'dd'])

    def test_infix_to_postfix(self):
        """
        测试infix_to_postfix
        """
        tokens = ['aa', '&', '(', 'bb', '|', 'cc', '&', 'ee', ')', '-', 'dd']
        expr = infix_to_postfix(tokens)
        self.assertEqual(expr, ['aa', 'bb', 'cc', 'ee', '&', '|', '&', 'dd', '-'])

    def test_term_to_doc_ids(self):
        """
        测试term_to_doc_ids
        """
        doc_ids = term_to_doc_ids({'豆腐脑'})
        self.assertEqual(doc_ids, ({25549, 48349, 63477}, {'豆腐脑'}))
        doc_ids = term_to_doc_ids({'宜川县'})
        self.assertEqual(doc_ids, ({5365, 22270, 25549, 31319, 35654, 40766}, {'宜川县'}))
        doc_ids = term_to_doc_ids({'硫酸铝钾'})
        self.assertEqual(doc_ids, ({25549, 51343}, {'硫酸铝钾'}))
        doc_ids = term_to_doc_ids({'豆腐脑', '宜川县'})
        self.assertEqual(doc_ids, ({5365, 22270, 25549, 31319, 35654, 40766, 48349, 63477}, {'豆腐脑', '宜川县'}))

    def test_cal_doc_ids(self):
        """
        测试cal_doc_ids
        """
        expr = ['豆腐脑', '宜川县', '&']
        doc_ids = cal_doc_ids(expr)
        self.assertEqual(doc_ids, ({25549}, {'豆腐脑', '宜川县'}))

        expr = ['豆腐脑', '宜川县', '|']
        doc_ids = cal_doc_ids(expr)
        self.assertEqual(doc_ids, ({5365, 22270, 25549, 31319, 35654, 40766, 48349, 63477}, {'豆腐脑', '宜川县'}))

        expr = ['豆腐脑', '宜川县', '-']
        doc_ids = cal_doc_ids(expr)
        self.assertEqual(doc_ids, ({48349, 63477}, {'豆腐脑'}))

        expr = ['豆腐脑', '宜川县', '|', '硫酸铝钾', '-']
        doc_ids = cal_doc_ids(expr)
        self.assertEqual(doc_ids, ({5365, 22270, 31319, 35654, 40766, 48349, 63477}, {'豆腐脑', '宜川县'}))


