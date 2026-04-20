import json
import os
import sys
from datetime import datetime, timezone

import requests

API = "https://apis.datos.gob.ar/series/api/series/"

SERIES_IDS = {
    "ng_nac": "145.3_INGNACNAL_DICI_M_15",
    "ng_gba": "145.3_INGGBAGBA_DICI_M_10",
    "ng_pam": "145.3_INGPAMANA_DICI_M_15",
    "ng_nea": "145.3_INGNEANEA_DICI_M_10",
    "ng_noa": "145.3_INGNOANOA_DICI_M_10",
    "ng_cuy": "145.3_INGCUYUYO_DICI_M_11",
    "ng_pat": "145.3_INGPATNIA_DICI_M_16",
    "cap_ali": "146.3_IALIMENNAL_DICI_M_45",
    "cap_beb": "146.3_IBEBIDANAL_DICI_M_39",
    "cap_ves": "146.3_IPRENDANAL_DICI_M_35",
    "cap_viv": "146.3_IVIVIENNAL_DICI_M_52",
    "cap_equ": "146.3_IEQUIPANAL_DICI_M_46",
    "cap_sal": "146.3_ISALUDNAL_DICI_M_18",
    "cap_tra": "146.3_ITRANSPNAL_DICI_M_23",
    "cap_com": "146.3_ICOMUNINAL_DICI_M_27",
    "cap_rec": "146.3_IRECREANAL_DICI_M_31",
    "cap_edu": "146.3_IEDUCACNAL_DICI_M_22",
    "cap_res": "146.3_IRESTAUNAL_DICI_M_33",
    "cap_bsv": "146.3_IBIENESNAL_DICI_M_36",
    "cat_ng":  "148.3_INIVELNAL_DICI_M_26",
    "cat_nuc": "148.3_INUCLEONAL_DICI_M_19",
    "cat_est": "148.3_IESTACINAL_DICI_M_25",
    "cat_reg": "148.3_IREGULANAL_DICI_M_22",
}

GROUPS = {
    "regiones":  ["ng_nac", "ng_gba", "ng_pam", "ng_nea", "ng_noa", "ng_cuy", "ng_pat"],
    "capitulos": ["cap_ali", "cap_beb", "cap_ves", "cap_viv", "cap_equ", "cap_sal",
                  "cap_tra", "cap_com", "cap_rec", "cap_edu", "cap_res", "cap_bsv"],
    "categorias": ["cat_ng", "cat_nuc", "cat_est", "cat_reg"],
}

def fetch_group(keys):
    ids = ",".join(SERIES_IDS[k] for k in keys)
    url = f"{API}?ids={ids}&format=json&limit=300"
    resp = requests.get(url, timeout=30, headers={"User-Agent": "ipc-dashboard/1.0"})
    resp.raise_for_status()
    payload = resp.json()
    rows = payload["data"]
    dates  = [str(row[0]) for row in rows]
    values = [[row[i + 1] for row in rows] for i in range(len(keys))]
    return {"dates": dates, "values": values}

def main():
    output = {"updated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}
    reg_data = fetch_group(GROUPS["regiones"])
    output["resumen"] = {"dates": reg_data["dates"], "values": reg_data["values"][0]}
    output["regiones"] = reg_data
    for group in ("capitulos", "categorias"):
        print(f"  Fetching {group}...")
        output[group] = fetch_group(GROUPS[group])
    os.makedirs("data", exist_ok=True)
    with open(os.path.join("data", "ipc.json"), "w", encoding="utf-8") as f:
        json.dump(output, f, separators=(",", ":"), ensure_ascii=False)
    print(f"OK — {len(output['resumen']['dates'])} períodos guardados")

if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
