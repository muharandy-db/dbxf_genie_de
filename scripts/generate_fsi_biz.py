#!/usr/bin/env python3
"""Generate the reduced, Indonesia-localized FSI (banking) dataset used by
TUTORIAL_FSI_SIMPLE.md.

Produces 3 denormalized CSV tables under data/fsi_biz/ for a single fictitious
bank ("Bank Nusantara Sejahtera"):

    banking_branches      (~200 rows)  - master data cabang
    banking_accounts      (~5000 rows) - rekening nasabah (branch_id FK)
    banking_transactions  (~12000 rows) - transaksi (account_id + branch_id FK)

Mirrors the pharma_biz reduction pattern: stdlib-only, deterministic, clean FKs.
Run:  python3 scripts/generate_fsi_biz.py
"""

import csv
import os
import random
from datetime import datetime, timedelta

random.seed(42)

BANK_NAME = "Bank Nusantara Sejahtera"

N_BRANCHES = 200
N_ACCOUNTS = 5000
N_TRANSACTIONS = 12000

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "data", "fsi_biz")

# (city, province, region) — mirrors the pharma_biz Indonesian geography
CITIES = [
    ("Jakarta", "DKI Jakarta", "Jawa"),
    ("Bandung", "Jawa Barat", "Jawa"),
    ("Bogor", "Jawa Barat", "Jawa"),
    ("Bekasi", "Jawa Barat", "Jawa"),
    ("Semarang", "Jawa Tengah", "Jawa"),
    ("Surakarta", "Jawa Tengah", "Jawa"),
    ("Yogyakarta", "DI Yogyakarta", "Jawa"),
    ("Surabaya", "Jawa Timur", "Jawa"),
    ("Malang", "Jawa Timur", "Jawa"),
    ("Tangerang", "Banten", "Jawa"),
    ("Serang", "Banten", "Jawa"),
    ("Denpasar", "Bali", "Bali Nusa Tenggara"),
    ("Mataram", "Nusa Tenggara Barat", "Bali Nusa Tenggara"),
    ("Kupang", "Nusa Tenggara Timur", "Bali Nusa Tenggara"),
    ("Medan", "Sumatera Utara", "Sumatera"),
    ("Pekanbaru", "Riau", "Sumatera"),
    ("Padang", "Sumatera Barat", "Sumatera"),
    ("Palembang", "Sumatera Selatan", "Sumatera"),
    ("Bandar Lampung", "Lampung", "Sumatera"),
    ("Batam", "Kepulauan Riau", "Sumatera"),
    ("Pontianak", "Kalimantan Barat", "Kalimantan"),
    ("Banjarmasin", "Kalimantan Selatan", "Kalimantan"),
    ("Balikpapan", "Kalimantan Timur", "Kalimantan"),
    ("Samarinda", "Kalimantan Timur", "Kalimantan"),
    ("Makassar", "Sulawesi Selatan", "Sulawesi"),
    ("Manado", "Sulawesi Utara", "Sulawesi"),
    ("Palu", "Sulawesi Tengah", "Sulawesi"),
    ("Kendari", "Sulawesi Tenggara", "Sulawesi"),
    ("Ambon", "Maluku", "Maluku Papua"),
    ("Jayapura", "Papua", "Maluku Papua"),
]

# Named areas used for the more prominent (utama) branches
AREAS = [
    "Kota Kasablanka", "Sudirman", "Thamrin", "Gatot Subroto", "Kuningan",
    "Cikini", "Menteng", "Kelapa Gading", "Pluit", "Alam Sutera",
    "Darmo", "Basuki Rahmat", "Dago", "Asia Afrika", "Malioboro",
    "Panakkukang", "Sam Ratulangi", "Diponegoro", "Ahmad Yani", "Gajah Mada",
]

BRANCH_TYPES = ["cabang_utama", "cabang_pembantu", "kantor_kas"]
BRANCH_TYPE_WEIGHTS = [0.15, 0.55, 0.30]
TIERS = ["bronze", "silver", "gold", "platinum"]
TIER_WEIGHTS = [0.35, 0.35, 0.20, 0.10]

