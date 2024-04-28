
<div align="center">
  <img alt="expanse"
       height="320px"
       src="https://github.com/tosh/expanse/assets/14825/0f766786-31c9-434e-ae65-66cf7331a27b">
</div>

# expanse

Expanse lets you explore your Apple Health data.

---

[![PyPI](https://img.shields.io/pypi/v/expanse.svg)](https://pypi.org/project/expanse/)
[![Tests](https://github.com/tosh/expanse/actions/workflows/test.yml/badge.svg)](https://github.com/tosh/expanse/actions/workflows/test.yml)
[![Changelog](https://img.shields.io/github/v/release/tosh/expanse?include_prereleases&label=changelog)](https://github.com/tosh/expanse/releases)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/tosh/expanse/blob/main/LICENSE)

## Installation

Install expanse using `pipx`:
```bash
brew install pipx
pipx install expanse
```

## Explore

First we create the `.parquet` file from the `export.xml` file.

```bash
expanse parquet export.xml -o ah.parquet
```

We can explore the data in many ways.

It is just a table/dataframe/parquet file with 5 columns.

But here we'll use `clickhouse local`:

```bash
clickhouse local
```

Let's take a look at the table.

```sql
DESCRIBE TABLE `ah.parquet`
```

```
Query id: b2ba2921-f40e-4509-9bed-9b258cd7b79d

┌─name────┬─type────────────────────┬─default_type─┬─default_expression─┬─comment─┬─codec_expression─┬─ttl_expression─┐
│ type    │ Nullable(String)        │              │                    │         │                  │                │
│ start   │ Nullable(DateTime64(6)) │              │                    │         │                  │                │
│ end     │ Nullable(DateTime64(6)) │              │                    │         │                  │                │
│ created │ Nullable(DateTime64(6)) │              │                    │         │                  │                │
│ value   │ Nullable(String)        │              │                    │         │                  │                │
└─────────┴─────────────────────────┴──────────────┴────────────────────┴─────────┴──────────────────┴────────────────┘

5 rows in set. Elapsed: 0.009 sec. 
```

What kind of "types" do we have and how many?

```sql
SELECT
    type,
    COUNT(*) AS count
FROM `ah.parquet`
GROUP BY type
ORDER BY count DESC
```

```
Query id: ce9cbd6d-f282-4196-ab07-b2d8ad9c0011

┌─type───────────────────────────┬──count─┐
│ ActiveEnergyBurned             │ 879902 │
│ HeartRate                      │ 451854 │
│ BasalEnergyBurned              │ 289031 │
│ DistanceWalkingRunning         │ 260500 │
│ StepCount                      │ 217384 │
│ PhysicalEffort                 │  69747 │
│ AppleExerciseTime              │  61363 │
│ AppleStandTime                 │  58309 │
│ EnvironmentalAudioExposure     │  44535 │
│ SleepAnalysis                  │  36599 │
│ WalkingStepLength              │  28281 │
│ WalkingSpeed                   │  28281 │
│ RespiratoryRate                │  27829 │
│ AppleStandHour                 │  25877 │
│ FlightsClimbed                 │  22690 │
│ WalkingDoubleSupportPercentage │  21900 │
│ WalkingAsymmetryPercentage     │  13820 │
│ HeartRateVariabilitySDNN       │  11961 │
│ OxygenSaturation               │   4912 │
│ StairDescentSpeed              │   4718 │
│ StairAscentSpeed               │   4249 │
│ DistanceCycling                │   2890 │
│ TimeInDaylight                 │   2403 │
│ HeadphoneAudioExposure         │   2323 │
│ RestingHeartRate               │   1399 │
│ WalkingHeartRateAverage        │   1176 │
│ DistanceSwimming               │    455 │
│ SwimmingStrokeCount            │    455 │
│ AppleSleepingWristTemperature  │    442 │
│ RunningSpeed                   │    391 │
│ VO2Max                         │    366 │
│ RunningPower                   │    173 │
│ DietaryCaffeine                │    171 │
│ AppleWalkingSteadiness         │    138 │
│ SixMinuteWalkTestDistance      │    122 │
│ HeartRateRecoveryOneMinute     │     76 │
│ RunningVerticalOscillation     │     74 │
│ RunningGroundContactTime       │     67 │
│ RunningStrideLength            │     54 │
│ MindfulSession                 │     34 │
│ HighHeartRateEvent             │     18 │
│ AudioExposureEvent             │     14 │
│ BodyMass                       │     14 │
│ Height                         │      5 │
│ Fatigue                        │      1 │
│ HKDataTypeSleepDurationGoal    │      1 │
└────────────────────────────────┴────────┘
```

## How to get the Apple Health export.xml file

![group-figma-small](https://github.com/tosh/expanse/assets/14825/e48971a3-bc13-4496-8fe2-5dcd292c9019)

- open the Apple **Health** app on iOS
- tap on your **profile picture** (or initials) at the top right
- tap on **Export All Health Data**
- tap on **Export**
- **wait** a few seconds to a few minutes (~3min for 10 years of data)
- **get the export.zip** archive via Airdrop to a Mac (or save to Files)

> [!NOTE]  
> The **export.xml** file is **in** the **export.zip** archive.

You can expand the **export.zip** file by double-clicking on it.

This creates a directory named **apple_health_export** and in it is the **export.xml** file.

<img src="https://github.com/tosh/expanse/assets/14825/c519f3e9-23bf-4f90-909f-30a07b286d57" width="66%">

<img src="https://github.com/tosh/expanse/assets/14825/64409b40-c87f-4bbc-9df8-778d758517fc" width="66%">

<img src="https://github.com/tosh/expanse/assets/14825/0f83fc2d-6728-4023-8074-75517a2af49f" width="66%">

<img src="https://github.com/tosh/expanse/assets/14825/35e9d36e-9a7a-46aa-b6da-1420d05b1f20" width="66%">


See: [Apple Support on how to export Apple Health and Fitness in XML format](https://support.apple.com/en-gb/guide/iphone/iph5ede58c3d/ios#:~:text=Share%20your%20health%20and%20fitness%20data%20in%20XML%20format)

## Usage

`expanse parquet export.xml`

## Features

- turn export.xml into a simple parquet file

