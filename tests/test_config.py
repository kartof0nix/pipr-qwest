from ..src.common.config import Config, Setting, clearAllSettings
import pytest


def test_config():
    a = Config("pytest_b", {
        "colors": "bop",
        "time" : 12
    })
    assert ( a['time']  == 12)
    a['time']=15
    assert ( a['time']  == 15)
    a.reset()
    assert ( a['time']  == 12)
    
def test_saving():
    clearAllSettings()
    a = Config("pytest_saving", {
        "speed" : 12
    })
    assert(a['speed'] == 12)
    a['speed']=16
    a.save_to_file()
    del a
    b = Config("pytest_saving", {
        "speed" : 12
    })
    assert(b['speed'] == 16)

def test_settings():
    
    a = Setting(
    "pytest_a",
    {
        "fps": 60,
        "volume":69
    }, {
        "fps" : {
            "value_type" : "selectable",
            "selectable" : [15, 30, 60, 144]
        },
        "volume" : {
            "type" : type(1),
            "value_type" : "bound",
            "min_val" : 0,
            "max_val" : 100
        }
    })   
    assert(a['fps'] == 60) 
    with pytest.raises(TypeError) as e:
        a['fps'] = "44"
    with pytest.raises(TypeError) as e:
        a['volume'] = "44"
    with pytest.raises(ValueError) as e:
        a['fps'] = 42
    with pytest.raises(ValueError) as e:
        a['volume'] = 101
    a['fps'] = 144
    a['volume'] = 11
     
        
    assert(a['fps'] == 144) 
    assert(a['volume'] == 11) 
