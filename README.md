#### Script to retrieve and store your historical scan data locally

#### Program description

The Python program file ‘archive_scans.py’ retrieves and archives information on historical scans.

The program makes use of the Halo SDK which handles functions like making REST calls, creating and parsing JSON responses, authentication and error handling.

#### Install instructions

1. Requires Python 2.7.10 version or higher 
2. Install the SDK `pip install cloudpassage`
3. Halo requires the script to pass both the key ID and secret key values for a valid Halo API key in order to make API calls.
4. Copy the API Key_id and Secret Key from your Halo account into `portal.yml` located in `configs/portal.yml`

    ```
    key_id: 12345
    secret_key: abcabcabcabcabc
    ```

#### Program Usage
Run the following command to see program usage:
```python archive_scans.py -h```

Output:
usage: archive_scans.py [-h] [--since SINCE] [--until UNTIL]

Archive Scans

```
optional arguments:
  -h, --help     show this help message and exit
  --since SINCE  Only get historical scans after <when> (ISO-8601 format)
  --until UNTIL  Only get historical scans till <when> (ISO-8601 format)
```

Either since or until has to be a required flag.

After the program has run successfully, you will find a directory called “details” created under your current working directory under which the scan details will be archived.

To retrieve and archive scan data since, say January 1 of 2015, use the following command: `python archive_scans.py --since=2015-01-01`