FIRST_NAMES = [
    "Budi", "Siti", "Agus", "Dewi", "Andi", "Rina", "Joko", "Sri", "Ahmad",
    "Ayu", "Bambang", "Wati", "Eko", "Fitri", "Hendra", "Indah", "Rizki",
    "Nur", "Dedi", "Maya", "Slamet", "Lestari", "Yusuf", "Ratna", "Iwan",
    "Sari", "Fajar", "Putri", "Wahyu", "Kartika", "Rudi", "Endah", "Teguh",
    "Melati", "Arif", "Novi", "Doni", "Rahma", "Gunawan", "Yuni",
]
LAST_NAMES = [
    "Santoso", "Wijaya", "Kusuma", "Hidayat", "Nugroho", "Saputra", "Pratama",
    "Utami", "Halim", "Setiawan", "Wibowo", "Suryadi", "Maulana", "Anggraini",
    "Permana", "Puspita", "Firmansyah", "Handayani", "Gunawan", "Rahayu",
    "Susanto", "Kurniawan", "Hartono", "Cahyani", "Ramadhan", "Lestari",
    "Purnomo", "Wulandari", "Siregar", "Simanjuntak", "Nasution", "Tanuwijaya",
]

ACCOUNT_TYPES = ["tabungan", "giro", "deposito", "pinjaman"]
ACCOUNT_TYPE_WEIGHTS = [0.55, 0.15, 0.20, 0.10]
ACCOUNT_STATUS = ["aktif", "dorman", "ditutup"]
ACCOUNT_STATUS_WEIGHTS = [0.82, 0.13, 0.05]

TXN_TYPES = ["setoran", "tarik_tunai", "transfer", "pembayaran", "pembelian"]
TXN_TYPE_WEIGHTS = [0.20, 0.22, 0.28, 0.18, 0.12]
CHANNELS = ["teller", "atm", "mobile_banking", "internet_banking", "edc"]
CHANNEL_WEIGHTS = [0.12, 0.28, 0.38, 0.12, 0.10]
TXN_STATUS = ["berhasil", "gagal", "pending"]
TXN_STATUS_WEIGHTS = [0.94, 0.04, 0.02]

TXN_DESCRIPTIONS = {
    "setoran": ["Setoran tunai", "Setoran gaji", "Setoran cek"],
    "tarik_tunai": ["Penarikan tunai", "Tarik tunai"],
    "transfer": ["Transfer antar rekening", "Transfer antar bank", "Transfer BI-FAST"],
    "pembayaran": ["Pembayaran tagihan listrik", "Pembayaran BPJS",
                   "Pembayaran kartu kredit", "Pembayaran PDAM"],
    "pembelian": ["Pembelian pulsa", "Pembelian di merchant", "Pembelian e-commerce"],
}


def rand_date(start, end):
    delta = (end - start).days
    return start + timedelta(days=random.randint(0, delta))


def write_csv(path, header, rows):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)
    print(f"  wrote {len(rows):>6} rows -> {os.path.relpath(path, ROOT)}")


def gen_branches():
    header = ["branch_id", "branch_name", "branch_type", "bank_name", "city",
              "province", "region", "branch_code", "phone", "opened_date",
              "status", "tier"]
    rows = []
    start, end = datetime(2008, 1, 1), datetime(2024, 6, 30)
    for i in range(1, N_BRANCHES + 1):
        branch_id = f"BR-{i:04d}"
        city, province, region = random.choice(CITIES)
        btype = random.choices(BRANCH_TYPES, BRANCH_TYPE_WEIGHTS)[0]
        if btype == "cabang_utama":
            code_prefix = "KC"
        else:
            code_prefix = "KCP" if btype == "cabang_pembantu" else "KK"
        # In Jakarta, name the branch after a known area; elsewhere use the city.
        if city == "Jakarta":
            loc = random.choice(AREAS)
        else:
            loc = city
        branch_name = f"{BANK_NAME} {code_prefix} {loc}"
        branch_code = f"{code_prefix}-{random.randint(100000, 999999)}"
        phone = f"+62-{random.randint(21, 99)}-{random.randint(1000000, 9999999)}"
        opened = rand_date(start, end).strftime("%Y-%m-%d")
        status = random.choices(["aktif", "tutup"], [0.95, 0.05])[0]
        tier = random.choices(TIERS, TIER_WEIGHTS)[0]
        rows.append([branch_id, branch_name, btype, BANK_NAME, city, province,
                     region, branch_code, phone, opened, status, tier])
    return header, rows


