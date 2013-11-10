# PDF HIDE

This is a steganographic tool in Python for hiding data in [PDF](https://github.com/ncanceill/pdf_hide/wiki/PDF) files

* [What can it do?](#basic-usage)
* [How can I get it?](#getting-started)
* [How can I improve it?](#project-status)
* [Licensing](#license-information)

This tool is an ongoing effort to bring a novel open-source method of steganography to the public. It is able to embed arbitrary data in a covert way inside any PDF file containing enough text. As a result, no one but the intented recipient suspects the existence of embedded data. The same tool can then be used to extract the concealed data.

This project stems from research conducted at the University of Amsterdam, The Netherlands, in December 2012: [Using Steganography to hide messages inside PDF files](https://www.os3.nl/_media/2012-2013/courses/ssn/using_steganography_to_hide_messages_inside_pdf_files.pdf), written by [Fahimeh Alizadeh](mailto:Fahimeh.Alizadeh@os3.nl), [Nicolas Canceill](mailto:Nicolas.Canceill@os3.nl), [Sebastian Dabkiewicz](mailto:Sebastian.Dabkiewicz@os3.nl) and [Diederik Vandevenne](mailto:Diederik.Vandevenne@os3.nl).

## Basic usage

````bash
pdf_hide [-o <embedded.pdf>] embed <data_file> <innocent.pdf>
````

````bash
pdf_hide [-o <extracted_file>] extract <embedded.pdf>
````

## Getting started

Please read the [guide](https://github.com/ncanceill/pdf_hide/wiki/Quickstart).

### Requirements

This tool is a Python 3 program: it requires a basic [Python](http://www.python.org) 3 installation.

It requires [QPDF](http://qpdf.sourceforge.net) in order to modify compressed PDF files.

Additionally, it requires [GNU Make](http://www.gnu.org/software/make/) and [`pdflatex`](http://www.ctan.org) to build samples for the tests.

### Setup

You can find the latest version packaged on the [releases page](https://github.com/ncanceill/pdf_hide/releases). The current version is 0.0: [tgz](https://github.com/ncanceill/pdf_hide/archive/v0.0.tar.gz) — [zip](https://github.com/ncanceill/pdf_hide/archive/v0.0.zip).

Alternatively, you can clone the git repository at: `github.com/ncanceill/pdf_hide.git`

You can run the tests with: `make tests`

You can install the package (as root) on your system's Python path with: `make install` or `./setup.py install`

## Project status

Current version is [0.0](https://github.com/ncanceill/pdf_hide/releases/tag/v0.0).

Please check the [project status](https://github.com/ncanceill/pdf_hide/wiki/Status) for more details.

### Stability

The current version is STABLE. It may be run in production.

### Contributions

General rule: any contributions are welcome.

Do not hesitate to [drop an issue](https://github.com/ncanceill/pdf_hide/issues/new) if you found a bug, if you either want to see a new feature or wish to suggest an improvement, or even if you simply have a question.

Please check the [contribution status](https://github.com/ncanceill/pdf_hide/wiki/Contribute#status) if you want to get involved.

## License information

This project, including this README, distributes under [GNU General Public License v3](LICENSE.md) from the Free Software Foundation.

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.  If not, see [http://www.gnu.org/licenses/].

***

Copyright (C) 2013 Nicolas Canceill
