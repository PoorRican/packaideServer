# CHANGELOG

## v1.0.1

- Disable `persist` flag when running packaide
- Improve `Dockerfile` to use `python:3.10-bookworm` as the base image (more reliable, smaller image, and should long-term reliability)
- Remove usage of `LiteralString` which is not supported by python3.10