import argparse

import joblib
import pandas as pd
from haversine import haversine, Unit
from sklearn.preprocessing import LabelEncoder


def preprocess_data(group_folder, file, preprocess_dsource=False):
    separator = '\t'
    base_folder = 'data'

    dsource_file = f"{base_folder}/donnees_sources"
    dtarget_file = f"{base_folder}/{group_folder}/donnees_anonymes{file}"

    ################################
    print('Read dtarget file')
    dtarget = pd.read_csv(dtarget_file, sep=separator)

    dtarget.columns = ['id', 'date', 'lat', 'long']
    print('Delete some rows')
    dtarget = dtarget[~(dtarget == 'DEL').any(axis=1)]

    try:
        dtarget['id'] = dtarget['id'].astype('int32')
    except:
        print('Need to use LabelEncoder on IDs')
        encoder = LabelEncoder()
        dtarget['id'] = encoder.fit_transform(dtarget['id'])
        joblib.dump(encoder, f"{base_folder}/{group_folder}/LabelEncoder{file}.joblib")

    print('Fix some coordinates problems')
    dtarget['lat'] = pd.to_numeric(dtarget['lat'], errors='coerce').clip(lower=-90, upper=90).astype('float32')
    dtarget['long'] = pd.to_numeric(dtarget['long'], errors='coerce').clip(lower=-180, upper=180).astype('float32')

    print('Calculate haversine distance')
    dtarget['distance'] = dtarget.apply(
        lambda row: haversine((row['lat'], row['long']), (0, 0), unit=Unit.KILOMETERS), axis=1)

    print('Calculate date and timestamp')
    dtarget['date'] = pd.to_datetime(dtarget['date'])
    dtarget['timestamp'] = (dtarget['date'] - pd.Timestamp("1970-01-01")) // pd.Timedelta('1s')
    dtarget['week_year'] = dtarget['date'].dt.strftime('%Y-%U')

    print('Store dtarget preprocessing')
    dtarget.to_pickle(f"{dtarget_file}.pkl")

    #########################################
    if not preprocess_dsource:
        print("Preprocessing completed")
        return

    print('Read dsource file')
    dsource = pd.read_csv(dsource_file, sep=separator)

    dsource.columns = ['id', 'date', 'lat', 'long']

    dsource['id'] = dsource['id'].astype('int32')

    print('Fix some coordinates problems')
    dsource['lat'] = pd.to_numeric(dsource['lat']).clip(lower=-90, upper=90).astype('float32')
    dsource['long'] = pd.to_numeric(dsource['long']).clip(lower=-180, upper=180).astype('float32')

    print('Calculate haversine distance')
    dsource['distance'] = dsource.apply(
        lambda row: haversine((row['lat'], row['long']), (0, 0), unit=Unit.KILOMETERS), axis=1)

    print('Calculate date and timestamp')
    dsource['date'] = pd.to_datetime(dsource['date'])
    dsource['timestamp'] = (dsource['date'] - pd.Timestamp("1970-01-01")) // pd.Timedelta('1s')
    dsource['week_year'] = dsource['date'].dt.strftime('%Y-%U')

    print('Store dsource preprocessing')
    dsource.to_pickle(f"{dsource_file}.pkl")

    print("Preprocessing completed.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Preprocess data from command line.")
    parser.add_argument("--group_folder", type=str, help="Group folder path", default="")
    parser.add_argument("--file", type=str, help="File name", default="3")
    parser.add_argument("--preprocess_dsource", action="store_true", help="Flag to preprocess dsource")

    args = parser.parse_args()

    preprocess_data(args.group_folder, args.file, args.preprocess_dsource)
