
import gspread
from google.oauth2.service_account import Credentials

# ================= AUTH ================= #

def authenticate():
    print("🔐 Authenticating with Google...")

    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = Credentials.from_service_account_file("key.json", scopes=scopes)
    client = gspread.authorize(creds)

    print("✅ Authentication successful!\n")
    return client


# ================= SYNC FUNCTION ================= #

def sync_sheet(client, source_id, source_tab, target_id, target_tab):

    try:
        print(f"🔄 Syncing '{source_tab}' → '{target_tab}'")

        source = client.open_by_key(source_id).worksheet(source_tab)
        target = client.open_by_key(target_id).worksheet(target_tab)

        data = source.get_all_values()

        if not data:
            print("⚠️ Source sheet is empty. Skipping...\n")
            return

        # Clear target
        target.clear()

        # Upload in ONE batch (fast)
        target.update(values=data, range_name="A1")

        print(f"✅ SUCCESS: {source_tab} synced!\n")

    except Exception as e:
        print(f"❌ ERROR syncing {source_tab}: {str(e)}\n")
        raise   # VERY IMPORTANT → shows error in GitHub



def run_all_jobs():

    client = authenticate()

    jobs = [

    ("1kAMIsRtTArl89vUjfewOxjmVZ7DgTUAepckLeQzD0h4", "POReport6098192864", "1yoFK7BQtCv-S2Wg4cZvmFM13ENtShcF7dRx7UQ5nag8", "Sheet1")
]

    print("🚀 Starting all sheet sync jobs...\n")

    for job in jobs:
        sync_sheet(client, *job)

    print("🎉 ALL SHEETS SYNCED SUCCESSFULLY!")



if __name__ == "__main__":
    run_all_jobs()
