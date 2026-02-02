from circle.web3 import utils

def gen_entity_secret():
    utils.generate_entity_secret()

def regi_entity():
    api_key = "TEST_API_KEY:bad55294b4f94e8167e415c6b541eafc:873323c074b4acb46e951314109badc5"
    entity_secret = "4e294671e493a7e5d8668365746831bfb2aef84c5d58e17bca6955dfb70bce1d"
    result = utils.register_entity_secret_ciphertext(
    api_key=api_key,
    entity_secret=entity_secret,
    recoveryFileDownloadPath='')

    print(result)

def main():
    #gen_entity_secret()
    regi_entity()

if __name__ == "__main__":
    main()
