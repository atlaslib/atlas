
<div align="center">
  <img alt="expanse"
       height="320px"
       src="https://github.com/tosh/expanse/assets/14825/d8c8e3ed-442c-4545-a6a2-e3d70b770db0"
       style="border-radius: 6%">
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

## How to get the Apple Health export.xml file

![group-figma-small](https://github.com/tosh/expanse/assets/14825/e48971a3-bc13-4496-8fe2-5dcd292c9019)

- open the Apple **Health** app on iOS
- tap on your **profile picture** (or initials) at the top right
- tap on **Export All Health Data**
- tap on **Export**
- **wait** a few seconds to a few minutes (~3min for 10 years of data)
- **get the export.zip** archive via Airdrop to a Mac (or save to Files)

The **export.xml** file is in the **export.zip** archive.

See: [Apple Support on how to export Apple Health and Fitness in XML format](https://support.apple.com/en-gb/guide/iphone/iph5ede58c3d/ios#:~:text=Share%20your%20health%20and%20fitness%20data%20in%20XML%20format)

## Usage

`expanse parquet export.xml`

## Features

- turn export.xml into a simple parquet file

