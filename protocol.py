from selenium import webdriver

def tor():

    host = 'localhost'
    port = 9050

    socks = webdriver.FirefoxProfile()

    socks.set_preference("network.proxy.type", 1)
    socks.set_preference("network.proxy.socks", host)
    socks.set_preference("network.proxy.socks_port", port)
    socks.set_preference("network.proxy.socks_remote_dns", True)

    socks.update_preferences()
    
    return socks

def i2p():

    host = 'localhost'
    port = 4444

    garlic = webdriver.FirefoxProfile()

    garlic.set_preference("network.proxy.type", 1)
    garlic.set_preference("network.proxy.http", host)
    garlic.set_preference("network.proxy.http_port", port)
    garlic.set_preference("network.proxy.ssl", host)
    garlic.set_preference("network.proxy.ssl_port", port)
    
    garlic.update_preferences()
    
    return garlic