def gen_accounts(branch_ids):
    header = ["account_id", "customer_name", "account_type", "account_number",
              "branch_id", "balance", "currency", "status", "interest_rate",
              "opened_date", "last_activity_date"]
    rows = []
    open_start, open_end = datetime(2015, 1, 1), datetime(2025, 8, 31)
    accounts = []  # (account_id, branch_id, opened_date, status)
    for i in range(N_ACCOUNTS):
        account_id = f"ACC-{600001 + i}"
        name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
        atype = random.choices(ACCOUNT_TYPES, ACCOUNT_TYPE_WEIGHTS)[0]
        acct_no = "-".join(f"{random.randint(1000, 9999)}" for _ in range(4))
        branch_id = random.choice(branch_ids)
        if atype == "deposito":
            balance = round(random.uniform(25_000_000, 1_500_000_000), 2)
            rate = round(random.uniform(0.03, 0.06), 4)
        elif atype == "giro":
            balance = round(random.uniform(5_000_000, 800_000_000), 2)
            rate = round(random.uniform(0.001, 0.015), 4)
        elif atype == "pinjaman":
            balance = round(-random.uniform(10_000_000, 900_000_000), 2)
            rate = round(random.uniform(0.08, 0.18), 4)
        else:  # tabungan
            balance = round(random.uniform(100_000, 250_000_000), 2)
            rate = round(random.uniform(0.005, 0.025), 4)
        status = random.choices(ACCOUNT_STATUS, ACCOUNT_STATUS_WEIGHTS)[0]
        opened_dt = rand_date(open_start, open_end)
        last_act = rand_date(opened_dt, datetime(2025, 9, 22))
        rows.append([account_id, name, atype, acct_no, branch_id,
                     f"{balance:.2f}", "IDR", status, f"{rate:.4f}",
                     opened_dt.strftime("%Y-%m-%d"),
                     last_act.strftime("%Y-%m-%d")])
        accounts.append((account_id, branch_id, opened_dt, status))
    return header, rows, accounts


def gen_transactions(accounts):
    header = ["transaction_id", "account_id", "branch_id", "transaction_type",
              "channel", "amount", "balance_after", "description",
              "transaction_date", "status", "created_at"]
    rows = []
    # Only transact on non-closed accounts
    active = [a for a in accounts if a[3] != "ditutup"] or accounts
    end_dt = datetime(2026, 3, 31)
    for i in range(1, N_TRANSACTIONS + 1):
        txn_id = f"TXN-{i:07d}"
        account_id, branch_id, opened_dt, _ = random.choice(active)
        ttype = random.choices(TXN_TYPES, TXN_TYPE_WEIGHTS)[0]
        channel = random.choices(CHANNELS, CHANNEL_WEIGHTS)[0]
        # ATM channel skews to cash operations
        if channel == "atm" and ttype in ("pembayaran", "pembelian"):
            ttype = random.choice(["tarik_tunai", "transfer"])
        if ttype in ("setoran", "transfer"):
            amount = round(random.uniform(50_000, 50_000_000), 2)
        elif ttype == "tarik_tunai":
            amount = round(random.uniform(50_000, 5_000_000), 2)
        else:
            amount = round(random.uniform(20_000, 10_000_000), 2)
        balance_after = round(random.uniform(100_000, 300_000_000), 2)
        desc = random.choice(TXN_DESCRIPTIONS[ttype])
        tx_start = max(opened_dt, datetime(2024, 1, 1))
        if tx_start > end_dt:
            tx_start = end_dt - timedelta(days=1)
        tx_dt = rand_date(tx_start, end_dt)
        created = tx_dt.replace(hour=random.randint(0, 23),
                                minute=random.randint(0, 59),
                                second=random.randint(0, 59))
        status = random.choices(TXN_STATUS, TXN_STATUS_WEIGHTS)[0]
        rows.append([txn_id, account_id, branch_id, ttype, channel,
                     f"{amount:.2f}", f"{balance_after:.2f}", desc,
                     tx_dt.strftime("%Y-%m-%d"), status,
                     created.strftime("%Y-%m-%d %H:%M:%S")])
    return header, rows


def main():
    print(f"Generating fsi_biz dataset for '{BANK_NAME}' -> {OUT_DIR}")
    b_header, b_rows = gen_branches()
    write_csv(os.path.join(OUT_DIR, "banking_branches", "banking_branches.csv"),
              b_header, b_rows)

    branch_ids = [r[0] for r in b_rows if r[10] == "aktif"]  # open branches only
    a_header, a_rows, accounts = gen_accounts(branch_ids)
    write_csv(os.path.join(OUT_DIR, "banking_accounts", "banking_accounts.csv"),
              a_header, a_rows)

    t_header, t_rows = gen_transactions(accounts)
    write_csv(os.path.join(OUT_DIR, "banking_transactions",
                           "banking_transactions.csv"), t_header, t_rows)
    print("Done.")


if __name__ == "__main__":
    main()
