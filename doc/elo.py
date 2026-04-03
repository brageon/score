import os, sys, time, math, requests, threading
from concurrent.futures import ThreadPoolExecutor, as_completed

# ---------------- CONFIG ----------------
base_url = "https://api.api-tennis.com/tennis/"
api_key = os.getenv("API_TENNIS_KEY")
event_date = "2025-10-11"
timer_running = True

player_cache = {}
odds_cache = {}

# ---------------- TIMER ----------------
def live_timer():
    start = time.time()
    while timer_running:
        elapsed = time.time() - start
        mins, secs = divmod(int(elapsed), 60)
        sys.stdout.write(f"\rElapsed Time: {mins:02d}:{secs:02d}")
        sys.stdout.flush()
        time.sleep(1)
    print()


# ---------------- API CALLS ----------------
def get_fixtures(date_start=event_date, date_stop=event_date):
    url = f"{base_url}?method=get_fixtures&APIkey={api_key}&date_start={date_start}&date_stop={date_stop}"
    resp = requests.get(url).json()
    return resp.get("result", [])

def fetch_player(player_key):
    if player_key in player_cache:
        return player_cache[player_key]
    url = f"{base_url}?method=get_players&player_key={player_key}&APIkey={api_key}"
    try:
        resp = requests.get(url).json()
        result = resp.get("result", [])
        if result:
            player_cache[player_key] = result[0]
            return result[0]
    except Exception as e:
        print(f"Error fetching player {player_key}: {e}")
    return None

def fetch_odds(event_key):
    if not event_key:
        return {}
    if event_key in odds_cache:
        return odds_cache[event_key]
    url = f"{base_url}?method=get_odds&match_key={event_key}&APIkey={api_key}"
    try:
        resp = requests.get(url).json()
        match_data = resp.get("result", {}).get(str(event_key), {})
        home_away = match_data.get("Home/Away", {})
        odds = {}
        if home_away:
            home_bk = home_away.get("Home", {})
            away_bk = home_away.get("Away", {})
            if home_bk and away_bk:
                first_bk = list(home_bk.keys())[0]
                odds = {"home": home_bk.get(first_bk), "away": away_bk.get(first_bk)}
        odds_cache[event_key] = odds
        return odds
    except Exception as e:
        print(f"Error fetching odds for {event_key}: {e}")
        odds_cache[event_key] = {}
        return {}


