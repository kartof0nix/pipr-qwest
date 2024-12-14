from ..src.common.config import Config, Setting
import pytest


def test_config():
    a = Config({
        "colors": "bop",
        "time" : 12
    })
    assert ( a['time']  == 12)
    a['time']=15
    assert ( a['time']  == 15)

def test_settings():
    a = Setting(
    {
        "fps": 60,
        "volume":69
    }, {
        "fps" : {
            "value_type" : "choice",
            "choice" : [15, 30, 60, 144]
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
