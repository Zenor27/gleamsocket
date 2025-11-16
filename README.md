# gleamsocket

A simple TCP Echo Server written in Gleam.

This project was made for benchmarking Gleam/Erlang sockets and process handling.

It also demonstrate how to do basic Erlang FFI with Gleam.

## Benchmarks

![Gleam benchmark](https://github.com/Zenor27/gleamsock/blob/main/benchmark_gleam.png?raw=true)

![Go benchmark](https://github.com/Zenor27/gleamsock/blob/main/benchmark_golang.png?raw=true)

Go comparaison was made with [venilnoronha tcp-echo-server](https://github.com/venilnoronha/tcp-echo-server/).


## Run echo server

```console
$ gleam run
```

## Run benchmark

> Make sure server is available localy on port `6969`

```
$ python -m venv .venv
$ source .venv/bin/activate
$ pip install
$ python src/benchmark.py
```
