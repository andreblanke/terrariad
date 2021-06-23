# terrariad

A small Python program that listens for connections from Terraria clients, disconnects them with
a configurable reason, and then launches the actual server.

## About

Socket activation of certain services, in this case a Terraria server instance, is particularly
useful in more memory-constrained environments such as single-board computers like Raspberry Pis.

As the default Terraria server supports no such functionality out of the box, "third party"
solutions like
[systemd-socket-proxyd](https://www.freedesktop.org/software/systemd/man/systemd-socket-proxyd.html)
need to be employed. A usage of direct systemd socket activation, i.e. without the use of
`systemd-socket-proxyd`, would also require built-in support, as the socket handed over by systemd
must be used in favor of one created by the program itself.

The issue with `systemd-socket-proxyd` is that while a service may be successfully started by it,
the proxy will attempt to tunnel the incoming connection much faster than some services can start,
a Terraria server being one of those. The first connection attempt will basically be voided,
users, or rather players in this case, possibly confused.

`terrariad` attempts to solve this issue by basically doing what `systemd-socket-proxyd` would do,
but instead of the first connection made getting voided because the server is unable to start fast
enough a disconnect message is sent to the client containing a configurable reason,
such as "The server is starting. Please wait and retry connecting in a bit."

### Other options

A different approach to the issue would be direct patching of the Terraria server on a lower level,
probably using [Open Terraria API](https://github.com/DeathCradle/Open-Terraria-API), in order to
get the server to accept a socket passed by systemd. However, we would still be left with the fact
that the server startup might be too slow and players would end up cancelling the connection
attempt, as we cannot send arbitrary messages to inform them that a startup is in progress.

## Usage

## See also

- [andreblanke/EmptyServerShutdown](https://github.com/andreblanke/EmptyServerShutdown) to shut
  down the server some time after the last player left the server.

### Related

- [tylerjwatson/Multiplicity](https://github.com/tylerjwatson/Multiplicity) A C# Terraria packet
  deserialization library.

- [Terraria Network Protocol](https://seancode.com/terrafirma/net.html) A description of the
  Terraria network protocol. Might be outdated.
