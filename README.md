# pdf_hide

A Python 3 steganographic tool for hiding data in [PDF](https://www.adobe.com/devnet/acrobat/pdfs/PDF32000_2008.pdf) files

* [What can it do?](#basic-usage)
* [How to get it](#getting-started)
* [How to improve it](#project-status)
* [Licensing](#license-information)

This tool is an ongoing effort to bring a novel open-source method of steganography to the public. It is able to embed arbitrary data in a covert way inside any PDF file containing enough text. As a result, no one but the intented recipient suspects the existence of embedded data. The same tool can then be used to extract the concealed data.

This project stems from research conducted at the University of Amsterdam, The Netherlands, in December 2012: [Using Steganography to hide messages inside PDF files](https://www.os3.nl/_media/2012-2013/courses/ssn/using_steganography_to_hide_messages_inside_pdf_files.pdf), written by [Fahimeh Alizadeh](mailto:Fahimeh.Alizadeh@os3.nl), [Nicolas Canceill](mailto:Nicolas.Canceill@os3.nl), [Sebastian Dabkiewicz](mailto:Sebastian.Dabkiewicz@os3.nl) and [Diederik Vandevenne](mailto:Diederik.Vandevenne@os3.nl).

## Basic usage

````bash
pdf_hide -k "secret key" embed secret_data_file innocent_file.pdf
````

````bash
pdf_hide -k "secret key" extract innocent_file.pdf
````

## Getting started

Please visit the [wiki](../../wiki).

### Requirements

This tool is a Python 3 program: it requires a basic [Python](http://www.python.org) 3 installation (currently tested on 3.3.2, should be retro-compatible down to 3.2). Python 3 distributes under [Python License](http://docs.python.org/3/license.html) from the Python Software Foundation.

It requires [QPDF](http://qpdf.sourceforge.net) in order to modify compressed PDF files. QPDF distributes under [Artistic license v2](http://opensource.org/licenses/artistic-license-2.0.php) from the Perl Foundation.

### Setup

You can find the latest version packaged on the [releases page](../../releases). The current version is [0.0 beta](../../releases/tag/v0.0b): [tgz](../../archive/v0.0b.tar.gz) — [zip](../../archive/v0.0b.zip).

## Project status

Current version is 0.0 beta

### Stability

The current version is UNSTABLE and should not be run in production.

### Changelog

#### version 0.0b

[Changelog discussion](../../issues/9)

* Refactored code (logging, input, comments, debug)
* Migrated to Python 3
* Migrated to argparse

#### version 0.0a

* Licensing
* Refactored code
* Improved Makefile support
* Unit tests

### Contributions

General rule: any contributions are welcome.

Do not hesitate to [drop an issue](../../issues/new) if you found a bug, if you either want to see a new feature or wish to suggest an improvement, or even if you simply have a question.

Please check the [contributions status](../../wiki/contribute#status) if you want to get involved.

## License information

This project distributes under [GNU General Public License v3](LICENSE.md) from the Free Software Foundation.

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.  If not, see [http://www.gnu.org/licenses/].

Copyright (C) 2013 Nicolas Canceill
