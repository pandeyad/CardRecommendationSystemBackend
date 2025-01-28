from src.data_factories import BaseDataFactory

class CreditCardDataCrawlerFactory(BaseDataFactory):

    def run(self):
        from src.webcrawler.bank.hdfc import HDFCBankCrawler
        HDFCBankCrawler().crawl_data(bank='hdfc')