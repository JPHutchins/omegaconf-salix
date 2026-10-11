import copy
import pickle
import sys
import timeit
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from omegaconf import OmegaConf

@dataclass
class User:
    name: str = "bond"
    age: int = 7

@dataclass
class Server:
    host: str = "localhost"
    port: int = 8080
    users: Optional[List[User]] = None
    tags: Optional[Dict[str, str]] = None

NESTED = {"a": 1, "b": {"c": [1, 2, 3], "d": {"e": "f"}}, "x": "${missing:}"}

def bench(label, stmt, number):
    timer = timeit.Timer(stmt, globals=globals())
    total = timer.timeit(number=number)
    print(f"{label:28s} {total/number*1e6:10.1f} us/iter")
    return total / number

cfg = OmegaConf.create(NESTED)
srv = OmegaConf.structured(Server)
large = OmegaConf.create({"k%d" % i: {"v": [i] * 10} for i in range(200)})

print(f"python {sys.version.split()[0]}  omegaconf {OmegaConf.__module__}")
results = {}
results["create(nested dict)"] = bench("create(nested dict)", "OmegaConf.create(NESTED)", 2000)
results["create(200-key dict)"] = bench("create(200-key dict)", "OmegaConf.create({'k%d' % i: {'v': [i] * 10} for i in range(200)})", 200)
results["structured(dataclass)"] = bench("structured(dataclass)", "OmegaConf.structured(Server)", 2000)
results["to_container(200-key)"] = bench("to_container(200-key)", "OmegaConf.to_container(large)", 500)
results["deepcopy(config)"] = bench("deepcopy(config)", "copy.deepcopy(cfg)", 2000)
results["pickle round-trip"] = bench("pickle round-trip", "pickle.loads(pickle.dumps(cfg))", 2000)
