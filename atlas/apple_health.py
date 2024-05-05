import os
import polars as pl
import lxml.etree as et
import sys
import time


def to_df(file_path):
    start_time = time.time()
    last_time = time.time()

    print("transform apple health export.xml to parquet")
    print("- parsing xml", end="")
    sys.stdout.flush()

    attributes = []

    for event, elem in et.iterparse(file_path, tag="Record"):
        attributes.append(
            {
                attr: elem.get(attr)
                for attr in ["value", "type", "startDate", "endDate", "creationDate"]
                if elem.get(attr) is not None
            }
        )
        elem.clear()

    last_time = time.time()
    elapsed_time = last_time - start_time
    print(f" ({elapsed_time} s)")
    print("- loading df", end="")
    sys.stdout.flush()

    df = pl.DataFrame(attributes)

    last_time = time.time()
    elapsed_time = last_time - start_time
    print(f" ({elapsed_time} s)")
    print("- drop rows where type is missing", end="")
    sys.stdout.flush()

    df = df.filter(pl.col("type").is_not_null())

    # replace remove prefixes
    # print(df.shape)
    last_time = time.time()
    elapsed_time = last_time - start_time
    print(f" ({elapsed_time} s)")
    print("- remove prefixes", end="")
    sys.stdout.flush()

    df = df.with_columns(
        pl.col("type").str.replace(r"^HKQuantityTypeIdentifier", "")
    ).with_columns(pl.col("type").str.replace(r"^HKCategoryTypeIdentifier", ""))
    df = df.select(
        pl.all().name.map(
            lambda col_name: col_name.replace("HKCharacteristicTypeIdentifier", "")
        )
    )

    # print(df.shape)
    last_time = time.time()
    elapsed_time = last_time - start_time
    print(f" ({elapsed_time} s)")
    print("- convert time strings to datetime", end="")
    sys.stdout.flush()

    # convert datetime strings to datetime (example: "2024-02-18 15:15:06 +0100")
    # TODO: add timezone handling (currently the timezone offset is ignored via truncation)
    df = df.with_columns(
        pl.col("startDate").str.slice(0, 19).str.to_datetime(),
        pl.col("endDate").str.slice(0, 19).str.to_datetime(),
        pl.col("creationDate").str.slice(0, 19).str.to_datetime(),
    )

    df = df.rename({"startDate": "start", "endDate": "end", "creationDate": "created"})

    # drop unneeded entries
    last_time = time.time()
    elapsed_time = last_time - start_time
    print(f" ({elapsed_time} s)")
    print("- drop unneeded entries", end="")
    sys.stdout.flush()

    # replacement map for enums
    replacement_map = {
        # 'HKCategoryValueSeverityUnspecified': '1',
        # 'HKCategoryValueLowCardioFitnessEventLowFitness': '1',
        # 'HKCategoryValueNotApplicable': '-1',
        # 'HKCategoryValueEnvironmentalAudioExposureEventMomentaryLimit': '1',
        # 'HKCategoryValueAppleStandHourStood': '1',
        # 'HKCategoryValueAppleStandHourIdle': '0',
        # 'HKCategoryValueSleepAnalysisAwake': '0',
        # 'HKCategoryValueSleepAnalysisAsleepCore': '1',
        # 'HKCategoryValueSleepAnalysisAsleepDeep': '2',
        # 'HKCategoryValueSleepAnalysisAsleepREM': '3',
        # 'HKCategoryValueSleepAnalysisAsleepUnspecified': '1',
        # 'HKCategoryValueSleepAnalysisInBed': '-1',
        # '2024-02-24 12:46:57 +0100': '-1'
    }

    # Replace string values
    # print(df.shape)
    last_time = time.time()
    elapsed_time = last_time - start_time
    print(f" ({elapsed_time} s)")
    print("- replace string values", end="")
    sys.stdout.flush()

    for key, val in replacement_map.items():
        df = df.with_columns(pl.col("value").str.replace(key, val))

    # split "value" column "23.1 kPa" -> ["23.1", "kPa"]
    # if there are multiple parts, only take the 0th part
    df = (
        df.with_columns(
            pl.col("value")
            .str.splitn(" ", 2)
            .struct.rename_fields(["frst", "rest"])
            .alias("fields"),
        )
        .unnest("fields")
        .drop("rest")
        .drop("value")
        .rename({"frst": "value"})
    )

    last_time = time.time()
    elapsed_time = last_time - start_time
    print(f" ({elapsed_time} s)")
    print("- convert 'value' column to numeric", end="")
    sys.stdout.flush()

    # convert 'value' column to float
    # df = df.with_columns(
    #     pl.col('value').cast(pl.Float64)
    # )

    # sort: newest data DESC
    # print(df.shape)
    last_time = time.time()
    elapsed_time = last_time - start_time
    print(f" ({elapsed_time} s)")
    print("- sort: newest data first", end="")
    sys.stdout.flush()

    df = df.sort("type").sort("start", descending=True)

    last_time = time.time()
    elapsed_time = last_time - start_time
    print(f" ({elapsed_time} s)")

    print(f"\ndf data shape: {df.shape}")
    print(f"total elapsed time: {elapsed_time} s\n")
    sys.stdout.flush()

    return df


def write_parquet(df, path=None):
    df.write_parquet(path, compression="zstd", compression_level=22)
    return
