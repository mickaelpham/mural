# Mural

A Command-Line Interface (CLI) for [Mural](https://mural.co).

## Setup

### Register an application

1. [Register an app](https://developers.mural.co/public/docs/register-your-app)
   with Mural, store the `client_id` and `client_secret` somewhere safe
2. In a browser window,
   [authorize the app](https://developers.mural.co/public/docs/oauth#authenticate-users-authorization-request)
   with your logged in user
3. Copy the authorization code from the URL and create an
   [access token](https://developers.mural.co/public/docs/oauth#authenticate-users-access-token-request)
4. Copy the `refresh_token` in the response

### Install the CLI

Clone the repository.

```sh
git clone https://github.com/mickaelpham/mural.git
cd mural
```

Make a copy of the `config.sample.toml` and fill in the blanks with the
`refresh_token`, `client_id` and `client_secret` from the _register an
application_ step above.

```sh
cp config.sample.toml config.toml
```

Create and activate a virtual environment:

```sh
python -m venv venv

# on macOS or GNU/Linux
source venv/bin/activate
```

Install the CLI locally:

```sh
pip install --editable .
```

## Usage

Show the logged in user information.

```sh
mural me
```

List all rooms and their members in a given workspace.

```sh
mural rooms WORKSPACE_ID --include-members
```
