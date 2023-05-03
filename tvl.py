from solana.rpc.api import Client
from solders.pubkey import Pubkey
from solders.keypair import Keypair
from spl.token.client import Token
from spl.token.constants import ASSOCIATED_TOKEN_PROGRAM_ID
from solana.rpc.commitment import Commitment
import json
import time

# Create a Solana client instance
solana_client = Client("https://api.devnet.solana.com")
program_id = Pubkey.from_string("zbcKGdAmXfthXY3rEPBzexVByT2cqRqCZb9NwWdGQ2T")
zbc_devnet = Pubkey.from_string("zebeczgi5fSEtbpfQKVZKCJ3WgYXxjkMUkNNx7fLKAF")


def payer() -> Keypair:
    with open("./test.json") as f:
        faucet_keypair_json: List[int] = json.load(f)
    return Keypair.from_bytes(faucet_keypair_json)


token = Token(solana_client, zbc_devnet, ASSOCIATED_TOKEN_PROGRAM_ID, payer())

# Call getProgramAccounts() to retrieve the list of owned accounts
accounts = solana_client.get_program_accounts(program_id)

tvl_sol = 0
tvl_zbc = 0

associated_address = Token.get_accounts_by_owner_json_parsed(
    token,
    owner=Pubkey.from_string("2usaNXXRyQGobJBSevEqQ5VXCEgKQgYs2PynmX13oaf9"),
    commitment=Commitment("confirmed")
)

# Loop through the list of owned accounts and print their public keys
for account in accounts.value:
    # time.sleep(5)
    tvl_sol += account.account.lamports
    print(account.pubkey)
    # Get the associated token account address
    associated_address = Token.get_accounts_by_owner_json_parsed(
        token,
        owner=account.pubkey,
        commitment=Commitment("confirmed")
    )
    print(associated_address)
    if associated_address.value != []:
        tvl_zbc += associated_address.value[0].account.data.parsed['info']['tokenAmount']['uiAmount']

print(tvl_sol)
print(tvl_zbc)
