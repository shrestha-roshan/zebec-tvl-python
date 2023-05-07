from solana.rpc.api import Client
from solders.pubkey import Pubkey
from solana.rpc import types
from spl.token.constants import ASSOCIATED_TOKEN_PROGRAM_ID
from solana.rpc.commitment import Commitment
import time

# Create a Solana client instance
solana_client = Client("https://api.devnet.solana.com")
program_id = Pubkey.from_string("zbcKGdAmXfthXY3rEPBzexVByT2cqRqCZb9NwWdGQ2T")
zbc_devnet = Pubkey.from_string("zebeczgi5fSEtbpfQKVZKCJ3WgYXxjkMUkNNx7fLKAF")

# Call getProgramAccounts() to retrieve the list of owned accounts
accounts = solana_client.get_program_accounts(program_id)

tvl_sol = 0
tvl_zbc = 0

# Loop through the list of owned accounts
for account in accounts.value:
    # time.sleep(5)
    tvl_sol += account.account.lamports
    print("owner : ", account.pubkey)
    # Get the associated token account address
    associated_address = solana_client.get_token_accounts_by_owner_json_parsed(
        owner=account.pubkey,
        opts=types.TokenAccountOpts(
            mint=zbc_devnet,
            program_id=ASSOCIATED_TOKEN_PROGRAM_ID,
        ),
        commitment=Commitment("confirmed")
    )
    print(associated_address)
    if associated_address.value != []:
        tvl_zbc += associated_address.value[0].account.data.parsed['info']['tokenAmount']['uiAmount']

print(tvl_sol)
print(tvl_zbc)
