import unittest
import tracerAS

grey = r"192.168.0.0"
ip0 = r"188.234.131.144"
ip1 = r"212.193.80.0"
grey_country = "EU"
ip01_country = "RU"
ip1_asn = "5468"
ip0_asn = "9049"
ip0_prov = "CJSC \"ER-Telecom Holding\" Saint-Petersburg branchSaint-Petersburg, RussiaPPPOE individual customers"
ip1_prov = "URFU, Network for services S. Kovalevskoy 5Yekaterinburg, Russia"
grey_prov ="grey address is not managed by the RIPE NCC"

test_list = ['',
             'Трассировка маршрута к 8.8.8.8 с максимальным числом прыжков 10','',
             '  1     1 ms     1 ms     1 ms  192.168.0.1 ',
             '  2     3 ms     4 ms     3 ms  109.195.110.124 ',
             '  3     2 ms     2 ms     4 ms  109.195.104.241 ',
             '  4    36 ms    38 ms    36 ms  188.234.131.145 ',
             '  5    34 ms    34 ms    32 ms  188.234.131.144 ',
             '  6    35 ms    35 ms    36 ms  108.170.250.34 ',
             '  7    41 ms    41 ms    41 ms  216.239.50.46 ',
             '  8    40 ms    41 ms    41 ms  108.170.235.64 ',
             '  9    44 ms    44 ms    45 ms  72.14.237.201 ',
             ' 10     *        *        *     Превышен интервал ожидания для запроса.',
             '', 'Трассировка завершена.', '']

filtered_list = ['192.168.0.1',
                 '109.195.110.124',
                 '109.195.104.241',
                 '188.234.131.145',
                 '188.234.131.144',
                 '108.170.250.34',
                 '216.239.50.46',
                 '108.170.235.64',
                 '72.14.237.201']


class Test(unittest.TestCase):

    def test_asn(self):
        self.assertEqual(tracerAS.get_asn(ip0), ip0_asn)
        self.assertEqual(tracerAS.get_asn(ip1), ip1_asn)
        self.assertIsNone(tracerAS.get_asn(grey))

    def test_county_provider(self):
        self.assertEqual(tracerAS.get_country_provider(ip0,False), (ip01_country, ip0_prov))
        self.assertEqual(tracerAS.get_country_provider(ip1, False), (ip01_country, ip1_prov))
        self.assertEqual(tracerAS.get_country_provider(grey, True), (grey_country, grey_prov))

    def test_filter_list(self):
        res_list=tracerAS.filter_list(test_list)
        self.assertEqual(len(res_list), 9)
        self.assertEqual(res_list, filtered_list)


if __name__ == '__main__':
    unittest.main()