# ---------------- CONCURRENT FETCH ----------------
def fetch_players_concurrent(player_keys):
    if not player_keys:
        return
    max_workers = min(32, max(4, len(player_keys)//2))
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(fetch_player, pk): pk for pk in player_keys}
        for f in as_completed(futures):
            pass  # results auto-populate player_cache

def fetch_odds_concurrent(match_keys):
    if not match_keys:
        return
    max_workers = min(32, max(4, len(match_keys)//2))
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(fetch_odds, mk): mk for mk in match_keys}
        for f in as_completed(futures):
            pass  # results auto-populate odds_cache


# ---------------- PROCESSING ----------------
def sum_player_record(player_data):
    wins = loss = 0
    for row in player_data.get("stats", []):
        wins += int(row.get("matches_won", 0) or 0)
        loss += int(row.get("matches_lost", 0) or 0)
    total = wins + loss
    trust = abs(wins - loss)
    p = (wins + 1) / (total + 2)
    dc = math.sqrt(p * (1 - p) * total)
    win_rate = (wins / total * 100) if total > 0 else 0
    effect = abs(total - trust) / (total + trust + 1)
    raw = (p - 0.5) * dc
    return {
        "player": player_data.get("player_full_name"),
        "country": player_data.get("player_country"),
        "birth": player_data.get("player_bday"),
        "win": f"{win_rate:.1f}%",
        "match": total,
        "total": round(effect, 3),
        "curve": round(math.tanh(raw), 3) }

def extract_h2h(fixtures):
    """DC HN CH NC CN [5,6,4,1] [1,2,3] win break"""
    evaluated = []

    # Gather all unique player keys and match keys
    player_keys = set()
    match_keys = set()
    for event in fixtures:
        if event.get("first_player_key"):
            player_keys.add(event["first_player_key"])
        if event.get("second_player_key"):
            player_keys.add(event["second_player_key"])
        if event.get("event_key"):
            match_keys.add(event["event_key"])

    # Fetch all players and odds in parallel
    fetch_players_concurrent(player_keys)
    fetch_odds_concurrent(match_keys)

    for event in fixtures:
        a = player_cache.get(event.get("first_player_key"))
        b = player_cache.get(event.get("second_player_key"))
        c = odds_cache.get(event.get("event_key"), {})
        if not a or not b or not c:
            continue

        waa, war = sum_player_record(a), sum_player_record(b)
        wa = float(waa["win"].replace("%", ""))
        wb = float(war["win"].replace("%", ""))
        wc, wd = waa["curve"], war["curve"]
        we, wf = waa["total"], war["total"]
        mid, nid = abs(wc - we), abs(wd - wf)
        wow, wos = abs(wa - wb), abs(wc - wd)

        if wa < 56 or wb < 56 or wow < 3 or wow > 7:
            continue

        me = int(waa["birth"].split(".")[2])
        mf = int(war["birth"].split(".")[2])
        mc, md = waa["match"], war["match"]
        tan, dan = me - mf, mc - md
        vin, iva = mc / md, md / mc
        wii = vin if vin > iva else iva
        est = "Old" if me < mf else "Kid"
        mes = "Old" if mc > md else "Kid"

        if dan == 0 or tan == 0:
            dan, tan = 1, 1
        if est == mes:
            ant = ((abs(dan) / abs(tan)) / 50) - 1
        else:
            ant = ((abs(dan) / -abs(tan)) / 50) + 1

        mma = round(wii * ant, 2)
        tao = "Am" if abs(mid - mma) < abs(nid - mma) else "Bm"
        oak = "Aw" if abs(mid - mma) < abs(nid - mma) else "Bw"
        tao = tao if mma > 0 else oak
        if mma > 1.1 or mma < -1.1:
            continue

        evaluated.append({
            "tour": event.get("tournament_name"),
            "time": event.get("event_time"),
            "gap": round(wow, 2),
            "kin": round(mma, 2),
            "pal": waa,
            "pub": war,
            "hom": tao,
            "mate": c })

        if len(evaluated) >= 10:
            break

    return evaluated


# ---------------- RUN SCRIPT ----------------
if __name__ == "__main__":
    timer_running = True
    t = threading.Thread(target=live_timer)
    t.start()

    fixtures = get_fixtures()
    h2h_events = extract_h2h(fixtures)
    news = len(h2h_events)
    h2h_events.sort(key=lambda x: x["gap"])
    print(f"\nPrecomputed {news} ranked matches.")

    budget = int(0.65 * news) / news
    budget = budget if not news %2 else news * 0.65
    kely, crit = int(budget * 80), int(budget * 90)
    kit = kely if not news %2 else crit
    kit = kit if kit < 100 else kit / 10
    print(f"Stake: {int(kit)}% total.")

    for idx, zen in enumerate(h2h_events, 1):
        print(f"\n--- Fixture {idx} ---\n")
        print(f"Odds: {zen['mate']}")
        print(f"Tour: {zen['tour']}")
        print(f"Time: {zen['time']}")
        print(f"Rate: {zen['kin']}")
        print(f"Pick: {zen['hom']}")

        print("\nPlayer A:")
        for k, v in zen['pal'].items():
            print(f"{k}: {v}")

        print("\nPlayer B:")
        for k, v in zen['pub'].items():
            print(f"{k}: {v}")

    timer_running = False
    t.join()

    print("Script finished.")
