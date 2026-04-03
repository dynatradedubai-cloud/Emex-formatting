import streamlit as st
import pandas as pd
import re

# ==============================
# Mapping dictionaries (same)
# ==============================
oem_brand_map = {
    "ABC": "AIRCOMFORT", "ABG": "AIRTECH", "ACK": "ARCEK", "AE": "AE", "AFR": "Ayfar", "AFT": "AIRKRAFT",
    "AHU": "ALHU", "ALP": "ALP", "AM": "Allmakes 4x4", "AMK": "AMK", "ANC": "AD", "ARN": "ARNOTT",
    "ASO": "ASSO", "ATE": "ATE", "ATP": "ATP", "BBO": "BREMBO", "BER": "BERAL", "BF": "BGF", "BHR": "BEHR",
    "BHT": "BEHR", "BLN": "BILSTEIN", "BLP": "BLUE PRINT", "BMI": "BREMI", "BOG": "BOGE", "BOR": "BORGWARNER",
    "BPW": "BPW", "BRU": "BERU", "BSH": "BOSCH", "CEI": "CEI", "CFW": "CORTECO", "COH": "COHLINE",
    "CON": "CONTITECH", "COS": "COSIBO", "CPN": "CHAMPION", "CSZ": "Sanz", "DIN": "Dinex", "DPH": "DPH",
    "DPI": "DELPHI", "DPO": "DEPO", "DSO": "DENSO", "EBI": "EURORICAMBI", "EBS": "EBS", "EKP": "EKIP",
    "ELF": "ELF", "ELR": "ELRING", "ENO": "ENOC", "ENX": "EURONAX", "ETG": "ETG", "ETP": "ETP",
    "ETR": "EUROTRADING", "FAG": "FAG", "FAS": "SACHS", "FBI": "FEBI", "FER": "FERODO", "FLG": "FLAG",
    "FLT": "FLEETGUARD", "FM": "FEDERAL MOGUL", "FNO": "Sampa", "FRA": "ITAL Express", "FSA": "FERSA",
    "FTE": "FTE", "GBA": "GEBA", "GEN": "GEN", "GER": "DT Spare Parts", "GK": "GKN", "GLY": "GLYCO",
    "GMO": "GERMO", "GRT": "GARRETT", "GST": "GST", "GTS": "GATES", "GTZ": "GOETZE", "HCC": "HC-CARGO",
    "HDX": "HALDEX", "HEL": "HELLA", "HLT": "HOLSET", "HST": "HENGST", "HUT": "Hutchinson", "HYD": "Heyd",
    "INA": "INA", "INP": "EKIP", "IWS": "IWIS", "JPG": "JP GROUP", "JST": "JOST", "KAT": "G+M KAT",
    "KAV": "KAHVECI OTOMOTIV", "KKK": "KKK", "KM": "KM AUTO TECHNIK", "KME": "KME", "KNG": "Kongsberg Automotive",
    "KNR": "Knorr-Bremse", "KS": "Kolbenschmidt", "KST": "TRW", "KZR": "KACMAZLAR", "LAS": "LASO",
    "LEM": "LEMFORDER", "LMA": "Lema", "LUK": "LUK", "MAH": "MAHLE", "MAN": "MANN", "MEY": "MEYLE",
    "MHA": "MAHLE", "MHB": "MAHLE", "MHF": "MAHLE", "MHT": "MAHLE", "MHV": "MAHLE", "MIB": "MIBA",
    "MK": "MRK", "MNK": "MONARK", "MOB": "MOBIl", "MRO": "MONROE", "MXN": "MAXION", "MXP": "MAXPART",
    "NSN": "Nissens", "NUR": "NURAL", "OE": "ORIGINAL GENUINE", "OPM": "OPTIMUM", "OSR": "Osram",
    "PB": "PAUL BERNHARDT", "PBG": "PIERBURG", "PBK": "Banks Power", "PE": "PE Automotive", "PEN": "PENTOSIN",
    "PRO": "PROVIA", "RNZ": "Victor Reinz", "SAF": "SAF-Holland", "SAU": "Sauer", "SBO": "Sabo",
    "SCH": "SCHNEIDER", "SDN": "SANDEN", "SIM": "SIMER", "SKF": "SKF", "SLP": "SLP", "SM": "SCHOTTLE",
    "SNP": "SNP", "SPA": "Sampa", "SRB": "SRB", "STB": "STABILUS", "SWF": "SWF", "SWG": "SWAG",
    "TAS": "TAS", "TDR": "TOP DRIVE", "TEM": "TEMAC", "TEX": "Textar", "TFA": "TRIFA", "TLX": "TRILEX",
    "TNK": "TruckTechnic", "TRW": "TRW", "TRX": "G+M KAT", "TTC": "TRUCKTEC", "TWN": "TW", "VAL": "VALEO",
    "VDO": "VDO", "VKO": "VAICO", "WAB": "WABCO", "WEB": "WEBER", "ZF": "ZF Parts", "ZXL": "JapanParts"
}

