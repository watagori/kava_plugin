import sys

import pandas as pd
from senkalib.chain.kava.kava_transaction_generator import (
    KavaTransactionGenerator,
)
from senkalib.senka_lib import SenkaLib
from senkalib.senka_setting import SenkaSetting

from kava_plugin.kava_plugin import KavaPlugin
from senkalib.token_original_id_table import TokenOriginalIdTable

TOKEN_ORIGINAL_IDS_URL = "https://raw.githubusercontent.com/ca3-caaip/token_original_id/master/token_original_id.csv"


if __name__ == "__main__":
    args = sys.argv
    address = args[1]
    caajs = []
    settings = SenkaSetting({})
    token_original_ids = TokenOriginalIdTable(TOKEN_ORIGINAL_IDS_URL)
    transactions = KavaTransactionGenerator.get_transactions(
        settings, address, None, None
    )

    for transaction in transactions:
        if KavaPlugin.can_handle(transaction):
            caaj_peace = KavaPlugin.get_caajs(
                address, transaction, token_original_ids
            )
            caajs.extend(caaj_peace)

    df = pd.DataFrame(caajs)
    df = df.sort_values("time")
    caaj_csv = df.to_csv(None, index=False)
    print(caaj_csv)
