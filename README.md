# haxkohle

Haxkohle is a tool for associations to manage their financial operations.
Its main purpose is to provide a dashboard for each member, giving them information on membership fees already paid and outstanding.

It provides some management functions for authorized members to give them insight into outstanding membership fees.

In addition, a further planning component is planned. Its purpose is to plan transactions and especially recurring transactions.
To forecast the financial status of the club in the future.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Support](#support)
- [Development](#development)
- [Contributing](#contributing)

## Installation

To install haxkohle, run the flollowing commands in your `Bash`-compatible shell. For the following commands to work we assume that `python3`, `pip3` and `npm` is installed on your machine.

```sh
git clone https://github.com/haxko/haxkohle
cd haxkohle

python3 -m venv .env
source .env/bin/activate
pip install -r requirements.txt

npm install
npm run build # or "npm run start" to autocompile if changes are present

python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py createsuperuser

python3 manage.py runserver
```
## Usage

The project is currently in a early development state. Therefore production usage is not recommended.

After install, the admin panel is available under  `/admin`, apart from that only the `/account`, `/account/register`, `/account/logout` are existent.
Othere routes will be notet here, as they come available.

For more security a password is required in addition to the user password to upload CAMT archives. This is needed to secure hashed user data.
The default development passwort is `haxkohle`. 
It is strongly recommended, to change this passwort in production. Which can be done in `clubfinance/settings.py`, using a sha224 hash of the upload password.


## Support

Please [open an issue](https://github.com/haxko/haxkohle/issues/new) for support.

## Development

### Technologies

The project is based on [python3](https://www.python.org/doc/) and [django](https://docs.djangoproject.com/en/3.0/) the additional packages are notet in the [requirements.txt](requirements.txt).

The client side libraries are loaded using [npm](https://www.npmjs.com/) and are compiled using [webpack](https://webpack.js.org/).
The major frontent packages used are [bootstrap](https://getbootstrap.com/docs/4.5/getting-started/introduction/) and [vuejs](https://vuejs.org/v2/guide/).

### Specifications

Bankdata can be exported from your bank and imported into haxkohle using the `CAMT.052` standart.
Which is implemented as described [here](https://www.rabobank.com/en/images/rcc-format-description-camt.052-v1.02.pdf).

We furthermore plan to implement bank data download via EBICS and FinTS in the future. But for this purpose nothing is implemented yet.

## Contributing

Contribution rules and workflows are not developed. Comming soon.

