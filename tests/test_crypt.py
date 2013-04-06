#-*- coding:utf-8 -*-
__author__ = 'bluele'


if __name__ == '__main__':
    #from Crypto.Cipher import AES # 補完が効かない
    import Crypto.Cipher.AES as AES
    from Padding import appendPadding, removePadding, AES_blocksize
    from Crypto.Hash import SHA256
    import unittest
    class TestCrypt(unittest.TestCase):
        def setUp(self):
            self.password = 'password'
            self.message = """\
暗号メッセージ構文(Cryptographic Message Syntax:CMS)は暗号で保護されたメッセージに関するIETFの標準規格である。任意の形式のデジタルデータに対してデジタル署名、メッセージダイジェスト、メッセージ認証もしくは暗号化を行うために利用することができる。
CMSは、PEM(Privacy-Enhanced Mail)に基づいたPKCS#7の構文に基づいている。CMSの(2004年の)最新版はRFC 3852により規定されている。
CMSのアーキテクチャは、PKIXワーキンググループにより規定されたプロファイルなどの証明書に基づく鍵管理の上に構築されている。
CMSは、S/MIME、PKCS#12やRFC 3161 デジタルタイムスタンプ（英語版）プロトコルといった他の多くの暗号に関する標準の主要な暗号コンポーネントとして利用されている。
""" * 100

        def createSha256(self, string):
            hash = SHA256.new()
            hash.update(string)
            return hash.digest()

        @staticmethod
        def appendPadding(string):
            return appendPadding(string, blocksize=AES_blocksize, mode='CMS')

        @staticmethod
        def removePadding(string):
            return removePadding(string, blocksize=AES_blocksize, mode='CMS')

        def testAES(self):
            hash_key = self.createSha256(self.password)
            message = self.appendPadding(self.message)

            c_obj = AES.new(hash_key, AES.MODE_ECB)
            ciphertext = c_obj.encrypt(message)

            obj = AES.new(hash_key, AES.MODE_ECB)
            string = self.removePadding(obj.decrypt(ciphertext))
            self.assertEqual(string, self.message)

    unittest.main()