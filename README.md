# Schedulify

Schedulify is a tool for scheduling Python functions on Google Cloud Platform
with minimal boilerplate.

NOTE: Schedulify is currently under development, so the full vision has not been
realized yet. If you use this tool, please expect significant changes.

## Motivation

Google Cloud Platform offers Cloud Scheduler for running tasks according to a
schedule. The process to set up a scheduled task involves many steps:

*  Uploading the application. Depending on the runtime chosen, this may involve
   containerizing the application and exposing the functions through a web
   server.

*  Creating and configuring a service account to establish trust between the
   runtime and Cloud Scheduler.

*  Creating a task in Cloud Scheduler.

The motivation behind this tool is to simplify this process.

## Requirements

To use this tool, you must have:

*  A Google Cloud project with billing enabled
*  The following APIs enabled:
   *  Cloud Build
   *  Cloud Run
   *  Cloud Scheduler
*  [The Google Cloud SDK](https://cloud.google.com/sdk/docs/quickstarts)
   installed on your computer
*  A Python 3.7-compatible app with one or more functions that you want to run
   periodically
*  A `requirements.txt` file that specifies non-standard dependencies, if any

## Status

Currently, the tool performs the following tasks, which are meant to be opaque
to the user:

*  Generates a Flask server that allows the invocation of the functions over
   HTTP;
*  Generates configs to containerize the app using the [Python 3.7
   slim](https://hub.docker.com/_/python) Docker image;
*  Submits the app to Cloud Build; and
*  Starts a Cloud Build service.

Note that the tool does not yet perform any operations in Cloud Scheduler.
Support for this along with many other improvements are forthcoming. Refer to
the Future Work section below for a full list of improvements.

If the above tasks provide utility for your workload and you are comfortable
with the instability that comes with a nascent tool, then you may proceed to the
next section which describes how to get started.

## Getting Started

First, install Schedulify:

```
pip install schedulify
```

Then, navigate to your Python project that contains the functions you want to
run. Add a file named `shedulify.json`, formatted as follows:

```
{
    "project-id": "my-project-id",
    "region": "us-west1",
    "functions": [
        {
            "module": "my_module",
            "function": "my_function",
        }
    ]
}
```

All function references are relative to where `schedulify.json` is location. If
your project contains a `requirements.txt` file, it must be present in the same
directory as `schedulify.json`.

NOTE: The scheduling portion of this tool is not implemented yet, so the
configuration file does not accept configuration for how often the function
should be executed.

Authenticate through the Google Cloud SDK:

```
gcloud auth login
```

Then, from the directory that `schedulify.json` resides in, run:

```
schedulify
```

You will see the `gcloud` invocations printed to standard out. You should see
the tool building the image and deploying it to Cloud Run.

## Future Tasks

*  Do not rely on `gcloud` for configuring Google Cloud Platform resources.
*  (Maybe) Use Cloud Functions. Cloud Functions is probably good enough for most
   use-cases and allows us to substantially reduce the complexity of
   containerizing an arbitrary Python app.
*  Add support for configuring Cloud Scheduler.

## Development Guide

### Performing a Release

Refer to [Python's Packaging
documentation](https://packaging.python.org/guides/distributing-packages-using-setuptools/#packaging-your-project)
for full details on performing a release. Assuming all tools are set up, run the
following to push a new package to PyPI:

```
python setup.py bdist_wheel
twine upload dist/*
```
