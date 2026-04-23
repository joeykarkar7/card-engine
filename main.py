from fastapi import FastAPI
import statistics
import random

app = FastAPI()

def comps():
    base = 100 + random.randint(0, 120)
    return [
        base + random.randint(-20, 20),
        base + random.randint(-15, 25),
        base + random.randint(-30, 10),
        base + random.randint(-10, 15),
        base + random.randint(-25, 30),
    ]

def trimmed(data):
    data = sorted(data)
    t = int(len(data) * 0.2)
    data = data[t: len(data)-t]
    return sum(data)/len(data)

def vol(data):
    if len(data) < 2:
        return 0
    return statistics.stdev(data)/statistics.mean(data)

@app.get("/comps")
def run(player: str, ask: float):

    c = comps()

    fair = trimmed(c)

    mis = (ask - fair) / fair

    v = vol(c)

    conf = (1 - min(v,1)) * 0.8

    edge = max(0, min(100, (-mis*100)*conf))

    verdict = "PASS"
    if edge >= 75:
        verdict = "STRONG BUY"
    elif edge >= 55:
        verdict = "BUY"
    elif edge >= 35:
        verdict = "WATCH"

    return {
        "player": player,
        "comps": c,
        "fair_value": fair,
        "ask": ask,
        "edge_score": edge,
        "verdict": verdict
    }
