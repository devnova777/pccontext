from pycardano import Address

from pccontext import AddressInfo


def test_address_info_model(fake_payment_address):
    address = Address.from_primitive(fake_payment_address)
    address_info = AddressInfo(address=address)
    assert address_info is not None
