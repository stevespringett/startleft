## Command-Line
For help, just run `startleft` without arguments:

```
$ startleft
Usage: startleft [OPTIONS] COMMAND [ARGS]...

  Parse IaC files to the Open Threat Model format and upload them to IriusRisk

Options:
  -l, --log-level TEXT      Set the log level. Must be one of: crit, error,
                            warn, info, debug, none.
  --verbose / --no-verbose  Makes logging more verbose.
  --version                 Show the version and exit.
  --help                    Show this message and exit.

Commands:
  parse        Parses IaC files to the Open Threat Model format
  run          Parses IaC files to the Open Threat Model format and...
  search       Searches source files for the given query
  server       Launches a REST server to receive and parse IaC files,...
  threatmodel  Uploads an OTM file to IriusRisk
  validate     Validates a mapping or OTM file
```

You can also get help for the specific commands.

```
$ startleft run --help
Usage: startleft run [OPTIONS] [FILENAME]...

  Parses IaC files to the Open Threat Model and upload them to 
  IriusRisk

Options:
  -t, --type  [JSON|YAML|CloudFormation|HCL2|Terraform]
                                  Specify the source file type.
  -m, --map TEXT                  Map file to use when parsing source files
  -o, --otm TEXT                  OTM output file name
  -n, --name TEXT                 Project name
  --id TEXT                       Project ID
  --recreate / --no-recreate      Delete and recreate the product each time
  --irius-server TEXT             IriusRisk server to connect to
                                  (proto://server[:port])'
  --api-token  TEXT               IriusRisk API token
  --help                          Show this message and exit.
```

## API server

StartLeft can also be deployed as a standalone webserver if you prefer the communication via API. If you want to use the server option on the application:

```
$ startleft server --help
Usage: startleft server [OPTIONS]...

  Launches a REST server to receive and parse IaC files, finally uploading
  resultant OTM files to IriusRisk

Options:
  --port INTEGER                  The port to deploy this application to
  --irius-server TEXT             IriusRisk server to connect to (proto://server[:port])
  --help                          Show this message and exit.

```

By executing `startleft server` it is possible to see the command-line messages finishing with the following:

```Uvicorn running on http://127.0.0.1:5000 (Press CTRL+C to quit)```

so indicating Startleft's REST API is ready. You can see the endpoints provided by opening the following URL in a web browser: http://127.0.0.1:5000/docs

Available endpoints:
```
GET /health
```
```
POST /api/v1/startleft/cloudformation
Headers:
    api_token                   Required: IriusRisk API token
Request Body:
    cft_file:                   Required. File that contains the CloudFormation Template
    type                        Required. Format of the CloudFormation Template
    id                          Required. ID of the new project
    name                        Required. Name of the new project
    mapping_file                Optional. File that contains the mapping between AWS components and IriusRisk components. Providing this file will completely override default values
```
```
PUT /api/v1/startleft/cloudformation/projects/{project_id}
Headers:
    api_token                   Required: IriusRisk API token
Path parameter:
    project_id:                 Required. IriusRisk project identifier
Request Body:
    cft_file:                   Required. File that contains the CloudFormation Template
    type:                       Required. Format of the CloudFormation Template
    name                        Required. Name of the project to update
    mapping_file                Optional. File that contains the mapping between AWS components and IriusRisk components. Providing this file will completely override default values
```