-module(listen_tcp).
-export([listen_tcp/1]).

listen_tcp(Port) ->
    gen_tcp:listen(Port, [binary, {packet, 0}, {active, false}, {reuseaddr, true}]).
