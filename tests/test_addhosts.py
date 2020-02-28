from forms.hosts_forms.addhosts import AddHosts
import pytest

def test_is_valid_ip_address():
    assert AddHosts.is_valid_ip_address('192.168.5.5') == True
    assert AddHosts.is_valid_ip_address('192.168.5') == False
    assert AddHosts.is_valid_ip_address('192.168.5.5') == True
    assert AddHosts.is_valid_ip_address('2001:0db8:85a3:0000:0000:8a2e:0370:7334') == True
    assert AddHosts.is_valid_ip_address('2001:0db8:85a3:0000:0000:8a2e:0370:73342') == False

def test_is_valid_hostname():
    assert AddHosts.is_valid_hostname('valid.hostname') == True
    assert AddHosts.is_valid_hostname('inv@lid.hostname') == False
    assert AddHosts.is_valid_hostname('ValidHostname') == True