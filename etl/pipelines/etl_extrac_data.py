import os,shutil
import pandas as pd
from sqlalchemy import create_engine,text

# Configuración
DATA_DIR = 'data'
PROCESSED_DIR = os.path.join(DATA_DIR, 'procesados')
DB_URL = 'postgresql://postgres:123@localhost:5432/etl_db'

# Asegurar carpetas
os.makedirs(PROCESSED_DIR, exist_ok=True)

def get_pending_files():
    #Detecta archivos CSV pendientes en la carpeta data/
    return [f for f in os.listdir(DATA_DIR)
            if f.endswith('.csv') and os.path.isfile(os.path.join(DATA_DIR, f))]

def extract_data(file_path: str) -> pd.DataFrame:     
    return pd.read_csv(file_path)

def clear_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.dropna(how='all')      

    df['id'] = df['id'].astype(str).str.strip().replace('', pd.NA)
    df['company_id'] = df['company_id'].astype(str).str.strip().replace('', pd.NA)
    df['name'] = df['name'].astype(str).str.strip().replace('', pd.NA)      
    df['amount'] = df['amount'].astype(str).str.strip().replace('', pd.NA)  
    df['status'] = df['status'].astype(str).str.strip().replace('', pd.NA)  
    df['created_at'] = df['created_at'].astype(str).str.strip().replace('', pd.NA)  
    df['paid_at'] = df['paid_at'].astype(str).str.strip().replace('', pd.NA)  

    df = df[df['id'].astype(str).str.lower() != 'nan']
    df = df[df['company_id'].astype(str).str.lower() != 'nan']
    df = df[df['name'].astype(str).str.lower() != 'nan']
    df = df[df['amount'].astype(str).str.lower() != 'nan']
    df = df[df['status'].astype(str).str.lower() != 'nan']
    df = df[df['created_at'].astype(str).str.lower() != 'nan']    
    df = df[df['paid_at'].astype(str).str.lower() != 'nan']    

    #df = df.drop(columns=['paid_at'], errors='ignore')

    return df

def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    #Transforma los datos para cumplir con el esquema charges
    df['amount'] = df['amount'].astype(float).round(2)
    df['created_at'] = df['created_at'].str.strip()    
    df['status'] = df['status'].str.lower().str.strip()
    df['name'] = df['name'].str.strip()

    df = df.rename(columns={'paid_at': 'updated_at'})
    df['updated_at'] = df['updated_at'].str.strip()

    return df    

def load_data(df: pd.DataFrame):
    #Carga los datos transformados en BD
    engine = create_engine(DB_URL)

    # Cargar tabla companies
    df['name'] = df['name'].str.strip().str.lower()
    companies = df[['company_id', 'name']].drop_duplicates(subset='company_id')

    #obtener Ids existentes
    with engine.connect() as conn:
        existing_ids = conn.execute(text("SELECT company_id FROM etl.companies")).fetchall()
        existing_ids = set(row[0] for row in existing_ids)
    
    #filtrar nuevos
    new_companies = companies[~companies['company_id'].isin(existing_ids)]

    #insertar solo los nuevos
    if not new_companies.empty:
        companies.to_sql('companies', engine, schema='etl', if_exists='append', index=False)

    # Cargar tabla charges
    charges = df[['id', 'company_id', 'amount', 'status', 'created_at', 'updated_at']]
    charges.to_sql('charges', engine, schema='etl', if_exists='append', index=False)

def move_to_processed(file_name: str):
    #Mueve el archivo procesado a la subcarpeta procesados/
    src = os.path.join(DATA_DIR, file_name)
    dst = os.path.join(PROCESSED_DIR, file_name)
    
    shutil.move(src, dst)        

def run_batch_etl():
    #Ejecuta el proceso ETL para todos los archivos pendientes
    pending_files = get_pending_files()

    if not pending_files:
        print("No hay archivos pendientes...")
        return

    for file_name in pending_files:
        try:
            file_path = os.path.join(DATA_DIR, file_name)
            df = extract_data(file_path)
            df = clear_data(df)
            df = transform_data(df)
            load_data(df)
            move_to_processed(file_name)
        except Exception as e:
            print(f"Error procesando {file_name}: {e}")

if __name__ == '__main__':
    run_batch_etl()