vehicle_map = {
    "HB": ("BMW", "CAR"), "HW": ("VOLKSWAGEN", "CAR"), "HR": ("RENAULT", "TRUCK"),
    "HD": ("DAIMLER AG", "CAR"), "HV": ("VOLVO", "TRUCK"), "HN": ("MAN", "TRUCK"),
    "HM": ("DAIMLER AG", "TRUCK"), "HS": ("SCANIA", "TRUCK"), "HC": ("PORSCHE", "CAR"),
    "HT": ("TRAILER", "TRUCK"), "HI": ("IVECO", "TRUCK"), "HF": ("DAF", "TRUCK"),
    "HL": ("LAND ROVER", "CAR"), "HZ": ("MISC", "TRUCK"), "JC": ("JAPANPARTS", "CAR"),
    "HE": ("DAIMLER AG", "TRUCK"), "HY": ("JAGUAR", "CAR"), "HO": ("OPEL", "CAR"),
    "HU": ("RENAULT", "CAR"), "HX": ("DEUTZ", "TRUCK"), "HK": ("VOLVO", "CAR"),
    "CC": ("EQUIPMENTS", "TRUCK"), "HP": ("PEUGEOT", "CAR"), "HA": ("AMERICAN PARTS", "CAR"),
    "HJ": ("JEEP", "CAR"), "HH": ("HINO", "TRUCK"), "JV": ("MISC", "TRUCK"),
    "HQ": ("NISSAN UD", "TRUCK"), "HG": ("TATA", "TRUCK")
}

banned_keywords = [
    "#N/A","MXP CAR CATALOGUE","MERCEDES CATALOGUE","MXP CATALOGUE HV HS HN HI HT",
    "MAXPART FOLDER","MAXPART L T-SHIRT","MAXPART POLY BAG SMALL 30 X40",
    "MAXPART XL T-SHIRT","MAXPART XXL T-SHIRT","MAXPART WRIST WATCH",
    "MAXPART POLY BAG BIG FOR","NO WARRANTY","Expired","0009823108/26(EXPIRED)",
    "EXPIRED","MAXPART  XXL  T-SHIRT","MISC","EQUIPMENTS"
]

banned_types = ["AAL","AIC","ATK","BEL","CLA","EMR","EUR","GF","ICE","MRR","OTO","RCD","RFG","SAM","ST","TZR","UGR"]

# ==============================
# UI
# ==============================
st.title("EMEX Dump Formatter (Optimized 🚀)")

uploaded_file = st.file_uploader("Upload Dump Excel File", type=["xlsx"])

if uploaded_file:

    df = pd.read_excel(uploaded_file, engine="openpyxl")

    keep_cols = ["PMPDGP","PMMANF","PMPNO","PMMFPT","PMPNAM","SOH_QTY","LC","R2RATE"]
    df = df[[col for col in keep_cols if col in df.columns]]

    # ==============================
    # Transformations
    # ==============================
    df["Comb"] = df["PMPNO"].astype(str) + df["PMMANF"].astype(str)
    df["OEM Brand"] = df["PMMANF"].map(oem_brand_map)
    df["Manufacturer No."] = df["PMMFPT"]
    df["Unit Price in AED"] = ""
    df["Stock"] = df["SOH_QTY"].clip(upper=30000)
    df["Pack"] = ""
    df["Part Description"] = df["PMPNAM"]
    df["Vehicle"] = df["PMPDGP"].map(lambda x: vehicle_map.get(x, ("",""))[0])
    df["Original Part No."] = df["PMPNO"]
    df["WEIGHT"] = ""
    df["Type"] = df["PMMANF"]
    df["Car/Truck"] = df["PMPDGP"].map(lambda x: vehicle_map.get(x, ("",""))[1])

    # Replace ORIGINAL GENUINE
    df["OEM Brand"] = df["OEM Brand"].mask(
        df["OEM Brand"] == "ORIGINAL GENUINE",
        df["Vehicle"]
    )

    # ==============================
    # 🔥 FAST FILTER (VECTORISED)
    # ==============================

    # Combine all banned keywords into ONE regex
    pattern = "|".join(map(re.escape, banned_keywords))

    mask = df.astype(str).apply(
        lambda col: col.str.contains(pattern, case=False, na=False)
    )

    df = df[~mask.any(axis=1)]

    # Other filters
    df = df[~df["Type"].isin(banned_types)]
    df = df[~df["PMPDGP"].astype(str).str.contains("VW", case=False, na=False)]

    # ==============================
    # Final column order
    # ==============================
    df = df[[
        "Comb","OEM Brand","Manufacturer No.","Unit Price in AED","Stock","Pack",
        "Part Description","Vehicle","Original Part No.","WEIGHT","Type","Car/Truck",
        "LC","R2RATE","PMPDGP"
    ]]

    # ==============================
    # Output
    # ==============================
    df.to_excel("Stock list.xlsx", index=False)

    st.success(f"✅ Done! {len(df)} rows after cleaning")

    with open("Stock list.xlsx", "rb") as f:
        st.download_button("Download Cleaned File", f, file_name="Stock list.xlsx")
