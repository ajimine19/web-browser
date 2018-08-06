import simpleCache

def test_contains():
    myCache = simpleCache.simpleCache()
    myCache.updateCache("k", "100")
    assert myCache.__contains__("k") == True
    assert myCache.__contains__("x") == False
'''
def test_size():
    myCache = simpleCache.simpleCache()
    assert myCache.sizeOfCache() == 0
    myCache.updateCache("k", "100")
    assert myCache.sizeOfCache() == 1
'''
def test_makespace():
    myCache = simpleCache.simpleCache()
    myCache.updateCache("k", "100")
    myCache.makeSpace()
    assert myCache.sizeOfCache() == 0
    assert myCache.__contains__("k") == False

def test_update():
    myCache = simpleCache.simpleCache()
    myCache.updateCache("k", "100")
    assert myCache.__contains__("k") == True
    assert myCache.sizeOfCache() == 1
    myCache.updateCache("b", "200")
    myCache.updateCache("c", "300")
    assert myCache.sizeOfCache() == 3
    myCache.updateCache("a", "1")
    assert myCache.__contains__("a") == True
    assert myCache.__contains__("k") == False
    assert myCache.sizeOfCache() == 3
